#!/usr/bin/env bash
#
# SRP production domain reachability check.
#
# Checks all 29 hosts of the CRA Single Reporting Platform production zone
# (portal, auth, and the 27 Member State instances) and records four stages
# per host: DNS resolution, TCP 443, TLS handshake, HTTP status code.
#
# Dependencies: bash + curl. Optionally dig/getent/python3 for DNS.
#
# ---------------------------------------------------------------------------
# WHAT "REACHABLE" MEANS HERE
#
# The production zone is provisioned but access-filtered: the WEDOS edge
# accepts TCP and then drops the TLS handshake for any source IP that is not
# allowlisted. So this check only reports a host as reachable when it runs
# from an allowlisted source IP -- OR when the allowlist has been lifted.
#
# A successful HTTP response from an arbitrary IP therefore means the public
# launch has happened. That is the signal this monitor exists to catch.
#
# ---------------------------------------------------------------------------
# WHY LIVENESS IS DECIDED ON HTTP AND NOT ON THE TLS HANDSHAKE
#
# Do not "simplify" this script to treat a completed TLS handshake as launch.
# It was written that way first and it was wrong.
#
# When this runs behind an intercepting egress proxy (as it does in the
# Claude Code cloud environment), the proxy terminates TCP and TLS itself,
# before it knows whether the upstream host works at all. Measured there:
#
#   - TCP connect succeeds even to 240.0.0.1, a reserved unroutable address.
#   - The TLS handshake completes against all 29 SRP hosts -- while the
#     platform is dark -- presenting a certificate issued by
#     "Anthropic / Egress Gateway SDS Issuing CA (production)".
#
# Both lower stages are therefore forged in that environment and would report
# all 29 hosts LIVE forever. Only an actual HTTP status code, relayed from
# upstream, is trustworthy. TCP and TLS are still recorded because they are
# meaningful when this runs from a normal network, but they are marked
# trust=proxied and never set first_live.
#
# curl's exit code separates the states that matter:
#
#   HTTP code returned      -> LIVE          (upstream answered)
#   HTTP code returned, but
#   the body is WEDOS's own
#   branded error page      -> EDGE_BLOCKED  (the WEDOS edge answered, not
#                                             the SRP origin -- see below)
#   exit 35/28/7/52/56*     -> PROVISIONED   (connected, upstream dropped)
#   exit 56 + "403"         -> BLOCKED       (egress policy; check is blind,
#                                             never a statement about the SRP)
#   exit 6                  -> NXDOMAIN      (curl itself could not resolve)
#   exit 28, and the local
#   DNS step also hung      -> DNS_TIMEOUT   (nothing answered in time;
#                                             check is blind, never a
#                                             statement about the SRP)
#
# ---------------------------------------------------------------------------
# WHY A RETURNED HTTP CODE CAN STILL BE EDGE_BLOCKED, NOT LIVE
#
# 2026-09-11: a run got a real HTTP response -- no forged cert, no proxy
# artifact, a genuine Sectigo cert for the exact hostname -- from 28 of 29
# hosts, all HTTP 456. That first looked like the go-live this monitor exists
# to catch. Reading the body told a different story: every response was
# WEDOS's own templated error page ("WEDOS.protection - 404 Not Found"),
# generated entirely at the edge (its diagnostic block reads "Server: - /
# ip_denied" -- an empty origin field, i.e. the request never reached the SRP
# application at all) and branded throughout with WEDOS.protection /
# WEDOS.delivery / WEDOS.status.online. A second run eight minutes later, and
# several manual checks in between, mostly got the old TLS-drop
# (PROVISIONED) for the same hosts, with only "portal" answering this way
# consistently. A genuine public launch does not flap between 28/29 live and
# 1/29 live within minutes with no origin content ever served; an edge access
# rule that sometimes answers with a decoy 404 instead of dropping the
# connection does. So this state is still counted as the check having seen
# something real (unlike BLOCKED/DNS_TIMEOUT, which mean the check was
# blind) -- it just isn't a platform signal, so it is barred from LIVE the
# same way: it never sets first_live and never counts toward the live tally.
#
# NXDOMAIN and DNS_TIMEOUT are both decided primarily from curl's own attempt
# during the same HTTP probe that decides LIVE/PROVISIONED/BLOCKED -- not from
# a separate DNS lookup gating the whole host. Two incidents established why:
#
# 2026-09-08: resolve() called getent/python3 with no timeout at all. When
# this zone's real records stopped answering, the hang silently read as an
# empty result -- indistinguishable from a genuine negative -- and the whole
# 29-host zone was recorded NXDOMAIN, as if the entire production zone had
# vanished overnight. A control lookup of a name known not to exist under the
# same zone answered in under a second, while the 29 monitored hosts (which
# had resolved fine hours earlier) never answered at all: a resolver timeout,
# not a negative DNS response.
#
# 2026-09-09, same day the above fix landed: bounding resolve() with `timeout`
# and introducing a distinct DNS_TIMEOUT state stopped the false NXDOMAIN, but
# the local resolvers (getent, then python3's socket.getaddrinfo -- dig is
# absent from this image) kept hanging for minutes on every host regardless,
# so every run kept reporting DNS_TIMEOUT and never got a fresh reading. In
# the same runs, curl resolved and connected to every one of the same 29
# hosts in about a second. So the check now always attempts the curl probe
# -- even when resolve() itself timed out -- and only falls back to
# DNS_TIMEOUT when curl's own attempt also fails to get an answer (exit 28).
# resolve() still runs, bounded, purely to populate the informational
# "Resolves to" column; it never gates classification.
#
# Usage:  bash srp-domains/check.sh [--quiet]
# Exit:   0 = no state change, 1 = at least one host changed state, 2 = error
# ---------------------------------------------------------------------------

set -uo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 2
DIR="srp-domains"
MANIFEST="$DIR/manifest.json"
LOG="$DIR/reachability-log.csv"
STATUS="$DIR/status.md"
NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
TODAY="${NOW%%T*}"
QUIET=0
[ "${1:-}" = "--quiet" ] && QUIET=1

ZONE="cra-srp.enisa.europa.eu"
COUNTRIES=(at be bg cy cz de dk ee es fi fr gr hr hu ie it lt lu lv mt nl pl pt ro se si sk)
HOSTS=("portal.$ZONE" "auth.$ZONE")
for cc in "${COUNTRIES[@]}"; do HOSTS+=("$cc.$ZONE"); done
TOTAL=${#HOSTS[@]}

say() { [ "$QUIET" -eq 1 ] || printf '%s\n' "$*"; }

# --- trust mode -------------------------------------------------------------
# An intercepting proxy makes the TCP and TLS stages meaningless (see above).
TRUST="direct"
if [ -n "${HTTPS_PROXY:-}${https_proxy:-}" ]; then
  TRUST="proxied"
else
  issuer="$(echo | timeout 10 openssl s_client -connect "portal.$ZONE:443" \
            -servername "portal.$ZONE" 2>/dev/null | grep -m1 '^issuer=' || true)"
  case "$issuer" in *Anthropic*|*"Egress Gateway"*) TRUST="proxied" ;; esac
fi

# --- DNS ----------------------------------------------------------------
# Informational only -- classification never gates on this (see header).
# Prints "TIMEOUT" if every method that ran hung rather than answering, so
# the caller can tell that apart from a genuine negative response (empty
# output, no timeout).
resolve() {
  local h="$1" out="" rc tmp saw_timeout=0
  tmp="$(mktemp)"

  if command -v dig >/dev/null 2>&1; then
    timeout 5 dig +short +time=3 +tries=1 A "$h" >"$tmp" 2>/dev/null; rc=$?
    if [ $rc -eq 124 ]; then saw_timeout=1; else out="$(grep -E '^[0-9.]+$' "$tmp" || true)"; fi
  fi
  if [ -z "$out" ] && command -v getent >/dev/null 2>&1; then
    timeout 5 getent ahostsv4 "$h" >"$tmp" 2>/dev/null; rc=$?
    if [ $rc -eq 124 ]; then saw_timeout=1; else out="$(awk '{print $1}' "$tmp" | sort -u || true)"; fi
  fi
  if [ -z "$out" ] && command -v python3 >/dev/null 2>&1; then
    timeout 5 python3 -c 'import socket,sys
try: print("\n".join(sorted({r[4][0] for r in socket.getaddrinfo(sys.argv[1],None,socket.AF_INET)})))
except Exception: pass' "$h" >"$tmp" 2>/dev/null; rc=$?
    if [ $rc -eq 124 ]; then saw_timeout=1; else out="$(cat "$tmp")"; fi
  fi
  rm -f "$tmp"

  if [ -z "$out" ] && [ "$saw_timeout" -eq 1 ]; then
    printf 'TIMEOUT'
  else
    printf '%s' "$(echo "$out" | sort -u | paste -sd' ' -)"
  fi
}

# --- probes -----------------------------------------------------------------
probe_tcp() {  # $1 host -> open|closed
  timeout 8 bash -c "exec 3<>/dev/tcp/$1/443" 2>/dev/null && echo open || echo closed
}
probe_tls() {  # $1 host -> ok|fail
  echo | timeout 12 openssl s_client -connect "$1:443" -servername "$1" \
      >/dev/null 2>&1 && echo ok || echo fail
}

[ -f "$LOG" ] || echo "timestamp_utc,host,dns,tcp443,tls,http_code,note" > "$LOG"

declare -A ST HTTP DNSIP NOTE
live=0; blocked=0; nxdomain=0; dns_timeout=0; edge_blocked=0; resolved=0

for h in "${HOSTS[@]}"; do
  # resolve() is informational only (see its header): its local resolvers
  # have hung on this zone in practice. So its result never gates the probe
  # below -- curl always gets a chance, since curl has proven far more
  # reliable at resolving these hosts than getent/python3 in this
  # environment. dns_hung just remembers whether resolve() itself timed out,
  # for the DNS_TIMEOUT fallback if curl times out too.
  ips="$(resolve "$h")"
  dns_hung=0
  if [ "$ips" = "TIMEOUT" ]; then
    dns_hung=1
    ips=""
  fi
  DNSIP[$h]="$ips"

  if [ "$TRUST" = "proxied" ]; then
    tcp="unreliable"; tls="unreliable"
  else
    tcp="$(probe_tcp "$h")"; tls="$(probe_tls "$h")"
  fi

  err="$(mktemp)"; hdr="$(mktemp)"; body="$(mktemp)"
  code="$(curl -sS -D "$hdr" -o "$body" -m 20 --max-filesize 2000000 -w '%{http_code}' "https://$h/" 2>"$err")"
  rc=$?
  msg="$(tr -d '\r' < "$err" | tr '\n' ' ' | sed 's/,/;/g' | cut -c1-160)"
  rm -f "$err"

  if [ $rc -eq 0 ] && [ "$code" != "000" ] \
     && grep -qi 'x-protected-by:.*WEDOS' "$hdr" \
     && grep -q 'WEDOS\.protection' "$body"; then
    # The WEDOS edge answered with its own branded error page, not the SRP
    # origin -- see the 2026-09-11 header note above. Real, but not a
    # platform signal: never LIVE, never first_live, never in the live tally.
    ST[$h]=EDGE_BLOCKED; HTTP[$h]="$code"; NOTE[$h]="http $code (WEDOS.protection edge page, not origin)"; edge_blocked=$((edge_blocked+1))
  elif [ $rc -eq 0 ] && [ "$code" != "000" ]; then
    ST[$h]=LIVE; HTTP[$h]="$code"; NOTE[$h]="http $code"; live=$((live+1))
  elif [ $rc -eq 6 ]; then
    ST[$h]=NXDOMAIN; HTTP[$h]=000; NOTE[$h]="curl could not resolve host"
    nxdomain=$((nxdomain+1))
  elif [ $rc -eq 56 ] && printf '%s' "$msg" | grep -q '403'; then
    ST[$h]=BLOCKED; HTTP[$h]=000; NOTE[$h]="egress policy denied CONNECT: $msg"
    blocked=$((blocked+1))
  elif [ $rc -eq 28 ] && [ "$dns_hung" -eq 1 ]; then
    ST[$h]=DNS_TIMEOUT; HTTP[$h]=000; NOTE[$h]="DNS never answered (local resolver and curl both timed out) - check was blind"
    dns_timeout=$((dns_timeout+1))
  else
    ST[$h]=PROVISIONED; HTTP[$h]=000; NOTE[$h]="curl exit $rc: $msg"
  fi
  rm -f "$hdr" "$body"

  # "ok" used to be unconditional, so the log said DNS worked even when
  # resolve() had returned nothing: every run since 2026-09-09 wrote "dns,ok"
  # beside an empty "Resolves to" column in status.md, the go-live run of
  # 2026-09-11 included. Say "ok" only when an address actually came back;
  # "unknown" when nothing resolved and nothing positively failed. The zone's
  # IP pool has to be established by an external lookup, never from this
  # column reading ok.
  # Note that resolve() reports a lookup timeout as the sentinel string
  # TIMEOUT, not as an address, so a bare -n test would read it as success.
  case "${DNSIP[$h]}" in
    ""|TIMEOUT) dnscol="unknown" ;;
    *)          dnscol="ok" ;;
  esac
  case "${ST[$h]}" in NXDOMAIN) dnscol="fail" ;; DNS_TIMEOUT) dnscol="timeout" ;; esac
  [ "$dnscol" = "ok" ] && resolved=$((resolved+1))
  echo "$NOW,$h,$dnscol,$tcp,$tls,${HTTP[$h]},${ST[$h]} ${NOTE[$h]}" >> "$LOG"
  printf -v line '  %-12s %-34s %s' "${ST[$h]}" "$h" "${NOTE[$h]}"
  say "$line"
done

say ""
say "$live/$TOTAL live   (trust=$TRUST, blocked=$blocked, nxdomain=$nxdomain, dns_timeout=$dns_timeout, edge_blocked=$edge_blocked, resolved=$resolved/$TOTAL)"

# --- status.md (overwritten each run) ---------------------------------------
{
  echo "# SRP production reachability — current status"
  echo
  echo "Generated by \`srp-domains/check.sh\` on $NOW."
  echo
  echo "**$live/$TOTAL live**"
  echo
  if [ "$TRUST" = "proxied" ]; then
    echo "> Run behind an intercepting egress proxy: the TCP and TLS columns are"
    echo "> forged by the proxy and are reported as \`unreliable\`. Only the HTTP"
    echo "> column decides liveness. See the header of \`check.sh\`."
    echo
  fi
  [ "$blocked" -gt 0 ] && { echo "> $blocked host(s) BLOCKED by egress policy — the check was blind for those,"; echo "> which says nothing about the platform."; echo; }
  [ "$dns_timeout" -gt 0 ] && { echo "> $dns_timeout host(s) had DNS_TIMEOUT — neither the local resolver nor curl"; echo "> got an answer in time. Says nothing about the platform; the last"; echo "> confirmed state stands."; echo; }
  [ "$edge_blocked" -gt 0 ] && { echo "> $edge_blocked host(s) got a real HTTP response that was WEDOS's own"; echo "> branded error page (WEDOS.protection), not the SRP origin — an edge"; echo "> access rule answering instead of dropping the connection. Not a"; echo "> platform signal; see the header of \`check.sh\` (2026-09-11)."; echo; }
  [ "$resolved" -eq 0 ] && [ "$nxdomain" -eq 0 ] && { echo "> No host resolved to an address in this run, so the \"Resolves to\""; echo "> column is empty throughout and the log records \`dns,unknown\`. That is"; echo "> a property of this monitoring environment, not of the platform — the"; echo "> local resolver has been unavailable since 2026-09-09. Liveness above"; echo "> is unaffected; it is decided on the HTTP column alone."; echo; }
  echo "| Host | Status | HTTP | Resolves to | Last checked |"
  echo "|---|---|---|---|---|"
  for h in "${HOSTS[@]}"; do
    echo "| \`$h\` | ${ST[$h]} | ${HTTP[$h]} | ${DNSIP[$h]:-—} | $NOW |"
  done
} > "$STATUS"

# --- manifest.json ----------------------------------------------------------
CHANGED=0
if command -v python3 >/dev/null 2>&1 && [ -f "$MANIFEST" ]; then
  export _NOW="$NOW" _TODAY="$TODAY" _TRUST="$TRUST" _LIVE="$live" _TOTAL="$TOTAL"
  _rows=""
  for h in "${HOSTS[@]}"; do
    _rows+="$h|${ST[$h]}|${HTTP[$h]}|${DNSIP[$h]}"$'\n'
  done
  export _ROWS="$_rows"
  python3 - <<'PY'
import json, os, sys
m = json.load(open("srp-domains/manifest.json"))
now, today = os.environ["_NOW"], os.environ["_TODAY"]
by = {h["host"]: h for h in m.get("hosts", [])}
changed = []
# BLOCKED and DNS_TIMEOUT mean the check couldn't get a real answer this run
# (egress policy, or nothing answering in time). Neither is ever a platform
# statement: they must not overwrite the last confirmed state and must not
# count as a change, or a monitoring hiccup reads as a go-live or a
# zone-wide removal. See check.sh's header for the 2026-09-08/09 incidents.
INCONCLUSIVE = {"BLOCKED", "DNS_TIMEOUT"}
for line in os.environ["_ROWS"].strip().splitlines():
    host, state, code, ips = line.split("|", 3)
    e = by.get(host)
    if state in INCONCLUSIVE:
        # Wait for a confirmed answer before recording an unseen host as new.
        if e is not None:
            e["last_checked"] = now
            e[f"last_{state.lower()}_at"] = now
        continue
    if e is None:
        e = {"host": host, "role": "country", "first_live": None}
        m.setdefault("hosts", []).append(e); by[host] = e
        changed.append(f"new host in zone: {host}")
    e["last_checked"] = now
    prev = e.get("state")
    if prev != state:
        changed.append(f"{host}: {prev or 'unknown'} -> {state}")
    e["state"] = state
    e["dns"] = ips or None
    e["tcp443"] = "unreliable" if os.environ["_TRUST"] == "proxied" else e.get("tcp443")
    e["tls"] = "unreliable" if os.environ["_TRUST"] == "proxied" else e.get("tls")
    e["http_code"] = code
    # first_live is set ONLY from a real upstream HTTP response.
    if state == "LIVE" and not e.get("first_live"):
        e["first_live"] = now
        changed.append(f"{host}: FIRST LIVE at {now}")
m["last_check"] = today
m["last_run_trust"] = os.environ["_TRUST"]
m["live_count"] = int(os.environ["_LIVE"])
m["host_count"] = int(os.environ["_TOTAL"])
if changed:
    m["last_change"] = today
json.dump(m, open("srp-domains/manifest.json", "w"), indent=2, ensure_ascii=False)
open("srp-domains/manifest.json", "a").write("\n")
for c in changed:
    print("CHANGE: " + c, file=sys.stderr)
sys.exit(1 if changed else 0)
PY
  CHANGED=$?
fi

if [ "$CHANGED" -ne 0 ]; then
  say ""
  say "State changed — the monitoring routine should record a delta."
fi
exit "$CHANGED"

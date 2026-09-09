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
# curl's exit code separates the three states that matter:
#
#   HTTP code returned      -> LIVE          (upstream answered)
#   exit 35/28/7/52/56*     -> PROVISIONED   (connected, upstream dropped)
#   exit 56 + "403"         -> BLOCKED       (egress policy; check is blind,
#                                             never a statement about the SRP)
#   exit 6                  -> NXDOMAIN      (curl itself could not resolve)
#
# NXDOMAIN is decided from curl's own resolution, not from a separate DNS
# lookup: a standalone `getent`/glibc lookup has been observed to hang for
# minutes against this zone while curl resolves the same name in ~1s, which
# previously produced a false "whole zone gone" reading. See resolve()
# below.
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

# --- DNS --------------------------------------------------------------------
# Informational only -- see below for why classification does not gate on it.
# `getent`/`socket.getaddrinfo()` go through glibc's resolver (NSS "dns"
# module), which on this zone has been observed to hang for a long time
# (confirmed 2026-09-09: killed manually after 2+ minutes) rather than
# returning promptly, when `dig` is absent from the image. curl resolves the
# same names in ~1s in the same run, so this is a glibc/NSS resolution path
# problem, not a real DNS failure. Every call here is `timeout`-bounded so a
# hang can cost at most a few seconds per host instead of stalling resolve()
# -- and, before the fix below, silently turning the whole zone NXDOMAIN.
resolve() {
  local h="$1" out=""
  if command -v dig >/dev/null 2>&1; then
    out="$(timeout 5 dig +short +time=3 +tries=1 A "$h" 2>/dev/null | grep -E '^[0-9.]+$' || true)"
  fi
  if [ -z "$out" ] && command -v getent >/dev/null 2>&1; then
    out="$(timeout 5 getent ahostsv4 "$h" 2>/dev/null | awk '{print $1}' | sort -u || true)"
  fi
  if [ -z "$out" ] && command -v python3 >/dev/null 2>&1; then
    out="$(timeout 5 python3 -c 'import socket,sys
try: print("\n".join(sorted({r[4][0] for r in socket.getaddrinfo(sys.argv[1],None,socket.AF_INET)})))
except Exception: pass' "$h" 2>/dev/null || true)"
  fi
  printf '%s' "$(echo "$out" | sort -u | paste -sd' ' -)"
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
live=0; blocked=0; nxdomain=0

for h in "${HOSTS[@]}"; do
  # DNS classification comes from curl's own resolution (exit 6 = could not
  # resolve), not from the resolve() helper above: that helper can only ever
  # be informational (see its header) because its resolvers have hung on
  # this zone in practice, and gating NXDOMAIN on a hung lookup previously
  # produced a false "whole zone gone" result while curl itself resolved
  # every host fine. resolve() still runs, bounded, to populate DNSIP for
  # the status table.
  ips="$(resolve "$h")"
  DNSIP[$h]="$ips"

  if [ "$TRUST" = "proxied" ]; then
    tcp="unreliable"; tls="unreliable"
  else
    tcp="$(probe_tcp "$h")"; tls="$(probe_tls "$h")"
  fi

  err="$(mktemp)"
  code="$(curl -sS -o /dev/null -m 20 -w '%{http_code}' "https://$h/" 2>"$err")"
  rc=$?
  msg="$(tr -d '\r' < "$err" | tr '\n' ' ' | sed 's/,/;/g' | cut -c1-160)"
  rm -f "$err"

  if [ $rc -eq 0 ] && [ "$code" != "000" ]; then
    ST[$h]=LIVE; HTTP[$h]="$code"; NOTE[$h]="http $code"; live=$((live+1))
  elif [ $rc -eq 6 ]; then
    ST[$h]=NXDOMAIN; HTTP[$h]=000; NOTE[$h]="curl could not resolve host"
    nxdomain=$((nxdomain+1))
  elif [ $rc -eq 56 ] && printf '%s' "$msg" | grep -q '403'; then
    ST[$h]=BLOCKED; HTTP[$h]=000; NOTE[$h]="egress policy denied CONNECT: $msg"
    blocked=$((blocked+1))
  else
    ST[$h]=PROVISIONED; HTTP[$h]=000; NOTE[$h]="curl exit $rc: $msg"
  fi

  dnscol="ok"; [ "${ST[$h]}" = "NXDOMAIN" ] && dnscol="fail"
  echo "$NOW,$h,$dnscol,$tcp,$tls,${HTTP[$h]},${ST[$h]} ${NOTE[$h]}" >> "$LOG"
  printf -v line '  %-12s %-34s %s' "${ST[$h]}" "$h" "${NOTE[$h]}"
  say "$line"
done

say ""
say "$live/$TOTAL live   (trust=$TRUST, blocked=$blocked, nxdomain=$nxdomain)"

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
for line in os.environ["_ROWS"].strip().splitlines():
    host, state, code, ips = line.split("|", 3)
    e = by.get(host)
    if e is None:
        e = {"host": host, "role": "country", "first_live": None}
        m.setdefault("hosts", []).append(e); by[host] = e
        changed.append(f"new host in zone: {host}")
    prev = e.get("state")
    if prev != state:
        changed.append(f"{host}: {prev or 'unknown'} -> {state}")
    e["state"] = state
    e["dns"] = ips or None
    e["tcp443"] = "unreliable" if os.environ["_TRUST"] == "proxied" else e.get("tcp443")
    e["tls"] = "unreliable" if os.environ["_TRUST"] == "proxied" else e.get("tls")
    e["http_code"] = code
    e["last_checked"] = now
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

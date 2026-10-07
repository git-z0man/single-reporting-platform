"""Everything the sources publish about one vulnerability, and a page to read it on.

Sources, all public and read-only:
  - EUVD   /api/enisaid?id=...    the full EUVD record (products, versions, advisories, references)
  - NVD    services.nvd.nist.gov  the CVE record (CVSS metrics, CWE, references, CISA fields)
  - CISA   known_exploited_vulnerabilities.json   the KEV catalogue entry for the CVE
  - CERTs  links in the records whose host is a CERT or CSIRT, listed by host
  - EUVD   /api/honeypotObservations/batch?ids=...   Shadowserver honeypot sensor sightings, read for
           every entry on every run (one call per 50 entries); the EUVD page shows them as "Honeypot sensors"
  - EUVD   /api/kevEntries/batch?ids=...   the day each KEV catalogue (CISA KEV, EU KEV) added the entry,
           per source; read for every entry on every run

Stored per entry in euvd/details/<EUVD-ID>.json. Volatile fields (EPSS, EUVD's
dataProcessed stamp, the honeypot counts, averages and trend) are kept as last seen but
never count as a change. Of a honeypot sighting only the fact, firstSeenAt and the
product fields count: the counts move every day.
"""
import html
import json
import re
import subprocess
import time
import urllib.parse

EUVD_ONE = "https://euvdservices.enisa.europa.eu/api/enisaid?id="
NVD = "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId="
CISA = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
HONEYPOT = "https://euvdservices.enisa.europa.eu/api/honeypotObservations/batch?ids="
KEV_ENTRIES = "https://euvdservices.enisa.europa.eu/api/kevEntries/batch?ids="
HONEYPOT_VOLATILE = {"lastSeenAt", "connections1d", "uniqueIps1d", "avg7d", "avg30d", "avg90d", "trend", "isNew"}
VOLATILE = {"epss", "dataProcessed"} | HONEYPOT_VOLATILE
CERT_SOURCES = ("cert", "ncsc", "cisa", "csirt", "bsi", "cnsa")
# host suffix -> display name
CERT_HOSTS = {
    "cert.europa.eu": "CERT-EU", "wid.cert-bund.de": "CERT-Bund", "cert-bund.de": "CERT-Bund",
    "bsi.bund.de": "BSI", "cvcn.gov.it": "CVCN (IT)", "acn.gov.it": "ACN (IT)", "cert.pl": "CERT Polska",
    "csirt.divd.nl": "DIVD CSIRT", "ncsc.nl": "NCSC-NL", "ncsc.gov.uk": "NCSC-UK", "cert.ssi.gouv.fr": "CERT-FR",
    "cert-fr.cossi.fr": "CERT-FR", "cert.at": "CERT.at", "ncsc.admin.ch": "NCSC-CH", "kb.cert.org": "CERT/CC",
    "jpcert.or.jp": "JPCERT/CC", "cisa.gov": "CISA", "us-cert.cisa.gov": "CISA", "ncsc.fi": "NCSC-FI",
    "cert.be": "CERT.be", "cncs.gov.pt": "CNCS (PT)", "incibe.es": "INCIBE", "cyber.gc.ca": "CCCS (CA)",
}


# every field of CISA's known_exploited_vulnerabilities_schema.json, in the schema's order
KEV_FIELDS = [("cveID", "CVE"), ("vendorProject", "Vendor / project"), ("product", "Product"),
              ("vulnerabilityName", "Name"), ("dateAdded", "Added to catalogue"), ("shortDescription", "Description"),
              ("requiredAction", "Required action"), ("dueDate", "Due"),
              ("knownRansomwareCampaignUse", "Known ransomware use"), ("forensicTriage", "Forensic triage (BOD 26-04)"),
              ("notes", "Notes"), ("cwes", "CWEs")]


class FetchError(Exception):
    pass


def _get(url, retries=4):
    for n in range(retries):
        r = subprocess.run(["curl", "-sS", "-m", "90", "-w", "\n%{http_code}", "-H", "accept: application/json", url],
                           capture_output=True, text=True)
        body, _, code = r.stdout.rpartition("\n")
        if r.returncode == 0 and code == "200":
            return body
        if code in ("403", "429", "502", "503") or r.returncode:
            time.sleep(6 * (n + 1))
            continue
        raise FetchError(f"HTTP {code} for {url}")
    raise FetchError(f"gave up on {url}")


def euvd_record(euvd_id):
    try:
        return json.loads(_get(EUVD_ONE + urllib.parse.quote(euvd_id)))
    except ValueError:
        raise FetchError(f"not JSON for {euvd_id}")


def nvd_record(cve):
    """The NVD CVE object, or None when NVD does not know the CVE."""
    time.sleep(1.0)
    try:
        v = json.loads(_get(NVD + urllib.parse.quote(cve))).get("vulnerabilities", [])
    except ValueError:
        raise FetchError(f"not JSON for {cve} from NVD")
    return v[0]["cve"] if v else None


def cisa_catalog():
    """{cve: entry} from the CISA KEV catalogue."""
    try:
        d = json.loads(_get(CISA))
        return {v["cveID"]: v for v in d["vulnerabilities"]}
    except (ValueError, KeyError):
        raise FetchError("CISA catalogue not parseable")


def _batch(base, what, ids, chunk=50):
    """{EUVD-ID: [object]} from one of the EUVD's batch endpoints; an ID without data maps to [].
    An answer that leaves out a requested ID, or is not a mapping of lists of objects, is a failed fetch."""
    out = {}
    for i in range(0, len(ids), chunk):
        part = ids[i:i + chunk]
        try:
            d = json.loads(_get(base + ",".join(urllib.parse.quote(x) for x in part)))
        except ValueError:
            raise FetchError(f"{what} answer is not JSON")
        if not isinstance(d, dict) or set(part) - set(d) or not all(isinstance(d[x], list) and all(isinstance(o, dict) for o in d[x]) for x in part):
            raise FetchError(f"{what} answer incomplete for {sorted(set(part) - set(d or {}))[:5] or part[:3]}")
        out.update({x: d[x] for x in part})
    return out


def honeypot_batch(ids):
    return _batch(HONEYPOT, "honeypot", ids)


def kev_batch(ids):
    """{EUVD-ID: [{"kevSource": {"code": "CISA" | "EUKEV", ...}, "dateAdded": ...}]}"""
    return _batch(KEV_ENTRIES, "kevEntries", ids)


def strip_volatile(x):
    if isinstance(x, dict):
        return {k: strip_volatile(v) for k, v in x.items() if k not in VOLATILE}
    if isinstance(x, list):
        return [strip_volatile(v) for v in x]
    return x


def cert_links(*texts):
    """[(CERT name, url)] for every http(s) link in the given reference texts, deduplicated."""
    seen, out = set(), []
    for t in texts:
        for u in re.findall(r"https?://[^\s\"'<>]+", t or ""):
            host = urllib.parse.urlparse(u).hostname or ""
            for suffix, name in CERT_HOSTS.items():
                if host == suffix or host.endswith("." + suffix):
                    if u not in seen:
                        seen.add(u)
                        out.append([name, u])
                    break
    return sorted(out)


def build_detail(old, row, euvd, nvd, kev, honeypot=None, kev_sources=None):
    """Merge freshly fetched parts over the stored detail.

    euvd=None keeps the stored EUVD part; nvd=False keeps the stored NVD part and
    nvd=None records that NVD does not know the CVE."""
    d = dict(old or {})
    d["id"] = row["id"]
    if euvd is not None:
        d["euvd"] = euvd
    if nvd is not False:
        d["nvd"] = nvd
    d.setdefault("nvd", None)
    d["cisa_kev"] = kev
    if honeypot is not None:
        d["honeypot"] = honeypot
    d.setdefault("honeypot", [])
    if kev_sources is not None:
        d["kev_sources"] = sorted(({"source": (e.get("kevSource") or {}).get("code"), "dateAdded": e.get("dateAdded")}
                                   for e in kev_sources), key=lambda x: (str(x["source"]), str(x["dateAdded"])))
    refs = [(d.get("euvd") or {}).get("references"), json.dumps((d.get("nvd") or {}).get("references") or [])]
    d["cert_links"] = cert_links(*refs)
    return d


# ---------- the page ----------

def esc(x):
    return html.escape("" if x is None else str(x), quote=True)


def link(u, text=None):
    u = str(u)
    if not re.match(r"https?://", u):
        return esc(u)
    return f'<a href="{esc(u)}" rel="noopener noreferrer">{esc(text or u)}</a>'


def kv(rows):
    return "<dl>" + "".join(f"<dt>{esc(k)}</dt><dd>{v}</dd>" for k, v in rows if v not in (None, "", [])) + "</dl>"


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>" if items else ""


def nvd_metrics(nvd):
    out = []
    for fam, lst in ((nvd or {}).get("metrics") or {}).items():
        for m in lst:
            c = m.get("cvssData", {})
            out.append(f"{esc(fam)} {esc(c.get('baseScore'))} {esc(c.get('baseSeverity') or m.get('baseSeverity'))} "
                       f"<code>{esc(c.get('vectorString'))}</code> <small>({esc(m.get('source'))})</small>")
    return out


def advisory(src, x):
    first = (x.get("references") or "").split()
    title = esc(x.get("id")) if not first else link(first[0], x.get("id"))
    summ = (x.get("summary") or "").strip()
    summ = summ[:400] + " ..." if len(summ) > 400 else summ
    return (f"<b>{title}</b> <small>{esc(src)} · published {esc(x.get('datePublished'))} · updated {esc(x.get('dateUpdated'))}"
            f" · {len(x.get('advisoryProduct') or [])} products</small><br>{esc(x.get('description'))}"
            + (f"<br><small>{esc(summ)}</small>" if summ else ""))


def render_entry(row, d):
    e, n, k = d.get("euvd") or {}, d.get("nvd"), d.get("cisa_kev")
    cve = row["cve"]
    prods = [f"{esc((p.get('product') or {}).get('name'))} "
             f"<small>({esc(((p.get('product') or {}).get('vendor') or {}).get('name'))}) {esc(p.get('product_version'))}</small>"
             for p in e.get("enisaIdProduct") or []]
    euvd_refs = [link(u) for u in (e.get("references") or "").split()]
    sec = [f"<section><h4>EUVD</h4>" + kv([
        ("EUVD ID", link(f"https://euvd.enisa.europa.eu/enisa/{row['id']}", row["id"])),
        ("Aliases", esc(", ".join((e.get("aliases") or "").split()))),
        ("Description", esc(e.get("description"))), ("Assigner", esc(e.get("assigner"))),
        ("Published", esc(e.get("datePublished"))), ("Updated", esc(e.get("dateUpdated"))),
        ("Exploited since", esc(e.get("exploitedSince"))),
        ("Base score", esc(f"{e.get('baseScore')} (CVSS {e.get('baseScoreVersion')})") if e.get("baseScore") is not None else ""),
        ("Vector", f"<code>{esc(e.get('baseScoreVector'))}</code>" if e.get("baseScoreVector") else ""),
        ("EPSS (as last recorded)", esc(e.get("epss"))),
        ("Products", ul(prods)), ("References", ul(euvd_refs))]) + "</section>"]
    if n:
        desc = next((x["value"] for x in n.get("descriptions", []) if x.get("lang") == "en"), "")
        cwes = [w2["value"] for w in n.get("weaknesses", []) for w2 in w.get("description", [])]
        sec.append("<section><h4>NIST NVD</h4>" + kv([
            ("CVE", link("https://nvd.nist.gov/vuln/detail/" + cve, cve)), ("Status", esc(n.get("vulnStatus"))),
            ("Published", esc(n.get("published"))), ("Last modified", esc(n.get("lastModified"))),
            ("Description", esc(desc)), ("Metrics", ul(nvd_metrics(n))), ("Weaknesses", esc(", ".join(sorted(set(cwes))))),
            ("Source", esc(n.get("sourceIdentifier"))),
            ("References", ul([link(r["url"]) + (f" <small>{esc(', '.join(r.get('tags', [])))}</small>" if r.get("tags") else "")
                              for r in n.get("references", [])]))]) + "</section>")
    else:
        sec.append(f"<section><h4>NIST NVD</h4><p>No NVD record for {esc(cve) or 'this entry'}.</p></section>")
    if k:
        known = [x for x in KEV_FIELDS if x[0] in k]
        extra = sorted(set(k) - {x[0] for x in KEV_FIELDS})      # fields CISA adds later still show up
        rows = [(label, esc(", ".join(k[key]) if isinstance(k[key], list) else k[key])) for key, label in known]
        rows += [(key, esc(json.dumps(k[key], ensure_ascii=False))) for key in extra]
        sec.append("<section><h4>CISA KEV catalogue</h4>" + kv(rows) + "</section>")
    else:
        sec.append("<section><h4>CISA KEV catalogue</h4><p><strong>Not in the CISA catalogue.</strong> "
                   "Another source flagged this entry as exploited.</p></section>")
    ks = row.get("kev_sources") or {}
    sec.append("<section><h4>KEV catalogues (per source, via EUVD)</h4>" + kv([
        ("EU KEV added", esc(ks.get("EUKEV")) or "not listed"), ("CISA KEV added", esc(ks.get("CISA")) or "not listed")]
        + [(code, esc(day_)) for code, day_ in sorted(ks.items()) if code not in ("EUKEV", "CISA")]) + "</section>")
    hp = d.get("honeypot") or []
    sec.append("<section><h4>Honeypot sensors (Shadowserver, via EUVD)</h4>" + (
        "".join(kv([("CVE", esc(o.get("cveId"))), ("Source", esc(o.get("source"))),
                    ("First seen", esc(o.get("firstSeenAt"))), ("Last seen (as last recorded)", esc(o.get("lastSeenAt"))),
                    ("Last 24 h (as last recorded)", esc(f"{o['connections1d']} connections, {o.get('uniqueIps1d')} unique IPs")
                     if o.get("connections1d") is not None else ""),
                    ("Averages 7d / 30d / 90d", esc(f"{o.get('avg7d')} / {o.get('avg30d')} / {o.get('avg90d')}")
                     if o.get("avg7d") is not None else ""),
                    ("Trend (as last recorded)", esc(o.get("trend"))),
                    ("Product", esc(f"{o.get('vendor') or ''} {o.get('product') or ''}".strip())),
                    ("Class", esc(o.get("vulnClass")))]) for o in hp)
        or "<p>Not seen by the honeypot sensors.</p>") + "</section>")
    certs = d.get("cert_links") or []
    cert_adv, vendor_adv = [], []
    for a in e.get("enisaIdAdvisory") or []:
        x = a.get("advisory", a)
        src = (x.get("source") or {}).get("name", "") if isinstance(x.get("source"), dict) else str(x.get("source") or "")
        (cert_adv if any(t in src for t in CERT_SOURCES) else vendor_adv).append((src, x))
    sec.append("<section><h4>CERT and CSIRT</h4>" + (ul([f"{esc(nm)}: {link(u)}" for nm, u in certs]) or "<p>No CERT links in the records.</p>")
               + ("<h5>Advisories from CERTs</h5>" + ul([advisory(s_, x) for s_, x in cert_adv]) if cert_adv else "") + "</section>")
    if vendor_adv:
        sec.append(f"<section><h4>Vendor advisories ({len(vendor_adv)})</h4>" + ul([advisory(s_, x) for s_, x in vendor_adv]) + "</section>")
    badge = ("" if k else ' <span class="badge">not in CISA KEV</span>') + (' <span class="badge">SRP candidate (indication only)</span>' if row.get("candidate") else "") + (' <span class="badge">seen in honeypot</span>' if hp else "")
    kevs = f"; KEV event {esc(', '.join(row['kev']))}" if row["kev"] else ""
    return (f'<details data-text="{esc((row["id"] + " " + cve + " " + row["vendor"] + " " + (e.get("description") or "")).lower())}">'
            f'<summary><b>{esc(row["id"])}</b> {esc(cve)} · {esc(row["vendor"])} · exploited since {esc(row["exploitedSince"])}'
            f'{kevs} · score {esc(e.get("baseScore", ""))}{badge}</summary>{"".join(sec)}</details>')


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>EUVD exploited vulnerabilities</title>
<style>
:root{--bg:#fbfbf9;--fg:#1d2330;--mut:#5b6472;--line:#d9dde3;--card:#fff;--acc:#1f5fa8}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#14181f;--fg:#e4e8ee;--mut:#9aa4b2;--line:#2c3440;--card:#1b212b;--acc:#7db2ee}}
body{margin:0;padding:1rem 16px 3rem;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif}
main{max-width:62rem;margin:0 auto}h1{font-size:1.5rem}h4{margin:.8rem 0 .2rem}
.note{border-left:4px solid var(--acc);padding:.2rem .8rem;background:var(--card)}
input{width:100%;box-sizing:border-box;padding:.5rem;margin:1rem 0;border:1px solid var(--line);background:var(--card);color:var(--fg)}
details{border:1px solid var(--line);background:var(--card);margin:.4rem 0;padding:.4rem .7rem}summary{cursor:pointer}
dl{display:grid;grid-template-columns:10rem 1fr;gap:.2rem .8rem;margin:0}dt{color:var(--mut)}dd{margin:0;overflow-wrap:anywhere}
code{font-size:.85em}a{color:var(--acc)}.badge{border:1px solid var(--line);padding:0 .4rem;font-size:.8rem}
@media (max-width:640px){dl{grid-template-columns:1fr}}
</style></head><body><main>
<h1>EUVD: actively exploited vulnerabilities from 1 September 2026</h1>
<p class="note">Everything the EUVD, NIST NVD, the CISA KEV catalogue and linked CERTs publish about the entries below.
It does <strong>not</strong> say which entry was first reported through the SRP: no source records the reporting route.
Overview and caveats: <a href="../euvd-exploited-baseline.md">euvd-exploited-baseline.md</a>. Charts and statistics: <a href="stats.html">stats.html</a>. Data in <code>euvd/details/</code>.</p>
<input id="q" type="search" placeholder="Filter by ID, CVE, vendor or text" aria-label="Filter">
<p id="n">__COUNT__ entries</p>
__ENTRIES__
<script>
var q=document.getElementById('q'),items=[].slice.call(document.querySelectorAll('details[data-text]')),n=document.getElementById('n');
q.addEventListener('input',function(){var t=q.value.toLowerCase(),c=0;items.forEach(function(d){var s=d.dataset.text.indexOf(t)>=0;d.hidden=!s;if(s)c++});n.textContent=c+' of '+items.length+' entries'});
</script></main></body></html>
"""


def render_page(rows, details):
    body = "\n".join(render_entry(r, details[r["id"]]) for r in rows if r["id"] in details)
    return PAGE.replace("__COUNT__", str(len(rows))).replace("__ENTRIES__", body)

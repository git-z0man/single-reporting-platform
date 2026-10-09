// Draws the EUVD statistics page from the JSON embedded in it (built by euvd/build_stats.py).
// Every figure in the text is computed here from the data, so the page stays true as the data moves.
(function () {
const S = JSON.parse(document.getElementById('data').textContent);
const NS = 'http://www.w3.org/2000/svg';
const MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const GO = S.go_live;
const $ = (t, a = {}, p) => { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; };
const tx = (p, x, y, s, a = {}) => { const e = $('text', Object.assign({x, y}, a), p); e.textContent = s; return e; };
const tip = (e, s) => { const t = $('title'); t.textContent = s; e.appendChild(t); return e; };
const col = n => `var(--${n})`;
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmt = n => (n == null ? 'n/a' : Number(n).toLocaleString('en-GB'));
const B = s => `<strong>${s}</strong>`;
const mlabel = m => MON[+m.slice(5, 7) - 1] + ' ' + m.slice(2, 4);
const dlabel = d => `${+d.slice(8, 10)} ${MON[+d.slice(5, 7) - 1]} ${d.slice(0, 4)}`;
const days = (a, b) => Math.round((new Date(b) - new Date(a)) / 864e5);
const sum = a => a.reduce((x, y) => x + y, 0);
let N = 0;
const host = document.getElementById('panels');
let GN = 0;
function topLink() { const p = document.createElement('p'); p.className = 'top'; p.innerHTML = '<a href="#top">Back to top</a>'; host.appendChild(p); }
function group(title, text) { if (GN) topLink(); GN++; const h = document.createElement('div'); h.innerHTML = `<h2 class="g" id="g${GN}">${title}</h2><p class="lede" style="margin:0 0 .4rem">${text}</p>`; host.appendChild(h); }
function panel(title, kind, src, see, limit, build) {
  N++; const s = document.createElement('section'); s.className = 'p';
  s.innerHTML = `<h2><span class="tag">${kind}</span>${N}. ${title}</h2><p class="src">${src}</p><div class="c"></div><div class="see"><b class="h">What you see</b><span class="w"></span></div><p class="limit"><strong>Limits:</strong> ${limit}</p>`;
  host.appendChild(s);
  try { build(s.querySelector('.c')); s.querySelector('.w').innerHTML = typeof see === 'function' ? see() : see;
    if (s.querySelector('.c svg.wide')) { const h = document.createElement('p'); h.className = 'swipe'; h.textContent = 'Scroll sideways for the whole chart.'; s.insertBefore(h, s.querySelector('.c')); } }
  catch (e) { s.querySelector('.c').innerHTML = `<p>This chart could not be drawn from today's data (${esc(e.message)}).</p>`; }
}
function svg(w, h, el) { const e = $('svg', Object.assign({viewBox: `0 0 ${w} ${h}`, role: 'img'}, w >= 600 ? {class: 'wide'} : {})); el.appendChild(e); return e; }
function yAxis(g, x0, x1, y0, y1, max, ticks, f = v => fmt(v)) { for (let i = 0; i <= ticks; i++) { const v = max * i / ticks, y = y0 - (y0 - y1) * i / ticks; $('line', {x1: x0, x2: x1, y1: y, y2: y, stroke: col('grid')}, g); tx(g, x0 - 6, y + 4, f(v), {'text-anchor': 'end'}); } }
function niceTop(v, step) { return Math.max(step, Math.ceil(v / step) * step); }
function nice(max) { const steps = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 2500, 5000, 10000, 20000, 25000, 50000]; const st = steps.find(x => Math.ceil(Math.max(max, 1) / x) <= 8) || steps[steps.length - 1]; const top = Math.max(st, Math.ceil(Math.max(max, 1) / st) * st); return [top, top / st]; }
const mlong = m => ['January','February','March','April','May','June','July','August','September','October','November','December'][+m.slice(5, 7) - 1] + ' ' + m.slice(0, 4);
function legend(el, items) { const d = document.createElement('div'); d.className = 'leg'; d.innerHTML = items.map(([c, t]) => `<span><i style="background:var(--${c})"></i>${t}</span>`).join(''); el.appendChild(d); }
function table(el, head, rows) { const w = document.createElement('div'); w.className = 'tbl'; const t = document.createElement('table'); t.innerHTML = '<tr>' + head.map(h => `<th>${h}</th>`).join('') + '</tr>' + rows.map(r => '<tr>' + r.map(c => `<td>${c}</td>`).join('') + '</tr>').join(''); w.appendChild(t); el.appendChild(w); }
function hbars(el, rows, opt) { // rows: [label, value, value2?]
  const W = 900, rh = opt.two ? 30 : 21, L = opt.L || 180, R = 50, T = 6, H = T + rows.length * rh + 6; const g = $('g', {}, svg(W, H, el));
  const mx = Math.max(1, ...rows.map(r => Math.max(r[1], r[2] || 0)));
  rows.forEach((r, i) => { const y = T + i * rh; tx(g, L - 8, y + 12, r[0], {'text-anchor': 'end', class: 't'});
    const w1 = (W - L - R) * r[1] / mx; tip($('rect', {x: L, y, width: w1, height: opt.two ? 11 : 13, fill: col(opt.c1 || 'cisa')}, g), `${r[0]}: ${r[1]}`); tx(g, L + w1 + 5, y + 11, fmt(r[1]), {class: 't'});
    if (opt.two) { const w2 = (W - L - R) * r[2] / mx; $('rect', {x: L, y: y + 13, width: w2, height: 8, fill: col(opt.c2 || 'steady'), opacity: .65}, g); tx(g, L + w2 + 5, y + 21, fmt(r[2])); } });
}
function monthBars(el, months, stacks, opt = {}) { // stacks: [[colour, values[], name]]
  const W = 900, H = opt.H || 260, L = 52, R = 10, T = 14, Bm = 30; const g = $('g', {}, svg(W, H, el));
  const tot = months.map((_, i) => sum(stacks.map(s => s[1][i])));
  const [nt, nk] = nice(Math.max(...tot)), top = opt.pct ? 100 : nt; yAxis(g, L, W - R, H - Bm, T, top, opt.pct ? 4 : nk, opt.pct ? v => v + '%' : undefined);
  const bw = (W - L - R) / months.length;
  months.forEach((m, i) => { const x = L + i * bw + 1; let y = H - Bm;
    stacks.forEach(([c, v, n]) => { const val = opt.pct ? (tot[i] ? 100 * v[i] / tot[i] : 0) : v[i]; const h = (H - Bm - T) * val / top; y -= h; if (v[i]) tip($('rect', {x, y, width: Math.max(bw - 2, 1), height: h, fill: col(c)}, g), `${m} ${n}: ${v[i]}`); });
    if (months.length > 30 ? m.endsWith('-01') : (i % 3 === 0)) tx(g, x, H - Bm + 14, mlabel(m));
    if (opt.mark && m === opt.mark) { $('line', {x1: x + bw / 2, x2: x + bw / 2, y1: T, y2: H - Bm, stroke: col('up'), 'stroke-dasharray': '3 3'}, g); tx(g, x + bw / 2 - 4, T + 8, 'SRP live', {'text-anchor': 'end', class: 't'}); } });
  return {g, L, W, H, Bm, T, bw, top};
}

document.getElementById('gen').textContent = dlabel(S.generated);
const mode = document.getElementById('mode');
if (mode && !mode.textContent) mode.textContent = 'Charts drawn in your browser from the data embedded in this page.';

// ================= Part 1: the EUVD as a whole =================
const G = S.gen;
group('Part 1: The EUVD as a whole', `All ${fmt(G.euvd_total)} records, not only the exploited ones. Counts come from <code>/api/search</code> with <code>fromDate</code>/<code>toDate</code> (publication date) and the <code>assigner</code> and <code>fromScore</code> filters; the field <code>total</code> gives the count without downloading the records.`);

panel('Records published per month', 'Volume', `<code>/api/search</code> totals per month, ${mlong(G.months[0])} to ${dlabel(S.generated)} (documented filters).`,
  () => { const full = G.months.length - 2, m = G.months[full], prev12 = G.all.slice(Math.max(0, full - 12), full), avg = Math.round(sum(prev12) / Math.max(1, prev12.length));
    const mx = Math.max(...G.all), mm = G.months[G.all.indexOf(mx)];
    return `Each bar is the number of records the EUVD published that month; the <span style="color:var(--up)">red part</span> is the critical ones (CVSS 9 or more). The last full month, ${B(mlong(m))}, had ${B(fmt(G.all[full]))} records (${fmt(G.crit[full])} critical), against an average of ${fmt(avg)} a month over the twelve months before it. ${mm === m ? 'It is the busiest month shown.' : `The busiest month shown is ${mlong(mm)} with ${fmt(mx)}.`}`; },
  'The date is when the EUVD published the record, not when the vulnerability was found. A jump can mean the EUVD ingested a new source rather than that more vulnerabilities exist; the API does not say which. The last bar is the current, unfinished month.',
  c => { const r = monthBars(c, G.months, [['up', G.crit, 'critical'], ['cisa', G.all.map((v, i) => v - G.crit[i]), 'other']], {step: 2000, H: 280}); legend(c, [['up', 'critical (CVSS 9+)'], ['cisa', 'other records']]); });

panel('European assigners, month by month', 'Small multiples', `<code>/api/search?assigner=...</code> totals per month for ${G.assigners.length} European CNAs, national CSIRTs and European vendors. The assigner is the body that issued the CVE record.`,
  () => { const last = G.assigners.map(([k, n, v, t]) => [n, sum(v.slice(-13, -1)), sum(v.slice(-7, -1)), sum(v.slice(-13, -7))]).sort((a, b) => b[1] - a[1]);
    const grow = last.filter(r => r[3] > 0 && r[2] >= 2 * r[3] && r[2] >= 10).map(r => r[0]);
    return `One small chart per assigner, same months as panel 1, each scaled to its own maximum (the number at top right). Most active over the last twelve full months: ${B(last[0][0])} (${fmt(last[0][1])}), ${last[1][0]} (${fmt(last[1][1])}) and ${last[2][0]} (${fmt(last[2][1])}). ${grow.length ? `At least doubled in the last six months against the six before: ${grow.join(', ')}.` : 'None of them doubled its output in the last six months.'} ${G.detail.name} is highlighted and shown in detail in panel 4.`; },
  `Each chart has its own scale, so compare shapes, not heights. Only the assigners listed here are counted; the API offers no list of all assigners (<code>/api/assigners/names</code> returns seven names), so the list is a choice made in <code>euvd/build_stats.py</code>. A vendor that uses a CSIRT as its CNA appears under the CSIRT.`,
  c => { const wrap = document.createElement('div'); wrap.style.cssText = 'display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.6rem'; c.appendChild(wrap);
    G.assigners.forEach(([k, n, v, tot]) => { const hi = k === G.detail.assigner, box = document.createElement('div'); box.style.cssText = 'border:1px solid var(--line);padding:.4rem .5rem' + (hi ? ';outline:2px solid var(--acc)' : ''); wrap.appendChild(box);
      box.innerHTML = `<div style="font-size:.85rem;color:var(--fg)">${esc(n)}</div><div style="font-size:.75rem;color:var(--mut)">${fmt(tot)} in total, ${fmt(sum(v.slice(-13, -1)))} in the last 12 months</div>`;
      const W = 200, H = 60, mx = Math.max(...v, 1), bw = W / v.length, g = $('g', {}, svg(W, H, box)); tx(g, W - 2, 10, mx, {'text-anchor': 'end'});
      v.forEach((x, i) => { const h = (H - 14) * x / mx; tip($('rect', {x: i * bw + .5, y: H - h, width: bw - 1, height: h, fill: col(hi ? 'acc' : 'cisa'), opacity: hi ? 1 : .75}, g), `${n} ${G.months[i]}: ${x}`); }); }); });

panel('Where European assigners stand', 'Ranking', '<code>/api/search?assigner=...</code> totals over all years, the European CNAs above against some of the largest global ones.',
  () => { const eu = G.rank.filter(r => r[2]), top = G.rank[0], topEu = eu[0], share = 100 * sum(eu.map(r => r[1])) / G.euvd_total;
    return `Bars on a logarithmic scale, <span style="color:var(--acc)">European assigners</span> in blue and global ones in grey. ${top[0]} has issued ${B(fmt(top[1]))} records; the largest European assigner here, ${topEu[0]}, ${fmt(topEu[1])}. The ${eu.length} European assigners listed together account for ${B(share.toFixed(1) + '%')} of the EUVD's ${fmt(G.euvd_total)} records.`; },
  'A logarithmic scale makes small numbers visible but shrinks large differences: each grid step is ten times the one before. The global list is a selection, not the complete top.',
  c => { const d = G.rank, W = 900, rh = 21, L = 200, R = 70, T = 22, H = T + d.length * rh + 6, g = $('g', {}, svg(W, H, c)), hi = Math.ceil(Math.log10(Math.max(10, d[0][1]))), X = v => L + (W - L - R) * Math.log10(Math.max(v, 1)) / hi;
    for (let k = 0; k <= hi; k++) { const x = X(Math.pow(10, k)); $('line', {x1: x, x2: x, y1: T - 6, y2: H - 4, stroke: col('grid')}, g); tx(g, x, T - 10, fmt(Math.pow(10, k)), {'text-anchor': 'middle'}); }
    d.forEach((r, i) => { const y = T + i * rh, w = X(r[1]) - L; tx(g, L - 8, y + 12, r[0], {'text-anchor': 'end', class: 't'}); $('rect', {x: L, y: y + 2, width: Math.max(w, 1), height: 13, fill: col(r[2] ? 'acc' : 'steady'), opacity: r[2] ? 1 : .6}, g); tx(g, L + w + 5, y + 13, fmt(r[1])); }); });

const V = G.detail;
panel(`${V.name} in detail`, 'Profile', `<code>/api/search?assigner=${esc(V.assigner)}</code>, all ${fmt(V.n)} records, with the EUVD record fields <code>datePublished</code>, <code>baseScore</code>, <code>epss</code> and vendor.`,
  () => { const yl = V.years[V.years.length - 1] || ['', 0], sev = V.sev.slice(0, 4).sort((a, b) => b[1] - a[1])[0];
    return `${B(`${esc(V.name)} assigns records in the EUVD`)}, as CNA <code>${esc(V.assigner)}</code>: ${fmt(V.n)} in all. Left: records by year of publication, ${fmt(yl[1])} in ${yl[0]} so far. Middle: the vendors they cover, led by ${V.vendors.slice(0, 3).map(v => esc(v[0])).join(', ')}. Right: severity; the largest group is ${sev[0].toLowerCase()}. ${V.exploited ? B(`${V.exploited} of them are flagged as exploited.`) : B('None of the records is flagged as exploited.')} The table lists the records with the highest EPSS, the modelled chance of exploitation.`; },
  `Assigning a CVE is not the same as reporting an exploited vulnerability: a CNA coordinates disclosure for the vendors it covers. A high EPSS is a prediction, not evidence of exploitation. ${fmt(V.undated)} records carry no publication date and are left out of the yearly count. Which assigner is shown here is set in <code>euvd/build_stats.py</code>.`,
  c => { const wrap = document.createElement('div'); wrap.style.cssText = 'display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1rem'; c.appendChild(wrap); const mk = () => { const d = document.createElement('div'); wrap.appendChild(d); return d; };
    let W = 280, H = 200, L = 34, R = 6, T = 14, Bm = 26, g = $('g', {}, svg(W, H, mk())); const [top, tk] = nice(Math.max(1, ...V.years.map(r => r[1]))); yAxis(g, L, W - R, H - Bm, T, top, tk); const bw = (W - L - R) / Math.max(1, V.years.length);
    V.years.forEach((r, i) => { const h = (H - Bm - T) * r[1] / top, x = L + i * bw + 3; $('rect', {x, y: H - Bm - h, width: bw - 6, height: h, fill: col('acc')}, g); tx(g, x + (bw - 6) / 2, H - Bm - h - 4, r[1], {'text-anchor': 'middle', class: 't'}); tx(g, x + (bw - 6) / 2, H - Bm + 13, "'" + r[0].slice(2), {'text-anchor': 'middle'}); });
    const vv = V.vendors, rh = 19, L2 = 118; g = $('g', {}, svg(W, vv.length * rh + 6, mk())); const mv = Math.max(1, ...vv.map(r => r[1]));
    vv.forEach((r, i) => { const y = 3 + i * rh, w = (W - L2 - 30) * r[1] / mv; tx(g, L2 - 5, y + 11, String(r[0]).slice(0, 18), {'text-anchor': 'end', class: 't'}); $('rect', {x: L2, y, width: w, height: 12, fill: col('cisa')}, g); tx(g, L2 + w + 4, y + 11, r[1]); });
    const cs = ['up', 'eu', 'both', 'down', 'steady']; g = $('g', {}, svg(W, V.sev.length * 30 + 6, mk())); const ms = Math.max(1, ...V.sev.map(r => r[1]));
    V.sev.forEach((r, i) => { const y = 4 + i * 30, w = (W - 20) * r[1] / ms; tx(g, 0, y + 10, `${r[0]}: ${r[1]}`, {class: 't'}); $('rect', {x: 0, y: y + 14, width: w, height: 9, fill: col(cs[i])}, g); });
    table(c, ['Record', 'Vendor', 'CVSS', 'EPSS'], V.epss_top.map(r => [esc(r[0]), esc(r[3]), esc(r[2] ?? ''), r[1] + '%'])); });

// ================= Part 2: flagged, and when =================
group('Part 2: What gets flagged, and when', `The ${fmt(S.total)} EUVD entries flagged as exploited and the KEV catalogues behind them, CISA KEV and the EU KEV: how many arrive, and how long after publication. Colours: <span style="color:var(--cisa)">CISA KEV only</span>, <span style="color:var(--both)">both catalogues</span>, <span style="color:var(--eu)">EU KEV only</span>.`);

panel('Known-exploited additions per month', 'Time series', '<code>/api/kev/dump</code> (documented): one entry per CVE with its earliest date across CISA KEV and EU KEV, refreshed daily by ENISA.',
  () => { const d = S.kev_month, last = d[d.length - 2] || d[d.length - 1], eu = sum(d.map(r => r[2] + r[3])), all = sum(d.map(r => r[1] + r[2] + r[3]));
    return `Each bar is one month, split by which catalogue lists the CVE; the dashed line marks the SRP go-live month. CISA dominates: ${fmt(all - eu)} of ${fmt(all)} entries are in CISA's catalogue only, ${fmt(eu)} are also or only in the EU KEV. The last full month, ${mlong(last[0])}, added ${fmt(last[1] + last[2] + last[3])}. The tall bars at the start are CISA building up its catalogue in 2021 and 2022, not surges.`; },
  'The month of the earliest date, not of the latest listing. It says what is flagged as exploited, not how it reached ENISA; nothing in this chart can show SRP reporting.',
  c => { const d = S.kev_month; monthBars(c, d.map(r => r[0]), [['cisa', d.map(r => r[1]), 'CISA only'], ['both', d.map(r => r[2]), 'both'], ['eu', d.map(r => r[3]), 'EU KEV only']], {step: 20, H: 300, mark: GO.slice(0, 7)}); });

panel('Daily additions, recent weeks', 'Time series', `The same dump, by day, ${dlabel(S.kev_day_from)} to ${dlabel(S.generated)}.`,
  () => { const n = sum(S.kev_day.map(r => r[1] + r[2] + r[3])), dd = days(S.kev_day_from, S.generated) + 1;
    return `One bar per day with at least one addition; the dashed line is the SRP go-live (${dlabel(GO)}) when it falls in the window. ${fmt(n)} additions on ${S.kev_day.length} of ${dd} days. Most days without a bar are weekends.`; },
  'A day without a bar is a day without additions, not missing data. Daily counts are small and noisy; do not read a trend out of a few days.',
  c => { const W = 900, H = 240, L = 34, R = 10, T = 12, Bm = 26, g = $('g', {}, svg(W, H, c)), a = new Date(S.kev_day_from), n = days(S.kev_day_from, S.generated) + 1, bw = (W - L - R) / n, m = {};
    S.kev_day.forEach(r => m[r[0]] = r); const [top, tk] = nice(Math.max(4, ...S.kev_day.map(r => r[1] + r[2] + r[3]))); yAxis(g, L, W - R, H - Bm, T, top, tk);
    for (let i = 0; i < n; i++) { const dt = new Date(a.getTime() + i * 864e5), k = dt.toISOString().slice(0, 10), r = m[k], x = L + i * bw; let y = H - Bm;
      if (r) [['cisa', r[1]], ['both', r[2]], ['eu', r[3]]].forEach(([c2, v]) => { const h = (H - Bm - T) * v / top; y -= h; if (v) tip($('rect', {x: x + 1, y, width: Math.max(bw - 2, 1), height: h, fill: col(c2)}, g), `${k}: ${v}`); });
      if (dt.getUTCDay() === 1) tx(g, x, H - Bm + 14, `${dt.getUTCDate()} ${MON[dt.getUTCMonth()]}`);
      if (k === GO) { $('line', {x1: x + bw / 2, x2: x + bw / 2, y1: T, y2: H - Bm, stroke: col('up'), 'stroke-dasharray': '3 3'}, g); tx(g, x + bw / 2 + 4, T + 8, 'SRP live', {class: 't'}); } } });

panel('How long after publication was an entry flagged?', 'Distribution', `EUVD record <code>datePublished</code> against <code>exploitedSince</code>, for entries flagged in the last 12 months (${fmt(S.tte_n)} entries).`,
  () => { const t = S.tte, top = [...t].sort((a, b) => b[1] - a[1])[0];
    return `Bars count entries by the gap between publication in the EUVD and the day they were flagged as exploited. The largest group is ${B(top[0])} (${top[1]} entries); ${t[6][1]} waited more than a year. The median gap is ${B(S.tte_median + ' days')}.`; },
  '"Before publication" means flagged before the EUVD record existed, usually a record created late. The gap measures when an entry was flagged, not when exploitation began.',
  c => { const d = S.tte, W = 900, H = 260, L = 40, R = 10, T = 14, Bm = 30, g = $('g', {}, svg(W, H, c)), [top, tk] = nice(Math.max(...d.map(r => r[1]))); yAxis(g, L, W - R, H - Bm, T, top, tk); const bw = (W - L - R) / d.length;
    d.forEach((r, i) => { const h = (H - Bm - T) * r[1] / top, x = L + i * bw + 10; $('rect', {x, y: H - Bm - h, width: bw - 20, height: h, fill: col('cisa')}, g); tx(g, x + (bw - 20) / 2, H - Bm - h - 5, r[1], {'text-anchor': 'middle', class: 't'}); tx(g, x + (bw - 20) / 2, H - Bm + 16, r[0], {'text-anchor': 'middle'}); }); });

panel('Who is faster: the EUVD or the KEV catalogues?', 'Comparison', `EUVD record <code>datePublished</code> against <code>exploitedSince</code> (the earliest KEV date), for every exploited entry flagged since ${mlong(S.speed_all.from)} (${fmt(S.speed_all.n)} entries), by month of flagging. Months with fewer than 5 entries are left out.`,
  () => { const A = S.speed_all, ms = S.speed_month.filter(r => r.n >= 5), first = sum(ms.map(r => r.first)), n = sum(ms.map(r => r.n)), lowest = Math.min(...ms.map(r => r.median));
    return `${B('Top:')} per month, how many entries were in the EUVD <span style="color:var(--cisa)">first</span>, on the <span style="color:var(--both)">same day</span>, or flagged by a KEV catalogue <span style="color:var(--eu)">first</span>; the EUVD was first for ${B(Math.round(100 * first / Math.max(1, n)) + '%')}. ${B('Bottom:')} the gap in days, bars for the ${B('median')} and hollow dots for the ${B('mean')}. Over the period the median is ${fmt(A.median)} days and the mean ${fmt(Math.round(A.mean))}: a few entries waited years, which pulls the mean up, so the median is the fairer "average". Since the go-live (${A.golive_n} entries) the median is ${fmt(A.golive_median)} and the mean ${fmt(Math.round(A.golive_mean))}${A.golive_median <= lowest ? ', as short as any month in the series' : ''}.`; },
  'The gap runs from the EUVD record to the first KEV listing: how long an entry waited in the EUVD before being flagged, not which source knew first, since a vulnerability may have been public elsewhere earlier. A change in the gap is an observation; the chart cannot say why it changed.',
  c => { const d = S.speed_month.filter(r => r.n >= 5), W = 900, L = 44, R = 10, bw = (W - L - R) / d.length;
    let g = $('g', {}, svg(W, 230, c)); const T = 14, Bm = 30, H = 230; yAxis(g, L, W - R, H - Bm, T, 100, 4, v => v + '%');
    d.forEach((r, i) => { const x = L + i * bw + 2; let y = H - Bm; [['cisa', r.first, 'EUVD first'], ['both', r.same, 'same day'], ['eu', r.kev, 'KEV first']].forEach(([k, v, n]) => { const h = (H - Bm - T) * v / r.n; y -= h; if (v) tip($('rect', {x, y, width: bw - 4, height: h, fill: col(k)}, g), `${r.m} ${n}: ${v} of ${r.n}`); }); if (i % 3 === 0) tx(g, x, H - Bm + 14, mlabel(r.m)); });
    g = $('g', {}, svg(W, 250, c)); const H2 = 250, T2 = 22, lg = v => Math.log10(Math.max(v, 0) + 1), top = Math.max(3, Math.ceil(lg(Math.max(...d.map(r => r.mean)))));
    [0, 1, 10, 100, 1000, 10000].filter(v => lg(v) <= top).forEach(v => { const y = H2 - Bm - (H2 - Bm - T2) * lg(v) / top; $('line', {x1: L, x2: W - R, y1: y, y2: y, stroke: col('grid')}, g); tx(g, L - 6, y + 4, fmt(v), {'text-anchor': 'end'}); });
    tx(g, L, 12, 'days from EUVD record to first KEV listing (log scale)');
    d.forEach((r, i) => { const x = L + i * bw + 2, y = H2 - Bm - (H2 - Bm - T2) * lg(r.median) / top; tip($('rect', {x, y, width: bw - 4, height: H2 - Bm - y, fill: col('cisa'), opacity: .8}, g), `${r.m}: median ${r.median} days, mean ${r.mean}, ${r.n} entries`);
      $('circle', {cx: x + (bw - 4) / 2, cy: H2 - Bm - (H2 - Bm - T2) * lg(r.mean) / top, r: 3.5, fill: 'var(--card)', stroke: col('up'), 'stroke-width': 1.6}, g); if (i % 3 === 0) tx(g, x, H2 - Bm + 14, mlabel(r.m)); }); });

panel('How often do exploited entries change?', 'Change', 'EUVD records: <code>dateUpdated</code> of the exploited entries per day, last 30 days. Also available through <code>fromUpdatedDate</code> in <code>/api/search</code>.',
  () => { const u = S.updates, mx = u.reduce((a, r) => r[1] > a[1] ? r : a, ['', 0]);
    return `Each bar is the number of exploited entries the EUVD edited that day (scores, references, advisories, product data): ${fmt(sum(u.map(r => r[1])))} edits in 30 days, most on ${mx[0] ? dlabel(mx[0]) : 'n/a'} (${mx[1]}).`; },
  'Editing activity on the record, not a change in whether something is exploited. A change in the exploited status itself shows up only by comparing daily snapshots, which this monitor keeps.',
  c => { const W = 900, H = 220, L = 34, R = 10, T = 12, Bm = 28, g = $('g', {}, svg(W, H, c)), m = Object.fromEntries(S.updates), [top, tk] = nice(Math.max(1, ...S.updates.map(r => r[1]))), bw = (W - L - R) / 30; yAxis(g, L, W - R, H - Bm, T, top, tk);
    for (let i = 0; i < 30; i++) { const k = new Date(new Date(S.updates_from).getTime() + i * 864e5).toISOString().slice(0, 10), v = m[k] || 0, h = (H - Bm - T) * v / top; if (v) tip($('rect', {x: L + i * bw + 1, y: H - Bm - h, width: bw - 2, height: h, fill: col('cisa')}, g), `${k}: ${v} entries`); if (i % 5 === 0) tx(g, L + i * bw, H - Bm + 14, k.slice(5)); } });

// ================= Part 3: EU KEV and the SRP =================
group('Part 3: EU KEV and the SRP', `The EU KEV, the catalogue ENISA keeps with the EU CSIRTs Network, against CISA's, and the entries whose dates fit an early notification. None of this shows the reporting route; the background is in <a href="https://github.com/git-z0man/single-reporting-platform/blob/main/euvd/EU-KEV.md">EU-KEV.md</a>.`);

const LD = S.lead;
panel('EU KEV against CISA: who lists a vulnerability first', 'Comparison', `<code>/api/kevEntries/batch</code> (undocumented): the day each catalogue added every entry the EU KEV lists. Shown: the entries the EU KEV added since ${dlabel(S.dumb_from)}.`,
  () => `One row per entry, newest at the top. A <span style="color:var(--eu)">gold</span> dot is the EU KEV date, a <span style="color:var(--cisa)">blue</span> dot the CISA date, joined by a grey line; a triangle at the left edge means CISA listed it before the window. In the last 90 days (${LD.recent.n} entries in both catalogues) the EU KEV was first for ${B(LD.recent.eu_first)}, on the same day for ${B(LD.recent.same)} and later for ${B(LD.recent.cisa_first)}; the median gap is ${fmt(LD.recent.median)} days. Before that (${LD.old.n} entries) CISA was first for ${LD.old.cisa_first}, with a median of ${fmt(Math.abs(LD.old.median ?? 0))} days: the EU KEV largely added older CISA entries. Rows with only a gold dot are not in CISA's catalogue.`,
  `The EU KEV is not the SRP. Its dates go back to ${S.eu_first_date ? dlabel(S.eu_first_date) : 'n/a'}, and ${S.eu_go_gap.length ? `${S.eu_go_gap.length} entries carry` : 'no entry carries'} an EU KEV date in the ten days from the go-live. An entry the EU KEV listed after the go-live and CISA did not, or did later, is a candidate for an SRP origin, nothing more. The date is when the catalogue added the entry, not when the vulnerability was reported.`,
  c => { const A = S.dumb_from, d = S.dumbbell.filter(r => r.eu >= A); if (!d.length) { c.innerHTML = '<p>No EU KEV entries in the window.</p>'; return; }
    const W = 900, rh = 13, L = 24, R = 24, T = 30, H = T + d.length * rh + 30, wrap = document.createElement('div'); wrap.className = 'scroll'; c.appendChild(wrap); const g = $('g', {}, svg(W, H, wrap)), a = +new Date(A), b = +new Date(S.generated) + 864e5, X = v => L + (W - L - R) * (Math.max(+new Date(v), a) - a) / (b - a);
    for (let t = new Date(A); +t <= b; t = new Date(Date.UTC(t.getUTCFullYear(), t.getUTCMonth() + 1, 1))) { const m = t.toISOString().slice(0, 10), x = X(m); if (m.endsWith('-01')) { $('line', {x1: x, x2: x, y1: T - 8, y2: H - 24, stroke: col('grid')}, g); tx(g, x + 3, T - 12, mlabel(m)); } }
    if (GO >= A) { const x = X(GO); $('line', {x1: x, x2: x, y1: T - 8, y2: H - 24, stroke: col('up'), 'stroke-dasharray': '3 3'}, g); tx(g, x, H - 8, 'SRP live', {'text-anchor': 'middle', class: 't'}); }
    d.forEach((r, i) => { const y = T + i * rh + 4, old = r.cisa && r.cisa < A; if (r.cisa) $('line', {x1: X(r.eu), x2: X(r.cisa), y1: y, y2: y, stroke: col('steady'), opacity: .6}, g);
      tip($('circle', {cx: X(r.eu), cy: y, r: 3.5, fill: col('eu')}, g), `${r.id} ${r.cve}: EU KEV ${r.eu}, CISA ${r.cisa || 'not listed'}, source ${r.origin}`);
      if (r.cisa && !old) $('circle', {cx: X(r.cisa), cy: y, r: 3.5, fill: col('cisa')}, g); if (old) $('path', {d: `M${L} ${y} l7 -4 v8 z`, fill: col('cisa')}, g); }); });

const CAND = S.dumbbell.filter(r => r.eu >= GO && (!r.cisa || r.cisa > r.eu)).sort((a, b) => a.eu < b.eu ? 1 : -1);
panel('Candidates: entries flagged after the go-live', 'Indication', 'From the previous panel: EU KEV date on or after the go-live, and CISA either absent or later. The same rule as <code>candidate</code> in <code>euvd/exploited.json</code>.',
  () => `A list rather than a chart: each row is an entry and the reason it qualifies. ${B(CAND.length + (CAND.length === 1 ? ' entry qualifies' : ' entries qualify'))} today.`,
  'The criteria are mechanical. A candidate may well have come from the vendor, a CSIRT or a researcher outside the SRP; no public source records the reporting route. The monitor applies the same rule only to the entries in its window (<code>euvd/exploited.json</code>), this panel to every EU KEV entry, so the two can differ for a day when the EU KEV adds a back-dated entry.',
  c => { if (!CAND.length) { c.innerHTML = '<p>No entry qualifies.</p>'; return; } table(c, ['Entry', 'CVE', 'EU KEV', 'CISA KEV', 'EU KEV source', 'Why it qualifies'], CAND.map(r => [esc(r.id), esc(r.cve), r.eu, r.cisa || 'not listed', esc(r.origin), r.cisa ? `EU KEV first, CISA ${days(r.eu, r.cisa)} days later` : 'EU KEV only'])); });

panel('Who reports into the EU KEV', 'Sources', '<code>/api/kevEntries/batch</code> (undocumented): the <code>originSource</code> of every EU KEV entry, the body that brought it in. Spellings are merged (for example <code>cnw</code> and <code>CNW</code>).',
  () => { const newer = S.origin.filter(r => r[2] > 0 && r[1] === 0);
    return `Pairs of bars per source: <span style="color:var(--steady)">grey</span> before the go-live, <span style="color:var(--eu)">gold</span> from ${dlabel(GO)}. ${newer.length ? `Appearing ${B('only after the go-live')}: ${newer.map(r => `${esc(r[0])} (${r[2]})`).join(', ')}.` : 'No source appears only after the go-live.'} The table lists every entry added since the go-live with its source.`; },
  'The origin is who brought the entry into the EU KEV, not how the vulnerability first reached anyone; a CSIRT can learn of exploitation in many ways besides an SRP notification. Still the most direct pointer the public data offers towards the SRP, because CRA notifications go to a national CSIRT.',
  c => { hbars(c, S.origin.map(r => [r[0], r[1], r[2]]), {two: true, L: 180, c1: 'steady', c2: 'eu'}); table(c, ['EU KEV date', 'Entry', 'Source', 'Vendor and product'], S.origin_after.map(r => [r[0], esc(r[1]), esc(r[2]), esc(r[3] + ' ' + r[4])])); });

// ================= Part 4: what is exploited =================
group('Part 4: What is exploited', 'The vendors behind the exploited entries, their severity against the modelled likelihood of exploitation, and how CISA rates urgency and ransomware use.');

panel('Which vendors are flagged most often', 'Ranking', 'EUVD records: the vendor on each exploited entry, by <code>exploitedSince</code>; the last 90 days against the 90 days before.',
  () => { const v = S.vendors, rise = v.filter(r => r[1] >= 3 && r[1] >= 2 * r[2]).map(r => r[0]);
    return `Pairs of bars per vendor: the last 90 days in blue, the 90 days before in grey. ${B(esc(v[0][0]))} leads with ${v[0][1]}. ${rise.length ? `Newly frequent (at least twice the count of the period before): ${rise.map(esc).join(', ')}.` : 'No vendor doubled its count against the period before.'} "n/a" is entries without a vendor name.`; },
  'Counts are entries, not incidents, and one product family can contribute many CVEs. The KEV dump has no vendor field, so this uses the per-entry records.',
  c => hbars(c, S.vendors, {two: true, L: 160}));

panel('Severity against likelihood of exploitation', 'Scatter', `EUVD records of the ${S.scatter.length} entries flagged in the last 90 days: CVSS base score and EPSS (the EUVD's own <code>epss</code> field).`,
  () => { const miss = S.scatter.filter(r => r.cvss >= 9 && r.epss < 10).length;
    return `Each dot is one recently flagged vulnerability. Horizontal: CVSS severity. Vertical: EPSS, the modelled chance of exploitation in the next 30 days. ${B(miss + ' entries')} are critical (CVSS 9+) but had an EPSS under 10% (red): critical flaws the model rated unlikely, yet they are exploited.`; },
  'EPSS is a prediction. These entries are already exploited, so low values show misses of the model, not errors in the data. EPSS changes daily; the chart shows the value at the last run.',
  c => { const W = 900, H = 320, L = 44, R = 14, T = 14, Bm = 34, g = $('g', {}, svg(W, H, c)); yAxis(g, L, W - R, H - Bm, T, 100, 5, v => v + '%');
    for (let i = 0; i <= 10; i++) tx(g, L + (W - L - R) * i / 10, H - Bm + 14, i, {'text-anchor': 'middle'}); tx(g, W / 2, H - 4, 'CVSS base score', {'text-anchor': 'middle'});
    S.scatter.forEach(r => tip($('circle', {cx: L + (W - L - R) * r.cvss / 10, cy: H - Bm - (H - Bm - T) * Math.min(r.epss, 100) / 100, r: 5, fill: col(r.cvss >= 9 && r.epss < 10 ? 'up' : 'cisa'), opacity: .75}, g), `${r.id} ${r.cve}: CVSS ${r.cvss}, EPSS ${r.epss}%`)); });

panel('How urgently CISA wants new entries fixed', 'Time series', 'CISA KEV catalogue (<code>dateAdded</code>, <code>dueDate</code>, <code>forensicTriage</code>), entries added in the last 24 months, by month.',
  () => { const u = S.urgency, last3 = u.slice(-4, -1), tot3 = sum(last3.map(r => r[1] + r[2] + r[3] + r[4] + r[5])), w3 = sum(last3.map(r => r[1])), ft = u.filter(r => r[6]), ftFirst = ft[0], since = u.slice(u.indexOf(ftFirst)), ftShare = ftFirst ? sum(since.map(r => r[6])) / Math.max(1, sum(since.map(r => r[1] + r[2] + r[3] + r[4] + r[5]))) : 0;
    return `Each bar splits a month's new entries by the remediation window CISA set for US federal agencies: <span style="color:var(--up)">3 days</span>, <span style="color:var(--eu)">7</span>, <span style="color:var(--both)">14</span>, <span style="color:var(--cisa)">21</span>. Hollow dots count entries marked for forensic triage. In the last three full months ${B(Math.round(100 * w3 / Math.max(1, tot3)) + '%')} of new entries got three days. ${ftFirst ? `Forensic triage first appears in ${mlong(ftFirst[0])} and covers ${Math.round(100 * ftShare)}% of the entries added since.` : 'No entry is marked for forensic triage.'}`; },
  'These are deadlines for US federal agencies, not for anyone in the EU; they show how CISA rates urgency, not how dangerous a flaw is in Europe. <code>forensicTriage</code> refers to BOD 26-04 and is absent for older entries.',
  c => { const u = S.urgency, r = monthBars(c, u.map(x => x[0]), [['up', u.map(x => x[1]), '3 days'], ['eu', u.map(x => x[2]), '7 days'], ['both', u.map(x => x[3]), '14 days'], ['cisa', u.map(x => x[4]), '21 days'], ['steady', u.map(x => x[5]), 'other']], {step: 10, H: 260});
    u.forEach((x, i) => { if (x[6]) tip($('circle', {cx: r.L + i * r.bw + r.bw / 2, cy: r.H - r.Bm - (r.H - r.Bm - r.T) * x[6] / r.top, r: 4, fill: 'var(--card)', stroke: col('fg'), 'stroke-width': 1.6}, r.g), `${x[0]} forensic triage: ${x[6]}`); }); });

panel('Ransomware use and weakness types', 'Profile', `CISA KEV catalogue: <code>knownRansomwareCampaignUse</code> by year added, and the <code>cwes</code> field across all ${fmt(S.cisa_n)} entries.`,
  () => { const f = S.ransom.filter(x => x[2] >= 20), r = f.length ? f : S.ransom, a = r[0], z = r[r.length - 1]; if (!a) return 'The CISA catalogue returned no entries.';
    return `${B('Left:')} the share of entries CISA knows to be used by ransomware groups, by year added: ${Math.round(100 * a[1] / a[2])}% in ${a[0]}, ${Math.round(100 * z[1] / z[2])}% in ${z[0]}. ${B('Right:')} the most frequent weakness types, led by ${S.cwe.slice(0, 3).map(w => w[1] || w[0]).join(', ')}.`; },
  '"Known" ransomware use is added as CISA learns of it, so recent years are low partly because that knowledge has not arrived yet. One entry can carry several weakness types, and older entries often carry none.',
  c => { const wrap = document.createElement('div'); wrap.className = 'grid2'; c.appendChild(wrap); const a = document.createElement('div'), b = document.createElement('div'); wrap.appendChild(a); wrap.appendChild(b);
    const d = S.ransom.filter(x => x[2] >= 20).length ? S.ransom.filter(x => x[2] >= 20) : S.ransom, W = 440, H = 230, L = 40, R = 8, T = 14, Bm = 30; let g = $('g', {}, svg(W, H, a)); const [top, tk] = nice(Math.max(...d.map(x => 100 * x[1] / x[2]))); yAxis(g, L, W - R, H - Bm, T, top, tk, v => v + '%'); const bw = (W - L - R) / d.length;
    d.forEach((r, i) => { const p = 100 * r[1] / r[2], h = (H - Bm - T) * p / top, x = L + i * bw + 6; $('rect', {x, y: H - Bm - h, width: bw - 12, height: h, fill: col('up'), opacity: .85}, g); tx(g, x + (bw - 12) / 2, H - Bm - h - 5, Math.round(p) + '%', {'text-anchor': 'middle', class: 't'}); tx(g, x + (bw - 12) / 2, H - Bm + 14, r[0], {'text-anchor': 'middle'}); });
    const e = S.cwe, rh = 26, L2 = 170; g = $('g', {}, svg(440, e.length * rh + 10, b)); const mx = Math.max(1, ...e.map(x => x[2]));
    e.forEach((r, i) => { const y = 6 + i * rh, w = (440 - L2 - 34) * r[2] / mx; tx(g, L2 - 6, y + 12, r[1] || r[0], {'text-anchor': 'end', class: 't'}); tip($('rect', {x: L2, y, width: w, height: 14, fill: col('cisa')}, g), `${r[0]} ${r[1]}: ${r[2]}`); tx(g, L2 + w + 5, y + 12, r[2]); }); });

// ================= Part 5: honeypot sensors =================
group('Part 5: Honeypot sensors', `Shadowserver's honeypot sensors as the EUVD serves them: which exploited entries the sensors see, how hard they are attacked today, whether a rise lasts, and whether the sensors saw attacks before the KEV listing. ${fmt(S.hp_with)} of ${fmt(S.total)} exploited entries have sensor data.`);

panel('How much of the exploited list do sensors see?', 'Coverage', `The same honeypot endpoint, checked for all ${fmt(S.total)} exploited entries, grouped by the year they were flagged.`,
  () => { const e = Object.entries(S.hp_cov).map(([y, [a, b]]) => [y, 100 * a / b]), lo = [...e].sort((a, b) => a[1] - b[1])[0], hi = [...e].sort((a, b) => b[1] - a[1])[0];
    return `Bars show the share of entries per year that have honeypot data: ${B(Math.round(100 * S.hp_with / S.total) + '%')} overall, highest for ${hi[0]} (${Math.round(hi[1])}%), lowest for ${lo[0]} (${Math.round(lo[1])}%).`; },
  'Absence from the sensors does not mean an entry is not attacked, only that the sensors do not emulate it. Edge devices and web applications dominate what sensors see.',
  c => { const e = Object.entries(S.hp_cov), W = 900, H = 220, L = 40, R = 10, T = 14, Bm = 36, g = $('g', {}, svg(W, H, c)); yAxis(g, L, W - R, H - Bm, T, 100, 4, v => v + '%'); const bw = (W - L - R) / e.length;
    e.forEach(([y, [a, b]], i) => { const p = 100 * a / b, h = (H - Bm - T) * p / 100, x = L + i * bw + 30; $('rect', {x, y: H - Bm - h, width: bw - 60, height: h, fill: col('both')}, g); tx(g, x + (bw - 60) / 2, H - Bm - h - 5, Math.round(p) + '%', {'text-anchor': 'middle', class: 't'}); tx(g, x + (bw - 60) / 2, H - Bm + 14, y, {'text-anchor': 'middle'}); tx(g, x + (bw - 60) / 2, H - Bm + 28, `${a} of ${b}`, {'text-anchor': 'middle'}); }); });

panel('Honeypot activity per entry: today against the usual level', 'Honeypot', '<code>/api/honeypotObservations/batch</code> (undocumented, used by the EUVD frontend): Shadowserver sensor connections in the last 24 hours and averages over 7, 30 and 90 days.',
  () => { const up = S.honeypot.filter(r => r.trend === 'UPTICK').length, t = S.hp_trend;
    return `Each row is one exploited vulnerability the sensors see attacked, the ${S.honeypot.length} busiest. The four dots, left to right on a logarithmic scale, are the 90-, 30- and 7-day averages and ${B('today (filled)')}; a filled dot far right of the others is a jump; \u201cBurst or campaign?\u201d below shows how concentrated it is. Red rows carry the EUVD's own ${B('UPTICK')} flag (${up} of the rows shown; ${fmt(t.UPTICK || 0)} of all ${fmt(sum(Object.values(t)))} entries with counts), grey is steady, green declining.`; },
  `Connection counts from sensors, not victims and not the reporting route. Only ${fmt(S.hp_with)} of ${fmt(S.total)} exploited entries appear in the sensors at all. The EUVD keeps no history of these counts; the daily record started by this monitor is in \u201cDo upticks last?\u201d and in the last panel.`,
  c => { const d = S.honeypot, W = 900, rh = 24, L = 360, R = 20, T = 24, H = T + d.length * rh + 30, g = $('g', {}, svg(W, H, c)), lg = v => Math.log10(v + 1), top = Math.max(1, Math.ceil(lg(Math.max(1, ...d.map(r => Math.max(r.d1, r.d7, r.d30, r.d90)))))), X = v => L + (W - L - R) * lg(v) / top;
    for (let k = 0; k <= top; k++) { const x = X(Math.pow(10, k) - 1); $('line', {x1: x, x2: x, y1: T - 8, y2: H - 24, stroke: col('grid')}, g); tx(g, x, H - 8, k ? fmt(Math.pow(10, k)) : '0', {'text-anchor': 'middle'}); }
    tx(g, L, 12, 'connections per day (log scale)');
    d.forEach((r, i) => { const y = T + i * rh + 10, c2 = r.trend === 'UPTICK' ? 'up' : r.trend === 'DECLINE' ? 'down' : 'steady';
      tx(g, L - 8, y + 4, `${r.id} ${r.vendor} ${String(r.product).slice(0, 22)}`, {'text-anchor': 'end', class: 't'});
      const xs = [r.d90, r.d30, r.d7, r.d1].map(X); $('line', {x1: Math.min(...xs), x2: Math.max(...xs), y1: y, y2: y, stroke: col(c2), 'stroke-width': 2, opacity: .45}, g);
      [[r.d90, '90-day avg'], [r.d30, '30-day avg'], [r.d7, '7-day avg']].forEach(([v, n]) => tip($('circle', {cx: X(v), cy: y, r: 3.5, fill: 'var(--card)', stroke: col(c2), 'stroke-width': 1.6}, g), `${r.id} ${n}: ${v}`));
      tip($('circle', {cx: X(r.d1), cy: y, r: 5, fill: col(c2)}, g), `${r.id} today: ${r.d1} connections from ${r.ips} IPs, ${r.trend}`); }); });

const SG = S.hp_surges || [], SURGE = new Set(SG.map(r => r.id)), SC = S.hp_scatter || [];
panel('Burst or campaign? Connections against source addresses', 'Honeypot', 'The same endpoint, today: <code>connections1d</code> and <code>uniqueIps1d</code> for every exploited entry the sensors saw attacked.',
  () => { const conc = SC.filter(r => r.d1 >= 1000 && r.ips < 20), top = [...conc].sort((a, b) => b.d1 - a.d1)[0], broad = SG.filter(r => r.kinds.includes('broad')).length;
    return `Each dot is one exploited vulnerability the sensors saw attacked today (${fmt(SC.length)}). Further right means more connections, higher up more distinct source addresses; both scales are logarithmic. Dots low and far right are hammered by a few sources: ${B(conc.length + (conc.length === 1 ? ' entry' : ' entries'))} had over 1,000 connections from fewer than 20 addresses${top ? `, the most ${esc(top.vendor)} ${esc(top.product)} (${esc(top.cve)}: ${fmt(top.d1)} connections from ${top.ips})` : ''}. Dots high up are scanned broadly. <span style="color:var(--up)">Red</span> carries the EUVD's UPTICK flag; a ring marks a surge as this monitor defines it (${broad} broad today). The numbered dots are listed below the chart.`; },
  'Connections and addresses as Shadowserver\'s sensors count them on one day. A few addresses can be one research scanner or one botnet node; many addresses can be a botnet or a crowd of scanners. The chart shows how concentrated the traffic is, not who sent it or why.',
  c => { if (!SC.length) { c.innerHTML = '<p>The sensors report no connections today.</p>'; return; }
    const W = 900, H = 394, L = 60, R = 18, T = 30, Bm = 40, g = $('g', {}, svg(W, H, c)), lx = v => Math.log10(Math.max(v, 1)),
      tx1 = Math.max(1, Math.ceil(lx(Math.max(...SC.map(r => r.d1))))), ty1 = Math.max(1, Math.ceil(lx(Math.max(...SC.map(r => r.ips))))),
      X = v => L + (W - L - R) * lx(v) / tx1, Y = v => H - Bm - (H - Bm - T) * lx(v) / ty1;
    for (let k = 0; k <= tx1; k++) { const x = X(Math.pow(10, k)); $('line', {x1: x, x2: x, y1: T, y2: H - Bm, stroke: col('grid')}, g); tx(g, x, H - Bm + 16, fmt(Math.pow(10, k)), {'text-anchor': 'middle'}); }
    for (let k = 0; k <= ty1; k++) { const y = Y(Math.pow(10, k)); $('line', {x1: L, x2: W - R, y1: y, y2: y, stroke: col('grid')}, g); tx(g, L - 6, y + 4, fmt(Math.pow(10, k)), {'text-anchor': 'end'}); }
    tx(g, (L + W - R) / 2, H - 6, 'connections today (log scale)', {'text-anchor': 'middle'}); tx(g, L, 14, 'distinct source addresses (log scale)', {class: 't'});
    const marked = [...new Set([...SC.slice(0, 5).map(r => r.id), ...[...SC].sort((a, b) => b.ips - a.ips).slice(0, 2).map(r => r.id), ...SC.filter(r => SURGE.has(r.id)).map(r => r.id)])].slice(0, 9);
    [...SC].reverse().forEach(r => { const c2 = r.trend === 'UPTICK' ? 'up' : r.trend === 'DECLINE' ? 'down' : 'steady', cx = X(r.d1), cy = Y(r.ips);
      tip($('circle', {cx, cy, r: 4.5, fill: col(c2), opacity: .8}, g), `${r.id} ${r.cve} ${r.vendor} ${r.product}: ${r.d1} connections from ${r.ips} addresses, ${r.trend}`);
      if (SURGE.has(r.id)) $('circle', {cx, cy, r: 8.5, fill: 'none', stroke: col('fg'), 'stroke-width': 1.4}, g);
      const n = marked.indexOf(r.id); if (n >= 0) tx(g, cx + 7, cy - 7, n + 1, {class: 't', 'font-weight': 600}); });
    legend(c, [['up', 'UPTICK'], ['steady', 'steady'], ['down', 'declining']]);
    table(c, ['#', 'Entry', 'CVE', 'Vendor and product', 'Connections', 'Addresses'], marked.map((id, n) => { const r = SC.find(x => x.id === id); return [n + 1, esc(r.id), esc(r.cve), esc(r.vendor + ' ' + r.product), fmt(r.d1), fmt(r.ips)]; })); });

const HT = S.hp_heat || {days: [], rows: [], n: 0};
panel('Do upticks last?', 'History', '<code>euvd/history.jsonl</code>: the connections, source addresses, trend flag and 30-day average this monitor records for every entry each day, because the EUVD keeps no history.',
  () => { const per = SG.filter(r => r.kinds.includes('persistent')).length, nd = HT.days.length;
    if (!HT.rows.length) return `No entry carries an UPTICK flag or a surge on the ${nd} recorded ${nd === 1 ? 'day' : 'days'}.`;
    return `One row per entry the EUVD flagged UPTICK, or this monitor marked as a surge, on any of the last ${B(nd + (nd === 1 ? ' recorded day' : ' recorded days'))} (${fmt(HT.n)} entries; the ${HT.rows.length} flagged most often are shown). One column per day. The colour is that day's connections against the entry's 30-day average, pale around the usual level and dark at ${B('20 times')} and more; a dot marks the UPTICK flag. ${per ? B(per + (per === 1 ? ' entry was' : ' entries were') + ' flagged on three recorded days in a row') + ', the persistent surges this monitor reports.' : 'No entry was flagged on three recorded days in a row yet.'}${nd < 7 ? ` The record is ${nd} ${nd === 1 ? 'day' : 'days'} long; the chart says more after about a week.` : ''}`; },
  'Starts with the monitor\'s record. Days recorded before 9 October 2026 hold only connection counts, so their cells are blank. A missing column is a day the monitor did not run. UPTICK compares one day with the 7-day average (inferred from the data, not documented), so one flag alone is a one-day burst.',
  c => { if (!HT.rows.length) return; const nd = HT.days.length, L = 330, R = 10, T = 26, rh = 20, cw = Math.min(28, (900 - L - R) / Math.max(1, nd)), W = 900, H = T + HT.rows.length * rh + 8, g = $('g', {}, svg(W, H, c)), top = Math.log10(20);
    HT.days.forEach((d, j) => { if (j === 0 || j === nd - 1 || j % 7 === 0) tx(g, L + j * cw + cw / 2, T - 10, `${+d.slice(8)} ${MON[+d.slice(5, 7) - 1]}`, {'text-anchor': 'middle'}); });
    HT.rows.forEach((r, i) => { const y = T + i * rh, m = SC.find(x => x.id === r.id) || {};
      tx(g, L - 8, y + 14, `${r.id} ${m.vendor || ''} ${String(m.product || '').slice(0, 18)}`, {'text-anchor': 'end', class: 't'});
      r.cells.forEach(([v, t], j) => { const x = L + j * cw, op = v == null ? 1 : .08 + .9 * Math.min(1, Math.log10(Math.max(v, 1)) / top);
        tip($('rect', {x: x + 1, y: y + 2, width: cw - 2, height: rh - 4, fill: v == null ? col('grid') : col('up'), opacity: op}, g), `${r.id} ${HT.days[j]}: ${v == null ? 'no ratio recorded' : v + 'x the 30-day average'}${t === 'U' ? ', UPTICK' : ''}`);
        if (t === 'U') $('circle', {cx: x + cw / 2, cy: y + rh / 2, r: 2.6, fill: col('fg')}, g); }); }); });

const LE = S.hp_lead || {n: 0, buckets: [], recent: []};
panel('Did the sensors see it before the KEV listing?', 'Timing', 'The honeypot observations\' <code>firstSeenAt</code> (the first day the sensors recorded attempts against the CVE) against <code>exploitedSince</code>, which for nearly every entry is the day CISA listed it.',
  () => { if (!LE.n) return 'No exploited entry has a first sighting yet.'; const b = Object.fromEntries(LE.buckets), before = b['over a year before'] + b['31-365 days before'] + b['1-30 days before'], after = b['1-30 days after'] + b['over 30 days after'];
    return `${fmt(LE.n)} exploited entries have a first sighting. ${B(fmt(LE.censored))} were first seen on ${dlabel(LE.start)}, the first day of the sensors' record, so their sighting may be older; they are left out of the bars. Of the other ${fmt(LE.n - LE.censored)}, ${B(fmt(before))} were seen before the entry was flagged (${fmt(b['1-30 days before'])} within 30 days before), ${fmt(b['same day'])} on the day and ${fmt(after)} after. The table lists the ${LE.recent.length} entries flagged since the go-live.`; },
  'A first sighting is the first day Shadowserver\'s sensors recorded attempts against the CVE. Sensors learn new vulnerabilities over time, so "after" can mean the sensor came late, not the attacks. Neither date says how the vulnerability reached ENISA.',
  c => { if (!LE.n) return; hbars(c, LE.buckets.map(([n, v]) => ['sensors ' + n, v]), {L: 230, c1: 'both'});
    if (LE.recent.length) table(c, ['Entry', 'CVE', 'Vendor', 'Flagged', 'EU KEV', 'First seen by sensors', 'Sensors'], LE.recent.map(r => [esc(r.id), esc(r.cve), esc(r.vendor), r.flagged, r.eu || '-', r.seen,
      r.censored ? 'at or before the sensors\' start' : r.lead > 0 ? `${r.lead} days before` : r.lead === 0 ? 'same day' : `${-r.lead} days after`])); });

// ================= Part 6: the monitor's record =================
group('Part 6: The monitor\'s own record', 'What this monitor records itself, every day, because the EUVD keeps no history of it.');

const HS = S.history || [];
panel('The monitor\'s own daily record', 'History', '<code>euvd/history.jsonl</code>: one line per day written by this monitor, because the EUVD keeps no history of these values: size of the exploited set, size of the EUVD, entries seen by the honeypot sensors, their connections and the number flagged UPTICK.',
  () => HS.length < 2 ? `The record has ${B(HS.length + (HS.length === 1 ? ' day' : ' days'))} so far; a line chart appears from the second day and becomes useful after about a week. Once it has, this panel shows how the exploited set and the honeypot activity move from day to day, which no other source offers.`
    : `${B(HS.length + ' days')} recorded, ${dlabel(HS[0][0])} to ${dlabel(HS[HS.length - 1][0])}. The exploited set went from ${fmt(HS[0][1])} to ${fmt(HS[HS.length - 1][1])} entries; honeypot connections across all entries from ${fmt(HS[0][4])} to ${fmt(HS[HS.length - 1][4])} a day${HS[HS.length - 1][5] != null ? `; the EUVD flagged ${fmt(HS[HS.length - 1][5])} entries UPTICK on the last day` : ''}.`,
  'Starts on the day the monitor began recording; nothing before that can be reconstructed. A missing day means the monitor did not run, not that nothing happened.',
  c => { if (HS.length < 2) { table(c, ['Day', 'Exploited entries', 'EUVD records', 'Seen by sensors', 'Sensor connections'], HS.map(r => [r[0], fmt(r[1]), fmt(r[2]), fmt(r[3]), fmt(r[4])])); return; }
    [[1, 'exploited entries', 'cisa'], [4, 'honeypot connections per day', 'up'], [5, 'entries flagged UPTICK per day (recorded from 9 October 2026)', 'steady']].forEach(([k, name, cc]) => { const pts = HS.map((r, i) => [i, r[k]]).filter(p => p[1] != null); if (pts.length < 2) { const p = document.createElement('p'); p.className = 'limit'; p.textContent = `${name[0].toUpperCase() + name.slice(1)}: the line appears from the second recorded day.`; c.appendChild(p); return; }
      const W = 900, H = 180, L = 60, R = 10, T = 18, Bm = 26, g = $('g', {}, svg(W, H, c)), v = pts.map(p => p[1]), lo = Math.min(...v), hi = Math.max(...v), span = Math.max(1, hi - lo), Y = x => H - Bm - (H - Bm - T) * (x - lo) / span, X = i => L + (W - L - R) * i / Math.max(1, HS.length - 1);
      yAxis(g, L, W - R, H - Bm, T, 1, 2, f => fmt(Math.round(lo + span * f))); tx(g, L, 12, name, {class: 't'});
      $('polyline', {points: pts.map(([i, x]) => `${X(i)},${Y(x)}`).join(' '), fill: 'none', stroke: col(cc), 'stroke-width': 2}, g);
      pts.forEach(([i, x]) => { const r = HS[i]; tip($('circle', {cx: X(i), cy: Y(x), r: 3, fill: col(cc)}, g), `${r[0]}: ${fmt(x)}`); if (i === 0 || i === HS.length - 1 || i % 7 === 0) tx(g, X(i), H - Bm + 14, r[0].slice(5), {'text-anchor': 'middle'}); }); }); });
topLink();
})();

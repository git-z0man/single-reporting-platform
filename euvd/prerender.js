// Draws the charts of euvd/stats.html into the file itself, so the page reads in viewers that run
// no JavaScript, and writes one standalone SVG per panel into euvd/panels/ so a panel can be saved
// or pasted elsewhere with its chart, legend and both texts together. Called by euvd/build_stats.py;
// needs node and Playwright with a Chromium.
//   node euvd/prerender.js euvd/stats.html
const fs = require('fs'), path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { console.error('playwright not installed'); process.exit(3); }

// Runs in the page. Builds one self-contained SVG per panel: the colours are read back from the
// rendered chart (the page's CSS variables mean nothing outside it), and the prose is wrapped by
// measuring a real text node, because SVG does not wrap text by itself.
function exportPanels() {
  const NS = 'http://www.w3.org/2000/svg', PAD = 18, INK = '#1b2230', MUT = '#5d6677', ACC = '#1f5fa8', LINE = '#dde1e8';
  const esc = s => String(s).replace(/[&<>]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;'}[c]));
  const slug = s => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 60);
  const m = document.createElementNS(NS, 'svg'), mt = document.createElementNS(NS, 'text');
  m.style.cssText = 'position:absolute;left:-9999px'; m.appendChild(mt); document.body.appendChild(m);
  const wrap = (s, px, bold, max) => { mt.setAttribute('font-size', px); mt.setAttribute('font-weight', bold ? 600 : 400);
    const out = []; let line = '';
    for (const w of String(s).split(/\s+/).filter(Boolean)) { const t = line ? line + ' ' + w : w; mt.textContent = t;
      if (mt.getComputedTextLength() > max && line) { out.push(line); line = w; } else line = t; }
    if (line) out.push(line); return out; };

  const files = [];
  document.querySelectorAll('section.p').forEach((sec, i) => {
    const charts = [...sec.querySelectorAll('.c svg')];
    if (!charts.length) return;                                  // a table-only panel has no image to save
    const inner = Math.max(...charts.map(s => s.viewBox.baseVal.width), 620), W = inner + 2 * PAD;
    const parts = []; let y = PAD;
    const put = (lines, px, fill, bold, lh) => lines.forEach(l => { y += lh;
      parts.push(`<text x="${PAD}" y="${y}" font-size="${px}" fill="${fill}"${bold ? ' font-weight="600"' : ''}>${esc(l)}</text>`); });
    const tag = (sec.querySelector('.tag') || {}).textContent || '', title = sec.querySelector('h2').textContent.slice(tag.length);
    if (tag) { y += 11; parts.push(`<text x="${PAD}" y="${y}" font-size="10" letter-spacing="0.6" fill="${MUT}">${esc(tag.toUpperCase())}</text>`); }
    put(wrap(title, 17, true, inner), 17, INK, true, 21);
    const src = sec.querySelector('.src');
    if (src) { y += 4; put(wrap(src.textContent, 11.5, false, inner), 11.5, MUT, false, 15); }
    y += 10;
    charts.forEach(sv => { const vb = sv.viewBox.baseVal, k = Math.min(1, inner / vb.width);
      const cl = sv.cloneNode(true), a = [...sv.querySelectorAll('*')], b = [...cl.querySelectorAll('*')];
      a.forEach((o, j) => { const cs = getComputedStyle(o), d = b[j];
        if (d.hasAttribute('fill') || cs.fill !== 'rgb(0, 0, 0)') d.setAttribute('fill', cs.fill);
        if (d.hasAttribute('stroke') && cs.stroke !== 'none') d.setAttribute('stroke', cs.stroke); });
      cl.removeAttribute('class'); cl.setAttribute('width', vb.width); cl.setAttribute('height', vb.height);
      parts.push(`<g transform="translate(${PAD},${y}) scale(${k})" font-size="11">${cl.outerHTML}</g>`);
      y += vb.height * k + 8; });
    const leg = [...sec.querySelectorAll('.leg span')];
    if (leg.length) { y += 10; let x = PAD;
      leg.forEach(sp => { const c = getComputedStyle(sp.querySelector('i')).backgroundColor;
        mt.setAttribute('font-size', 12); mt.setAttribute('font-weight', 400); mt.textContent = sp.textContent;
        const w = mt.getComputedTextLength() + 34;
        if (x > PAD && x + w > W - PAD) { x = PAD; y += 18; }
        parts.push(`<rect x="${x}" y="${y - 9}" width="11" height="11" fill="${c}"/><text x="${x + 16}" y="${y}" font-size="12" fill="${MUT}">${esc(sp.textContent)}</text>`);
        x += w; });
      y += 6; }
    const see = sec.querySelector('.see .w'), lim = sec.querySelector('.limit');
    if (see) { y += 16; const box = y - 12, lines = wrap(see.textContent, 12.5, false, inner - 22), bh = lines.length * 17 + 30;
      parts.push(`<rect x="${PAD}" y="${box}" width="${inner}" height="${bh}" fill="#eef3fa"/><rect x="${PAD}" y="${box}" width="3" height="${bh}" fill="${ACC}"/>`);
      y += 4; parts.push(`<text x="${PAD + 12}" y="${y}" font-size="9.5" letter-spacing="0.6" font-weight="600" fill="${ACC}">WHAT YOU SEE</text>`);
      lines.forEach(l => { y += 17; parts.push(`<text x="${PAD + 12}" y="${y}" font-size="12.5" fill="${INK}">${esc(l)}</text>`); });
      y += 14; }
    if (lim) { y += 12; put(wrap(lim.textContent, 11.5, false, inner), 11.5, MUT, false, 15); }
    if (sec.querySelector('table')) { y += 15; put(wrap('This panel also carries a table, which the image does not include; it is on the page.', 11.5, false, inner), 11.5, MUT, false, 15); }
    y += 6;
    put(wrap(`EUVD statistics, ${(document.getElementById('gen') || {}).textContent || ''} - github.com/git-z0man/single-reporting-platform`, 10.5, false, inner), 10.5, MUT, false, 14);
    y += PAD;
    const H = Math.ceil(y), n = String(i + 1).padStart(2, '0'), file = `${n}-${slug(title.replace(/^\d+\.\s*/, ''))}.svg`;
    files.push({file, svg: `<svg xmlns="${NS}" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="system-ui,-apple-system,'Segoe UI',sans-serif"><rect width="100%" height="100%" fill="#ffffff"/><rect x="0.5" y="0.5" width="${W - 1}" height="${H - 1}" fill="none" stroke="${LINE}"/>${parts.join('')}</svg>`});
    const p = document.createElement('p');
    p.className = 'dl';
    p.innerHTML = `<a href="panels/${file}" download>Save this panel as an image (SVG, with its legend and texts)</a>`;
    sec.appendChild(p);
  });
  m.remove();
  return files;
}

(async () => {
  const file = path.resolve(process.argv[2] || 'euvd/stats.html');
  const opts = {};
  for (const p of [process.env.CHROMIUM_PATH, '/opt/pw-browsers/chromium']) if (p && fs.existsSync(p)) { opts.executablePath = p; break; }
  const browser = await chromium.launch(opts);
  try {
    const page = await browser.newPage({ viewport: { width: 1100, height: 900 } });
    const errors = [];
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto('file://' + file);
    await page.waitForTimeout(500);
    const ok = await page.evaluate(() => document.querySelectorAll('section.p svg, section.p table').length);
    if (errors.length || !ok) { console.error('render failed: ' + (errors.join('; ') || 'no charts')); process.exit(4); }
    // The per-panel images are an extra; a fault in them must never cost the page its pre-rendering.
    try {
      const dir = path.join(path.dirname(file), 'panels');
      const files = await page.evaluate(exportPanels);
      fs.rmSync(dir, {recursive: true, force: true});            // drop images of panels that were renamed or removed
      fs.mkdirSync(dir, {recursive: true});
      for (const f of files) fs.writeFileSync(path.join(dir, f.file), f.svg + '\n');
      console.log(`panel images: ${files.length}`);
    } catch (e) { console.error('panel images skipped: ' + String(e).slice(0, 200)); }
    await page.evaluate(() => {
      document.getElementById('mode').textContent = 'This page is pre-rendered: the charts are drawn into the file, so it needs no JavaScript. Hover a bar or dot for its value where your viewer supports it. Each panel can be saved on its own as an image.';
      document.querySelectorAll('script').forEach(s => s.remove());
    });
    fs.writeFileSync(file, '<!doctype html>\n' + await page.evaluate(() => document.documentElement.outerHTML) + '\n');
  } finally { await browser.close(); }
})().catch(e => { console.error(String(e)); process.exit(5); });

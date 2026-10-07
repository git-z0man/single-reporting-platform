// Draws the charts of euvd/stats.html into the file itself, so the page reads in viewers that run
// no JavaScript. Called by euvd/build_stats.py; needs node and Playwright with a Chromium.
//   node euvd/prerender.js euvd/stats.html
const fs = require('fs'), path = require('path');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { console.error('playwright not installed'); process.exit(3); }
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
    await page.evaluate(() => {
      document.getElementById('mode').textContent = 'This page is pre-rendered: the charts are drawn into the file, so it needs no JavaScript. Hover a bar or dot for its value where your viewer supports it.';
      document.querySelectorAll('script').forEach(s => s.remove());
    });
    fs.writeFileSync(file, '<!doctype html>\n' + await page.evaluate(() => document.documentElement.outerHTML) + '\n');
  } finally { await browser.close(); }
})().catch(e => { console.error(String(e)); process.exit(5); });

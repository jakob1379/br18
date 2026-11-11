const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const html = fs.readFileSync(process.argv[2], 'utf8');
  const skel = `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><style>:root{color-scheme:light;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>${html}</body></html>`;
  fs.writeFileSync('/tmp/claude-0/-home-user-ai-job-search-fork/9c9ad245-1536-5d87-980d-1a4837c57ed1/scratchpad/mmd/test.html', skel);
  const b = await chromium.launch();
  const out = process.argv[3]; const errs = [];
  for (const [name, w, h, scheme, hash] of [['kat', 1440, 900, 'light', '#katalog'], ['kat-doc', 1440, 900, 'dark', '#kat-lta-2019-1399'], ['kat-phone', 400, 860, 'light', '#kat-lta-2016-1178'], ['net-kilde', 1440, 900, 'light', '#node-lov-byggeloven']]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h }, colorScheme: scheme });
    const p = await ctx.newPage();
    p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(`${name}: ${m.type()} ${m.text().slice(0, 200)}`); });
    p.on('pageerror', e => errs.push(`${name}: pageerror ${e.message}`));
    await p.route('https://cdn.jsdelivr.net/npm/cytoscape@3.30.2/dist/cytoscape.min.js', r => r.fulfill({ path: path.resolve(__dirname, 'node_modules/cytoscape/dist/cytoscape.min.js'), contentType: 'application/javascript' }));
    await p.route('https://fonts.googleapis.com/**', r => r.fulfill({ body: '', contentType: 'text/css' }));
    await p.goto('file:///tmp/claude-0/-home-user-ai-job-search-fork/9c9ad245-1536-5d87-980d-1a4837c57ed1/scratchpad/mmd/test.html' + hash);
    await p.waitForTimeout(1500);
    const ov = await p.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
    if (ov) errs.push(`${name}: HORIZONTAL OVERFLOW ${await p.evaluate(() => document.documentElement.scrollWidth)}`);
    await p.screenshot({ path: `${out}/${name}.png`, fullPage: false });
    await ctx.close();
  }
  await b.close();
  console.log(errs.length ? errs.join('\n') : 'no console errors');
})();

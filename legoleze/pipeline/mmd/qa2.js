// Targeted re-checks of the QA findings.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const html = fs.readFileSync('../dk-regulering/reguleringskort.html', 'utf8').replace("cy = cytoscape({", "cy = window.__cy = cytoscape({");
  fs.writeFileSync('qa2.html', `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head><body>${html}</body></html>`);
  const b = await chromium.launch();
  const mk = async (w = 1440, h = 900, scheme = 'light') => { const c = await b.newContext({ viewport: { width: w, height: h }, colorScheme: scheme }); const p = await c.newPage(); p.on('pageerror', e => console.log('PAGEERROR', e.message));
    await p.route('https://cdn.jsdelivr.net/**', r => r.fulfill({ path: path.resolve('node_modules/cytoscape/dist/cytoscape.min.js'), contentType: 'application/javascript' }));
    await p.route('https://fonts.googleapis.com/**', r => r.fulfill({ body: '', contentType: 'text/css' })); return p; };
  const url = h => 'file://' + path.resolve('qa2.html') + (h || '');
  let p = await mk(); await p.goto(url('#huller')); await p.waitForTimeout(600);
  console.log('h-dom options', await p.$$eval('#h-dom option', o => o.length));
  await p.selectOption('#h-dom', 'brand'); console.log('brand huller', await p.textContent('#h-count'));
  await p.goto(url('#node-lov-byggeloven')); await p.waitForTimeout(700);
  const vis = () => p.evaluate(() => [__cy.nodes(':visible').length, __cy.edges(':visible').length]);
  await p.click('text=Fokus: naboer'); await p.waitForTimeout(500); console.log('fokus1', await vis());
  await p.click('text=Fokus: 2 led'); await p.waitForTimeout(500); console.log('fokus2 efter fokus1', await vis());
  await p.click('text=Hele kortet'); await p.waitForTimeout(50); await p.waitForTimeout(600);
  console.log('hele kortet', await vis(), 'knap væk?', !(await p.$('text=Hele kortet')));
  const moved = await p.evaluate(() => __cy.nodes().filter(n => { const id = n.id(); return false; }).length);
  await p.goto(url('#node-bek-br18')); await p.waitForTimeout(600);
  await p.click('text=Fokus: naboer'); await p.waitForTimeout(500); console.log('br18 fokus', await vis());
  // search ranking
  for (const q of ['planloven', 'Planklagenævnet', 'Energistyrelsen', 'miljøbeskyttelsesloven', 'byggeloven']) { await p.fill('#q', q); await p.waitForTimeout(150); await p.press('#q', 'Enter'); await p.waitForTimeout(300); console.log('søg', q, '→', decodeURIComponent(await p.evaluate(() => location.hash))); }
  // chain
  await p.goto(url('#kaede-bek-br18')); await p.waitForTimeout(700);
  console.log('br18-kæde kolonner', await p.$$eval('#chain-cols .eyebrow', e => e.map(x => x.textContent)));
  await p.goto(url('#kaede-lov-byggeloven')); await p.waitForTimeout(700);
  console.log('byggelov-kæde kolonner', await p.$$eval('#chain-cols .eyebrow', e => e.map(x => x.textContent)));
  console.log('klage-kolonne', await p.$$eval('#chain-cols .col', cs => { const c = cs.find(x => x.textContent.startsWith('Klageinstanser')); return c ? [...c.querySelectorAll('li')].map(l => l.textContent) : null; }));
  await p.goto(url('#node-bek-hvileperiode')); await p.waitForTimeout(500); await p.click('text=Vis hjemmelskæde'); await p.waitForTimeout(600);
  console.log('hvileperiode select', await p.$eval('#chain-root', s => s.value), await p.$$eval('#chain-cols .eyebrow', e => e.map(x => x.textContent)));
  // history
  await p.goto(url('')); await p.waitForTimeout(500);
  for (const t of ['Ressort', 'Datakilder', 'Huller']) { await p.click(`nav.tabs >> text=${t}`); await p.waitForTimeout(200); }
  await p.goBack(); await p.waitForTimeout(300); console.log('tilbage →', await p.evaluate(() => location.hash));
  // kilder segment + cell
  await p.goto(url('#kilder')); await p.waitForTimeout(500);
  console.log('aria-pressed', await p.$$eval('#k-seg button', b => b.map(x => x.getAttribute('aria-pressed'))));
  await p.click('#k-seg >> text=Portaler og databaser'); await p.waitForTimeout(200);
  const cells = await p.$$eval('#matrix g.cell text', t => t.map(x => +x.textContent).reduce((a, b) => a + b, 0)); console.log('matrix sum (portaler)', cells, await p.textContent('#k-count'));
  await p.focus('#matrix g.cell[tabindex="0"]'); await p.keyboard.press('Enter'); await p.waitForTimeout(200);
  console.log('fokus efter Enter', await p.evaluate(() => document.activeElement.getAttribute('data-k')), await p.textContent('#k-count'));
  // ressort
  await p.goto(url('#ressort')); await p.waitForTimeout(500);
  console.log('BLM counts', await p.$$eval('.mcard', cs => cs.filter(c => c.textContent.includes('Beskæftigelses- og Ligestillingsministeriet')).map(c => c.querySelector('.counts').textContent)));
  console.log('tidslinje id-rester', await p.$$eval('#timeline .ft', f => f.filter(x => /\b(min|sty|org)-[a-z]/.test(x.textContent)).length));
  // phone overflow
  for (const h of ['#kaede-lov-byggeloven', '#huller', '#ressort', '#kilder']) { const q = await mk(400, 860); await q.goto(url(h)); await q.waitForTimeout(600);
    await q.$$eval('details', d => d.forEach(x => x.open = true)); await q.waitForTimeout(100);
    console.log('phone', h, 'scrollWidth', await q.evaluate(() => document.documentElement.scrollWidth)); }
  const d = await mk(1440, 900, 'dark'); await d.goto(url('#kilder')); await d.waitForTimeout(500);
  console.log('dark matrix text fill', await d.$$eval('#matrix g.cell text', t => [...new Set(t.map(x => getComputedStyle(x).fill))]));
  await b.close();
})();

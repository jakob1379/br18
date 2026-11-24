(() => {
'use strict';
const D = JSON.parse(document.getElementById('data').textContent);
const POS = JSON.parse(document.getElementById('pos').textContent);
const NODES = new Map(D.nodes.map(n => [n.id, n]));
const HISTORIC = new Set(['nedlagt', 'omdøbt', 'ophævet']);
const HIST_RE = /\[HISTORISK|^\s*(HISTORISK|Historisk)\b/;
const EDGES = D.edges.map((e, i) => ({
  i, from: e[0], to: e[1], type: e[2], cert: e[3], desc: e[4] || '', src: e[5] || [], dom: e[6] || [],
  hist: HIST_RE.test(e[4] || '') || HISTORIC.has(NODES.get(e[0])?.status) || HISTORIC.has(NODES.get(e[1])?.status),
  disp: /\[BESTRIDT/.test(e[4] || ''),
}));
const OUT = new Map(), INC = new Map();
for (const e of EDGES) {
  if (!OUT.has(e.from)) OUT.set(e.from, []); OUT.get(e.from).push(e);
  if (!INC.has(e.to)) INC.set(e.to, []); INC.get(e.to).push(e);
}
const nf = new Intl.NumberFormat('da-DK');
const $ = (s, r = document) => r.querySelector(s);
const el = (tag, attrs = {}, ...kids) => {
  const x = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k.startsWith('aria-') && typeof v === 'boolean') { x.setAttribute(k, String(v)); continue; }
    if (v == null || v === false) continue;
    if (k === 'class') x.className = v; else if (k === 'text') x.textContent = v;
    else if (k.startsWith('on')) x.addEventListener(k.slice(2), v); else x.setAttribute(k, v === true ? '' : v);
  }
  for (const k of kids.flat()) if (k != null && k !== false) x.append(k.nodeType ? k : document.createTextNode(String(k)));
  return x;
};
const safeUrl = u => (typeof u === 'string' && /^https?:\/\//i.test(u)) ? u : null;
const extLink = (u, label) => { const s = safeUrl(u); return s ? el('a', { href: s, target: '_blank', rel: 'noopener noreferrer', text: label || s }) : el('span', { text: label || u || '' }); };
const certBadge = c => el('span', { class: 'cert ' + c, text: c });
const certMark = c => el('span', { class: 'mk ' + c, title: c, 'aria-label': c, text: c === 'verificeret' ? '✓' : c === 'sandsynlig' ? '≈' : '?' });
const plural = (n, one, many) => `${nf.format(n)} ${n === 1 ? one : many}`;
const fmtDate = s => { const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s || ''); return m ? new Date(+m[1], +m[2] - 1, +m[3]).toLocaleDateString('da-DK', { day: 'numeric', month: 'long', year: 'numeric' }) : (s || ''); };
const reduceMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
const narrow = () => matchMedia('(max-width: 1180px)').matches;

/* ---------- vocabularies ---------- */
const CATS = [
  { key: 'ministerium', label: 'Ministerium', slot: 's1', shape: 'round-rectangle', types: ['ministerium'] },
  { key: 'klage', label: 'Klage- og praksisinstans', slot: 's2', shape: 'diamond', types: ['nævn', 'klagenævn', 'domstol', 'ombudsmand'] },
  { key: 'myndighed', label: 'Styrelse, tilsyn, råd, fond', slot: 's3', shape: 'ellipse', types: ['styrelse', 'direktorat', 'tilsyn', 'råd', 'fond', 'offentlig-virksomhed', 'kommune', 'region'] },
  { key: 'vejledning', label: 'Vejledning, plan, forskrift', slot: 's4', shape: 'triangle', types: ['vejledning', 'teknisk-forskrift', 'plan', 'regulativ'] },
  { key: 'bek', label: 'Bekendtgørelse, cirkulære', slot: 's5', shape: 'rectangle', types: ['bekendtgørelse', 'cirkulære'] },
  { key: 'eu', label: 'EU-retsakt og -institution', slot: 's6', shape: 'star', types: ['eu-direktiv', 'eu-forordning', 'eu-afgørelse', 'eu-institution'] },
  { key: 'lov', label: 'Lov', slot: 's7', shape: 'hexagon', types: ['lov'] },
  { key: 'kilde', label: 'Dokumentkilde, praksissamling', slot: 's8', shape: 'barrel', types: ['dokumentkilde', 'praksissamling'] },
  { key: 'meta', label: 'Standard, branche (metadata)', slot: 'meta', shape: 'tag', types: ['standard', 'branchevejledning', 'standardiseringsorgan', 'privat-organisation'] },
];
const CAT_OF = {}; for (const c of CATS) for (const t of c.types) CAT_OF[t] = c;
const catOf = n => CAT_OF[n.type] || CATS[CATS.length - 1];
const DOMS = [
  ['byggeri', 'Byggeri'], ['bolig', 'Bolig'], ['plan', 'Plan'], ['kommunalt', 'Kommunalt'], ['energi', 'Energi'], ['miljoe', 'Miljø'],
  ['natur-vand-kyst', 'Natur, vand og kyst'], ['arbejdsmiljoe', 'Arbejdsmiljø'], ['brand', 'Brand og beredskab'], ['el-gas-vvs', 'El, gas og VVS'],
  ['klage-tilsyn-praksis', 'Klage, tilsyn, praksis'], ['eu', 'EU'], ['datakilder-standarder', 'Datakilder, standarder'], ['baseline', 'Ressort-baseline'],
  ['_ingen', 'Uden domæne (tilføjet af kritiker)'],
];
for (const d of Object.entries(D.domnavne || {})) DOMS.splice(DOMS.length - 1, 0, d);
const DOM_LABEL = Object.fromEntries(DOMS);
DOM_LABEL.konsistenstjek = 'Konsistenstjek';
const KRIT_LABEL = { 'byggeri-bolig': 'byggeri og bolig', 'plan-kultur-kommunalt': 'plan, kultur og kommunalt', 'energi-forsyning': 'energi og forsyning', 'miljoe-natur': 'miljø og natur', 'arbejdsmiljoe-brand-elgasvvs': 'arbejdsmiljø, brand og el/gas/VVS', 'klage-praksis-kilder-eu': 'klage, praksis, kilder og EU' };
const domsOf = n => n.dom && n.dom.length ? n.dom : ['_ingen'];
const ETYPES = [
  ['ressortansvar', 'ressortansvar', 'ministerium → instans/lov'], ['delegation', 'delegation', 'ministerium/styrelse → styrelse/kommune'],
  ['hjemmel_for', 'hjemmel for', 'lov/bek. → bek./vejledning/instans/plan'], ['udsteder', 'udsteder', 'instans → retsakt/vejledning/kilde'],
  ['klageinstans', 'klageinstans', 'klageinstans → førsteinstans'], ['domstolsproevelse', 'domstolsprøvelse', 'domstol → instans/lov'], ['tilsyn', 'tilsyn', 'tilsynsmyndighed → tilsynsobjekt'],
  ['implementerer_EU', 'gennemfører EU', 'dansk retsakt → EU-retsakt'], ['henviser_til', 'henviser til', 'dokument → dokument'],
];
const ET_LABEL = Object.fromEntries(ETYPES.map(e => [e[0], e[1]]));
const ET_OUT = { ressortansvar: 'har ressort for', delegation: 'delegerer til', hjemmel_for: 'giver hjemmel til', udsteder: 'udsteder', klageinstans: 'klageinstans for', domstolsproevelse: 'prøver afgørelser fra', tilsyn: 'fører tilsyn med', implementerer_EU: 'gennemfører', henviser_til: 'henviser til' };
const ET_IN = { ressortansvar: 'ressort hos', delegation: 'delegeret fra', hjemmel_for: 'hjemmel i', udsteder: 'udstedt af', klageinstans: 'påklages til', domstolsproevelse: 'kan indbringes for', tilsyn: 'under tilsyn af', implementerer_EU: 'gennemført ved', henviser_til: 'omtalt i' };
const inLabel = e => e.type === 'klageinstans' && NODES.get(e.from)?.type === 'domstol' ? 'kan indbringes for' : ET_IN[e.type];
const FIELDS = [['hjemmel', 'Hjemmel / oprettelse'], ['dokumenttyper', 'Dokumenttyper'], ['url', 'Kanonisk URL'], ['adgang', 'Adgang'], ['identifikatorer', 'Identifikatorer'], ['licens', 'Licens og genbrug'], ['opdatering', 'Opdatering og versioner']];
const HTYPES = [['betalingsmur', 'Betalingsmur'], ['kun-pdf', 'Kun PDF'], ['ingen-api', 'Ingen API'], ['uklart', 'Uklart'], ['ikke-fundet', 'Ikke fundet'], ['andet', 'Andet']];
const shortName = (s, n = 42) => s.length > n ? s.slice(0, n - 1).trimEnd() + '…' : s;
const minName = id => NODES.get(id)?.navn || id;
const nodeLink = (id, label) => el('button', { class: 'lnk', type: 'button', onclick: () => selectNode(id, { from: 'list' }), text: label || minName(id) });
const edgeChips = e => [e.hist ? el('span', { class: 'chip hist', text: 'historisk' }) : null, e.disp ? el('span', { class: 'chip bestridt', title: e.desc, text: 'bestridt' }) : null];

/* ---------- theme tokens ---------- */
function tokens() {
  const s = getComputedStyle(document.documentElement); const g = v => s.getPropertyValue(v).trim();
  const t = { bg: g('--bg'), surface: g('--surface'), ink: g('--ink'), muted: g('--muted'), accent: g('--accent'), edge: g('--edge'), meta: g('--meta'), warn: g('--warn-ink') };
  for (let i = 1; i <= 8; i++) t['s' + i] = g('--s' + i);
  return t;
}

/* ---------- shape swatches ---------- */
function swatch(cat, size = 14) {
  const ns = 'http://www.w3.org/2000/svg', s = document.createElementNS(ns, 'svg');
  s.setAttribute('viewBox', '0 0 16 16'); s.setAttribute('width', size); s.setAttribute('height', size); s.setAttribute('aria-hidden', 'true');
  const P = d => { const p = document.createElementNS(ns, 'path'); p.setAttribute('d', d); return p; };
  let shp;
  switch (cat.shape) {
    case 'ellipse': shp = document.createElementNS(ns, 'circle'); shp.setAttribute('cx', 8); shp.setAttribute('cy', 8); shp.setAttribute('r', 6.5); break;
    case 'diamond': shp = P('M8 1 15 8 8 15 1 8Z'); break;
    case 'triangle': shp = P('M8 1.5 15 14.5H1Z'); break;
    case 'rectangle': shp = P('M2 2h12v12H2Z'); break;
    case 'round-rectangle': shp = P('M4 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2Z'); break;
    case 'star': shp = P('M8 1l2.1 4.6 5 .5-3.8 3.3 1.1 4.9L8 11.8 3.6 14.3l1.1-4.9L.9 6.1l5-.5Z'); break;
    case 'hexagon': shp = P('M4.5 2h7L15 8l-3.5 6h-7L1 8Z'); break;
    case 'barrel': shp = P('M3 3q5-2 10 0v10q-5 2-10 0Z'); break;
    default: shp = P('M1 3h10l4 5-4 5H1Z');
  }
  shp.setAttribute('fill', `var(--${cat.slot})`); s.append(shp); return s;
}

/* ---------- summary ---------- */
function renderSummary() {
  const box = $('#summary');
  const active = D.nodes.filter(n => n.type === 'ministerium' && n.status === 'aktiv').length;
  const cnt = { verificeret: 0, sandsynlig: 0, ukendt: 0 };
  for (const n of D.nodes) for (const [f] of FIELDS) cnt[n[f].sikkerhed]++;
  for (const e of EDGES) cnt[e.cert]++;
  const tot = cnt.verificeret + cnt.sandsynlig + cnt.ukendt;
  const pct = k => Math.round(100 * cnt[k] / tot);
  const stat = (v, l) => el('div', { class: 'stat' }, el('b', { text: nf.format(v) }), el('span', { text: l }));
  const bar = el('div', { class: 'bar', role: 'img', 'aria-label': `Sikkerhed: verificeret ${pct('verificeret')} %, sandsynlig ${pct('sandsynlig')} %, ukendt ${pct('ukendt')} %` });
  const col = { verificeret: 'var(--good)', sandsynlig: 'var(--warn)', ukendt: 'var(--unk)' };
  for (const k of ['verificeret', 'sandsynlig', 'ukendt']) bar.append(el('i', { style: `width:${100 * cnt[k] / tot}%;background:${col[k]}`, title: `${k}: ${nf.format(cnt[k])}` }));
  const lg = el('div', { class: 'lg' }, ...['verificeret', 'sandsynlig', 'ukendt'].map(k => el('span', {}, certMark(k), ` ${k} ${pct(k)} %`)));
  const katStat = el('a', { class: 'stat', href: '#katalog', onclick: ev => { ev.preventDefault(); showView('katalog'); window.scrollTo(0, 0); } }, el('b', { text: nf.format(K.n_total) }), el('span', { text: 'katalog-dokumenter' }));
  box.append(stat(D.nodes.length, 'noder'), stat(EDGES.length, 'kanter'), stat(active, 'aktive ministerier'), stat(D.huller.length, 'huller'), katStat,
    el('div', { class: 'certbar' }, el('span', { class: 'eyebrow', text: `Sikkerhed på ${nf.format(tot)} påstande og kanter i registret` }), bar, lg));
}

/* ---------- network ---------- */
let cy = null, cy2 = null, focusLayout = null, savedPos = null, forced = null;
const state = { cats: new Set(CATS.map(c => c.key)), doms: new Set(DOMS.map(d => d[0])), etypes: new Set(ETYPES.map(e => e[0])), hist: true, unk: true, selected: null, focus: false };
const SCALE = 1.9;

function cyStyle(t, chain = false) {
  return [
    { selector: 'node', style: {
      'background-color': 'data(color)', shape: 'data(shape)', width: 'data(size)', height: 'data(size)',
      label: 'data(label)', 'font-family': 'IBM Plex Sans, system-ui, sans-serif', 'font-size': chain ? 13 : 9, color: t.ink,
      'text-valign': 'bottom', 'text-margin-y': 3, 'text-wrap': 'wrap', 'text-max-width': chain ? 170 : 120,
      'min-zoomed-font-size': chain ? 0 : 7, 'text-outline-color': t.bg, 'text-outline-width': 2, 'text-outline-opacity': 0.85,
      'border-width': 1.5, 'border-color': t.surface, 'overlay-opacity': 0 } },
    { selector: 'node[?hist]', style: { 'background-color': t.surface, 'border-color': 'data(color)', 'border-style': 'dashed', 'border-width': 1.5, color: t.muted } },
    { selector: 'node[kind = "ministerium"]', style: { 'font-size': 12, 'font-weight': 600, 'min-zoomed-font-size': 0, 'text-max-width': 150 } },
    { selector: 'node[kind = "hdr"]', style: { shape: 'rectangle', 'background-opacity': 0, 'border-width': 0, width: 1, height: 1, label: 'data(label)', 'font-size': 12, 'font-weight': 600, color: t.muted, 'text-valign': 'center', 'text-transform': 'uppercase', events: 'no' } },
    { selector: 'edge', style: {
      width: 1, 'line-color': t.edge, 'target-arrow-color': t.edge, 'target-arrow-shape': 'triangle', 'arrow-scale': 0.6,
      'curve-style': chain ? 'bezier' : 'straight', opacity: chain ? 0.55 : 0.5 } },
    { selector: 'edge[cert = "sandsynlig"]', style: { 'line-style': 'dashed', 'line-dash-pattern': [5, 3] } },
    { selector: 'edge[cert = "ukendt"]', style: { 'line-style': 'dotted' } },
    { selector: 'edge[?disp]', style: { 'line-color': t.warn, 'target-arrow-color': t.warn } },
    { selector: 'edge[?hist]', style: { opacity: 0.25 } },
    { selector: 'edge.lbl', style: { label: 'data(tl)', 'font-size': 9, color: t.muted, 'text-rotation': 'autorotate', 'text-background-color': t.bg, 'text-background-opacity': 0.9, 'text-background-padding': 1, 'curve-style': 'bezier' } },
    { selector: '.dim', style: { opacity: 0.08 } },
    { selector: 'edge.dim', style: { opacity: 0.03 } },
    { selector: 'node.hl', style: { 'border-color': t.ink, 'border-width': 2, 'min-zoomed-font-size': 0, 'z-index': 10 } },
    { selector: 'node.sel', style: { 'border-color': t.accent, 'border-width': 4, 'min-zoomed-font-size': 0, 'font-weight': 600, 'z-index': 20 } },
    { selector: 'edge.hl', style: { 'line-color': t.accent, 'target-arrow-color': t.accent, width: 1.8, opacity: 0.95, 'z-index': 9 } },
    { selector: 'edge.hl[?disp]', style: { 'line-color': t.warn, 'target-arrow-color': t.warn } },
  ];
}
function nodeData(n, t) {
  const c = catOf(n);
  const size = n.type === 'ministerium' ? 46 : c.key === 'lov' ? 22 : c.key === 'myndighed' || c.key === 'klage' ? 18 : 13;
  return { id: n.id, label: shortName(n.navn), color: t[c.slot], shape: c.shape, size, kind: n.type, cat: c.key, hist: HISTORIC.has(n.status) };
}
const edgeData = e => ({ id: 'e' + e.i, source: e.from, target: e.to, et: e.type, tl: ET_LABEL[e.type], cert: e.cert, hist: e.hist, disp: e.disp });
const tipAt = (ev, text) => {
  const tip = $('#tip'), r = $('#graph').getBoundingClientRect();
  tip.textContent = text; tip.hidden = false;
  tip.style.left = Math.max(4, Math.min(ev.originalEvent.clientX - r.left + 12, r.width - 220)) + 'px';
  tip.style.top = (ev.originalEvent.clientY - r.top + 12) + 'px';
};
function initNetwork() {
  const t = tokens();
  const els = [];
  for (const n of D.nodes) { const p = POS[n.id] || [0, 0]; els.push({ group: 'nodes', data: nodeData(n, t), position: { x: p[0] * SCALE, y: p[1] * SCALE } }); }
  for (const e of EDGES) if (NODES.has(e.from) && NODES.has(e.to)) els.push({ group: 'edges', data: edgeData(e) });
  cy = cytoscape({ container: $('#cy'), elements: els, layout: { name: 'preset' }, style: cyStyle(t), minZoom: 0.08, maxZoom: 4, textureOnViewport: true, pixelRatio: 'auto' });
  cy.fit(undefined, 24);
  cy.on('mouseover mousemove', 'node', ev => { const n = NODES.get(ev.target.id()); tipAt(ev, `${n.navn} · ${n.type}`); });
  cy.on('mouseover mousemove', 'edge', ev => { const d = ev.target.data(); tipAt(ev, `${minName(d.source)} — ${d.tl} → ${minName(d.target)} (${d.cert}${d.disp ? ', bestridt' : ''}${d.hist ? ', historisk' : ''})`); });
  cy.on('mouseout', 'node, edge', () => { $('#tip').hidden = true; });
  cy.on('tap', 'node', ev => selectNode(ev.target.id(), { center: false, from: 'graph' }));
  cy.on('tap', ev => { if (ev.target === cy) clearSelection(); });
  const zc = () => ({ x: cy.width() / 2, y: cy.height() / 2 });
  $('#z-in').onclick = () => cy.zoom({ level: cy.zoom() * 1.3, renderedPosition: zc() });
  $('#z-out').onclick = () => cy.zoom({ level: cy.zoom() / 1.3, renderedPosition: zc() });
  $('#z-fit').onclick = () => cy.fit(cy.elements(':visible'), 24);
}
const toggle = (set, k, on) => on ? set.add(k) : set.delete(k);
function syncChecks() { document.querySelectorAll('.filters input[data-group]').forEach(i => { i.checked = state[i.dataset.group].has(i.dataset.k); }); }
function buildFilters() {
  const fc = $('#f-cat');
  for (const c of CATS) fc.append(el('label', { class: 'chk' }, el('input', { type: 'checkbox', checked: true, 'data-group': 'cats', 'data-k': c.key, onchange: ev => { toggle(state.cats, c.key, ev.target.checked); applyFilters(); } }), swatch(c), c.label, el('span', { class: 'n', text: D.nodes.filter(n => catOf(n).key === c.key).length })));
  const fd = $('#f-dom');
  fd.append(el('p', { class: 'knote', style: 'margin:0 0 4px', text: 'En node vises, hvis den hører til mindst ét valgt domæne. ”Kun” viser ét domæne.' }));
  for (const [k, l] of DOMS) {
    const n = D.nodes.filter(x => domsOf(x).includes(k)).length;
    fd.append(el('div', { class: 'chk' },
      el('input', { type: 'checkbox', id: 'dom-' + k, checked: true, 'data-group': 'doms', 'data-k': k, onchange: ev => { toggle(state.doms, k, ev.target.checked); applyFilters(); } }),
      el('label', { for: 'dom-' + k, text: l }),
      el('button', { class: 'only', type: 'button', title: `Vis kun ${l}`, onclick: () => { state.doms = new Set([k]); syncChecks(); applyFilters(true); }, text: 'kun' }),
      el('span', { class: 'n', text: n })));
  }
  const fe = $('#f-edge');
  for (const [k, l, h] of ETYPES) fe.append(el('label', { class: 'chk', title: h }, el('input', { type: 'checkbox', checked: true, 'data-group': 'etypes', 'data-k': k, onchange: ev => { toggle(state.etypes, k, ev.target.checked); applyFilters(); } }), l, el('span', { class: 'n', text: EDGES.filter(e => e.type === k).length })));
  $('#opt-hist').onchange = ev => { state.hist = ev.target.checked; applyFilters(); };
  $('#opt-unk').onchange = ev => { state.unk = ev.target.checked; applyFilters(); };
  $('#btn-reset').onclick = () => {
    state.cats = new Set(CATS.map(c => c.key)); state.doms = new Set(DOMS.map(d => d[0])); state.etypes = new Set(ETYPES.map(e => e[0])); state.hist = true; state.unk = true;
    syncChecks(); $('#opt-hist').checked = true; $('#opt-unk').checked = true; applyFilters(true);
  };
}
function nodeVisible(n) {
  if (!state.cats.has(catOf(n).key)) return false;
  if (!state.hist && HISTORIC.has(n.status)) return false;
  return domsOf(n).some(d => state.doms.has(d));
}
const edgeOk = d => state.etypes.has(d.et) && (state.unk || d.cert !== 'ukendt') && (state.hist || !d.hist);
function applyFilters(refit = false) {
  if (!cy) return;
  const wasFocus = state.focus;
  if (state.focus) { state.focus = false; restoreLayout(); }
  cy.batch(() => {
    cy.nodes().forEach(x => x.style('display', nodeVisible(NODES.get(x.id())) || x.id() === state.selected ? 'element' : 'none'));
    cy.edges().forEach(x => x.style('display', edgeOk(x.data()) ? 'element' : 'none'));
  });
  forced = state.selected && !nodeVisible(NODES.get(state.selected)) ? state.selected : null;
  if (wasFocus || refit) cy.fit(cy.elements(':visible'), 24);
  if (state.selected) { highlight(state.selected); if (wasFocus) renderDetail(state.selected); }
}
function highlight(id) {
  cy.elements().removeClass('dim hl sel lbl');
  if (!id) return;
  const node = cy.getElementById(id); if (node.empty()) return;
  const nb = node.closedNeighborhood().filter(':visible');
  cy.elements(':visible').not(nb).addClass('dim');
  nb.nodes().addClass('hl'); nb.edges().addClass('hl lbl'); node.removeClass('hl').addClass('sel');
}
function restoreLayout() {
  if (focusLayout) { focusLayout.stop(); focusLayout = null; }
  cy.nodes().stop(true, false);
  if (!savedPos) return;
  cy.nodes().forEach(n => { const p = savedPos[n.id()]; if (p) n.position(p); });
  savedPos = null;
}
function focusMode(id, depth = 1) {
  if (state.focus) { state.focus = false; restoreLayout(); applyFilters(); }
  savedPos = {}; cy.nodes().forEach(n => { savedPos[n.id()] = { ...n.position() }; });
  const node = cy.getElementById(id);
  const visEdges = c => c.connectedEdges().filter(e => edgeOk(e.data()));
  const visNodes = c => c.filter(n => n.id() === id || nodeVisible(NODES.get(n.id())));
  const e1 = visEdges(node), n1 = visNodes(e1.connectedNodes()).union(node);
  let col = n1.union(e1.filter(e => n1.contains(e.source()) && n1.contains(e.target())));
  if (depth > 1) {
    const e2 = visEdges(n1), n2 = visNodes(e2.connectedNodes()).union(n1);
    col = n2.union(e2.filter(e => n2.contains(e.source()) && n2.contains(e.target())));
  }
  state.focus = true;
  cy.batch(() => { cy.elements().not(col).style('display', 'none'); col.style('display', 'element'); });
  focusLayout = col.layout({ name: 'concentric', animate: !reduceMotion(), animationDuration: 350, concentric: n => n.id() === id ? 10 : (n1.contains(n) ? 5 : 1), levelWidth: () => 1, minNodeSpacing: 26, fit: true, padding: 30 });
  focusLayout.run();
  highlight(id);
  renderDetail(id);
}
function exitFocus() { state.focus = false; restoreLayout(); applyFilters(); cy.fit(cy.elements(':visible'), 24); if (state.selected) { highlight(state.selected); renderDetail(state.selected); } }
function selectNode(id, { center = true, from = 'list', push = true } = {}) {
  if (!NODES.has(id) || !cy) return;
  const switched = currentView() !== 'netvaerk';
  if (switched) showView('netvaerk', false);
  if (state.focus && !cy.getElementById(id).visible()) { state.focus = false; restoreLayout(); applyFilters(); cy.fit(cy.elements(':visible'), 24); }
  if (forced && forced !== id && !nodeVisible(NODES.get(forced))) cy.getElementById(forced).style('display', 'none');
  forced = null;
  state.selected = id;
  const x = cy.getElementById(id);
  if (x.style('display') === 'none') { x.style('display', 'element'); forced = id; }
  highlight(id);
  if (center) cy.animate({ center: { eles: x }, zoom: Math.max(cy.zoom(), 1.1) }, { duration: reduceMotion() ? 0 : 300 });
  renderDetail(id);
  setHash('node-' + id, push);
  if (switched) window.scrollTo(0, 0);
  if (from !== 'graph' && narrow()) $('#detail').scrollIntoView({ block: 'start', behavior: reduceMotion() ? 'auto' : 'smooth' });
}
function clearSelection() {
  if (forced && !nodeVisible(NODES.get(forced))) cy.getElementById(forced).style('display', 'none');
  forced = null; state.selected = null; highlight(null);
  if (state.focus) exitFocus();
  renderDetail(null); setHash('netvaerk');
}

/* ---------- detail panel ---------- */
function fieldValue(f, v) {
  if (f === 'url') return safeUrl(v.vaerdi) ? extLink(v.vaerdi) : el('span', { class: 'knote', text: v.vaerdi || 'ikke fundet' });
  if (f === 'dokumenttyper') return el('div', { class: 'chips' }, (v.liste || []).map(d => el('span', { class: 'chip', title: d.note || '' }, d.type, el('span', { class: 'mono', text: '· ' + d.bindende }))));
  if (f === 'adgang') return el('div', {}, el('div', { class: 'chips' }, (v.vaerdier || []).map(a => el('span', { class: 'chip', text: a }))), v.note ? el('div', { class: 'knote', text: v.note }) : null);
  if (f === 'identifikatorer') {
    const rows = ['eli', 'lovtidende', 'celex', 'journalnr', 'andet'].filter(k => v[k]);
    if (!rows.length) return el('span', { class: 'knote', text: 'ingen' });
    const senere = v.senere_aendringer || [];
    return el('div', {}, rows.map(k => el('div', {}, el('span', { class: 'eyebrow', text: k + ' ' }), safeUrl(v[k]) ? extLink(v[k]) : el('span', { class: k === 'andet' ? '' : 'mono', text: v[k] }))),
      v.aendringer_kontrolleret ? el('div', {}, el('span', { class: 'eyebrow', text: 'senere ændringer ' }), el('span', { class: 'knote', text: `${senere.length || 'ingen'} hos Retsinformation ${v.aendringer_kontrolleret}` })) : null,
      senere.length ? el('ul', { style: 'margin:0;padding-left:18px' }, senere.map(x => el('li', {}, extLink(x.eli, x.betegnelse)))) : null,
      v.katalog_note ? el('div', { class: 'knote', text: v.katalog_note }) : null);
  }
  if (f === 'opdatering') return el('div', {}, el('div', {}, el('b', { text: 'Frekvens: ' }), v.frekvens || 'ukendt'), el('div', {}, el('b', { text: 'Versioner: ' }), v.versionshistorik || 'ukendt'));
  return el('span', { text: v.tekst || '' });
}
function sources(list) {
  if (!list || !list.length) return null;
  return el('details', {}, el('summary', { text: plural(list.length, 'kilde', 'kilder') }), el('ol', {}, list.map(u => el('li', {}, extLink(u)))));
}
function relList(title, edges, dir) {
  if (!edges.length) return null;
  const groups = {};
  for (const e of edges) (groups[e.type] = groups[e.type] || []).push(e);
  const ul = el('ul');
  const other = e => dir === 'out' ? e.to : e.from;
  for (const [t] of ETYPES) for (const e of (groups[t] || []).sort((a, b) => minName(other(a)).localeCompare(minName(other(b)), 'da'))) {
    ul.append(el('li', { title: e.desc }, el('span', { class: 'et', text: dir === 'out' ? ET_OUT[t] : inLabel(e) }), certMark(e.cert), nodeLink(other(e)), edgeChips(e)));
  }
  return el('div', { class: 'rel' }, el('h3', { text: `${title} (${edges.length})` }), ul);
}
const CHAIN_TYPES = new Set(['lov', 'bekendtgørelse']);
function renderDetail(id) {
  const box = $('#detail'); box.replaceChildren();
  if (!id) {
    const sug = ['lov-byggeloven', 'bek-br18', 'naevn-byggeklageenheden', 'kilde-retsinformation', 'sty-social-og-boligstyrelsen', 'lov-planloven', 'eu-dir-2024-1275'].filter(i => NODES.has(i));
    box.append(el('div', { class: 'empty' }, el('span', { class: 'eyebrow', text: 'Ingen node valgt' }),
      el('p', { text: 'Klik på en node i kortet, eller søg øverst. Detaljerne viser hvert felt med sikkerhed og kilder, og alle ind- og udgående kanter.' }),
      el('div', {}, el('h3', { text: 'Gode steder at starte' }), el('ul', {}, sug.map(i => el('li', {}, nodeLink(i))))),
      el('div', {}, el('h3', { text: 'Nodetyper' }), el('ul', { class: 'plain' }, CATS.map(c => el('li', { style: 'display:flex;gap:6px;align-items:center' }, swatch(c), c.label))))));
    return;
  }
  const n = NODES.get(id), c = catOf(n);
  const chips = el('div', { class: 'chips' }, el('span', { class: 'chip' }, swatch(c, 12), n.type), el('span', { class: 'chip status-' + n.status, text: n.status }),
    (n.dom || []).map(d => el('span', { class: 'chip', text: DOM_LABEL[d] || d })),
    (n.kritiker || []).map(k => el('span', { class: 'chip', title: 'Tilføjet af completeness-kritikeren for dette ministerområde', text: `tilføjet af kritiker: ${KRIT_LABEL[k] || k}` })));
  const head = el('div', { class: 'head' }, chips, el('h3', { class: 'title', text: n.navn }), el('div', { class: 'mono idline', text: n.id }),
    n.min && n.min !== 'ingen' ? el('div', {}, el('span', { class: 'eyebrow', text: 'Ministerium ' }), nodeLink(n.min)) : null,
    n.kat ? el('div', {}, el('span', { class: 'eyebrow', text: 'Katalog ' }), KIDX.has(n.kat) ? katLink(n.kat, `${n.kat} · ${KIDX.get(n.kat).lt}`) : el('span', { class: 'mono', title: 'Historisk version – kun i katalog/retsinformation_lta.jsonl', text: n.kat + ' (historisk)' })) : null);
  const acts = el('div', { class: 'btnrow' },
    el('button', { class: 'btn', type: 'button', onclick: () => focusMode(id, 1), text: 'Fokus: naboer' }),
    el('button', { class: 'btn', type: 'button', onclick: () => focusMode(id, 2), text: 'Fokus: 2 led' }),
    state.focus ? el('button', { class: 'btn', type: 'button', onclick: exitFocus, text: 'Hele kortet' }) : null,
    CHAIN_TYPES.has(n.type) ? el('button', { class: 'btn primary', type: 'button', onclick: () => { showView('kaeder', false); setChainRoot(id); }, text: 'Vis hjemmelskæde' }) : null);
  const fields = el('div', { class: 'fields' });
  for (const [f, l] of FIELDS) {
    const v = n[f]; if (!v) continue;
    fields.append(el('div', { class: 'field' }, el('div', { class: 'fh' }, el('span', { class: 'eyebrow', text: l }), certBadge(v.sikkerhed)), el('div', { class: 'fv' }, fieldValue(f, v)), v.kilde_note ? el('div', { class: 'knote', text: v.kilde_note }) : null, sources(v.kilder)));
  }
  if (n.prev && n.prev.length) fields.append(el('div', { class: 'field' }, el('div', { class: 'fh' }, el('span', { class: 'eyebrow', text: 'Tidligere navne' })),
    el('ul', { style: 'margin:0;padding-left:18px' }, n.prev.map(p => el('li', {}, `${p.navn} `, el('span', { class: 'mono', text: p.periode || '' }), ' ', certMark(p.sikkerhed), p.efterfoelger && NODES.has(p.efterfoelger) ? el('span', {}, ' → ', nodeLink(p.efterfoelger)) : null)))));
  if (n.kx && n.kx.length) fields.append(el('div', { class: 'field' }, el('span', { class: 'eyebrow', text: 'Typiske krydsreferencer i teksten' }), el('ul', { style: 'margin:0;padding-left:18px' }, n.kx.map(k => el('li', { class: 'mono', text: k })))));
  if (n.ingest) fields.append(el('div', { class: 'field' }, el('span', { class: 'eyebrow', text: 'Ingest-vurdering' }), el('div', {}, `Værdi ${n.ingest.vaerdi} · besvær ${n.ingest.besvaer} · prioritet ${(n.ingest.vaerdi / n.ingest.besvaer).toFixed(2).replace('.', ',')}`), el('div', { class: 'knote', text: n.ingest.begrundelse })));
  if (n.note) fields.append(el('div', { class: 'field' }, el('span', { class: 'eyebrow', text: 'Note' }), el('div', { class: 'fv', style: 'color:var(--ink-2);font-size:.85rem', text: n.note })));
  box.append(head, acts, relList('Udgående', OUT.get(id) || [], 'out'), relList('Indgående', INC.get(id) || [], 'in'), fields);
  box.scrollTop = 0;
}

/* ---------- search ---------- */
const norm = s => (s || '').toLowerCase().replace(/æ/g, 'ae').replace(/ø/g, 'oe').replace(/å/g, 'aa').normalize('NFKD').replace(/[̀-ͯ]/g, '');
const SIDX = D.nodes.map(n => ({ id: n.id, name: norm(n.navn), all: norm(n.navn + ' ' + n.id + ' ' + (n.identifikatorer?.lovtidende || '') + ' ' + (n.prev || []).map(p => p.navn).join(' ')) }));
function score(r, v) {
  const paren = r.name.replace(/\s*\(.*?\)\s*/g, ' ').trim();
  if (r.name === v || paren === v) return 0;
  if (new RegExp('(^|[^a-z0-9])' + v.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '([^a-z0-9]|$)').test(r.name)) return 1;
  if (r.name.startsWith(v)) return 2;
  if (r.name.includes(v)) return 3;
  return 4;
}
function initSearch() {
  const q = $('#q'), box = $('#qres'); let items = [], act = -1;
  q.setAttribute('role', 'combobox'); q.setAttribute('aria-expanded', 'false'); q.setAttribute('aria-autocomplete', 'list');
  const close = () => { box.hidden = true; act = -1; q.setAttribute('aria-expanded', 'false'); q.removeAttribute('aria-activedescendant'); };
  const pick = id => { close(); q.value = ''; selectNode(id, { from: 'search' }); };
  q.addEventListener('input', () => {
    const v = norm(q.value.trim()); box.replaceChildren(); act = -1;
    if (v.length < 2) return close();
    const words = v.split(/\s+/);
    items = SIDX.filter(r => words.every(w => r.all.includes(w))).map(r => [r, score(r, v)]).sort((a, b) => a[1] - b[1] || a[0].name.length - b[0].name.length).slice(0, 40).map(x => x[0].id);
    const raw = q.value.trim(), kn = katMatches(raw, false).length;
    const katBtn = el('button', { type: 'button', role: 'option', id: 'qo-kat', 'aria-selected': false, onclick: () => { close(); q.value = ''; katState.q = raw; katState.min = katState.omr = katState.type = 'alle'; katState.limit = 200;
      if (rendered.has('katalog')) { $('#kat-q').value = raw; ['#kat-min', '#kat-omr', '#kat-type'].forEach(s => { $(s).value = 'alle'; }); renderKatBars(); renderKatalog(); } showView('katalog'); window.scrollTo(0, 0); } },
      el('span', { text: `Søg “${raw}” i katalog over gældende lovgivning` }), el('span', { class: 'rid', text: `${nf.format(kn)} træf` }));
    if (!items.length) { box.append(el('div', { class: 'hint', style: 'padding:8px 10px', text: 'Ingen træf i registret' }), katBtn); box.hidden = false; q.setAttribute('aria-expanded', 'true'); return; }
    items.forEach((id, i) => { const n = NODES.get(id); box.append(el('button', { type: 'button', role: 'option', id: 'qo' + i, 'aria-selected': false, onclick: () => pick(id) }, swatch(catOf(n), 12), el('span', { text: n.navn }), el('span', { class: 'rid', text: n.id }))); });
    box.append(katBtn);
    box.hidden = false; q.setAttribute('aria-expanded', 'true');
  });
  q.addEventListener('keydown', ev => {
    if (box.hidden) return;
    const opts = [...box.querySelectorAll('button')];
    if ((ev.key === 'ArrowDown' || ev.key === 'ArrowUp') && opts.length) {
      ev.preventDefault(); act = (act + (ev.key === 'ArrowDown' ? 1 : -1) + opts.length) % opts.length;
      opts.forEach((o, i) => o.setAttribute('aria-selected', String(i === act))); opts[act].scrollIntoView({ block: 'nearest' });
      q.setAttribute('aria-activedescendant', opts[act].id);
    } else if (ev.key === 'Enter') { ev.preventDefault(); const b = opts[act >= 0 ? act : 0]; if (b) b.click(); }
    else if (ev.key === 'Escape') close();
  });
  document.addEventListener('click', ev => { if (!ev.target.closest('.search')) close(); });
}

/* ---------- chain view ---------- */
let chainRoot = null;
const HUB = new Set(['kommune-alle', 'region-alle']);
const isDoc = n => ['lov', 'bek', 'vejledning', 'eu', 'kilde', 'meta'].includes(catOf(n).key);
const COLS = ['Hjemmel i', 'Ressort og udsteder', 'Udgangspunkt', 'Hjemmel 1. led', 'Hjemmel 2. led', 'Instanser med hjemmel i kæden', 'Klage og domstolsprøvelse', 'Vejledning og praksis', 'Retsakter der henviser hertil', 'Henviser til (standarder m.m.)', 'EU-retsakter'];
function chainCandidates() {
  return D.nodes.filter(n => CHAIN_TYPES.has(n.type)).sort((a, b) => (a.type === b.type ? 0 : a.type === 'lov' ? -1 : 1) || a.navn.localeCompare(b.navn, 'da'));
}
function buildChain(root) {
  const col = new Map(); const add = (id, c) => { if (!col.has(id) && NODES.has(id)) col.set(id, c); };
  add(root, 2);
  for (const e of INC.get(root) || []) if (e.type === 'hjemmel_for') add(e.from, 0);
  for (const e of INC.get(root) || []) if (['ressortansvar', 'udsteder', 'delegation'].includes(e.type)) add(e.from, 1);
  const rn = NODES.get(root);
  if (![...col.values()].includes(1) && rn.min && rn.min !== 'ingen') add(rn.min, 1);
  const l1 = [];
  for (const e of OUT.get(root) || []) if (e.type === 'hjemmel_for') { const t = NODES.get(e.to); if (!t) continue; if (isDoc(t)) { add(e.to, 3); l1.push(e.to); } else add(e.to, 5); }
  const l2 = [];
  for (const id of l1) for (const e of OUT.get(id) || []) if (e.type === 'hjemmel_for' && !col.has(e.to)) { const t = NODES.get(e.to); if (!t) continue; if (isDoc(t)) { add(e.to, 4); l2.push(e.to); } else add(e.to, 5); }
  const chainIds = [root, ...l1, ...l2];
  for (const id of chainIds) for (const e of INC.get(id) || []) if (['klageinstans', 'domstolsproevelse'].includes(e.type)) add(e.from, 6);
  for (const id of chainIds) for (const e of INC.get(id) || []) if (e.type === 'henviser_til' && !HUB.has(e.from)) {
    const s = NODES.get(e.from); if (!s) continue;
    add(e.from, ['lov', 'bek'].includes(catOf(s).key) ? 8 : 7);
  }
  for (const id of [root, ...l1]) for (const e of OUT.get(id) || []) if (e.type === 'henviser_til') add(e.to, 9);
  for (const id of chainIds) for (const e of OUT.get(id) || []) if (e.type === 'implementerer_EU') add(e.to, 10);
  for (const id of [...col.keys()]) if (col.get(id) === 5 && !HUB.has(id)) for (const e of INC.get(id) || []) if (['klageinstans', 'domstolsproevelse'].includes(e.type) && !HUB.has(e.from)) add(e.from, 6);
  return col;
}
function fitChain() {
  if (!cy2) return;
  cy2.resize(); cy2.fit(undefined, 30);
  if (cy2.zoom() < 0.55) {
    const root = cy2.getElementById(chainRoot);
    cy2.zoom(0.55);
    const first = cy2.nodes('[kind = "hdr"]').min(n => n.position('x'));
    const x0 = first && first.ele ? first.ele.position('x') : root.position('x');
    cy2.pan({ x: 60 - x0 * 0.55, y: cy2.height() / 2 - root.position('y') * 0.55 });
  }
}
function ensureOption(id) {
  const sel = $('#chain-root');
  if (![...sel.options].some(o => o.value === id)) sel.append(el('option', { value: id, text: shortName(NODES.get(id).navn, 80) }));
  sel.value = id;
}
function setChainRoot(id, push = true) {
  if (!NODES.has(id) || !CHAIN_TYPES.has(NODES.get(id).type)) return;
  chainRoot = id; ensureOption(id); setHash('kaede-' + id, push);
  const t = tokens(); const col = buildChain(id);
  const byCol = COLS.map(() => []);
  for (const [nid, c] of col) byCol[c].push(nid);
  byCol.forEach(l => l.sort((a, b) => catOf(NODES.get(a)).key.localeCompare(catOf(NODES.get(b)).key) || minName(a).localeCompare(minName(b), 'da')));
  const els = []; const SUBW = 215, GAP = 70, Y = 64, ROWS = 12; let x0 = 0;
  byCol.forEach((ids, c) => {
    if (!ids.length) return;
    const subs = Math.ceil(ids.length / ROWS), rows = Math.min(ids.length, ROWS), h = (rows - 1) * Y;
    els.push({ group: 'nodes', data: { id: 'hdr' + c, label: COLS[c], kind: 'hdr', color: t.bg, shape: 'rectangle', size: 1 }, position: { x: x0 + (subs - 1) * SUBW / 2, y: -h / 2 - 64 } });
    ids.forEach((nid, i) => els.push({ group: 'nodes', data: { ...nodeData(NODES.get(nid), t), label: shortName(NODES.get(nid).navn, 60) }, position: { x: x0 + Math.floor(i / ROWS) * SUBW, y: -h / 2 + (i % ROWS) * Y } }));
    x0 += subs * SUBW + GAP;
  });
  for (const e of EDGES) if (col.has(e.from) && col.has(e.to) && (col.get(e.from) !== col.get(e.to) || e.type === 'hjemmel_for')) els.push({ group: 'edges', data: edgeData(e) });
  if (!cy2) {
    cy2 = cytoscape({ container: $('#cy2'), elements: els, layout: { name: 'preset' }, style: cyStyle(t, true), minZoom: 0.1, maxZoom: 3 });
    cy2.on('mouseover', 'node', ev => { if (ev.target.data('kind') === 'hdr') return; const nb = ev.target.closedNeighborhood(); cy2.elements().not(nb).addClass('dim'); nb.edges().addClass('hl lbl'); ev.target.addClass('sel'); });
    cy2.on('mouseout', 'node', () => cy2.elements().removeClass('dim hl lbl sel'));
    cy2.on('tap', 'node', ev => { const nid = ev.target.id(); const n = NODES.get(nid); if (!n) return; if (CHAIN_TYPES.has(n.type) && nid !== chainRoot) setChainRoot(nid); else selectNode(nid, { from: 'list' }); });
  } else { cy2.elements().remove(); cy2.add(els); }
  fitChain();
  const cols = $('#chain-cols'); cols.replaceChildren();
  byCol.forEach((ids, c) => {
    if (!ids.length && c !== 3) return;
    cols.append(el('div', { class: 'panel col' }, el('span', { class: 'eyebrow', text: `${COLS[c]} (${ids.length})` }),
      ids.length ? el('ul', {}, ids.map(nid => el('li', {}, swatch(catOf(NODES.get(nid)), 11), nodeLink(nid), HISTORIC.has(NODES.get(nid).status) ? el('span', { class: 'chip hist', text: NODES.get(nid).status }) : null))) : el('div', { class: 'knote', text: 'Ingen i registret' })));
  });
}
function initChain() {
  const sel = $('#chain-root');
  const g1 = el('optgroup', { label: 'Love' }), g2 = el('optgroup', { label: 'Bekendtgørelser' });
  for (const n of chainCandidates()) (n.type === 'lov' ? g1 : g2).append(el('option', { value: n.id, text: shortName(n.navn, 80) }));
  sel.append(g1, g2);
  sel.onchange = () => setChainRoot(sel.value);
  $('#chain-open').onclick = () => selectNode(chainRoot, { from: 'list' });
}

/* ---------- ressort view ---------- */
function linkify(s) {
  return String(s).split(/\b((?:min|sty|org|naevn|raad|tilsyn|fond|ombud|dom)-[a-z0-9-]+)\b/).map(t => NODES.has(t) ? nodeLink(t) : t);
}
function renderRessort() {
  const mins = D.nodes.filter(n => n.type === 'ministerium');
  const edgesOf = id => (OUT.get(id) || []).filter(e => e.type === 'ressortansvar' && NODES.has(e.to));
  const active = mins.filter(n => n.status === 'aktiv').sort((a, b) => edgesOf(b.id).length - edgesOf(a.id).length || a.navn.localeCompare(b.navn, 'da'));
  const old = mins.filter(n => n.status !== 'aktiv');
  const r = D.regering;
  $('#ressort-lede').textContent = `${r.navn} blev dannet ${fmtDate(r.dannet)} (${r.partier.join(', ')}). Hvert kort viser de instanser, love og bekendtgørelser, som ministeriet har ressort for: via kanten ressortansvar, og ellers via nodens ministeriumfelt (mærket ”felt”).`;
  const grid = $('#min-grid');
  const byName = (a, b) => minName(a.to).localeCompare(minName(b.to), 'da');
  const item = e => el('li', {}, swatch(catOf(NODES.get(e.to)), 11), e.viaField ? el('span', { class: 'chip', title: 'Kun angivet i nodens ministeriumfelt, ingen ressortansvar-kant', text: 'felt' }) : certMark(e.cert), nodeLink(e.to),
    HISTORIC.has(NODES.get(e.to).status) ? el('span', { class: 'chip hist', text: NODES.get(e.to).status }) : null, e.hist && !HISTORIC.has(NODES.get(e.to).status) ? el('span', { class: 'chip hist', text: 'historisk' }) : null);
  const group = (label, list, open = false) => list.length ? el('details', open ? { open: true } : {}, el('summary', { text: `${label} (${list.length})` }), el('ul', {}, list.sort(byName).map(item))) : null;
  for (const m of [...active, ...old]) {
    const viaEdge = edgesOf(m.id);
    const seen = new Set(viaEdge.map(e => e.to));
    const viaField = D.nodes.filter(n => n.min === m.id && n.id !== m.id && !seen.has(n.id)).map(n => ({ to: n.id, cert: 'ukendt', viaField: true, hist: false, disp: false }));
    const all = [...viaEdge, ...viaField];
    const disputed = all.filter(e => e.disp);
    const ok = all.filter(e => !e.disp);
    const isInst = e => ['myndighed', 'klage'].includes(catOf(NODES.get(e.to)).key);
    const cur = e => !HISTORIC.has(NODES.get(e.to).status) && !e.hist;
    const inst = ok.filter(e => isInst(e) && cur(e)), gone = ok.filter(e => isInst(e) && !cur(e));
    const laws = ok.filter(e => NODES.get(e.to).type === 'lov'), other = ok.filter(e => !isInst(e) && NODES.get(e.to).type !== 'lov');
    const minister = ((m.note || '').match(/Minister pr\. 2026-10-28: (.*?)\.(?:\s|$)/) || [])[1];
    const areas = D.omraader.filter(o => o.ministerium_id === m.id).map(o => o.omraade);
    const period = m.status !== 'aktiv';
    grid.append(el('article', { class: 'panel mcard' + (period ? ' old' : '') },
      el('div', { class: 'mh' }, el('span', { class: 'eyebrow', text: period ? `Ministerium · ${m.status}` : 'Ministerium' }),
        el('button', { class: 'lnk mname', type: 'button', onclick: () => selectNode(m.id, { from: 'list' }), text: m.navn }),
        minister ? el('span', { class: 'minister', text: minister }) : null),
      el('div', { class: 'counts' }, el('span', { text: plural(inst.length, 'instans', 'instanser') + (period ? ' i perioden' : '') }), el('span', { text: plural(laws.length, 'lov', 'love') }), el('span', { text: plural(other.length, 'øvrig retsakt', 'øvrige retsakter') })),
      period ? group('Instanser i perioden', inst) : (inst.length ? el('ul', {}, inst.sort(byName).map(item)) : null),
      group('Nedlagte, omdøbte og historiske', gone),
      group('Love', laws), group('Bekendtgørelser og øvrige', other),
      disputed.length ? el('details', {}, el('summary', { text: `Bestridte (${disputed.length})` }), el('ul', {}, disputed.sort(byName).map(e => el('li', { title: e.desc }, certMark(e.cert), nodeLink(e.to), el('span', { class: 'chip bestridt', text: 'bestridt' }))))) : null,
      areas.length ? el('div', { class: 'areas' }, el('span', { class: 'eyebrow', text: 'Områder i kortlægningen ' }), areas.join(' · ')) : null));
  }
  const tl = $('#timeline');
  for (const x of [...D.ressortomlaegninger].sort((a, b) => (b.dato || '').localeCompare(a.dato || ''))) tl.append(el('li', {}, el('div', { class: 'date', text: x.dato }), el('div', { class: 'what' },
    el('div', { style: 'display:flex;gap:8px;align-items:center;flex-wrap:wrap' }, el('b', { text: x.omraade }), certBadge(x.sikkerhed)),
    el('div', { class: 'ft' }, el('b', {}, linkify(x.fra)), ' → ', el('b', {}, linkify(x.til)), x.retsakt ? el('span', { text: ` · ${x.retsakt}` }) : null), sources(x.kilder))));
}

/* ---------- kilder view ---------- */
const KSEG = [['alle', 'Alle'], ['portal', 'Portaler og databaser'], ['instans', 'Instanser'], ['retsakt', 'Retsakter og samlinger']];
const kState = { seg: 'alle', q: '', cell: null, sort: 'prio', dir: -1 };
const kSection = n => ['dokumentkilde', 'praksissamling'].includes(n.type) ? 'portal' : ['ministerium', 'myndighed', 'klage'].includes(catOf(n).key) || ['privat-organisation', 'standardiseringsorgan', 'eu-institution'].includes(n.type) ? 'instans' : 'retsakt';
const prio = n => n.ingest.vaerdi / n.ingest.besvaer;
const RATED = D.nodes.filter(n => n.ingest);
const kBase = () => { const q = norm(kState.q); return RATED.filter(n => (kState.seg === 'alle' || kSection(n) === kState.seg) && (!q || norm(n.navn + ' ' + n.id + ' ' + (n.ingest.begrundelse || '')).includes(q))); };
function renderMatrix(focusKey) {
  const base = kBase();
  const box = $('#matrix'); box.replaceChildren();
  const counts = {}; for (const n of base) { const k = n.ingest.vaerdi + ':' + n.ingest.besvaer; counts[k] = (counts[k] || 0) + 1; }
  const max = Math.max(1, ...Object.values(counts));
  const ns = 'http://www.w3.org/2000/svg', S = 50, L = 46, T = 14, W = L + 5 * S + 10, H = T + 5 * S + 46;
  const svg = document.createElementNS(ns, 'svg'); svg.setAttribute('viewBox', `0 0 ${W} ${H}`); svg.setAttribute('role', 'group');
  svg.setAttribute('aria-label', 'Prioritetsmatrix: antal kilder pr. kombination af værdi og besvær');
  const T_ = (x, y, s, a = {}) => { const t = document.createElementNS(ns, 'text'); t.setAttribute('x', x); t.setAttribute('y', y); t.textContent = s; t.setAttribute('font-size', a.fs || 11); t.setAttribute('fill', a.fill || 'var(--ink-2)'); t.setAttribute('text-anchor', a.anchor || 'middle'); if (a.weight) t.setAttribute('font-weight', a.weight); if (a.dom) t.setAttribute('dominant-baseline', a.dom); return t; };
  const steps = ['--seq-1', '--seq-2', '--seq-3', '--seq-4', '--seq-5', '--seq-6'];
  for (let v = 5; v >= 1; v--) for (let b = 1; b <= 5; b++) {
    const key = v + ':' + b, c = counts[key] || 0, x = L + (b - 1) * S, y = T + (5 - v) * S;
    const g = document.createElementNS(ns, 'g'); g.setAttribute('class', 'cell' + (kState.cell === key ? ' on' : '')); g.setAttribute('data-k', key);
    if (c || kState.cell === key) { g.setAttribute('tabindex', 0); g.setAttribute('role', 'button'); g.setAttribute('aria-pressed', String(kState.cell === key)); g.setAttribute('aria-label', `Værdi ${v}, besvær ${b}: ${plural(c, 'kilde', 'kilder')}`); }
    const r = document.createElementNS(ns, 'rect'); r.setAttribute('x', x + 1); r.setAttribute('y', y + 1); r.setAttribute('width', S - 2); r.setAttribute('height', S - 2); r.setAttribute('rx', 3);
    const lvl = c ? Math.min(5, Math.floor((c / max) * 5.999)) : -1;
    r.setAttribute('fill', c ? `var(${steps[lvl]})` : 'var(--surface-2)');
    g.append(r);
    if (c) g.append(T_(x + S / 2, y + S / 2 + 1, c, { fs: 13, weight: 600, fill: lvl >= 3 ? 'var(--seq-ink-hi)' : 'var(--ink)', dom: 'middle' }));
    const ttl = document.createElementNS(ns, 'title'); ttl.textContent = `Værdi ${v} · besvær ${b} · prioritet ${(v / b).toFixed(2).replace('.', ',')} · ${plural(c, 'kilde', 'kilder')}`; g.append(ttl);
    const act = () => { if (!c && kState.cell !== key) return; kState.cell = kState.cell === key ? null : key; renderKTable(key); };
    g.addEventListener('click', act); g.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); act(); } });
    svg.append(g);
  }
  for (let v = 1; v <= 5; v++) svg.append(T_(L - 10, T + (5 - v) * S + S / 2 + 4, v, { anchor: 'end' }));
  for (let b = 1; b <= 5; b++) svg.append(T_(L + (b - 1) * S + S / 2, T + 5 * S + 16, b));
  svg.append(T_(L + 2.5 * S, T + 5 * S + 36, 'Besvær →', { fs: 11, fill: 'var(--muted)' }));
  const yl = T_(12, T + 2.5 * S, 'Værdi →', { fs: 11, fill: 'var(--muted)' }); yl.setAttribute('transform', `rotate(-90 12 ${T + 2.5 * S})`); svg.append(yl);
  box.append(el('div', { class: 'eyebrow', style: 'margin-bottom:6px', text: `Prioritetsmatrix · ${plural(base.length, 'vurderet node', 'vurderede noder')}` }), svg,
    el('p', { class: 'knote', style: 'margin:6px 0 0', text: kState.cell ? 'Klik på den markerede celle igen for at fjerne filteret.' : 'Øverst til venstre er størst værdi for mindst besvær.' }));
  if (focusKey) svg.querySelector(`[data-k="${focusKey}"]`)?.focus();
}
function renderKTable(focusCell, focusSort) {
  renderMatrix(focusCell);
  const rows = kBase().filter(n => !kState.cell || kState.cell === n.ingest.vaerdi + ':' + n.ingest.besvaer);
  const key = { prio: n => prio(n), v: n => n.ingest.vaerdi, b: n => n.ingest.besvaer, navn: n => n.navn };
  rows.sort((a, b) => { const ka = key[kState.sort](a), kb = key[kState.sort](b); return (typeof ka === 'string' ? ka.localeCompare(kb, 'da') : ka - kb) * kState.dir || prio(b) - prio(a) || a.navn.localeCompare(b.navn, 'da'); });
  $('#k-count').textContent = `${rows.length} af ${RATED.length}`;
  const th = (k, l) => el('th', {}, k ? el('button', { type: 'button', 'data-sort': k, 'aria-sort': kState.sort === k ? (kState.dir > 0 ? 'ascending' : 'descending') : null, onclick: () => { kState.dir = kState.sort === k ? -kState.dir : (k === 'navn' ? 1 : -1); kState.sort = k; renderKTable(null, k); }, text: l }) : l);
  const body = rows.length ? rows.map((n, i) => el('tr', {},
    el('td', { class: 'num', text: i + 1 }),
    el('td', {}, el('div', { style: 'display:flex;gap:6px;align-items:baseline' }, swatch(catOf(n), 11), nodeLink(n.id)), safeUrl(n.url.vaerdi) ? el('div', { class: 'mono idline' }, extLink(n.url.vaerdi, n.url.vaerdi.replace(/^https?:\/\/(www\.)?/, '').slice(0, 48))) : null),
    el('td', { class: 'num', text: n.ingest.vaerdi }), el('td', { class: 'num', text: n.ingest.besvaer }),
    el('td', { class: 'num', text: prio(n).toFixed(2).replace('.', ',') }),
    el('td', {}, el('div', { class: 'chips' }, (n.adgang.vaerdier || []).map(a => el('span', { class: 'chip', text: a })))),
    el('td', {}, certBadge(n.adgang.sikkerhed)),
    el('td', {}, el('div', { class: 'why' }, certMark(n.licens.sikkerhed), ' ', n.licens.tekst || ''), el('div', { class: 'why', style: 'color:var(--muted)', text: n.ingest.begrundelse || '' }))))
    : [el('tr', {}, el('td', { colspan: 8, class: 'knote', text: 'Ingen kilder matcher. Skift segment, ryd søgningen eller fjern cellefilteret.' }))];
  $('#k-table').replaceChildren(
    el('thead', {}, el('tr', {}, th(null, '#'), th('navn', 'Kilde'), th('v', 'Værdi'), th('b', 'Besvær'), th('prio', 'Prioritet'), th(null, 'Adgang'), th(null, 'Sikkerhed (adgang)'), th(null, 'Licens og begrundelse'))),
    el('tbody', {}, body));
  if (focusSort) $(`#k-table th button[data-sort="${focusSort}"]`)?.focus();
}
function initKilder() {
  const seg = $('#k-seg');
  for (const [k, l] of KSEG) seg.append(el('button', { type: 'button', 'aria-pressed': k === kState.seg, onclick: ev => { kState.seg = k; seg.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === ev.currentTarget))); renderKTable(); }, text: l }));
  $('#k-q').addEventListener('input', ev => { kState.q = ev.target.value; renderKTable(); });
  renderKTable();
}

/* ---------- huller view ---------- */
const hState = { type: 'alle', dom: 'alle', q: '' };
const HIDX = D.huller.map(h => norm(h.emne + ' ' + h.beskrivelse + ' ' + (h.noder || []).map(id => id + ' ' + minName(id)).join(' ')));
function renderHuller() {
  const box = $('#hbars'); box.replaceChildren();
  const cnt = {}; for (const h of D.huller) cnt[h.type] = (cnt[h.type] || 0) + 1;
  const max = Math.max(...Object.values(cnt));
  for (const [k, l] of HTYPES) if (cnt[k]) box.append(el('span', { text: l }), el('div', { class: 'track' }, el('div', { class: 'fill', style: `width:${100 * cnt[k] / max}%` })), el('span', { class: 'v', text: cnt[k] }));
  const q = norm(hState.q);
  const rows = D.huller.filter((h, i) => (hState.type === 'alle' || h.type === hState.type) && (hState.dom === 'alle' || (h.domaener || []).includes(hState.dom)) && (!q || HIDX[i].includes(q)));
  $('#h-count').textContent = `${rows.length} af ${D.huller.length}`;
  const list = $('#hlist'); list.replaceChildren();
  if (!rows.length) list.append(el('p', { class: 'knote', text: 'Ingen huller matcher. Vælg ”Alle”, et andet domæne eller ryd søgningen.' }));
  for (const h of rows) {
    const ids = (h.noder || []).filter(id => NODES.has(id));
    list.append(el('article', { class: 'panel hcard' },
      el('span', { class: 'htype', text: (HTYPES.find(x => x[0] === h.type) || [, h.type])[1] }),
      el('h3', { text: h.emne }), el('p', { text: h.beskrivelse }),
      ids.length ? el('div', { class: 'nodes' }, ids.slice(0, 12).map(id => nodeLink(id))) : null,
      ids.length > 12 ? el('details', {}, el('summary', { text: `+${ids.length - 12} flere noder` }), el('div', { class: 'nodes' }, ids.slice(12).map(id => nodeLink(id)))) : null,
      (h.domaener || []).length ? el('div', { class: 'chips' }, h.domaener.map(d => el('span', { class: 'chip', text: DOM_LABEL[d] || d }))) : null,
      sources(h.kilder)));
  }
}
function initHuller() {
  const seg = $('#h-seg');
  for (const [k, l] of [['alle', 'Alle'], ...HTYPES]) if (k === 'alle' || D.huller.some(h => h.type === k)) seg.append(el('button', { type: 'button', 'aria-pressed': k === hState.type, onclick: ev => { hState.type = k; seg.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === ev.currentTarget))); renderHuller(); }, text: l }));
  const sel = $('#h-dom');
  sel.append(el('option', { value: 'alle', text: 'Alle domæner' }), ...DOMS.filter(([k]) => D.huller.some(h => (h.domaener || []).includes(k))).map(([k, l]) => el('option', { value: k, text: l })));
  sel.onchange = () => { hState.dom = sel.value; renderHuller(); };
  $('#h-q').addEventListener('input', ev => { hState.q = ev.target.value; renderHuller(); });
  renderHuller();
}

/* ---------- katalog (hele Lovtidende A, gældende dokumenter) ---------- */
const K = JSON.parse(document.getElementById('kat').textContent);
const KCERT = ['verificeret', 'sandsynlig', 'ukendt'];
const KTYPE = { 'lov': 'Lov', 'ændringslov': 'Ændringslov', 'lovbekendtgørelse': 'Lovbekendtgørelse', 'bekendtgørelse': 'Bekendtgørelse', 'ændringsbekendtgørelse': 'Ændringsbekendtgørelse',
  'ikrafttrædelsesbekendtgørelse': 'Ikrafttrædelsesbekendtgørelse', 'bekendtgørelse-international': 'Bekendtgørelse (traktat)', 'anordning': 'Anordning', 'ændringsanordning': 'Ændringsanordning',
  'ikrafttrædelsesanordning': 'Ikrafttrædelsesanordning', 'bekendtgørelse-af-anordning': 'Bekendtgørelse af anordning', 'åbent-brev': 'Åbent brev' };
const KOMR = { statsret: 'Statsret', kommuner: 'Kommuner og regioner', valg: 'Valg', international: 'Internationale aftaler', forsvar: 'Forsvar', 'beredskab-brand': 'Beredskab og brand',
  'strafferet-politi': 'Strafferet og politi', retspleje: 'Retspleje og domstole', 'familie-person': 'Familie- og personret', erhvervsret: 'Erhvervsret', finansiel: 'Finansiel regulering',
  skat: 'Skat og afgifter', 'offentlig-oekonomi': 'Offentlig økonomi og personale', arbejdsmarked: 'Arbejdsmarked og ydelser', arbejdsmiljoe: 'Arbejdsmiljø', social: 'Social', aeldre: 'Ældre',
  'boern-dagtilbud': 'Børn og dagtilbud', sundhed: 'Sundhed', undervisning: 'Undervisning', 'forskning-videregaaende': 'Forskning og videregående uddannelse', 'kultur-medier': 'Kultur og medier',
  kirke: 'Kirke og trossamfund', udlaendinge: 'Udlændinge og integration', transport: 'Transport', soefart: 'Søfart', 'plan-landdistrikter': 'Plan og landdistrikter', byggeri: 'Byggeri', bolig: 'Bolig',
  'energi-forsyning': 'Energi og forsyning', klima: 'Klima', 'el-gas-vvs': 'El, gas og VVS', miljoe: 'Miljø', affald: 'Affald', 'natur-vandmiljoe': 'Natur og vandmiljø', 'landbrug-dyr': 'Landbrug og dyr',
  foedevarer: 'Fødevarer', fiskeri: 'Fiskeri', 'digitalisering-tele': 'Digitalisering og tele', persondata: 'Persondata', 'forbruger-konkurrence': 'Forbruger og konkurrence', andet: 'Andet',
  'ikke klassificeret': 'Ikke klassificeret' };
const KROWS = K.rows.map(r => ({
  id: 'lta-' + r[0], yn: r[0], t: r[1], type: K.types[r[2]], d: r[3], u: K.udst[r[4]], uc: KCERT[r[5]], m: K.mins[r[6]], mc: KCERT[r[7]], o: K.omr[r[8]],
  reg: r[9] ? r[9].split(',') : [],
  refs: r[10] ? r[10].split(',').map(x => ({ id: 'lta-' + x.replace('~', ''), c: x.endsWith('~') ? 'sandsynlig' : 'verificeret' })) : [],
  eu: r[11] ? r[11].split(',').map(x => ({ id: 'eu-' + x.replace('*', ''), imp: x.endsWith('*') })) : [],
  am: r[12] ? r[12].split(',').map(x => 'lta-' + x) : [], lt: r[13],
}));
const KIDX = new Map(KROWS.map(r => [r.id, r]));
const katState = { q: '', min: 'alle', omr: 'alle', type: 'alle', limit: 200, sel: null };
let KSRCH = null, KINB = null;
const katMinName = id => NODES.get(id)?.navn || (id === 'ingen' ? 'Intet ministerium (Folketinget m.fl.)' : id === 'ukendt' ? 'Ukendt ressort' : id);
// Samme URL som datasættets eget kilde-felt (viz_kat.py afviser data, hvor de afviger).
const katUrl = r => { const [y, n] = r.yn.split('-'); return `https://www.retsinformation.dk/eli/lta/${y}/${n}/xml`; };
const katSearchIdx = () => KSRCH || (KSRCH = KROWS.map(r => norm(r.t + ' ' + r.id + ' ' + r.lt)));
const katInbound = () => {
  if (KINB) return KINB;
  KINB = new Map();
  for (const r of KROWS) for (const x of r.refs) { if (!KINB.has(x.id)) KINB.set(x.id, []); KINB.get(x.id).push(r.id); }
  return KINB;
};
function katMatches(q, filters = true) {
  const words = norm(q.trim()).split(/\s+/).filter(Boolean), idx = words.length ? katSearchIdx() : null;
  const f = filters ? katState : { min: 'alle', omr: 'alle', type: 'alle' };
  return KROWS.filter((r, i) => (f.min === 'alle' || r.m === f.min) && (f.omr === 'alle' || r.o === f.omr) && (f.type === 'alle' || r.type === f.type)
    && (!idx || words.every(w => idx[i].includes(w))));
}
function katLink(id, label) {
  const r = KIDX.get(id);
  if (!r) return el('span', { class: 'mono', title: 'Historisk eller ikke i kataloget over gældende dokumenter', text: label || id });
  return el('button', { class: 'lnk', type: 'button', onclick: () => katSelect(id), text: label || r.t });
}
function katSelect(id, { push = true } = {}) {
  if (!KIDX.has(id)) return;
  if (currentView() !== 'katalog') showView('katalog', false);
  katState.sel = id; renderKatDetail(id);
  document.querySelectorAll('#kat-table tr[data-id]').forEach(tr => tr.classList.toggle('sel', tr.dataset.id === id));
  setHash('kat-' + id, push);
}
function renderKatBars() {
  const box = $('#kat-bars'); box.replaceChildren();
  const cnt = {}; for (const r of KROWS) cnt[r.m] = (cnt[r.m] || 0) + 1;
  const rows = Object.entries(cnt).sort((a, b) => b[1] - a[1]); const max = rows[0][1];
  for (const [m, n] of rows) {
    box.append(el('button', { type: 'button', 'aria-pressed': katState.min === m, onclick: () => { katState.min = katState.min === m ? 'alle' : m; $('#kat-min').value = katState.min; katState.limit = 200; renderKatBars(); renderKatalog(); }, text: katMinName(m) }),
      el('div', { class: 'track' }, el('div', { class: 'fill', style: `width:${100 * n / max}%` })), el('span', { class: 'v', text: nf.format(n) }));
  }
}
function renderKatalog() {
  const rows = katMatches(katState.q);
  $('#kat-count').textContent = `${nf.format(rows.length)} af ${nf.format(KROWS.length)} gældende dokumenter`;
  const tb = $('#kat-table'); tb.replaceChildren();
  tb.append(el('thead', {}, el('tr', {}, el('th', { text: 'Udstedt' }), el('th', { text: 'Titel' }), el('th', { text: 'Type' }), el('th', { text: 'Ressort' }), el('th', { text: 'Retsområde' }))));
  const body = el('tbody');
  for (const r of rows.slice(0, katState.limit)) {
    body.append(el('tr', { 'data-id': r.id, class: r.id === katState.sel ? 'sel' : null },
      el('td', { class: 'mono', text: r.d }), el('td', { class: 't' }, el('button', { class: 'lnk', type: 'button', onclick: () => katSelect(r.id), text: r.t })),
      el('td', { text: KTYPE[r.type] || r.type }), el('td', {}, katMinName(r.m), ' ', certMark(r.mc)), el('td', { text: KOMR[r.o] || r.o })));
  }
  if (!rows.length) body.append(el('tr', {}, el('td', { colspan: 5, class: 'knote', text: 'Ingen dokumenter matcher. Ryd søgningen eller vælg “Alle” i filtrene.' })));
  tb.append(body);
  const more = $('#kat-more'); more.hidden = rows.length <= katState.limit;
  more.textContent = `Vis flere (${nf.format(Math.min(200, rows.length - katState.limit))} af ${nf.format(rows.length - katState.limit)} tilbage)`;
}
function katField(label, cert, ...kids) {
  return el('div', { class: 'field' }, el('div', { class: 'fh' }, el('span', { class: 'eyebrow', text: label }), cert ? certBadge(cert) : null), el('div', { class: 'fv' }, ...kids));
}
function renderKatDetail(id) {
  const box = $('#kat-detail'); box.replaceChildren();
  if (!id || !KIDX.has(id)) {
    const ex = ['lta-2019-1399', 'lta-2016-1178', 'lta-2024-572'].filter(i => KIDX.has(i));
    box.append(el('div', { class: 'empty' }, el('span', { class: 'eyebrow', text: 'Intet dokument valgt' }),
      el('p', { text: 'Vælg et dokument i listen. Detaljerne viser Lovtidende-nummer, udstedende ministerium, nuværende ressort, de love dokumentet nævner, hvem der nævner det, og EU-retsakter.' }),
      ex.length ? el('ul', {}, ex.map(i => el('li', {}, katLink(i)))) : null));
    return;
  }
  const r = KIDX.get(id), inb = katInbound().get(id) || [];
  const head = el('div', { class: 'head' }, el('div', { class: 'chips' }, el('span', { class: 'chip', text: KTYPE[r.type] || r.type }), el('span', { class: 'chip', text: `gældende pr. ${fmtDate(K.pr)}` })),
    el('h3', { class: 'title', text: r.t }), el('div', { class: 'mono idline', text: `${r.id} · ${r.lt}` }));
  const fields = el('div', { class: 'fields' },
    katField('Kilde', 'verificeret', extLink(katUrl(r), 'Retsinformation (ELI-XML)'), el('div', { class: 'knote', text: 'Lovtidende-nr., status og datoer er taget direkte fra bulk-høsten (Ansvar-Systems/danish-law-mcp).' })),
    katField('Udstedt', null, fmtDate(r.d)),
    katField('Udstedt af (dengang)', r.uc, r.u, el('div', { class: 'knote', text: 'Udledt af præfikset i Retsinformations DocumentId og ministertitler i teksten.' })),
    katField('Nuværende ressort', r.mc, NODES.has(r.m) ? nodeLink(r.m) : katMinName(r.m), el('div', { class: 'knote', text: 'Klassificeret (Haiku) ud fra titel, udsteder og ressortfordelingen efter kgl. res. 3. juni 2026.' })),
    katField('Retsområde', null, KOMR[r.o] || r.o));
  if (r.reg.length) fields.append(katField('I registry', null, el('div', { class: 'nodes' }, r.reg.filter(x => NODES.has(x)).map(x => nodeLink(x)))));
  if (r.am.length) fields.append(katField('Ændrer (ifølge titlen)', 'sandsynlig', el('ul', { style: 'margin:0;padding-left:18px' }, r.am.map(x => el('li', {}, katLink(x))))));
  if (r.refs.length) fields.append(katField('Nævner disse love', null, el('ul', { style: 'margin:0;padding-left:18px' }, r.refs.map(x => el('li', {}, katLink(x.id), ' ', certMark(x.c)))),
    el('div', { class: 'knote', text: '✓ = nævnt med nummer og dato; ≈ = nævnt ved navn (titelmatch). Hjemmel kan ikke udledes, fordi præamblen mangler i bulk-kilden.' })));
  if (inb.length) fields.append(katField(`Nævnt af ${plural(inb.length, 'gældende dokument', 'gældende dokumenter')}`, null,
    el('ul', { style: 'margin:0;padding-left:18px' }, inb.slice(0, 15).map(x => el('li', {}, katLink(x)))), inb.length > 15 ? el('div', { class: 'knote', text: `+${nf.format(inb.length - 15)} flere i katalog/kanter.jsonl` }) : null));
  if (r.eu.length) fields.append(katField('EU-retsakter i teksten', null, el('ul', { style: 'margin:0;padding-left:18px' }, r.eu.map(x => el('li', {}, NODES.has(x.id) ? nodeLink(x.id) : el('span', { class: 'mono', text: x.id }), x.imp ? el('span', { class: 'chip', style: 'margin-left:6px', text: 'gennemfører (sandsynlig)' }) : null)))));
  box.append(head, fields); box.scrollTop = 0;
}
function initKatalog() {
  $('#kat-lede').textContent = `Hele Lovtidende A fra Retsinformation: ${nf.format(K.n_total)} love, lovbekendtgørelser, bekendtgørelser og anordninger. Her vises de ${nf.format(KROWS.length)} gældende (status pr. ${fmtDate(K.pr)}); de ${nf.format(K.n_hist)} historiske står i katalog/retsinformation_lta.jsonl. Datasættet dækker udstedelser til og med ${fmtDate(K.max_udstedt)}. Ressort og retsområde er klassificeret og har højst sikkerheden sandsynlig. Klik på et ministerium for at filtrere.`;
  const opt = (sel, all, entries) => { sel.append(el('option', { value: 'alle', text: all }), ...entries.map(([k, l]) => el('option', { value: k, text: l }))); };
  const cnt = f => { const c = {}; for (const r of KROWS) c[r[f]] = (c[r[f]] || 0) + 1; return c; };
  const cm = cnt('m'), co = cnt('o'), ct = cnt('type');
  opt($('#kat-min'), 'Alle ministerier', Object.keys(cm).sort((a, b) => katMinName(a).localeCompare(katMinName(b), 'da')).map(k => [k, `${katMinName(k)} (${nf.format(cm[k])})`]));
  opt($('#kat-omr'), 'Alle retsområder', Object.keys(co).sort((a, b) => (KOMR[a] || a).localeCompare(KOMR[b] || b, 'da')).map(k => [k, `${KOMR[k] || k} (${nf.format(co[k])})`]));
  opt($('#kat-type'), 'Alle typer', Object.keys(ct).sort((a, b) => ct[b] - ct[a]).map(k => [k, `${KTYPE[k] || k} (${nf.format(ct[k])})`]));
  for (const [s, f] of [['#kat-min', 'min'], ['#kat-omr', 'omr'], ['#kat-type', 'type']]) $(s).onchange = ev => { katState[f] = ev.target.value; katState.limit = 200; if (f === 'min') renderKatBars(); renderKatalog(); };
  let t = null;
  $('#kat-q').addEventListener('input', ev => { clearTimeout(t); t = setTimeout(() => { katState.q = ev.target.value; katState.limit = 200; renderKatalog(); }, 120); });
  $('#kat-more').onclick = () => { katState.limit += 200; renderKatalog(); };
  if (katState.q) $('#kat-q').value = katState.q;
  renderKatBars(); renderKatalog(); renderKatDetail(katState.sel);
}

/* ---------- om ---------- */
function renderOm() {
  const p = D.prov, noUrl = D.nodes.filter(n => !safeUrl(n.url.vaerdi)).length;
  $('#om').append(
    el('h2', { text: 'Om kortet' }),
    el('p', { text: 'Kortet viser myndigheder, retsakter, klage- og tilsynsveje, EU-retsakter og dokumentkilder inden for byggeri, bolig, plan, energi, miljø, arbejdsmiljø, brand og el/gas/VVS. Det er bygget til et korpus, hvor søgning skal kunne følge hjemmelskæder fra lov til bekendtgørelse, vejledning og praksis. Der er ikke hentet dokumenter.' }),
    el('h3', { text: 'Sådan er det lavet' }),
    el('ol', {},
      el('li', { text: 'To uafhængige kortlægninger af regering og ressort blev afstemt til en fælles baseline med faste id’er.' }),
      el('li', { text: '13 domæner blev researchet hver for sig. Derefter fik hvert domæne en adversariel verifikator med reelt søgebudget, som rettede, nedgraderede eller fjernede påstande.' }),
      el('li', { text: `Kanoniske URL’er, ELI-, Lovtidende- og CELEX-numre samt adgangsform blev eftersøgt for 387 noder. ${nf.format(noUrl)} noder har stadig ingen fundet kanonisk URL.` }),
      el('li', { text: 'Seks kritikere, en pr. ministerområde, ledte efter manglende instanser, love, klageveje og EU-gennemførelse. De tilføjede noder har ikke et fagdomæne, men er mærket ”tilføjet af kritiker”. 23 kanter blev bestridt, gennemgået manuelt og fjernet eller mærket som historiske eller bestridte.' }),
      el('li', { text: 'Alle påstande, der stadig var sandsynlige eller ukendte, blev efterprøvet node for node i 75 batches. Generelle forhold blev belagt én gang pr. nodeklasse med officielle kilder: ophavsretslovens § 9 for love og bekendtgørelser, EU’s genbrugsregler, og opdatering og adgang på Retsinformation og EUR-Lex.' }),
      el('li', { text: `Alle kilde-URL’er er tjekket mod de ${nf.format(p.urls)} URL’er, der faktisk optrådte i resultaterne af ${nf.format(p.results)} søgninger. ${nf.format(p.fjernet)} af ${nf.format(p.kilder)} kilder optrådte ikke og er fjernet.` })),
    el('h3', { text: 'Sikkerhed' }),
    el('ul', {},
      el('li', {}, certBadge('verificeret'), ' Påstanden fremgår direkte af et søgeresultat fra en officiel eller primær kilde (fx retsinformation.dk, ft.dk, eur-lex eller myndighedens eget domæne) eller af to uafhængige troværdige sekundærkilder, og afspejler tilstanden pr. 28. oktober 2026.'),
      el('li', {}, certBadge('sandsynlig'), ' Påstanden bygger på én sekundærkilde, en officiel kilde der kan være forældet, eller en faglig slutning.'),
      el('li', {}, certBadge('ukendt'), ' Der er ikke fundet evidens.')),
    el('p', {}, 'Kanter mærket ', el('span', { class: 'chip bestridt', text: 'bestridt' }), ' er rejst af en kritiker og ikke afgjort. Kanter mærket ', el('span', { class: 'chip hist', text: 'historisk' }), ' gjaldt tidligere, men ikke pr. 28. oktober 2026.'),
    el('h3', { text: 'Kanttyper' }),
    el('div', { class: 'tablewrap' }, el('table', {}, el('thead', {}, el('tr', {}, el('th', { text: 'Kant' }), el('th', { text: 'Retning' }), el('th', { text: 'Antal' }))),
      el('tbody', {}, ETYPES.map(([k, l, h]) => el('tr', {}, el('td', { text: l }), el('td', { text: h }), el('td', { class: 'num', text: EDGES.filter(e => e.type === k).length })))))),
    el('h3', { text: 'Begrænsninger' }),
    el('ul', {},
      el('li', { text: 'Siderne er ikke åbnet direkte, fordi netværkspolitikken under kortlægningen blokerede retsinformation.dk, eur-lex.europa.eu og ministeriernes sider. Al evidens er søgeresultater: titel, URL og uddrag.' }),
      el('li', { text: 'URL’er er aldrig konstrueret. Står der ”ikke fundet”, er siden ikke set i et søgeresultat, også når adressen kunne forudsiges ud fra ELI-mønsteret.' }),
      el('li', { text: 'Ressortforhold ændrer sig ofte. Nedlagte og omdøbte instanser er tegnet med stiplet kant og har status nedlagt eller omdøbt. Perioden står i Note eller i ”Tidligere navne”, hvor den er kendt.' }),
      el('li', { text: 'Standarder og branchevejledninger er kun med som metadata. Kommuner og regioner er samlet i to noder.' })));
  if (D.konflikter && D.konflikter.length) $('#om').append(el('h3', { text: 'Uafklarede konflikter fra ressort-afstemningen' }), el('ul', {}, D.konflikter.map(k => el('li', { text: k }))));
}

/* ---------- routing ---------- */
const VIEWS = ['netvaerk', 'kaeder', 'katalog', 'ressort', 'kilder', 'huller', 'om'];
const rendered = new Set();
const currentView = () => VIEWS.find(v => !$('#view-' + v).hidden) || 'netvaerk';
let routing = false;
function setHash(h, push = true) {
  if (routing || location.hash.slice(1) === h) return;
  try { push ? history.pushState(null, '', '#' + h) : history.replaceState(null, '', '#' + h); } catch { /* sandboxed */ }
}
function showView(v, updateHash = true) {
  for (const x of VIEWS) $('#view-' + x).hidden = x !== v;
  document.querySelectorAll('nav.tabs a').forEach(a => { if (a.dataset.view === v) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
  if (!rendered.has(v)) {
    rendered.add(v);
    if (v === 'katalog') initKatalog(); else if (v === 'ressort') renderRessort(); else if (v === 'kilder') initKilder(); else if (v === 'huller') initHuller(); else if (v === 'om') renderOm();
    else if (v === 'kaeder') { initChain(); setChainRoot(chainRoot || 'lov-byggeloven', false); }
  }
  if (v === 'netvaerk' && cy) cy.resize();
  if (v === 'kaeder') fitChain();
  if (updateHash) setHash(v === 'kaeder' && chainRoot ? 'kaede-' + chainRoot : v === 'katalog' && katState.sel ? 'kat-' + katState.sel : v);
}
function route() {
  routing = true;
  try {
    const h = decodeURIComponent(location.hash.slice(1));
    if (h.startsWith('node-') && NODES.has(h.slice(5))) { showView('netvaerk', false); selectNode(h.slice(5), { push: false }); return; }
    if (h.startsWith('kaede-') && NODES.has(h.slice(6)) && CHAIN_TYPES.has(NODES.get(h.slice(6)).type)) {
      chainRoot = h.slice(6); const first = !rendered.has('kaeder'); showView('kaeder', false); if (!first) setChainRoot(chainRoot, false); return;
    }
    if (h.startsWith('kat-') && KIDX.has(h.slice(4))) { katState.sel = h.slice(4); const first = !rendered.has('katalog'); showView('katalog', false); if (!first) katSelect(katState.sel, { push: false }); return; }
    if (h === 'netvaerk' && state.selected) { state.selected = null; highlight(null); renderDetail(null); }
    showView(VIEWS.includes(h) ? h : 'netvaerk', false);
  } finally { routing = false; }
}
document.querySelectorAll('nav.tabs a').forEach(a => a.addEventListener('click', ev => { ev.preventDefault(); showView(a.dataset.view); window.scrollTo(0, 0); }));
window.addEventListener('hashchange', route);
window.addEventListener('popstate', route);

/* ---------- theme changes ---------- */
function restyle() {
  const t = tokens();
  const recolor = c => c.nodes().forEach(x => { const n = NODES.get(x.id()); if (n) x.data('color', t[catOf(n).slot]); else x.data('color', t.bg); });
  if (cy) { cy.style(cyStyle(t)); recolor(cy); }
  if (cy2) { cy2.style(cyStyle(t, true)); recolor(cy2); }
}
try { matchMedia('(prefers-color-scheme: dark)').addEventListener('change', restyle); } catch { /* old browsers */ }
new MutationObserver(restyle).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

/* ---------- boot ---------- */
renderSummary(); buildFilters(); renderDetail(null); initSearch();
if (narrow()) $('#filters').open = false;
if (window.cytoscape) initNetwork(); else $('#hint').textContent = 'Grafbiblioteket kunne ikke indlæses. Lister og tabeller virker stadig.';
route();
})();

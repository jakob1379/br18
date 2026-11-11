const cytoscape = require('cytoscape'); const fcose = require('cytoscape-fcose'); cytoscape.use(fcose);
const fs = require('fs');
const d = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const ids = new Set(d.nodes.map(n => n.id));
const els = d.nodes.map(n => ({ data: { id: n.id, w: n.type === 'ministerium' ? 3 : 1 } }))
  .concat(d.edges.filter(e => ids.has(e[0]) && ids.has(e[1])).map((e, i) => ({ data: { id: 'e' + i, source: e[0], target: e[1], t: e[2] } })));
const cy = cytoscape({ headless: true, elements: els, styleEnabled: true, style: [{ selector: 'node', style: { width: 18, height: 18 } }, { selector: 'node[w > 1]', style: { width: 46, height: 46 } }] });
const lay = cy.layout({ name: 'fcose', quality: 'proof', randomize: true, animate: false, nodeSeparation: 90, idealEdgeLength: e => e.data('t') === 'ressortansvar' ? 70 : 110,
  nodeRepulsion: n => n.data('w') > 1 ? 90000 : 9000, gravity: 0.3, gravityRange: 3.0, numIter: 5000, packComponents: true, tile: true, seed: 7 });
lay.run();
const pos = {}; cy.nodes().forEach(n => { const p = n.position(); pos[n.id()] = [Math.round(p.x), Math.round(p.y)]; });
fs.writeFileSync(process.argv[3], JSON.stringify(pos));
console.log('positions', Object.keys(pos).length);

// Figma build: one review-table section from generated data (CLAUDE.md page style).
// Prepend `const PAGE = '...'; const T = {...};` where T comes from a scripts/*.py emitter, e.g.
//   python3 scripts/figma_system_colors.py <section-id>   (prints the JS for one section)
// T = { name: 'NN · Title', title, intro, columns: [{name, w}], rows: [ [cell...] | {group: 'text'} ] }
// cell: 'text' | {t: 'text', sw: '#rrggbb' | null, b: bold, v: 'Collection name::variable/name' | 'key:<library variable key>'} | {chip: 'Core' | 'Core alias' | 'Core, per-platform value' | 'iOS only' | 'Android only' | 'Differs' | 'Token'}
//       | {clone: [sectionName, rowName, cellName, pageName?], alt: 'text'}  copies that cell from another section (this page, or pageName,
//         which the emitter must load first), e.g. glyph previews; alt if missing
//       v binds the swatch fill to that variable (DEC-12: linked to tokens); sw is only the fallback color shown before binding.
// Re-running replaces only the section with the same name (rule 4). Sections stack downward in creation order.
const CHIPS = { 'Core': ['#e6f4ea', '#14532d'], 'Core alias': ['#e6f4ea', '#14532d'], 'Core, per-platform value': ['#fff4d6', '#6b4500'],
  'iOS only': ['#e3eefc', '#0b3d7a'], 'Android only': ['#efe7fb', '#43217a'], 'Differs': ['#fde8e8', '#8a1c1c'], 'Token': ['#f1f1f1', '#333333'] };
const hex = (h) => { h = h.replace('#', ''); return { r: parseInt(h.slice(0, 2), 16) / 255, g: parseInt(h.slice(2, 4), 16) / 255, b: parseInt(h.slice(4, 6), 16) / 255 }; };
const solid = (h, o) => ({ type: 'SOLID', color: hex(h), opacity: o ?? 1 });
await Promise.all(['Regular', 'Bold', 'SemiBold'].map(style => figma.loadFontAsync({ family: 'Open Sans', style })));
function text(chars, size, style = 'Regular', color = '#1a1a1a', lh) {
  const t = figma.createText(); t.fontName = { family: 'Open Sans', style }; t.fontSize = size; t.characters = String(chars);
  t.fills = [solid(color)]; if (lh) t.lineHeight = { value: lh, unit: 'PIXELS' }; return t;
}
function frame(name, dir = 'VERTICAL', gap = 0) {
  const f = figma.createFrame(); f.name = name; f.layoutMode = dir; f.itemSpacing = gap;
  f.primaryAxisSizingMode = 'AUTO'; f.counterAxisSizingMode = 'AUTO'; f.fills = []; return f;
}
const _tables = {};
function cloneSource([sec, row, cell, pg]) {
  if (!(sec in _tables)) { const P = pg ? figma.root.children.find(p => p.name === pg) : page; const s = P && P.children.find(n => n.name === sec); const t = s && ('children' in s) ? (s.type === 'SECTION' ? s.children[0] : s) : null; _tables[sec] = t; }
  const t = _tables[sec]; const r = t && t.children.find(n => n.name === row); return r ? r.children.find(n => n.name === cell) || null : null;
}
function cellNode(c, w) {
  const f = frame('cell', 'HORIZONTAL', 8); f.counterAxisAlignItems = 'CENTER';
  f.primaryAxisSizingMode = 'FIXED'; f.resize(w, 10); f.counterAxisSizingMode = 'AUTO';
  if (c && typeof c === 'object' && c.clone) { const src = cloneSource(c.clone); if (src) { f.appendChild(src.clone()); return f; } c = c.alt ?? '—'; }
  if (c && typeof c === 'object' && c.chip) {
    const [bg, fg] = CHIPS[c.chip] || CHIPS['Token']; const ch = frame('chip', 'HORIZONTAL'); ch.paddingLeft = ch.paddingRight = 8; ch.paddingTop = ch.paddingBottom = 3;
    ch.cornerRadius = 4; ch.fills = [solid(bg)]; ch.appendChild(text(c.chip, 11, 'SemiBold', fg)); f.appendChild(ch); return f;
  }
  const o = (c && typeof c === 'object') ? c : { t: c ?? '' };
  if (o.sw !== undefined) {
    const s = figma.createRectangle(); s.name = 'swatch'; s.resize(20, 20); s.cornerRadius = 4;
    if (o.sw) { const h = o.sw.replace('#', ''); s.fills = [solid('#' + h.slice(0, 6), h.length === 8 ? parseInt(h.slice(6), 16) / 255 : 1)]; }
    else { s.fills = []; s.dashPattern = [3, 2]; }
    if (o.v) { if (!s.fills.length) s.fills = [solid('#000000')]; s.fills = [figma.variables.setBoundVariableForPaint(s.fills[0], 'color', _vars[o.v])]; s.name = 'swatch · ' + _vars[o.v].name; }
    s.strokes = [solid('#cccccc')]; s.strokeWeight = 1; f.appendChild(s);
  }
  const t = text(o.t, 12, o.b ? 'SemiBold' : 'Regular', '#1a1a1a', 18); f.appendChild(t);
  t.layoutGrow = 1; t.textAutoResize = 'HEIGHT';
  return f;
}
const _vars = {};
for (const r of T.rows) if (Array.isArray(r)) for (const c of r) if (c && typeof c === 'object' && c.v) _vars[c.v] = null;
if (Object.keys(_vars).length) {
  const cols = await figma.variables.getLocalVariableCollectionsAsync();
  for (const k of Object.keys(_vars)) {
    if (k.startsWith('key:')) {
      _vars[k] = await Promise.race([figma.variables.importVariableByKeyAsync(k.slice(4)),
        new Promise((_, rej) => setTimeout(() => rej(new Error('Library variable import timed out: accept Core library updates in this file')), 15000))]);
      continue;
    }
    const [cn, vn] = k.split('::'); const col = cols.find(c => c.name === cn);
    if (col) for (const id of col.variableIds) { const v = await figma.variables.getVariableByIdAsync(id); if (v.name === vn) { _vars[k] = v; break; } }
    if (!_vars[k]) throw new Error('Variable not found: ' + k);
  }
}
let page = figma.root.children.find(p => p.name === PAGE);
if (!page) { page = figma.createPage(); page.name = PAGE; }
await page.loadAsync();
const old = page.children.find(n => n.name === T.name); const keepY = old ? old.y : null; if (old) old.remove();
const W = T.columns.reduce((a, c) => a + c.w, 0);
const root = frame(T.name, 'VERTICAL', 0); root.fills = [solid('#ffffff')];
root.paddingLeft = root.paddingRight = root.paddingTop = root.paddingBottom = 64;
root.appendChild(text(T.title, 32, 'Bold', '#1a1a1a', 44));
if (T.intro) { const s = frame('spacer'); s.resize(1, 12); root.appendChild(s); const i = text(T.intro, 14, 'Regular', '#333333', 22); i.resize(W, i.height); i.textAutoResize = 'HEIGHT'; root.appendChild(i); }
const gap = frame('spacer'); gap.resize(1, 24); root.appendChild(gap);
const head = frame('Header', 'HORIZONTAL'); head.paddingTop = head.paddingBottom = 8;
head.strokes = [solid('#1a1a1a')]; head.strokeBottomWeight = 2; head.strokeTopWeight = head.strokeLeftWeight = head.strokeRightWeight = 0;
for (const c of T.columns) { const cf = cellNode({ t: c.name, b: true }, c.w); head.appendChild(cf); }
root.appendChild(head);
for (const r of T.rows) {
  if (r && r.group) {
    const g = frame('Group', 'HORIZONTAL'); g.paddingLeft = 8; g.paddingTop = g.paddingBottom = 8; g.fills = [solid('#1a1a1a')];
    g.primaryAxisSizingMode = 'FIXED'; g.resize(W, 10); g.counterAxisSizingMode = 'AUTO'; g.appendChild(text(r.group, 13, 'SemiBold', '#ffffff')); root.appendChild(g); continue;
  }
  const row = frame('Row', 'HORIZONTAL'); row.paddingTop = row.paddingBottom = 8; row.counterAxisAlignItems = 'CENTER';
  row.strokes = [solid('#e6e6e6')]; row.strokeBottomWeight = 1; row.strokeTopWeight = row.strokeLeftWeight = row.strokeRightWeight = 0;
  r.forEach((c, i) => row.appendChild(cellNode(c, T.columns[i].w)));
  root.appendChild(row);
}
page.appendChild(root);
const others = page.children.filter(n => n !== root);
root.x = 0; root.y = keepY ?? (others.length ? Math.max(...others.map(n => n.y + n.height)) + 80 : 0);
return { id: root.id, rows: T.rows.length, w: root.width, h: root.height };

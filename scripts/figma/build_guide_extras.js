// Figma build (Android file): style-guide extras (DEC-12, DEC-16), from data/guide-extras.json via scripts/figma_guide_extras.py.
// Prepend `const MODE = 'vars' | 'ads'; const D = {...};`
//   vars: adds / updates the ad slot sizes in "Components · Android" (ad/<size>/width|height, FLOAT) and the PageSuite eEdition colors
//         in "System colors · Android" (eedition-<id>, COLOR). Never deletes (rule 4).
//   ads:  section D.name on page D.page: one card per ad size, the slot frame bound to its width / height variables and filled with
//         the Core library's ad/background (imported by key). Re-running replaces only this section.
const hex = (h) => { h = h.replace('#', ''); return { r: parseInt(h.slice(0, 2), 16) / 255, g: parseInt(h.slice(2, 4), 16) / 255, b: parseInt(h.slice(4, 6), 16) / 255 }; };
const solid = (h) => ({ type: 'SOLID', color: hex(h) });
const cols = await figma.variables.getLocalVariableCollectionsAsync();
async function byName(colName) {
  const col = cols.find(c => c.name === colName); if (!col) throw new Error('Missing collection ' + colName);
  const m = {}; for (const id of col.variableIds) { const v = await figma.variables.getVariableByIdAsync(id); m[v.name] = v; }
  return { col, m };
}
if (MODE === 'vars') {
  const comp = await byName('Components · Android'), sys = await byName('System colors · Android');
  let made = 0, updated = 0;
  for (const f of D.floats) {
    let v = comp.m[f.name]; if (!v) { v = figma.variables.createVariable(f.name, comp.col, 'FLOAT'); made++; } else updated++;
    v.setValueForMode(comp.col.modes[0].modeId, f.value); v.scopes = ['WIDTH_HEIGHT']; v.description = f.desc;
  }
  for (const c of D.colors) {
    let v = sys.m[c.name]; if (!v) { v = figma.variables.createVariable(c.name, sys.col, 'COLOR'); made++; } else updated++;
    v.setValueForMode(sys.col.modes[0].modeId, { ...hex(c.value), a: 1 }); v.scopes = ['ALL_FILLS', 'STROKE_COLOR']; v.description = c.desc;
  }
  return { made, updated, components: comp.col.variableIds.length, system: sys.col.variableIds.length };
}
// ---- ads
await Promise.all(['Regular', 'Bold', 'SemiBold'].map(style => figma.loadFontAsync({ family: 'Open Sans', style })));
const text = (chars, size, style = 'Regular', color = '#1a1a1a', lh) => {
  const t = figma.createText(); t.fontName = { family: 'Open Sans', style }; t.fontSize = size; t.characters = String(chars);
  t.fills = [solid(color)]; if (lh) t.lineHeight = { value: lh, unit: 'PIXELS' }; return t;
};
const frame = (name, dir = 'VERTICAL', gap = 0) => { const f = figma.createFrame(); f.name = name; f.layoutMode = dir; f.itemSpacing = gap; f.primaryAxisSizingMode = 'AUTO'; f.counterAxisSizingMode = 'AUTO'; f.fills = []; return f; };
const comp = await byName('Components · Android');
const bg = await Promise.race([figma.variables.importVariableByKeyAsync(D.bgKey),
  new Promise((_, rej) => setTimeout(() => rej(new Error('Core ad/background import timed out: accept Core library updates in this file')), 15000))]);
let page = figma.root.children.find(p => p.name === D.page);
if (!page) { page = figma.createPage(); page.name = D.page; }
await page.loadAsync();
const old = page.children.find(n => n.name === D.name); const keepY = old ? old.y : null; if (old) old.remove();
const root = frame(D.name, 'VERTICAL', 0); root.fills = [solid('#ffffff')];
root.paddingLeft = root.paddingRight = root.paddingTop = root.paddingBottom = 64;
root.appendChild(text(D.title, 32, 'Bold', '#1a1a1a', 44));
const sp = (h) => { const s = frame('spacer'); s.resize(1, h); return s; };
root.appendChild(sp(12));
const intro = text(D.intro, 14, 'Regular', '#333333', 22); intro.resize(D.width, intro.height); intro.textAutoResize = 'HEIGHT'; root.appendChild(intro);
root.appendChild(sp(32));
const row = frame('Slots', 'HORIZONTAL', 48); row.counterAxisAlignItems = 'MIN';
for (const s of D.slots) {
  const card = frame('Card · ' + s.id, 'VERTICAL', 12);
  const slot = figma.createFrame(); slot.name = 'Ad slot · ' + s.id; slot.resize(s.width, s.height);
  slot.fills = [figma.variables.setBoundVariableForPaint(solid('#ffffff'), 'color', bg)];
  slot.strokes = [solid('#999999')]; slot.strokeWeight = 1; slot.dashPattern = [4, 3];
  slot.setBoundVariable('width', comp.m[`ad/${s.id}/width`]); slot.setBoundVariable('height', comp.m[`ad/${s.id}/height`]);
  card.appendChild(slot);
  card.appendChild(text(`${s.id} · ${s.width} × ${s.height} dp`, 13, 'SemiBold'));
  const u = text(s.uses, 12, 'Regular', '#333333', 18); u.resize(Math.max(240, Math.min(s.width, 320)), u.height); u.textAutoResize = 'HEIGHT'; card.appendChild(u);
  card.appendChild(text(`Tokens: component.android.ad.${s.id}.width / .height`, 11, 'Regular', '#666666', 16));
  row.appendChild(card);
}
root.appendChild(row);
root.appendChild(sp(32));
for (const r of D.rules) { const t = text('• ' + r, 13, 'Regular', '#333333', 20); t.resize(D.width, t.height); t.textAutoResize = 'HEIGHT'; root.appendChild(t); }
page.appendChild(root);
const others = page.children.filter(n => n !== root);
root.x = 0; root.y = keepY ?? (others.length ? Math.max(...others.map(n => n.y + n.height)) + 80 : 0);
return { id: root.id, w: root.width, h: root.height };

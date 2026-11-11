// Figma build (iOS file): Components · Controls › 02 · Checkbox (as shipped). DEC-09: built as shipped, from images.
// Prepend `const DATA = {...};` (python3 scripts/figma_ios_checkbox.py build).
// Images go up first, one per call (python3 scripts/figma_ios_checkbox.py upload <file>): each call checks byte length and
// FNV-1a hash against the local file, keeps the image in a temporary frame and its hash in root plugin data. This build
// uses those hashes and removes the temporary frame.
// One component set: Set (Generic + 7 market sets) × State (Checked / Unchecked). Each variant is the 30 × 30 pt control
// (width and height bound to Components · iOS › checkbox/size) with the shipped @3x image, 17 × 18 pt, centered
// (placement unconfirmed: MISSING-ASSETS 5.7). Re-running replaces only this section (rule 4).
const PAGE = 'Components · Controls', SECTION = '02 · Checkbox (as shipped)';
const hex = (h) => { h = h.replace('#', ''); return { r: parseInt(h.slice(0, 2), 16) / 255, g: parseInt(h.slice(2, 4), 16) / 255, b: parseInt(h.slice(4, 6), 16) / 255 }; };
const solid = (h) => ({ type: 'SOLID', color: hex(h) });
await Promise.all(['Regular', 'Bold', 'SemiBold'].map(style => figma.loadFontAsync({ family: 'Open Sans', style })));
function text(chars, size, style = 'Regular', color = '#1a1a1a', lh) { const t = figma.createText(); t.fontName = { family: 'Open Sans', style }; t.fontSize = size; t.characters = String(chars); t.fills = [solid(color)]; if (lh) t.lineHeight = { value: lh, unit: 'PIXELS' }; return t; }
function frame(name, dir = 'VERTICAL', gap = 0) { const f = figma.createFrame(); f.name = name; f.layoutMode = dir; f.itemSpacing = gap; f.primaryAxisSizingMode = 'AUTO'; f.counterAxisSizingMode = 'AUTO'; f.fills = []; return f; }
const sizeVar = (await figma.variables.getLocalVariablesAsync('FLOAT')).find(v => v.name === 'checkbox/size');
const KEY = 'mng-ios-checkbox-images', TEMP = '_checkbox images (temporary)';
const hash = JSON.parse(figma.root.getPluginData(KEY) || '{}');
const needed = [...DATA.sets.flatMap(s => [s.checked.file, s.unchecked.file]), ...DATA.not_mapped.map(e => e.file)];
const missing = needed.filter(f => !hash[f]); if (missing.length) return { error: 'images not uploaded yet', missing };
const S = DATA.control_size_pt, IW = 17, IH = 18;
function imageRect(file) { const r = figma.createRectangle(); r.name = file; r.resize(IW, IH); r.fills = [{ type: 'IMAGE', imageHash: hash[file], scaleMode: 'FILL' }]; return r; }

const page = figma.root.children.find(p => p.name === PAGE); await page.loadAsync();
page.children.filter(n => n.name === SECTION).forEach(n => n.remove());
const others = page.children.filter(n => n.name !== TEMP); const y0 = others.length ? Math.max(...others.map(n => n.y + n.height)) + 200 : 0;

const comps = [];
for (const s of DATA.sets) for (const state of ['Checked', 'Unchecked']) {
  const file = state === 'Checked' ? s.checked.file : s.unchecked.file;
  const c = figma.createComponent(); c.name = `Set=${s.set}, State=${state}`; c.resize(S, S); c.fills = []; c.clipsContent = false;
  if (sizeVar) { c.setBoundVariable('width', sizeVar); c.setBoundVariable('height', sizeVar); }
  const r = imageRect(file); c.appendChild(r); r.x = (S - IW) / 2; r.y = (S - IH) / 2; r.constraints = { horizontal: 'CENTER', vertical: 'CENTER' };
  c.description = `${s.set} set, ${state}: ${file} (TroncKit Assets.xcassets @3x, 51 × 54 px). Markets: ${s.markets.join(', ')}.`;
  page.appendChild(c); comps.push(c);
}
const set = figma.combineAsVariants(comps, page); set.name = 'Checkbox · iOS (as shipped)';
set.description = 'iOS Your News topic checkbox as shipped: an image per market set, not a tinted control. 30 × 30 pt control (checkbox/size), image 17 × 18 pt centered (MISSING-ASSETS 5.7). Source: data/ios-checkbox.json · docs/components/CHECKBOX-IOS.md.';
set.fills = [solid('#ffffff')]; set.strokes = [solid('#e6e6e6')]; set.strokeWeight = 1; set.cornerRadius = 8;
const STEP = 70, PAD = 32;
set.children.forEach(c => { const [setName, state] = c.name.split(', ').map(x => x.split('=')[1]); const i = DATA.sets.findIndex(s => s.set === setName); c.x = PAD + i * STEP; c.y = PAD + (state === 'Checked' ? 0 : STEP); });
set.resizeWithoutConstraints(PAD * 2 + (DATA.sets.length - 1) * STEP + S, PAD * 2 + STEP + S);

// documentation frame around the component set
const root = frame(SECTION, 'VERTICAL', 24); root.fills = [solid('#ffffff')]; root.paddingLeft = root.paddingRight = root.paddingTop = root.paddingBottom = 64;
root.appendChild(text('Checkbox · iOS (as shipped)', 32, 'Bold', '#1a1a1a', 44));
const intro = text(`iOS draws the Your News topic checkbox with images: ${DATA.sets.length} sets (generic + market sets), checked and unchecked. Control ${S} × ${S} pt, bound to Components · iOS › checkbox/size; below the 44 pt touch target. Images 51 × 54 px @3x = 17 × 18 pt, ${DATA.image_placement}. Android draws a tinted checkbox instead (Components · Controls in the Android file, DEC-14). Source: ${DATA.source} · data/ios-checkbox.json · docs/components/CHECKBOX-IOS.md.`, 14, 'Regular', '#333333', 22);
intro.resize(1200, intro.height); intro.textAutoResize = 'HEIGHT'; root.appendChild(intro);
const labels = frame('Set labels', 'HORIZONTAL', 0); labels.paddingLeft = PAD;
DATA.sets.forEach(s => { const f = frame(s.set, 'VERTICAL'); f.primaryAxisSizingMode = 'FIXED'; f.counterAxisSizingMode = 'FIXED'; f.resize(STEP, 20); f.appendChild(text(s.set, 11, 'SemiBold', '#333333')); labels.appendChild(f); });
root.appendChild(labels);
const holder = frame('Component set', 'HORIZONTAL', 16); holder.counterAxisAlignItems = 'CENTER'; root.appendChild(holder);
const states = frame('State labels', 'VERTICAL', STEP - 16); states.appendChild(text('Checked', 11, 'SemiBold', '#333333')); states.appendChild(text('Unchecked', 11, 'SemiBold', '#333333'));
holder.appendChild(set); holder.appendChild(states);
// markets per set
const table = frame('Markets per set', 'VERTICAL', 0);
const row = (a, b, bold) => { const r = frame('Row', 'HORIZONTAL', 16); r.paddingTop = r.paddingBottom = 8; r.strokes = [solid('#e6e6e6')]; r.strokeBottomWeight = 1; r.strokeTopWeight = r.strokeLeftWeight = r.strokeRightWeight = 0;
  const x = text(a, 12, bold ? 'SemiBold' : 'Regular'); x.resize(140, x.height); x.textAutoResize = 'HEIGHT'; const y = text(b, 12, bold ? 'SemiBold' : 'Regular'); y.resize(1040, y.height); y.textAutoResize = 'HEIGHT'; r.appendChild(x); r.appendChild(y); return r; };
table.appendChild(row('Set', 'Markets', true));
DATA.sets.forEach(s => table.appendChild(row(`${s.set} (${s.markets.length})`, s.markets.join(', '))));
DATA.not_mapped.forEach(e => table.appendChild(row(e.file, e.note + ' (MISSING-ASSETS 5.7)')));
root.appendChild(table);
const extra = frame('Not mapped', 'HORIZONTAL', 8); extra.counterAxisAlignItems = 'CENTER';
DATA.not_mapped.forEach(e => { extra.appendChild(imageRect(e.file)); extra.appendChild(text(`${e.file}: in the asset catalog, use not documented`, 11, 'Regular', '#555555')); });
root.appendChild(extra);
page.children.filter(n => n.name === TEMP).forEach(n => n.remove());
const sec = figma.createSection(); sec.name = SECTION; page.appendChild(sec); sec.appendChild(root);
root.x = 80; root.y = 80; sec.resizeWithoutConstraints(root.width + 160, root.height + 160); sec.x = 0; sec.y = y0;
return { section: sec.id, set: set.id, variants: set.children.length, boundSize: !!sizeVar, images: Object.keys(hash).length, generic: DATA.sets[0].markets.length };

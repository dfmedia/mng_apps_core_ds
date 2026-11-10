// Figma build: system color variables (DEC-16), from data/system-tokens.json (scripts/build_system_tokens.py).
// Run through the Desktop Bridge (figma_execute) with these prepended:
//   const FILE = 'core' | 'ios' | 'android';
//   const DATA = [...tokens from data/system-tokens.json with collection === 'core' (Core file) or === FILE (platform files)];
//   const THEME_KEYS = { action: '<key>', navbar: '<key>', navtext: '<key>' };   // platform files only: Core "Brand theme" variable keys
// Core file:      collection "System colors", modes iOS / Android, one variable per approved pair (same value in both modes, or per platform).
// Platform files: collection "System colors · iOS" / "· Android", one mode; majority values; brand-following colors alias the
//                 Core Brand theme variable (so they take each market's color from the frame's Brand theme mode).
// Re-running updates values of the variables this script created and adds missing ones; it never deletes (rule 4).
const hex = (h) => { h = h.replace('#', ''); return { r: parseInt(h.slice(0, 2), 16) / 255, g: parseInt(h.slice(2, 4), 16) / 255, b: parseInt(h.slice(4, 6), 16) / 255, a: h.length === 8 ? parseInt(h.slice(6, 8), 16) / 255 : 1 }; };
const NAME = { core: 'System colors', ios: 'System colors · iOS', android: 'System colors · Android' }[FILE];
const cols = await figma.variables.getLocalVariableCollectionsAsync();
let col = cols.find(c => c.name === NAME);
if (!col) col = figma.variables.createVariableCollection(NAME);
let modes = {};
if (FILE === 'core') {
  if (col.modes.length === 1 && col.modes[0].name !== 'iOS') col.renameMode(col.modes[0].modeId, 'iOS');
  if (!col.modes.find(m => m.name === 'Android')) col.addMode('Android');
  modes = { ios: col.modes.find(m => m.name === 'iOS').modeId, android: col.modes.find(m => m.name === 'Android').modeId };
} else {
  if (col.modes[0].name !== 'Value') col.renameMode(col.modes[0].modeId, 'Value');
  modes = { value: col.modes[0].modeId };
}
const existing = {};
for (const id of col.variableIds) { const v = await figma.variables.getVariableByIdAsync(id); existing[v.name] = v; }
const theme = {};
if (FILE !== 'core') for (const [role, key] of Object.entries(THEME_KEYS)) {
  theme[role] = await Promise.race([figma.variables.importVariableByKeyAsync(key), new Promise((_, r) => setTimeout(() => r(new Error('Brand theme import timed out: accept Core library updates / bring the file to the front')), 15000))]);
}
let made = 0, updated = 0;
for (const t of DATA) {
  let v = existing[t.name];
  if (!v) { v = figma.variables.createVariable(t.name, col, 'COLOR'); made++; } else updated++;
  v.scopes = ['ALL_FILLS', 'STROKE_COLOR'];
  if (FILE === 'core') {
    v.setValueForMode(modes.ios, hex(t.values.ios)); v.setValueForMode(modes.android, hex(t.values.android));
    v.description = `${t.what}. iOS ${t.values.ios}${t.uikit ? ' (UIKit ' + t.uikit + ', not set by the app)' : ''} (${t.sources.ios}); Android ${t.values.android} (${t.sources.android}). ${t.same ? 'Same on both apps.' : 'Core, value per platform.'} DEC-16`;
  } else if (t.follows) {
    v.setValueForMode(modes.value, { type: 'VARIABLE_ALIAS', id: theme[t.follows].id });
    v.description = `${t.source}: follows the market's ${t.follows} (Core Brand theme) in ${t.markets} of 77 markets; ${t.exceptions} exceptions documented only (DEC-16)`;
  } else {
    v.setValueForMode(modes.value, hex(t.value));
    v.description = `${t.source}: ${t.kind === 'fixed' ? 'same in all 77 markets' : t.markets + ' of 77 markets; ' + t.exceptions + ' exceptions documented only'}${t.uikit ? '; not set by the app, UIKit ' + t.uikit : ''} (DEC-16)`;
  }
}
return { collection: NAME, made, updated, total: col.variableIds.length };

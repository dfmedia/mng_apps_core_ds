// Figma build: header band (iOS) / status bar (Android) exception samples, DEC-15.
// Data: data/shell-colors.json `role_exceptions` (scripts/build_shell_colors.py). Run through the Desktop Bridge
// (figma_execute) in the platform file, with PLATFORM and DATA prepended by scripts/figma_role_exceptions.py ios|android.
// Re-running replaces only the section this script created (CLAUDE.md rule 4).
// Each exception market gets two mock-ups side by side: the majority build (bound to Core navbar) and the override
// (bound to the <market>/<role> variable, which holds the shipped color once Karl accepted it; DEC-15, 2026-11-05).
// Android (2026-11-10, confirmed on device): the cards compare Android 14 and below (override, white icons) with
// Android 15+ (navbar, icon style from e.android15; bound to Core navbar).
// Sizes are illustrative: production app shell sizes wait on the Apps team (MISSING-ASSETS 5.5).

const ROLE = PLATFORM === 'iOS' ? 'header' : 'statusbar';
const PAGE = 'Components · App shell';
const SECTION = PLATFORM === 'iOS' ? '01 · Header band exceptions' : '01 · Status bar exceptions';
const hex = (h) => { h = h.replace('#', ''); return { r: parseInt(h.slice(0, 2), 16) / 255, g: parseInt(h.slice(2, 4), 16) / 255, b: parseInt(h.slice(4, 6), 16) / 255 }; };
const solid = (h) => ({ type: 'SOLID', color: hex(h) });
const rgbTxt = (h) => { const c = hex(h); return [c.r, c.g, c.b].map(v => Math.round(v * 255)).join(', '); };

await Promise.all([['Open Sans', 'Regular'], ['Open Sans', 'Bold'], ['Open Sans', 'SemiBold']].map(([family, style]) => figma.loadFontAsync({ family, style })));

// --- variables: local role vars + the Core navbar/navtext they alias -----------------------------------------
const locals = await figma.variables.getLocalVariablesAsync('COLOR');
const byName = {};
for (const v of locals) {
  byName[v.name] = v;
  for (const val of Object.values(v.valuesByMode)) if (val && val.type === 'VARIABLE_ALIAS') {
    const a = await figma.variables.getVariableByIdAsync(val.id); if (a && a.remote) byName['core:' + a.name] = a;
  }
}
// Override markets have no local alias of Core navbar/navtext: import them from the Core library (Brand colors).
// Imports stall when the file has unaccepted Core library updates (CLAUDE.md), so each import is capped at 8 s.
const need = DATA.flatMap(e => ['navbar', 'navtext'].map(r => `${e.code.toUpperCase()}/${r}`)).filter(n => !byName['core:' + n]);
if (need.length) {
  const withTimeout = (p) => Promise.race([p, new Promise(r => setTimeout(() => r(null), 8000))]);
  const cols = (await withTimeout(figma.teamLibrary.getAvailableLibraryVariableCollectionsAsync())) || [];
  const brand = cols.find(c => c.name === 'Brand colors');
  const libVars = brand ? (await withTimeout(figma.teamLibrary.getVariablesInLibraryCollectionAsync(brand.key))) || [] : [];
  for (const n of need) {
    const lv = libVars.find(v => v.name === n); if (!lv) continue;
    const v = await withTimeout(figma.variables.importVariableByKeyAsync(lv.key)); if (v) byName['core:' + n] = v;
  }
}
const paintFor = (h, v) => v ? figma.variables.setBoundVariableForPaint(solid(h), 'color', v) : solid(h);

function text(chars, size, style = 'Regular', color = '#1a1a1a', lh) {
  const t = figma.createText(); t.fontName = { family: 'Open Sans', style }; t.fontSize = size; t.characters = chars;
  t.fills = [solid(color)]; if (lh) t.lineHeight = { value: lh, unit: 'PIXELS' }; return t;
}
function frame(name, dir = 'VERTICAL', gap = 0, pad = 0) {
  const f = figma.createFrame(); f.name = name; f.layoutMode = dir; f.itemSpacing = gap;
  f.paddingLeft = f.paddingRight = f.paddingTop = f.paddingBottom = pad;
  f.primaryAxisSizingMode = 'AUTO'; f.counterAxisSizingMode = 'AUTO'; f.fills = []; return f;
}
function chip(label, bg, fg) { const c = frame('chip', 'HORIZONTAL', 0, 0); c.paddingLeft = c.paddingRight = 8; c.paddingTop = c.paddingBottom = 3; c.cornerRadius = 4; c.fills = [solid(bg)]; c.appendChild(text(label, 11, 'SemiBold', fg)); return c; }
function bar(name, w, h, paint) { const f = figma.createFrame(); f.name = name; f.resize(w, h); f.fills = [paint]; f.clipsContent = true; return f; }

function mock(e, roleHex, roleVar, navHex, navVar, navtextHex, navtextVar, fgOverride) {
  const W = 260, m = frame('Mock-up', 'VERTICAL', 0, 0); m.cornerRadius = 12; m.clipsContent = true;
  m.strokes = [solid('#d0d0d0')]; m.strokeWeight = 1;
  const fg = fgOverride || e.foreground;
  if (PLATFORM === 'Android') {
    const sb = bar('Status bar · statusbar', W, 24, paintFor(roleHex, roleVar));
    const time = text('9:41', 11, 'SemiBold', fg); time.x = 12; time.y = 4; sb.appendChild(time);
    [0, 1, 2].forEach(i => { const r = figma.createRectangle(); r.resize(i === 2 ? 14 : 8, 8); r.x = W - 48 + i * 12; r.y = 8; r.fills = [solid(fg)]; r.name = 'icon'; sb.appendChild(r); });
    m.appendChild(sb);
    const tb = bar('Top bar · navbar', W, 56, paintFor(navHex, navVar));
    const t = text(e.market, 16, 'Bold', navtextHex); t.fills = [paintFor(navtextHex, navtextVar)]; t.x = 16; t.y = 16; tb.appendChild(t); m.appendChild(tb);
  } else {
    const sb = bar('Status bar (takes navbar)', W, 20, paintFor(navHex, navVar));
    const time = text('9:41', 11, 'SemiBold', navtextHex); time.fills = [paintFor(navtextHex, navtextVar)]; time.x = 16; time.y = 2; sb.appendChild(time); m.appendChild(sb);
    const tb = bar('Nav bar · navbar', W, 44, paintFor(navHex, navVar));
    const t = text(e.market, 16, 'Bold', navtextHex); t.fills = [paintFor(navtextHex, navtextVar)]; t.textAlignHorizontal = 'CENTER'; t.resize(W, 22); t.y = 11; tb.appendChild(t); m.appendChild(tb);
    const hb = bar('Header band · header', W, 32, paintFor(roleHex, roleVar));
    const ht = text('SECTION TITLE', 12, 'Bold', fg); ht.x = 16; ht.y = 8; hb.appendChild(ht); m.appendChild(hb);
  }
  const body = bar('Content', W, 72, solid('#ffffff'));
  [0, 1, 2].forEach(i => { const r = figma.createRectangle(); r.resize(i === 2 ? 140 : 220, 8); r.x = 16; r.y = 16 + i * 16; r.cornerRadius = 2; r.fills = [solid('#e6e6e6')]; body.appendChild(r); });
  m.appendChild(body);
  return m;
}

// --- page + section ---------------------------------------------------------------------------------------
let page = figma.root.children.find(p => p.name === PAGE);
if (!page) { page = figma.createPage(); page.name = PAGE; }
await page.loadAsync();
page.children.filter(n => n.name === SECTION).forEach(n => n.remove());
const others = page.children; const y0 = others.length ? Math.max(...others.map(n => n.y + n.height)) + 200 : 0;

const root = frame(SECTION, 'VERTICAL', 32, 64); root.fills = [solid('#ffffff')];
const what = PLATFORM === 'iOS' ? 'section header band (`header`)' : 'status bar (`statusbar`)';
const fgWhat = PLATFORM === 'iOS' ? 'White section title text (Style.json cell-tertiary-headertext, #ffffff in all 77 markets), target 4.5:1.'
  : 'Status-bar icons: white on Android 14 and below (the main theme never sets windowLightStatusBar). On Android 15+ the status bar shows navbar and the app picks dark icons only when that color is exactly #FFFFFF (EdgeToEdgeUtil.java:30): DP, MC, NYDN, OS, SS, VP. TSAR: the export gives white icons on its #F5F5F5 bar; Karl (2026-11-10) set Android 15+ to a white status bar with dark icons, assumed corrected in production (TSAR/statusbar15; Ameer to confirm, MISSING-ASSETS 5.5). Rule confirmed by the Apps team (Ameer M., 2026-11-10). Icon colors are drawn by the system; contrast shown for white / black icons, target 3:1.';
root.appendChild(text(SECTION.replace('01 · ', '') + (PLATFORM === 'Android' ? ' · Android 14 and below vs 15+' : '') + ' · DEC-15', 32, 'Bold', '#1a1a1a', 44));
const how = PLATFORM === 'iOS'
  ? 'Left: what the majority rule builds (Core navbar). Right: the accepted override, the color the app ships (<market>/header variable).'
  : 'Left: Android 14 and below, the accepted override (<market>/statusbar variable) with white icons. Right: Android 15+, the status bar shows the top bar (Core navbar) with the icon style the app picks. Tokens: statusbar.android.<m>.icons / icons15; Kotlin statusbarFor(sdkInt), XML values-v35.';
const intro = text(`The ${what} follows the top bar (alias of Core navbar) in every market. These ${DATA.length} markets ship something else on ${PLATFORM === 'Android' ? 'Android 14 and below' : 'iOS'}. ` +
  `${how} ${fgWhat} Sizes are illustrative (MISSING-ASSETS 5.5). Source: data/shell-colors.json · docs/SHELL-EXCEPTIONS.md.`, 14, 'Regular', '#333333', 22);
intro.resize(1860, intro.height); intro.textAutoResize = 'HEIGHT'; root.appendChild(intro);

const grid = frame('Exceptions', 'HORIZONTAL', 32, 0); grid.layoutWrap = 'WRAP'; grid.counterAxisSpacing = 32;
grid.primaryAxisSizingMode = 'FIXED'; grid.resize(1860, 100); grid.counterAxisSizingMode = 'AUTO';
for (const e of DATA) {
  const M = e.code.toUpperCase();
  const roleVar = byName[`${M}/${ROLE}`], navVar = byName[`core:${M}/navbar`], navtextVar = byName[`core:${M}/navtext`];
  const navtextHex = e.navtext;
  const card = frame(`${M} · ${e.market}`, 'VERTICAL', 16, 24); card.cornerRadius = 8; card.strokes = [solid('#e6e6e6')]; card.strokeWeight = 1; card.fills = [solid('#ffffff')];
  card.appendChild(text(`${e.market} (${M})`, 16, 'Bold'));
  const row = frame('Compare', 'HORIZONTAL', 24, 0);
  const pass = (c) => c >= e.target;
  const ovChip = () => chip(e.accepted ? 'Override accepted' : 'Suggested override', '#fff4d6', '#6b4500');
  const a15 = e.android15;
  // DEC-15 production correction (Karl, 2026-11-10): the Android 15+ status bar is not navbar -> its own variable <M>/statusbar15,
  // created next to <M>/statusbar in the same collection (additive) and bound on the 15+ side.
  let v15 = navVar;
  if (PLATFORM === 'Android' && a15 && a15.correction && roleVar) {
    const coll = await figma.variables.getVariableCollectionByIdAsync(roleVar.variableCollectionId);
    v15 = byName[`${M}/statusbar15`] || figma.variables.createVariable(`${M}/statusbar15`, coll, 'COLOR');
    v15.setValueForMode(coll.modes[0].modeId, { ...hex(a15.statusbar), a: 1 }); v15.scopes = ['FRAME_FILL', 'SHAPE_FILL'];
    v15.description = `Status bar on Android 15+ (Android only): ${a15.statusbar}, production correction (DEC-15, ${a15.correction.decided}) ${a15.correction.confirm}. Token color.android.${e.code}.statusbar15.`;
    byName[`${M}/statusbar15`] = v15;
  }
  const cols = PLATFORM === 'Android' && a15 ? [
    { title: 'Android 14 and below', chip: () => chip('Android 14 and below · override', '#fff4d6', '#6b4500'),
      sub: `statusbar = ${e.override} · ${rgbTxt(e.override)} (shipped, accepted) · white icons`, hexv: e.override, v: e.accepted ? roleVar : null, c: e.contrast_override, fg: e.foreground, fgName: 'white icons' },
    { title: 'Android 15+', chip: () => chip(`Android 15+ · ${a15.correction ? 'white bar (correction)' : 'navbar'}, ${a15.icons} icons`, '#efe7fb', '#43217a'),
      sub: `statusbar = ${a15.correction ? 'statusbar15' : 'navbar'} ${a15.statusbar} · ${rgbTxt(a15.statusbar)} · ${a15.icons} icons (system)${a15.correction ? ' · production correction (Karl, 2026-11-10)' : ''}`, hexv: a15.statusbar, v: v15, c: a15.contrast, fg: a15.icon_hex_for_contrast, fgName: `${a15.icons} icons` },
  ] : [
    { title: 'Majority · built', chip: () => pass(e.contrast_built) ? chip('Majority · passes', '#e6f4ea', '#14532d') : chip('Majority · fails', '#fde8e8', '#8a1c1c'),
      sub: `majority: navbar ${e.built} · ${rgbTxt(e.built)}`, hexv: e.built, v: navVar, c: e.contrast_built, fg: e.foreground, fgName: e.foreground },
    { title: 'Suggested override', chip: ovChip, sub: `${ROLE} = ${e.override} · ${rgbTxt(e.override)} (shipped${e.accepted ? ', accepted' : ''})`, hexv: e.override, v: e.accepted ? roleVar : null, c: e.contrast_override, fg: e.foreground, fgName: e.foreground },
  ];
  for (const col of cols) {
    const cf = frame(col.title, 'VERTICAL', 8, 0);
    cf.appendChild(col.chip());
    cf.appendChild(text(col.sub, 11, 'Regular', '#333333'));
    cf.appendChild(mock(e, col.hexv, col.v, e.navbar, navVar, navtextHex, navtextVar, col.fg));
    cf.appendChild(text(`${col.fgName} on ${col.hexv}: ${col.c}:1 ${pass(col.c) ? 'passes' : 'FAILS'} ${e.target}:1`, 12, 'SemiBold', pass(col.c) ? '#14532d' : '#8a1c1c'));
    row.appendChild(cf);
  }
  card.appendChild(row);
  if (PLATFORM === 'Android' && a15) card.appendChild(text(`Without the override, Android 14 and below would show white icons on navbar ${e.built}: ${e.contrast_built}:1 (fails 3:1).`, 11, 'Regular', '#555555'));
  if (!roleVar || !navVar) card.appendChild(text('Variables not linked yet (library import pending): colors drawn as raw values.', 11, 'Regular', '#8a1c1c'));
  grid.appendChild(card);
}
root.appendChild(grid);
const sec = figma.createSection(); sec.name = SECTION; page.appendChild(sec); sec.appendChild(root);
root.x = 80; root.y = 80; sec.resizeWithoutConstraints(root.width + 160, root.height + 160); sec.x = 0; sec.y = y0;
return { page: page.id, section: sec.id, cards: DATA.length, linked: DATA.filter(e => byName[`${e.code.toUpperCase()}/${ROLE}`]).length, navLinked: DATA.filter(e => byName[`core:${e.code.toUpperCase()}/navbar`]).length };

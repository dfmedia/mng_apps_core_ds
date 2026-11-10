"""Emit the Figma build for Core page "Icons · System Comparison" › 05 · Icon list (combined), from data/icon-names.json (DEC-17).
One list with everything: shared name, purpose, bucket, what each app ships, notes and Apps team questions, the reference glyphs
(nearest SF Symbol / Material Symbol / Font Awesome, copied from section 02, not redrawn) and the earlier recommendation.
Usage: python3 scripts/figma_icon_names.py  ->  prints JS for figma_execute in the Core file (prepends a compact row list
expanded in Figma, then scripts/figma/build_table_section.js). 05 sits at x 0, y 800; 03 (SF Symbols sheet) to its right.
The glyph previews are copied from 02 · Comparison grid on the page Icons · Archive.
"""
import json
D = json.load(open('data/icon-names.json')); S = D['summary']
GRID = '02 · Comparison grid'; GRID_PAGE = 'Icons · Archive'   # 02 and 04 archived 2026-11-10 (Karl), merged into 05
C = {'name': '05 · Icon list', 'title': 'Icon list · one name per purpose, everything we know (DEC-17)',
     'intro': (f"One row per icon purpose ({S['purposes']} purposes → {S['names']} names). What ships: iOS {D['source']['ios']}, Android {D['source']['android']}. "
               "Nothing is redesigned: each app keeps its own glyphs; the name is shared (proposals for Karl). Rule: lowercase words joined by hyphens, "
               "named for what the icon does; prefixes tab-, enews-, brand-. Reference columns (Ref ·) are not what ships: the nearest SF Symbol, "
               "Material Symbol and Font Awesome 5.15.1 glyph (copied from 02 · Comparison grid, now on Icons · Archive) and the October recommendation, not decided. "
               "Source: data/icon-names.json (scripts/build_icon_names.py) · docs/ICON-NAMES.md · Apps team questions: docs/MISSING-ASSETS.md §1."),
     'columns': [{'name': 'Name', 'w': 180}, {'name': 'Purpose', 'w': 190}, {'name': 'Bucket', 'w': 200}, {'name': 'iOS ships', 'w': 300},
                 {'name': 'Android ships', 'w': 300}, {'name': 'Note · Apps team', 'w': 300}, {'name': 'Ref · SF Symbol', 'w': 190},
                 {'name': 'Ref · Material Symbol', 'w': 190}, {'name': 'Ref · Font Awesome', 'w': 190}, {'name': 'Ref · earlier recommendation (not decided)', 'w': 280}],
     'rows': []}
for g in dict.fromkeys(r['group'] for r in D['icons']):
    rs = [r for r in D['icons'] if r['group'] == g]
    C['rows'].append(f'{g} ({len(rs)})')
    for r in rs:
        rf = r['reference']
        na = ' · '.join(x for x in (r['note'], ('Ask: MISSING-ASSETS ' + r['apps_team']) if r['apps_team'] else '') if x) or '—'
        rec = ' · '.join(x for x in (rf['recommendation'], rf['ownership_note']) if x) or '—'
        C['rows'].append([r['name'], r['purpose'], r['bucket'], r['ios'] or '—', r['android'] or '—', na, rec,
                          [rf['sf_symbol'] or '—', rf['material'] or '—', rf['font_awesome'] or '—']])
EXPAND = """await figma.root.children.find(p => p.name === GRID_PAGE).loadAsync();
const T = { ...C, rows: C.rows.map(r => typeof r === 'string' ? { group: r } : [
  { t: r[0], b: true }, r[1], { chip: r[2] }, r[3], r[4], r[5],
  { clone: [GRID, r[1], 'SF Symbols', GRID_PAGE], alt: r[7][0] }, { clone: [GRID, r[1], 'Material Symbols', GRID_PAGE], alt: r[7][1] }, { clone: [GRID, r[1], 'Font Awesome', GRID_PAGE], alt: r[7][2] }, r[6]]) };
"""
MOVE = """const _old = page.children.find(n => n.name === '05 · Icon names'); if (_old) _old.remove();   // the earlier names-only version (2026-11-10)
const _n = await figma.getNodeByIdAsync(root.id); _n.x = 0; _n.y = 800;
const _s03 = page.children.find(n => n.name.startsWith('03 · Source')); if (_s03) { _s03.x = _n.width + 200; _s03.y = 800; }
"""
js = open('scripts/figma/build_table_section.js').read()
i = js.rindex('return {')
print(f"const PAGE = {json.dumps('Icons · System Comparison')}; const GRID = {json.dumps(GRID)}; const GRID_PAGE = {json.dumps(GRID_PAGE)}; const C = {json.dumps(C, ensure_ascii=False, separators=(',', ':'))};\n"
      + EXPAND + js[:i] + MOVE + js[i:])

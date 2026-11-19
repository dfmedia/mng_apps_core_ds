"""Emit Figma builds (Core file) from data/shipped-specs.json (scripts/build_shipped_specs.py).
Usage: python3 scripts/figma_shipped_specs.py shell|motion|controls   -> prints JS (PAGE + T + scripts/figma/build_table_section.js)
  shell     Layout · iOS vs Android › 03 · App shell sizes (as shipped)
  motion    Layout · iOS vs Android › 04 · Elevation and motion (as shipped)
  controls  Components · Controls › 01 · Other controls (as shipped)
"""
import json, re, sys
D = json.load(open('data/shipped-specs.json'))
rgb = lambda m: f"{m.group(0)} · {int(m.group(0)[1:3], 16)}, {int(m.group(0)[3:5], 16)}, {int(m.group(0)[5:7], 16)}"
hexrgb = lambda s: re.sub(r'#[0-9A-Fa-f]{6}(?![0-9A-Fa-f])', rgb, s)
SRC = f"Sources: iOS {D['sources']['ios']}; Android {D['sources']['android']}. data/shipped-specs.json · docs/SHIPPED-SPECS.md."
MODE = sys.argv[1] if len(sys.argv) > 1 else ''
if MODE == 'shell':
    PAGE = 'Layout · iOS vs Android'
    T = {'name': '03 · App shell sizes (as shipped)', 'title': 'App shell sizes (as shipped)',
         'intro': ('Heights, spacing and label type of the app shell on each app, documented exactly as shipped (DEC-09). Android values are tokens '
                   '(Components · Android variables in the Android file). iOS values come from the Apps team answers and export at f79fe3339 '
                   'and are iOS tokens too (Components · iOS variables in the iOS file). ' + SRC),
         'columns': [{'name': 'Part', 'w': 180}, {'name': 'Owner', 'w': 200}, {'name': 'iOS', 'w': 440}, {'name': 'Android', 'w': 520}, {'name': 'Android tokens', 'w': 300}],
         'rows': [[{'t': r['what'], 'b': True}, {'chip': r['bucket']}, hexrgb(r['ios']), hexrgb(r['android']), r['tokens'] or '—'] for r in D['shell']]}
elif MODE == 'motion':
    PAGE = 'Layout · iOS vs Android'
    E, M = D['elevation'], D['motion']
    rows = [{'group': f"iOS shadows ({len(E['ios'])}): {E['ios_note']}"}]
    rows += [[{'t': s['where'], 'b': True}, f"opacity {s['opacity']} · radius {s['radius']} · offset {s['offset']} (black)"] for s in E['ios']]
    rows += [{'group': f"Android elevation ({len(E['android'])}): tokens component.android.elevation.*"}]
    rows += [[{'t': e['where'], 'b': True}, re.sub(r'^(\d+)', r'\1dp', e['dp']).replace('cards 4)', 'cards 4dp)')] for e in E['android']]
    rows += [{'group': f"iOS motion ({len(M['ios'])}): no shared spec"}] + [[{'t': m['where'], 'b': True}, m['duration']] for m in M['ios']]
    rows += [{'group': f"Android motion ({len(M['android'])}): no shared spec"}] + [[{'t': m['where'], 'b': True}, m['duration']] for m in M['android']]
    T = {'name': '04 · Elevation and motion (as shipped)', 'title': 'Elevation and motion (as shipped)',
         'intro': ('Neither app has a shared elevation scale or motion spec: each value is set where it is used. Documented as shipped (DEC-09); '
                   'nothing new is designed (Karl, 2026-11-10). Owner: split per platform, iOS only + Android only (Karl, 2026-11-19, DEC-21). ' + SRC),
         'columns': [{'name': 'Where', 'w': 460}, {'name': 'Value', 'w': 620}], 'rows': rows}
elif MODE == 'controls':
    PAGE = 'Components · Controls'
    T = {'name': '01 · Other controls (as shipped)', 'title': 'Other controls and buttons, iOS vs Android (as shipped)',
         'intro': ('Controls and small buttons that are not built as Core components yet, each app as it ships (DEC-09), with its owner bucket. '
                   'Open questions are numbered as in MISSING-ASSETS. ' + D['rule'].replace('Documented as shipped (DEC-09). ', '') + ' ' + SRC),
         'columns': [{'name': 'Control', 'w': 220}, {'name': 'Owner', 'w': 200}, {'name': 'iOS', 'w': 520}, {'name': 'Android', 'w': 560}],
         'rows': [[{'t': r['what'], 'b': True}, {'chip': r['bucket']}, hexrgb(r['ios']), hexrgb(r['android'])] for r in D['controls']]}
else:
    sys.exit(__doc__)
print(f"const PAGE = {json.dumps(PAGE)}; const T = {json.dumps(T, ensure_ascii=False)};\n" + open('scripts/figma/build_table_section.js').read())

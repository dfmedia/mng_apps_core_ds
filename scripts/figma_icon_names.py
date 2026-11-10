"""Emit the Figma build for Core page "Icons · System Comparison" › 05 · Icon names, from data/icon-names.json (DEC-17).
Usage: python3 scripts/figma_icon_names.py  ->  prints JS (PAGE + T + scripts/figma/build_table_section.js) for figma_execute in the Core file.
After the build, the frame is moved right of section 04 (x 4460, y 800) by the snippet appended below.
"""
import json
D = json.load(open('data/icon-names.json')); S = D['summary']
rows = []
for g in dict.fromkeys(r['group'] for r in D['icons']):
    rs = [r for r in D['icons'] if r['group'] == g]
    rows.append({'group': f'{g} ({len(rs)})'})
    for r in rs:
        extra = ' · '.join(x for x in (r['note'], ('Ask: MISSING-ASSETS ' + r['apps_team']) if r['apps_team'] else '') if x)
        rows.append([{'t': r['name'], 'b': True}, r['purpose'], {'chip': r['bucket']}, r['ios'] or '—', r['android'] or '—', extra or '—'])
T = dict(name='05 · Icon names', title='Icon names · one name per purpose (DEC-17)',
         intro=(f"One shared name for each icon purpose, next to what each app ships today ({D['source']['ios']}, {D['source']['android']}). "
                "Nothing is redesigned: each app keeps its own glyphs; only the name is shared. Names are proposals for Karl to review. "
                "Rule: lowercase words joined by hyphens, named for what the icon does; prefixes tab-, enews-, brand-. "
                f"{S['purposes']} purposes → {S['names']} names; 'saved' covers the Android special-section star (DEC-17). "
                "Source: data/icon-names.json (scripts/build_icon_names.py) · docs/ICON-NAMES.md."),
         columns=[{'name': 'Name', 'w': 200}, {'name': 'Purpose', 'w': 220}, {'name': 'Bucket', 'w': 210}, {'name': 'iOS ships', 'w': 400},
                  {'name': 'Android ships', 'w': 400}, {'name': 'Note · Apps team', 'w': 380}], rows=rows)
MOVE = "\nconst _n = await figma.getNodeByIdAsync(root.id); _n.x = 4460; _n.y = 800;\n"
js = open('scripts/figma/build_table_section.js').read()
i = js.rindex('return {')
print(f"const PAGE = {json.dumps('Icons · System Comparison')}; const T = {json.dumps(T, ensure_ascii=False, separators=(',', ':'))};\n" + js[:i] + MOVE + js[i:])

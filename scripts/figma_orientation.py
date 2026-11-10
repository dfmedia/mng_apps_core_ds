"""Emit the Figma build for Core page "Layout · iOS vs Android" › 01 · Orientation.
Usage: python3 scripts/figma_orientation.py  ->  prints JS (PAGE + T + scripts/figma/build_table_section.js) for figma_execute in the Core file.
Data: data/orientation.json (scripts/build_orientation.py). The table builder creates the page if it does not exist yet.
"""
import json
D = json.load(open('data/orientation.json'))
cell = lambda p: f"{p['orientation']}" + (f" · {p['device']}" if p.get('device') else '')
rows = []
for r in D['rows']:
    rows.append([{'t': r['device_class'], 'b': True}, {'t': cell(r['ios']), 'b': True}, {'t': cell(r['android']), 'b': True}, {'chip': r['bucket']}])
    rows.append(['How', r['ios']['how'] + '. Source: ' + r['ios']['evidence'], r['android']['how'] + '. Source: ' + r['android']['evidence'], ''])
T = {'name': '01 · Orientation', 'title': 'Orientation (as shipped)',
     'intro': (f"{D['summary']} {D['rule']} Source: iOS {D['source']['ios']}; Android {D['source']['android']} · "
               "data/orientation.json · docs/ORIENTATION.md."),
     'columns': [{'name': 'Device class', 'w': 140}, {'name': 'iOS', 'w': 520}, {'name': 'Android', 'w': 520}, {'name': 'Ownership', 'w': 120}],
     'rows': rows}
print(f"const PAGE = {json.dumps('Layout · iOS vs Android')}; const T = {json.dumps(T, ensure_ascii=False, separators=(',', ':'))};\n" + open('scripts/figma/build_table_section.js').read())

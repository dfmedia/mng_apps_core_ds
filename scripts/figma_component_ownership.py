"""Emit the Figma build for Core "Components · Platform Ownership" › 02 · Component ownership (generated)
from data/component-platform-map.json (scripts/component_platform_map.py).
Usage: python3 scripts/figma_component_ownership.py  -> prints JS (PAGE + T + scripts/figma/build_table_section.js)
to run with figma_execute in the Core file. Replaces the hand-built 01 section's role as the current table (2026-11-19);
01 is left in place for Karl (rule 4).
"""
import json
D = json.load(open('data/component-platform-map.json'))
CHIP = {'core': 'Core', 'core+variant': 'Core, per-platform value', 'ios': 'iOS only', 'android': 'Android only'}
T = {'name': '02 · Component ownership (generated)', 'title': 'Component ownership: Core / iOS / Android (as shipped)',
     'intro': (f"Every component and layout rule, with what each app ships and its owner bucket. Generated from data/component-platform-map.json "
               f"(scripts/component_platform_map.py; iOS {D['source']['ios']} plus Apps team answers, Android {D['source']['android']} plus Apps team answers "
               "and the Android style guide of 2026-11-19). Counts: " + ', '.join(f"{CHIP[k]} {v}" for k, v in D['summary'].items()) +
               ". Supersedes the hand-built 01 table above, which is kept until Karl archives it."),
     'columns': [{'name': 'Component', 'w': 200}, {'name': 'Owner', 'w': 200}, {'name': 'iOS ships', 'w': 420}, {'name': 'Android ships', 'w': 420}, {'name': 'Core spec / note', 'w': 360}],
     'rows': []}
for g in dict.fromkeys(i['group'] for i in D['items']):
    its = [i for i in D['items'] if i['group'] == g]
    T['rows'].append({'group': f"{'App shell' if g == 'App chrome' else g} ({len(its)})"})
    for i in its:
        T['rows'].append([{'t': i['name'], 'b': True}, {'chip': CHIP[i['owner']]}, i['ios_today'] or '—', i['android_today'] or '—', i['note'] or '—'])
print(f"const PAGE = {json.dumps('Components · Platform Ownership')}; const T = {json.dumps(T, ensure_ascii=False)};\n" + open('scripts/figma/build_table_section.js').read())

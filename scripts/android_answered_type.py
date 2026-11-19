"""Android text styles that the export lacks but the Apps team answered (DREAMT-4719).
extend(AND) appends them to the Android type source (data/source/android-type.json) in memory, so
compare_type.py and build_type_tokens.py treat them like exported styles. The source files are not edited."""
import json

ANSWERS = 'data/source/apps-team-answers/2026-11-19-DREAMT-4719-android.json'

def extend(src):
    extra = json.load(open(ANSWERS)).get('type_styles', {})
    for gname, styles in extra.items():
        if gname.startswith('$'): continue
        group = next((g for g in src['groups'] if g['name'] == gname), None)
        if group is None:
            group = {'name': gname, 'styles': []}; src['groups'].append(group)
        have = {s['name'] for s in group['styles']}
        group['styles'] += [dict(s, answered=True) for s in styles if s['name'] not in have]
    return src

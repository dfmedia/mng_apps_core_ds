"""Prints JS for the iOS file, page Components · Button: the primary button review (Karl, 2026-11-18). Findings only.
Usage: python3 scripts/figma_button_ios_review.py 3|4
  3  ->  03 · iOS buttons as shipped (Apps team)
  4  ->  04 · Primary button: our spec vs what ships
Data: data/button-ios-review.json (scripts/build_button_ios_review.py). Run each through figma_execute with fileKey uNxwBNoP4ODDUFGByi73mZ.
"""
import json, sys
D = json.load(open('data/button-ios-review.json'))
TABLE = open('scripts/figma/build_table_section.js').read()
PAGE = 'Components · Button'
SRC = f"Sources: our spec {D['sources']['spec']}; shipped {D['sources']['shipped']}. Data: data/button-ios-review.json."
dash = lambda v: '—' if v in (None, '') else str(v)
def table(T):
    return f"const PAGE = {json.dumps(PAGE)}; const T = {json.dumps(T, ensure_ascii=False, separators=(',', ':'))};\n" + TABLE
MODE = sys.argv[1]
if MODE == '3':
    rows = [{'group': 'Shown in production'}]
    for b in D['shipped']:
        rows.append([{'t': b['name'], 'b': True}, dash(b['height']), f"{b['radius']} pt" if b['radius'] is not None else '—', dash(b['label']), dash(b['fill']), dash(b.get('text'))])
    rows.append({'group': 'Never shown (login is the Auth0 Universal Login page)'})
    for n in D['not_shown']:
        rows.append([{'t': n['name'], 'b': True}, '—', '—', '—', '—', {'chip': 'Not shown'}])
    T = {'name': '03 · iOS buttons as shipped (Apps team)', 'title': 'iOS buttons as shipped (review)',
         'intro': 'The Apps team says iOS has no single primary button. These are the buttons it shows, from TroncKit f79fe3339. '
                  f"Pressed state on all of them: {D['pressed']} Our primary button (01) was built from the Log In / Register button, which is never shown. "
                  'Review only: nothing here changes the Button component. ' + SRC,
         'columns': [{'name': 'Button', 'w': 280}, {'name': 'Height', 'w': 270}, {'name': 'Radius', 'w': 90}, {'name': 'Label', 'w': 260}, {'name': 'Fill', 'w': 280}, {'name': 'Label text', 'w': 230}],
         'rows': rows}
elif MODE == '4':
    rows = [{'group': 'Our iOS primary button (DEC-07) vs the meter paywall purchase button'}]
    for r in D['comparison']:
        rows.append([{'t': r['property'], 'b': True}, r['spec'], r['shipped'], {'chip': r['verdict']}, dash(r['note'])])
    rows.append({'group': 'To settle before any rebuild'})
    for i, q in enumerate(D['questions'], 1):
        rows.append([{'t': f'Question {i}', 'b': True}, q, '—', {'chip': 'Open'}, '—'])
    T = {'name': '04 · Primary button: our spec vs what ships', 'title': 'Primary button: our spec vs what ships (review)',
         'intro': 'Compares the iOS primary button spec in 01 with the closest button iOS actually shows, the meter paywall purchase button. '
                  'Nothing is rebuilt until the questions below are settled (Karl, 2026-11-18). ' + SRC,
         'columns': [{'name': 'Property', 'w': 180}, {'name': 'Our spec (01)', 'w': 360}, {'name': 'Shipped purchase button', 'w': 380}, {'name': 'Same?', 'w': 110}, {'name': 'Note', 'w': 380}],
         'rows': rows}
else:
    sys.exit('mode: 3 or 4')
print(table(T))

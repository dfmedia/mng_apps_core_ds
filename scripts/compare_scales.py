"""Scales step 1: compare shipped spacing, radius, size and breakpoint values by role (read-only review).
Usage: python3 scripts/compare_scales.py
Reads:  data/source/ios-scales.json, data/source/android-scales.json (copied from the two style guides)
Writes: data/scale-comparison.json, docs/SCALES-COMPARISON.md
Values are read from the sources; only the role mapping below is hand-made. Neither app has a shared scale in code:
these are the values the code uses, each with its source. Units: pt (iOS), dp (Android); breakpoints as noted.
Match: same · close (within 2) · differs · ios-only · android-only
"""
import json

IOS = json.load(open('data/source/ios-scales.json'))
AND = json.load(open('data/source/android-scales.json'))

def index(src):
    out = {}
    for sec in ('spacing', 'radius', 'size', 'breakpoint'):
        for t in src[sec].get('tokens', []):
            out[t['name']] = {'name': t['name'], 'kind': sec, 'value': t['value'], 'usage': t.get('usage', '')}
    return out
I, A = index(IOS), index(AND)

# role, kind, iOS token, Android token, note
ROLES = [
 ('Section-front cell margin', 'spacing', 'space-cell-margin', 'space-cell-padding', 'Outer margin/padding of a section-front cell'),
 ('Section-front cell gap', 'spacing', 'space-cell-padding', 'space-cell-spacing', 'Space between elements inside a cell'),
 ('Article side margin, phone', 'spacing', 'space-article-margin-min', 'space-article-side', 'iOS: minimum; grows with width (0.3125 x width − 160)'),
 ('Article side margin, landscape', 'spacing', None, 'space-article-side-land', 'iOS uses the width formula instead'),
 ('Article side margin, tablet', 'spacing', None, 'space-article-side-tablet', 'iOS uses the width formula instead'),
 ('Article top margin, phone', 'spacing', 'space-article-top-phone', None, ''),
 ('Article top margin, tablet', 'spacing', 'space-article-top-pad', None, ''),
 ('Subscription option inset', 'spacing', 'space-subscription-inset', None, 'Android subscription options use 14dp padding (controls notes), not a token'),
 ('Paywall login button side margin', 'spacing', None, 'space-login-margin', ''),
 ('Primary button radius', 'radius', 'radius-button', 'radius-paywall', 'Kept per platform (DEC-07)'),
 ('Primary button radius, legacy template', 'radius', 'radius-button-legacy', None, 'iOS legacy template: documented only (DEC-10). Also the push-prompt Yes/No buttons'),
 ('Subscription option radius', 'radius', 'radius-subscription', None, 'Android subscription options are square (radius-paywall)'),
 ('Google sign-in radius', 'radius', 'radius-google', None, ''),
 ("What's New Continue / outlined sheet button radius", 'radius', None, 'radius-whatsnew', ''),
 ('Your News Continue radius', 'radius', None, 'radius-continue', 'iOS draws Continue as PNG images (DSC-24)'),
 ('Manage subscription / delete account radius', 'radius', None, 'radius-sheet-button', ''),
 ('Savings label radius', 'radius', None, 'radius-discount', ''),
 ('Minimum touch target', 'size', 'size-touch-min', 'size-touch-min', 'Platform convention: Apple 44 pt, Android 48 dp. Not enforced in either app'),
 ('Your News checkbox', 'size', 'size-checkbox', None, 'Below the touch minimum'),
 ('Social sign-in icon', 'size', 'size-social-icon', None, ''),
 ('Tab bar icon', 'size', 'size-tab-icon', 'size-nav-icon', 'iOS 26 x 23 pt (Font Awesome); Android 24 dp tall'),
 ('Audio player control', 'size', None, 'size-player-control', 'Below the touch minimum'),
 ('Author contact icon', 'size', None, 'size-author-icon', 'Below the touch minimum'),
 ('Overlay close button', 'size', None, 'size-overlay-close', 'Breaking news and live video; below the touch minimum'),
 ('Paywall primary button height', 'size', None, 'size-paywall-button', 'iOS height not in the source (44 provisional, DEC-07)'),
 ('Section-front grid columns', 'breakpoint', 'grid-columns', 'grid-columns', ''),
 ('Width class: small', 'breakpoint', 'bp-front-small', 'bp-small', 'iOS: window width in pt; Android: physical screen width in inches'),
 ('Width class: medium', 'breakpoint', 'bp-front-medium', 'bp-medium', 'iOS also has a second set for items (769 / 1025, LAY-01)'),
 ('Width class: large', 'breakpoint', 'bp-front-large', 'bp-large', ''),
 ('Width class: x-small', 'breakpoint', None, 'bp-xsmall', ''),
 ('Item width class: medium', 'breakpoint', 'bp-item-medium', None, 'Disagrees with bp-front-medium (LAY-01)'),
 ('Item width class: large', 'breakpoint', 'bp-item-large', None, 'Disagrees with bp-front-large (LAY-01)'),
 ('Tablet remote config', 'breakpoint', None, 'bp-tablet-config', ''),
 ('Tablet resources (article padding, type)', 'breakpoint', None, 'bp-tablet-res', ''),
]

def num(v):
    try: return float(str(v).split()[0].replace('px', ''))
    except ValueError: return None
def match(i, a):
    if not a: return 'ios-only'
    if not i: return 'android-only'
    vi, va = str(i['value']), str(a['value'])
    if vi == va: return 'same'
    ni, na = num(vi), num(va)
    if ni is not None and na is not None and 'in' not in va and abs(ni - na) <= 2: return 'close'
    return 'differs'

used_i, used_a, rows = set(), set(), []
for role, kind, si, sa, note in ROLES:
    i, a = I.get(si) if si else None, A.get(sa) if sa else None
    assert (si is None or i) and (sa is None or a), f'unknown token in {role}'
    if i: used_i.add(si)
    if a: used_a.add(sa)
    rows.append({'role': role, 'kind': kind, 'ios': i, 'android': a, 'match': match(i, a), 'note': note})
missing = sorted(set(I) - used_i) + sorted(set(A) - used_a)
assert not missing, f'values not mapped to a role: {missing}'

counts = {}
for r in rows: counts[r['match']] = counts.get(r['match'], 0) + 1
json.dump({'generated_by': 'scripts/compare_scales.py', 'counts': counts, 'roles': rows}, open('data/scale-comparison.json', 'w'), indent=1, ensure_ascii=False)

LABEL = {'same': '✅ same', 'close': '🟡 close', 'differs': '🔴 differs', 'ios-only': 'iOS only', 'android-only': 'Android only'}
fmt = lambda t: f"{str(t['value']).replace('px', '')} (`{t['name']}`)" if t else '—'
L = ['# Spacing, radius, size and breakpoints: iOS vs Android', '',
     'Generated by `scripts/compare_scales.py` from `data/source/ios-scales.json` and `data/source/android-scales.json`. Do not edit by hand. A read-only review, nothing decided yet.', '',
     'Neither app has a shared spacing scale in code; these are the values the code uses, each with its source. Units: pt on iOS, dp on Android; Android width classes are physical inches.', '',
     '## Summary', '', '| Match | Roles |', '|---|---|'] + [f'| {LABEL[k]} | {counts.get(k, 0)} |' for k in LABEL] + ['']
NAMES = {'spacing': 'Spacing', 'radius': 'Radius', 'size': 'Size', 'breakpoint': 'Breakpoints and grid'}
for kind, title in NAMES.items():
    L += [f'## {title}', '', '| Role | iOS | Android | Match | Note |', '|---|---|---|---|---|']
    for r in rows:
        if r['kind'] == kind:
            L.append(f"| {r['role']} | {fmt(r['ios'])} | {fmt(r['android'])} | {LABEL[r['match']]} | {r['note']} |")
    L.append('')
open('docs/SCALES-COMPARISON.md', 'w').write('\n'.join(L))
print(len(rows), 'roles:', counts)

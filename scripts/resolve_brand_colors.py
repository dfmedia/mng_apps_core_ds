"""Resolve each market's brand colors to one source of truth.
Usage: python3 scripts/resolve_brand_colors.py data/source/markets.json data/source/android-markets.json \
         data/source/migration-sheet-brand-colors.json data/brand-color-resolution.json
Evidence, strongest first:
  sheet        the migration sheet's Primary / Secondary color matches one app exactly
  sheet+drift  the sheet matches one app, and the other app's value is the sheet value after iOS 2-decimal rounding
  ios-close    no sheet value; iOS = Android after 2-decimal rounding. DEC-08: iOS value (was drift-rule -> Android under DEC-01)
  agree        both apps already ship the same value
  unresolved   none of the above; needs the Apps team
iOS drift: TroncKit stores each RGB channel as a 2-decimal fraction (0x22 = 0.133 -> 0.13 -> 0x21).
Roles: navbar, action (sheet Primary) and tabactive (sheet Secondary).
"""
import json, sys, math
ios_src, and_src, sheet_src, out = sys.argv[1:5]
ios = json.load(open(ios_src)); andr = json.load(open(and_src)); sheet = json.load(open(sheet_src))
def ch(h): return [int(h[i:i+2], 16) for i in (1, 3, 5)]
def norm(h): h = h.strip().lower()[:7]; return h if len(h) == 7 and h.startswith('#') else None
def drift(h): return '#' + ''.join('%02x' % int(round(round(c / 255, 2) * 255)) for c in ch(h))
def lin(c): return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
def oklab(h):
    r, g, b = [lin(v/255) for v in ch(h)]
    l=(0.4122214708*r+0.5363325363*g+0.0514459929*b)**(1/3); m=(0.2119034982*r+0.6806995451*g+0.1073969566*b)**(1/3); s=(0.0883024619*r+0.2817188376*g+0.6299787005*b)**(1/3)
    return (0.2104542553*l+0.7936177850*m-0.0040720468*s, 1.9779984951*l-2.4285922050*m+0.4505937099*s, 0.0259040371*l+0.7827717662*m-0.8086757660*s)
dE = lambda a, b: math.dist(oklab(a), oklab(b))
A = {m['code']: m for m in andr['markets']}
S = {r[1].upper(): dict(zip(sheet['columns'], r)) for r in sheet['rows']}
ROLES = {'navbar': ('bar', 'primary'), 'action': ('action', 'primary'), 'tabactive': ('navactive', 'secondary')}
res, stats = [], {}
for im in sorted(ios['markets'], key=lambda m: m['name']):
    c = im['code']; am = A[c]; sr = S.get(c, {}); row = {'code': c, 'name': im['name'], 'cluster': (sr.get('cluster') or '').strip(), 'sheet_status': sr.get('status_ios', ''), 'roles': {}}
    for role, (akey, skey) in ROLES.items():
        i = norm(im['core'][role]); a = norm(am['core'][akey]); s = norm(sr.get(skey, '') or '')
        r = {'ios': i, 'android': a, 'sheet': s}
        if s and dE(s, a) > 0.05 and dE(s, i) > 0.05: s = None          # sheet color is for another role here
        if s and s in (a, i):
            other = i if s == a else a
            ev = 'agree+sheet' if a == i else ('sheet+drift' if drift(s) == other else 'sheet')
            r.update(value=s, evidence=ev, fix=None if a == i else ('ios' if s == a else 'android'))
        elif s and drift(s) == i:
            r.update(value=s, evidence='sheet+drift', fix='both' if a != s else 'ios')
        elif a == i:
            r.update(value=a, evidence='agree', fix=None)
        elif drift(a) == i:
            # DEC-08 (2026-10-26): a close mismatch the sheet can't confirm takes the iOS value (was Android under DEC-01)
            r.update(value=i, evidence='ios-close', fix='android', previous={'value': a, 'evidence': 'drift-rule'})
        else:
            r.update(value=None, evidence='unresolved', fix='ask')
        row['roles'][role] = r; stats[r['evidence']] = stats.get(r['evidence'], 0) + 1
    res.append(row)
json.dump({'rule': __doc__.strip().split('\n')[2:12], 'stats': stats, 'markets': res}, open(out, 'w'), indent=1)
print(stats)
for row in res:
    for role, r in row['roles'].items():
        if r['evidence'] in ('sheet', 'sheet+drift', 'unresolved') and r['ios'] != r['android']:
            print(row['code'], role, r['evidence'], 'iOS', r['ios'], 'And', r['android'], 'sheet', r['sheet'], '->', r['value'], 'fix', r['fix'])

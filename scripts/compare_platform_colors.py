"""Compare brand color roles between iOS and Android market data.
Usage: python3 compare_platform_colors.py ios-markets.json android-markets.json out.json
Buckets per market x role:  match (same hex) | near (OKLab dE < NEAR) | differ
Role ownership: core (both platforms have the role) | ios-only | android-only
"""
import json, math, sys, collections
NEAR = 0.012   # same threshold the iOS merge-candidates step used (CLR-06)
CLOSE = 0.05   # "could match later": visibly similar, a design decision
ios = json.load(open(sys.argv[1])); andr = json.load(open(sys.argv[2])); out = sys.argv[3]

def hx(h): h = h.lstrip('#'); h = h[2:] if len(h) == 8 and h.upper().startswith('FF') else h[:6]; return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))
def norm(h): return None if not h or not h.startswith('#') else '#' + ''.join('%02x' % round(v*255) for v in hx(h))
def lin(c): return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
def oklab(h):
    r, g, b = [lin(v) for v in hx(h)]
    l = (0.4122214708*r+0.5363325363*g+0.0514459929*b)**(1/3); m = (0.2119034982*r+0.6806995451*g+0.1073969566*b)**(1/3); s = (0.0883024619*r+0.2817188376*g+0.6299787005*b)**(1/3)
    return (0.2104542553*l+0.7936177850*m-0.0040720468*s, 1.9779984951*l-2.4285922050*m+0.4505937099*s, 0.0259040371*l+0.7827717662*m-0.8086757660*s)
def dE(a, b): return math.dist(oklab(a), oklab(b))
def lum(h): r, g, b = [lin(v) for v in hx(h)]; return 0.2126*r+0.7152*g+0.0722*b
def cr(a, b): x, y = sorted([lum(a), lum(b)], reverse=True); return (x+0.05)/(y+0.05)

iv = lambda m, t: m['values'][ios['tokens'].index(t)]
av = lambda m, t: m['values'][andr['tokens'].index(t)]
# Shared roles: (core role, iOS getter, Android getter, iOS source, Android source)
SHARED = [
 ('navbar',    lambda m: m['core']['navbar'],    lambda m: m['core']['bar'],       'navigationBarBackgroundColor', 'Toolbar_Background'),
 ('navtext',   lambda m: m['core']['navtext'],   lambda m: m['core']['bartext'],   'navigationBarTitleColor', 'Toolbar_Text_Primary'),
 ('tabbar',    lambda m: m['core']['tabbar'],    lambda m: m['core']['bar'],       'tabBarBackgroundColor', 'NavigationBar_Background (= Toolbar_Background)'),
 ('tabactive', lambda m: m['core']['tabactive'], lambda m: m['core']['navactive'], 'tabBarSelectedTintColor', 'NavigationBar_Icon_ActiveTintColor'),
 ('tabinactive', lambda m: iv(m, 'tabBarUnselectedTintColor'), lambda m: m['core']['bartext'], 'tabBarUnselectedTintColor', 'NavigationBar_Icon_InactiveTintColor (= Toolbar_Text_Primary)'),
 ('action',    lambda m: m['core']['action'],    lambda m: m['core']['action'],    'paywallPrimaryActionColor', 'Paywall_PurchaseButton_Background'),
 ('alert',     lambda m: m['core']['alert'],     lambda m: '#cf000e',              'breakingNewsBannerBackgroundColor', 'br_news_red (fixed)'),
]
# Candidates: roles that exist on one platform; test whether a likely counterpart already lines up
CANDIDATES = [
 ('buy',    lambda m: iv(m, 'paywallViewPurchaseButtonColor'), lambda m: m['core']['buy'], 'paywallViewPurchaseButtonColor', 'Paywall_BuyButton_Background'),
 ('accent', lambda m: iv(m, 'alertTopicCellSwitchTint'), lambda m: m['core']['accent'], 'alertTopicCellSwitchTint', 'MainStyle_Accent'),
]
ONLY = {'ios': [('header', 'Style.json cell-tertiary-headerBg', 'Section-front header band; Android has no equivalent band')],
        'android': [('statusbar', 'MainStyle_Primary_Dark', 'Status bar; iOS status bar takes the nav bar color'),
                    ('continue', 'btn_continue', 'Your News Continue button + checked topic box; iOS uses pre-colored Continue-* PNGs')]}

A = {m['code']: m for m in andr['markets']}
def bucket(x, y):
    if x is None or y is None: return 'n/a', None
    d = dE(x, y)
    return ('match' if x == y else 'near' if d < NEAR else 'close' if d < CLOSE else 'differ'), round(d, 4)

rows, roleStats = [], collections.defaultdict(collections.Counter)
for im in sorted(ios['markets'], key=lambda m: m['name']):
    if im['code'] not in A:
        print('skip', im['code'], '(iOS only: no Android build yet; handled by apply_new_markets.py)'); continue
    am = A[im['code']]; r = {'code': im['code'], 'name': im['name'], 'template': im['template'], 'roles': {}}
    for role, gi, ga, *_ in SHARED + CANDIDATES:
        x, y = norm(gi(im)), norm(ga(am)); b, d = bucket(x, y)
        r['roles'][role] = {'ios': x, 'android': y, 'bucket': b, 'dE': d}; roleStats[role][b] += 1
    r['ios_only'] = {'header': norm(im['core']['header'])}
    r['android_only'] = {'statusbar': norm(am['core']['statusbar']), 'continue': norm(am['core']['continue'])}
    shared = [r['roles'][k]['bucket'] for k, *_ in SHARED]
    r['shared_match'] = sum(b in ('match', 'near') for b in shared); r['shared_total'] = len(shared)
    rows.append(r)

# Android palettes (same 7 shared roles as iOS minus header, so the two counts are comparable)
keyA = lambda r: tuple(r['roles'][k]['android'] for k in ('navbar', 'navtext', 'tabactive', 'action'))
keyI = lambda r: tuple(r['roles'][k]['ios'] for k in ('navbar', 'navtext', 'tabactive', 'action'))
palA = collections.defaultdict(list); palI = collections.defaultdict(list)
for r in rows: palA[keyA(r)].append(r['code']); palI[keyI(r)].append(r['code'])

# Unique hexes per platform across brand roles, and overlap
hexI = {r['roles'][k]['ios'] for r in rows for k in ('navbar', 'navtext', 'tabbar', 'tabactive', 'action', 'alert')} | {r['ios_only']['header'] for r in rows}
hexA = {r['roles'][k]['android'] for r in rows for k in ('navbar', 'navtext', 'tabactive', 'action', 'alert', 'buy', 'accent')} | {v for r in rows for v in r['android_only'].values()}
hexI.discard(None); hexA.discard(None)
nearCross = sorted({(a, b, round(dE(a, b), 4)) for a in hexA - hexI for b in hexI if dE(a, b) < NEAR}, key=lambda t: (t[2], t[0], t[1]))

# Contrast checks on Android, same targets as iOS
checks = collections.Counter()
for r in rows:
    R = r['roles']
    if cr(R['navtext']['android'], R['navbar']['android']) < 4.5: checks['nav title'] += 1
    if cr(R['tabactive']['android'], R['navbar']['android']) < 3: checks['selected tab'] += 1
    if cr('#ffffff', R['action']['android']) < 4.5: checks['button label'] += 1

res = {'sources': {'ios': ios['source'], 'android': andr['source']},
       'thresholds': {'near_dE': NEAR, 'close_dE': CLOSE},
       'shared_roles': [{'role': k, 'ios': si, 'android': sa} for k, gi, ga, si, sa in SHARED],
       'candidate_roles': [{'role': k, 'ios': si, 'android': sa} for k, gi, ga, si, sa in CANDIDATES],
       'platform_only_roles': ONLY,
       'role_stats': {k: dict(v) for k, v in roleStats.items()},
       'palettes': {'ios_unique_4role': len(palI), 'android_unique_4role': len(palA)},
       'unique_hex': {'ios': len(hexI), 'android': len(hexA), 'shared': len(hexI & hexA), 'ios_only': sorted(hexI - hexA), 'android_only': sorted(hexA - hexI), 'android_near_ios': nearCross},
       'android_contrast_fails': dict(checks),
       'markets_fully_matching_shared': sorted(r['code'] for r in rows if r['shared_match'] == r['shared_total']),
       'markets': rows}
json.dump(res, open(out, 'w'), indent=1)
print(json.dumps({k: res[k] for k in ('role_stats', 'palettes', 'android_contrast_fails')}, indent=0))
print('hex', {k: (len(v) if isinstance(v, list) else v) for k, v in res['unique_hex'].items()})
print('fully matching', len(res['markets_fully_matching_shared']), res['markets_fully_matching_shared'])

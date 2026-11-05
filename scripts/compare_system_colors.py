"""System colors, step 1 (PROGRESS 1.4): every themed color both apps ship, per market, compared and grouped.

Usage: python3 scripts/compare_system_colors.py
Reads:  data/source/markets.json (iOS TroncKit @ e30ad2585, 124 themed colors x 77 markets)
        data/source/android-markets.json (android-tribpub @ 1cfb069a6, 136 colors x 77 markets)
        data/system-color-pairs.json (proposed iOS <-> Android pairs; not confirmed by the Apps team)
        data/control-colors.json, data/shell-colors.json (colors that already have tokens)
Writes: data/system-color-comparison.json, docs/SYSTEM-COLORS.md

For each color on each platform:
  covered   already a token (brand role, app shell, control or button): listed, not re-classified
  kind      fixed        same value in all 77 markets                      -> one System variable
            follows      equals one of the market's own brand roles in most markets -> alias of that role
            majority     one value in >= 39 markets, the rest are exceptions
            per-market   no value reaches 39 markets
Palettes: each market's system colors, with brand-following values written as the role (=action) so markets that
differ only by brand color land in the same palette. Markets with identical palettes are grouped; every market is
in exactly one group, so every market's full palette is documented (majority palette + that group's differences).
Pairs: value agreement per market (OKLab dE < 0.012 = same, < 0.05 = close), and the ownership bucket.
Nothing here is a token yet: step 2 (tokens + Figma System collection) waits on Karl's review.
"""
import json, math
from collections import Counter, defaultdict

IOS = json.load(open('data/source/markets.json')); AND = json.load(open('data/source/android-markets.json'))
PAIRS = json.load(open('data/system-color-pairs.json'))
CTRL = json.load(open('data/control-colors.json'))
N = 77; MAJ = 39

def norm(h):
    """Lower-case #rrggbb; Android #AARRGGBB keeps its alpha as #rrggbbaa only when not opaque. None = not set."""
    if not h: return None
    if not h.startswith('#'): return h                    # e.g. an Android selector, kept as written
    h = h.lower().lstrip('#')
    if len(h) == 8 and IS_ANDROID: return '#' + h[2:] if h[:2] == 'ff' else '#' + h[2:] + h[:2]
    return '#' + h
def hx(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
def lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def oklab(h):
    r, g, b = [lin(v) for v in hx(h)]
    l = (0.4122214708*r+0.5363325363*g+0.0514459929*b)**(1/3); m = (0.2119034982*r+0.6806995451*g+0.1073969566*b)**(1/3); s = (0.0883024619*r+0.2817188376*g+0.6299787005*b)**(1/3)
    return (0.2104542553*l+0.7936177850*m-0.0040720468*s, 1.9779984951*l-2.4285922050*m+0.4505937099*s, 0.0259040371*l+0.7827717662*m-0.8086757660*s)
def dE(a, b):
    if a is None or b is None or not a.startswith('#') or not b.startswith('#'): return 0 if a == b else 9
    if len(a) != len(b): return 9                        # one has alpha, the other not
    return math.dist(oklab(a[:7]), oklab(b[:7])) + (0 if len(a) == 7 else abs(int(a[7:], 16) - int(b[7:], 16)) / 255)
rgb = lambda h: ', '.join(str(int(h[i:i + 2], 16)) for i in (1, 3, 5)) + (f', alpha {round(int(h[7:], 16) / 255, 2)}' if len(h) == 9 else '')
fmt = lambda h: '`not set` (system default)' if h is None else (f'`{h}`' if not h.startswith('#') else f'`{h}` · {rgb(h)}')

# Colors that already have tokens (so the system set is what's left)
COVERED = {
    'ios': {'navigationBarBackgroundColor': 'brand navbar', 'navigationBarTitleColor': 'brand navtext', 'navigationBarItemTintColor': 'brand navicon',
            'tabBarBackgroundColor': 'brand tabbar', 'tabBarSelectedTintColor': 'brand tabactive', 'tabBarUnselectedTintColor': 'brand tabinactive',
            'paywallPrimaryActionColor': 'brand action', 'paywallViewPurchaseButtonColor': 'brand buy (= action)',
            'breakingNewsBannerBackgroundColor': 'brand alert', 'breakingNewsBannerTextColor': 'brand alerttext',
            'sectionBarBackgroundColor': 'shell sectiontabbar', 'sectionBarTextColor': 'shell sectiontabtext',
            'sectionBarSelectedTextColor': 'shell sectiontabselected', 'sectionBarSelectedUnderBarColor': 'shell sectiontabindicator',
            'paywallLinkColor': 'button link'},
    'android': {'Toolbar_Background': 'brand navbar', 'Toolbar_Text_Primary': 'brand navtext', 'NavigationBar_Background': 'brand tabbar',
                'NavigationBar_Icon_ActiveTintColor': 'brand tabactive', 'NavigationBar_Icon_InactiveTintColor': 'brand tabinactive',
                'Paywall_LoginButton_Background': 'brand action', 'Paywall_PurchaseButton_Background': 'brand action (shared role)', 'MainStyle_Primary_Dark': 'statusbar (= navbar, DEC-15)',
                'Toolbar_Tabs_Background': 'shell sectiontabbar', 'Toolbar_Tabs_Text': 'shell sectiontabtext',
                'Toolbar_Tabs_Text_Selected': 'shell sectiontabselected', 'Toolbar_Tabs_Indicator': 'shell sectiontabindicator',
                'bottom_nav_selected_text_color': 'shell tablabelactive', 'bottom_nav_deselected_text_color': 'shell tablabelinactive',
                'Text_Disabled_Font': 'button disabled label'}}
for x in CTRL['follow'] + CTRL['const']:
    COVERED[x['platform']].setdefault(x['key'], 'control: ' + x['what'])

# Brand roles per market as each app ships them (for "follows")
# (aliases are left out: header/statusbar = navbar (DEC-15), buy/continue = action, so a color points at the real role)
ROLEMAP = {'ios': {'navbar': 'navbar', 'navtext': 'navtext', 'tabbar': 'tabbar', 'tabactive': 'tabactive', 'action': 'action', 'alert': 'alert'},
           'android': {'bar': 'navbar', 'bartext': 'navtext', 'navactive': 'tabactive', 'accent': 'accent', 'action': 'action'}}

OUT = {'generated_by': 'scripts/compare_system_colors.py', 'sources': {'ios': IOS['source'], 'android': AND['source']},
       'thresholds': {'same': 0.012, 'close': 0.05, 'majority_markets': MAJ}, 'platforms': {}}
for plat, D in (('ios', IOS), ('android', AND)):
    IS_ANDROID = plat == 'android'
    markets = sorted(D['markets'], key=lambda m: m['code'])
    codes = [m['code'] for m in markets]
    roles = {m['code']: {ROLEMAP[plat][k]: norm(v) for k, v in m['core'].items() if k in ROLEMAP[plat]} for m in markets}
    proto = dict(zip(D['tokens'], D.get('protocols', [None] * len(D['tokens']))))
    colors = []
    for i, key in enumerate(D['tokens']):
        vals = {m['code']: norm(m['values'][i]) for m in markets}
        cnt = Counter(vals.values()); top, topn = cnt.most_common(1)[0]
        # best brand role this color follows (same as the market's own role, near-identical allowed)
        fol = max(((r, sum(1 for c in codes if r in roles[c] and vals[c] is not None and dE(vals[c], roles[c][r]) < 0.012))
                   for r in set().union(*[roles[c].keys() for c in codes])), key=lambda t: t[1])
        if topn == N: kind = 'fixed'
        elif fol[1] >= MAJ and fol[1] > topn: kind = 'follows'
        elif topn >= MAJ: kind = 'majority'
        else: kind = 'per-market'
        groups = defaultdict(list)
        for c in codes: groups[vals[c]].append(c)
        exceptions = {}
        if kind == 'follows':
            exceptions = {c: vals[c] for c in codes if not (fol[0] in roles[c] and vals[c] is not None and dE(vals[c], roles[c][fol[0]]) < 0.012)}
        elif kind == 'majority':
            exceptions = {c: vals[c] for c in codes if vals[c] != top}
        colors.append({'key': key, 'protocol': proto.get(key), 'covered_by': COVERED[plat].get(key),
                       'kind': kind, 'majority': top, 'majority_markets': topn,
                       'follows': fol[0] if kind == 'follows' else None, 'follows_markets': fol[1] if kind == 'follows' else None,
                       'not_set_markets': [c for c in codes if vals[c] is None],
                       'exceptions': exceptions,
                       'values': sorted(({'value': v, 'markets': ms} for v, ms in groups.items()), key=lambda g: -len(g['markets'])),
                       'by_market': vals})
    # Palettes: system colors only (not covered); brand-following values written as the role
    # The launcher-icon backdrop is an app-icon asset (23 values), not UI color: listed with the colors, left out of palettes
    PALETTE_SKIP = {'ic_launcher_background'}
    sysc = [c for c in colors if not c['covered_by'] and c['key'] not in PALETTE_SKIP]
    def sym(col, code):
        v = col['by_market'][code]
        if col['kind'] == 'follows' and col['follows'] in roles[code] and v is not None and dE(v, roles[code][col['follows']]) < 0.012: return '=' + col['follows']
        return v
    base = {c['key']: ('=' + c['follows'] if c['kind'] == 'follows' else c['majority']) for c in sysc}
    pal = defaultdict(list)
    for code in codes: pal[tuple(sym(c, code) for c in sysc)].append(code)
    palettes = []
    for n, (vec, ms) in enumerate(sorted(pal.items(), key=lambda t: (-len(t[1]), t[1][0])), 1):
        diff = {c['key']: v for c, v in zip(sysc, vec) if v != base[c['key']]}
        palettes.append({'id': f"{'I' if plat == 'ios' else 'A'}{n:02d}", 'markets': ms, 'differences_from_majority': diff})
    names = {m['code']: m['name'] for m in markets}
    OUT['platforms'][plat] = {'markets': names, 'templates': {m['code']: m.get('template') for m in markets} if plat == 'ios' else None,
                              'colors': colors, 'majority_palette': base, 'palettes': palettes,
                              'summary': {'colors': len(colors), 'covered': sum(1 for c in colors if c['covered_by']),
                                          **Counter(c['kind'] for c in sysc), 'palettes': len(palettes)}}

# Pairs: value agreement market by market and ownership bucket
ci = {c['key']: c for c in OUT['platforms']['ios']['colors']}; ca = {c['key']: c for c in OUT['platforms']['android']['colors']}
pairs = []
for p in PAIRS['pairs']:
    a, b = ci[p['ios']], ca[p['android']]
    IS_ANDROID = False
    common = sorted(set(a['by_market']) & set(b['by_market']))
    same = [c for c in common if dE(a['by_market'][c], b['by_market'][c]) < 0.012]
    close = [c for c in common if 0.012 <= dE(a['by_market'][c], b['by_market'][c]) < 0.05]
    differ = [c for c in common if dE(a['by_market'][c], b['by_market'][c]) >= 0.05]
    if a['kind'] == b['kind'] == 'follows' and a['follows'] == b['follows']: bucket, why = 'Core alias', f"both follow {a['follows']}"
    elif len(same) >= MAJ and dE(a['majority'], b['majority']) < 0.012: bucket, why = 'Core', f'same value in {len(same)} of {len(common)} markets'
    else: bucket, why = 'Core, per-platform value', f'iOS {a["majority"]} ({a["kind"]}) vs Android {b["majority"]} ({b["kind"]})'
    check = 'values never match: pairing or design differs, ask Apps team' if not same and not close else ''
    pairs.append({**p, 'check': check, 'markets_compared': len(common), 'same': len(same), 'close': len(close), 'differ': len(differ),
                  'differ_markets': differ, 'bucket': bucket, 'why': why,
                  'ios_majority': a['majority'], 'android_majority': b['majority'], 'ios_kind': a['kind'], 'android_kind': b['kind']})
OUT['pairs'] = pairs; OUT['pairs_status'] = PAIRS['status']
paired = {'ios': {p['ios'] for p in pairs}, 'android': {p['android'] for p in pairs}}
for plat in ('ios', 'android'):
    for c in OUT['platforms'][plat]['colors']:
        c['bucket'] = (None if c['covered_by'] else
                       next(p['bucket'] for p in pairs if p[plat] == c['key']) if c['key'] in paired[plat] else
                       ('iOS only (until pairing confirmed)' if plat == 'ios' else 'Android only (until pairing confirmed)'))
json.dump(OUT, open('data/system-color-comparison.json', 'w'), indent=1)

# ---- docs/SYSTEM-COLORS.md ------------------------------------------------------------------------------------
P = OUT['platforms']; L = []
L += ['# System colors: iOS vs Android, every market', '',
      'Generated by `scripts/compare_system_colors.py` from `data/source/markets.json` (TroncKit @ e30ad2585) and '
      '`data/source/android-markets.json` (android-tribpub @ 1cfb069a6). Do not edit by hand. Data: `data/system-color-comparison.json`.', '',
      '**Step 1 (review only).** Nothing here is a token yet. Step 2, after Karl\'s review: tokens for every market '
      '(fixed colors in one System collection, the rest per market, with markets that share a palette noted together), Figma variables, Swift and Kotlin.', '',
      '## Summary', '',
      '| | iOS | Android |', '|---|---|---|']
for k, label in [('colors', 'Themed colors in the export'), ('covered', 'Already tokens (brand, app shell, controls, buttons)'),
                 ('fixed', 'Fixed: same in all 77 markets'), ('follows', 'Follows a brand role (alias)'), ('majority', 'Majority value + exceptions'),
                 ('per-market', 'Per market (no value in 39+ markets)'), ('palettes', 'Distinct market palettes')]:
    L.append(f"| {label} | {P['ios']['summary'].get(k, 0)} | {P['android']['summary'].get(k, 0)} |")
nb = Counter(p['bucket'] for p in pairs)
L += ['', f"Proposed iOS ↔ Android pairs: {len(pairs)} ({', '.join(f'{v} {k}' for k, v in nb.items())}). The rest are platform-only until the Apps team confirms the pairing (MISSING-ASSETS 3.4).", '',
      'How to read a value: hex · R, G, B (0–255). `not set` = iOS leaves it to the UIKit system default (MISSING-ASSETS 3.1). '
      'Android colors with transparency show alpha. "Follows" means the color equals that market\'s own brand role as the app ships it.', '']

L += ['## iOS ↔ Android pairs (proposed)', '',
      '| What | iOS | Android | Same / close / differ (markets) | iOS value | Android value | Bucket | Check |', '|---|---|---|---|---|---|---|---|']
for p in pairs:
    show = lambda kind, maj, fol: f'follows {fol}' if kind == 'follows' else fmt(maj) + ('' if kind == 'fixed' else f' ({kind})')
    L.append(f"| {p['what']} | `{p['ios']}` | `{p['android']}` | {p['same']} / {p['close']} / {p['differ']} | "
             f"{show(p['ios_kind'], p['ios_majority'], ci[p['ios']]['follows'])} | {show(p['android_kind'], p['android_majority'], ca[p['android']]['follows'])} | {p['bucket']} | {p['check'] or '—'} |")

for plat, title in (('ios', 'iOS'), ('android', 'Android')):
    D = P[plat]; nm = D['markets']
    L += ['', f'## {title}: every color', '',
          '| Color | Kind | Value (majority) | Markets | Exceptions / other values | Already a token / bucket |', '|---|---|---|---|---|---|']
    for c in sorted(D['colors'], key=lambda c: (c['covered_by'] is not None, ['fixed', 'follows', 'majority', 'per-market'].index(c['kind']), c['key'])):
        if c['kind'] == 'follows':
            val, n = f"= {c['follows']}", c['follows_markets']
            exc = ', '.join(f"{k} {fmt(v)}" for k, v in sorted(c['exceptions'].items()))
        elif c['kind'] == 'per-market':
            val, n = fmt(c['majority']), c['majority_markets']
            exc = f"{len(c['values'])} values: " + '; '.join(f"{fmt(g['value'])} ×{len(g['markets'])}" for g in c['values'][:6]) + (' …' if len(c['values']) > 6 else '')
        else:
            val, n = fmt(c['majority']), c['majority_markets']
            exc = ', '.join(f"{k} {fmt(v)}" for k, v in sorted(c['exceptions'].items()))
        L.append(f"| `{c['key']}` | {c['kind']} | {val} | {n} | {exc or '—'} | {('token: ' + c['covered_by']) if c['covered_by'] else c['bucket']} |")
    L += ['', f'## {title}: market palettes', '',
          f"Each market's system colors (the {len([c for c in D['colors'] if not c['covered_by']])} colors above that are not tokens yet). "
          'The majority palette is the value in the "Value" column for every color; each group below lists only where its markets differ. '
          'Markets in the same group have identical system palettes (brand-following colors compared as the role, so they still take each market\'s brand color). '
          f"{len(D['palettes'])} palettes for 77 markets." + (' Android `ic_launcher_background` (the app-icon backdrop, 23 values) is left out of the grouping; its value per market is in the color table above.' if plat == 'android' else ''), '']
    for g in D['palettes']:
        tpl = D['templates'] or {}
        ms = ', '.join(f'{c} ({nm[c]}' + (', legacy template' if tpl.get(c) == 'legacy' else '') + ')' for c in g['markets'])
        L.append(f"### {g['id']} · {len(g['markets'])} market{'s' if len(g['markets']) != 1 else ''}" + (' · majority palette' if not g['differences_from_majority'] else ''))
        L += ['', ms, '']
        if g['differences_from_majority']:
            L += ['| Color | This palette | Majority |', '|---|---|---|']
            for k, v in g['differences_from_majority'].items():
                b = D['majority_palette'][k]
                L.append(f"| `{k}` | {v if str(v).startswith('=') else fmt(v)} | {b if str(b).startswith('=') else fmt(b)} |")
            L.append('')
open('docs/SYSTEM-COLORS.md', 'w').write('\n'.join(L) + '\n')
for plat in ('ios', 'android'): print(plat, P[plat]['summary'])
print('pairs', dict(nb))

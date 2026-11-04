"""App shell colors (DEC-13): the per-market colors of the top bar, section tabs and bottom tab bar.
DEC-14 majority rule (Karl, 2026-11-04): each role is built with the majority value; markets that ship something else
are listed in docs/SHELL-EXCEPTIONS.md and NOT built.
Usage: python3 scripts/build_shell_colors.py   (after build_tokens.py; then `npm run build`)
Reads:  data/source/markets.json (iOS), data/source/android-markets.json, tokens/core/brand.tokens.json (markets, TDH)
Writes: tokens/core/shell.tokens.json      color.brand.<m>.navicon   alias of navtext (both apps: icon tint = title color in all 77 markets)
        tokens/ios/shell.tokens.json       color.ios.<m>.sectiontab*                       (iOS section bar, majority value)
        tokens/android/shell.tokens.json   color.android.<m>.sectiontab*, tablabel*       (Android section tabs + bottom-nav labels; aliases of the Core roles they follow in the majority)
        data/shell-colors.json             the same values for the Figma build and docs (plus shipped exceptions)
        docs/SHELL-EXCEPTIONS.md           exception markets, documented only
Per DEC-09/DEC-13 each app keeps its own production colors (the two apps design section tabs differently).
Values already covered elsewhere: top bar navbar/navtext, tab bar tabbar/tabactive/tabinactive, banner alert/alerttext (Core brand roles).
TDH (Daily Herald, provisional, no app yet) takes the standard-template values: iOS #ffffff/#333333; Android follows its top bar.
"""
import json
from collections import Counter
BRAND = json.load(open('tokens/core/brand.tokens.json'))['color']['brand']
def load(fn):
    d = json.load(open(fn)); T = {t: i for i, t in enumerate(d['tokens'])}
    return {m['code'].lower(): {k: (m['values'][i] or '').lower() for k, i in T.items()} for m in d['markets']}
I, A = load('data/source/markets.json'), load('data/source/android-markets.json')
hexn = lambda h: '#' + h.lstrip('#')[-6:] if h else None        # Android #AARRGGBB -> #RRGGBB
rgb = lambda h: [int(h[i:i + 2], 16) for i in (1, 3, 5)]

IOS_ROLES = {'sectiontabbar': ('sectionBarBackgroundColor', 'Section bar background'),
             'sectiontabtext': ('sectionBarTextColor', 'Section name'),
             'sectiontabselected': ('sectionBarSelectedTextColor', 'Selected section name'),
             'sectiontabindicator': ('sectionBarSelectedUnderBarColor', 'Selected section underline')}
AND_ROLES = {'sectiontabbar': ('Toolbar_Tabs_Background', 'Section tabs background'),
             'sectiontabtext': ('Toolbar_Tabs_Text', 'Section tab name'),
             'sectiontabselected': ('Toolbar_Tabs_Text_Selected', 'Selected section tab name'),
             'sectiontabindicator': ('Toolbar_Tabs_Indicator', 'Selected section tab indicator'),
             'tablabelactive': ('bottom_nav_selected_text_color', 'Selected bottom-nav label'),
             'tablabelinactive': ('bottom_nav_deselected_text_color', 'Other bottom-nav labels')}
# iOS majority per role (74 of 77 markets: white bar, #333333 text and underline)
IOS_MAJ = {r: Counter(hexn(I[k][src]) for k in I).most_common(1)[0][0] for r, (src, _) in IOS_ROLES.items()}
EXC = []   # (platform, market code, market, role, source key, shipped, built)
IOS_STD = {'sectiontabbar': '#ffffff', 'sectiontabtext': '#333333', 'sectiontabselected': '#333333', 'sectiontabindicator': '#333333'}

def tok(h, desc, **ext): return {'$value': h, '$type': 'color', '$description': desc, '$extensions': {'mng': dict(rgb=rgb(h), **ext)}}
core, ios, andr, data = {}, {}, {}, {}
for k in sorted(BRAND):
    name = BRAND[k]['navbar']['$extensions']['mng']['market']
    core[k] = {'navicon': {'$value': '{color.brand.%s.navtext}' % k, '$type': 'color',
                           '$description': 'Top bar icon tint: same as navtext in all 77 markets on both apps (DEC-13)'}}
    ios[k], andr[k], data[k] = {}, {}, {'market': name, 'ios': {}, 'android': {}}
    for role, (src, desc) in IOS_ROLES.items():
        h = IOS_MAJ[role]
        shipped = hexn(I[k][src]) if k in I else h
        if shipped != h: EXC.append(('iOS', k, name, role, src, shipped, h))
        ios[k][role] = tok(h, f'{name}: {desc} (iOS `{src}`, majority value; DEC-14)', market=name, source=src, provisional=k not in I)
        data[k]['ios'][role] = h
    # Android: section tabs follow the top bar and tab labels follow the tab icons in production (all markets but CT /
    # DP, MC, NYDN, OS, TSAR). Where that holds, the role is an alias of the Core role, so it follows Core decisions;
    # where production breaks the pattern, the shipped value is kept (DEC-13).
    FOLLOW = {'sectiontabbar': ('Toolbar_Background', 'navbar'), 'sectiontabtext': ('Toolbar_Text_Primary', 'navtext'),
              'sectiontabselected': ('Toolbar_Text_Primary', 'navtext'), 'sectiontabindicator': ('Toolbar_Text_Primary', 'navtext'),
              'tablabelactive': ('NavigationBar_Icon_ActiveTintColor', 'tabactive'), 'tablabelinactive': ('NavigationBar_Icon_InactiveTintColor', 'tabinactive')}
    for role, (src, desc) in AND_ROLES.items():
        base_src, core_role = FOLLOW[role]
        follows = k not in A or hexn(A[k][src]) == hexn(A[k][base_src])
        if not follows and hexn(A[k][src]) != BRAND[k][core_role]['$value']: EXC.append(('Android', k, name, role, src, hexn(A[k][src]), BRAND[k][core_role]['$value']))
        if True:   # DEC-14: every market follows the Core role; exceptions documented only
            andr[k][role] = {'$value': '{color.brand.%s.%s}' % (k, core_role), '$type': 'color',
                             '$description': f'{name}: {desc}; follows {core_role} (Android ships it equal to `{base_src}`)',
                             '$extensions': {'mng': {'market': name, 'source': src, 'follows': core_role, 'provisional': k not in A}}}
            data[k]['android'][role] = BRAND[k][core_role]['$value']
        data[k].setdefault('android_follows', {})[role] = follows

meta = {'$description': 'Generated by scripts/build_shell_colors.py (DEC-13, DEC-14). Majority values; exceptions in docs/SHELL-EXCEPTIONS.md. Do not edit by hand.'}
json.dump({**meta, 'color': {'brand': core}}, open('tokens/core/shell.tokens.json', 'w'), indent=1)
json.dump({**meta, 'color': {'ios': ios}}, open('tokens/ios/shell.tokens.json', 'w'), indent=1)
json.dump({**meta, 'color': {'android': andr}}, open('tokens/android/shell.tokens.json', 'w'), indent=1)
json.dump({'generated_by': 'scripts/build_shell_colors.py', 'roles': {'ios': list(IOS_ROLES), 'android': list(AND_ROLES)}, 'markets': data,
           'exceptions': [dict(zip(('platform', 'code', 'market', 'role', 'source', 'shipped', 'built'), e)) for e in EXC]},
          open('data/shell-colors.json', 'w'), indent=1)
L = ['# App shell colors: exception markets', '', 'Generated by `scripts/build_shell_colors.py`. Do not edit by hand.', '',
     'DEC-14 (Karl, 2026-11-04): the app shell is built with the majority value for every role. The markets below ship something else; '
     'they are **documented, not built**. Future: bring them in line or confirm them as a market-specific design.', '',
     '| Platform | Market | Role | Source key | Shipped | Built (majority) |', '|---|---|---|---|---|---|']
for p, k, n, r, src, sh, b in EXC:
    L.append(f'| {p} | {n} ({k.upper()}) | {r} | `{src}` | `{sh}` · {", ".join(map(str, rgb(sh)))} | `{b}` · {", ".join(map(str, rgb(b)))} |')
open('docs/SHELL-EXCEPTIONS.md', 'w').write('\n'.join(L) + '\n')
print(len(EXC), 'exceptions documented')
print(len(data), 'markets; iOS roles', len(IOS_ROLES), 'Android roles', len(AND_ROLES))

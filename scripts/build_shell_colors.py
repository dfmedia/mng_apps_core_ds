"""App shell colors (DEC-13): the per-market colors of the top bar, section tabs and bottom tab bar.
DEC-14 majority rule (Karl, 2026-11-04): each role is built with the majority value; markets that ship something else
are listed in docs/SHELL-EXCEPTIONS.md and NOT built.
DEC-15 (Karl, 2026-11-05): iOS `header` and Android `statusbar` follow the top bar (alias of Core navbar, written by
build_tokens.py). Markets whose app ships them different from its own top bar are exceptions: documented here with a
suggested override and drawn side by side in Figma (data/shell-colors.json `role_exceptions`); accepted ones (data/shell-overrides.json) are built.
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

# ---- DEC-15: header (iOS) and statusbar (Android) follow navbar; exceptions with a suggested override ----------
import math
def _hx(h): h = h.lstrip('#'); h = h[-6:]; return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
def _lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def _oklab(h):
    r, g, b = [_lin(v) for v in _hx(h)]
    l = (0.4122214708*r+0.5363325363*g+0.0514459929*b)**(1/3); m = (0.2119034982*r+0.6806995451*g+0.1073969566*b)**(1/3); q = (0.0883024619*r+0.2817188376*g+0.6299787005*b)**(1/3)
    return (0.2104542553*l+0.7936177850*m-0.0040720468*q, 1.9779984951*l-2.4285922050*m+0.4505937099*q, 0.0259040371*l+0.7827717662*m-0.8086757660*q)
dE = lambda a, b: math.dist(_oklab(a), _oklab(b))
def _lum(h): r, g, b = [_lin(v) for v in _hx(h)]; return 0.2126*r + 0.7152*g + 0.0722*b
def cr(a, b): x, y = sorted([_lum(a), _lum(b)], reverse=True); return round((x + 0.05) / (y + 0.05), 2)
CORE_ROLES = ['navbar', 'navtext', 'tabbar', 'tabactive', 'tabinactive', 'action']
IOS_SRC = json.load(open('data/source/markets.json')); AND_SRC = json.load(open('data/source/android-markets.json'))
HT = IOS_SRC['styleKeys'].index('cell-tertiary-headertext')
FOLLOW_ROLES = [
    # platform, role, shipped getter, own top bar getter, foreground on it, fg source, target, what the fg is
    ('iOS', 'header', 'Style.json cell-tertiary-headerBg', lambda m: m['core']['header'], lambda m: m['core']['navbar'],
     lambda m: m['style'][HT], 'Style.json cell-tertiary-headertext', 4.5, 'section title text'),
    ('Android', 'statusbar', 'MainStyle_Primary_Dark', lambda m: m['core']['statusbar'], lambda m: m['core']['bar'],
     lambda m: '#ffffff', 'Android 14 and below: light (white) status-bar icons; the main theme never sets windowLightStatusBar (Ameer M., confirmed on device 2026-11-10, MISSING-ASSETS 5.6)', 3.0, 'status-bar icons'),
]
ROLE_EXC = []
OVR = json.load(open('data/shell-overrides.json'))     # accepted by Karl 2026-11-05: these are built as override tokens
for plat, role, src, g_role, g_bar, g_fg, fg_src, target, fg_what in FOLLOW_ROLES:
    srcd = IOS_SRC if plat == 'iOS' else AND_SRC
    for m in srcd['markets']:
        k = m['code'].lower(); shipped, bar = hexn(g_role(m).lower()), hexn(g_bar(m).lower())
        if dE(shipped, bar) < 0.012: continue                      # follows its own top bar (same or near-identical)
        built = BRAND[k]['navbar']['$value']; fg = hexn(g_fg(m).lower()); name = BRAND[k]['navbar']['$extensions']['mng']['market']
        match = [r for r in CORE_ROLES if dE(shipped, BRAND[k][r]['$value']) < 0.012]
        ov = {'value': shipped, 'kind': 'market override (shipped value)', 'same_as': match}   # matching Core roles: information only
        accepted = k in OVR[role]
        ROLE_EXC.append({'platform': plat, 'code': k, 'market': name, 'role': role, 'source': src, 'shipped': shipped,
                         'shipped_topbar': bar, 'majority': built, 'built': shipped if accepted else built, 'accepted': accepted,
                         'built_alias': None if accepted else 'navbar', 'navtext': BRAND[k]['navtext']['$value'], 'override': ov,
                         'foreground': fg, 'foreground_source': fg_src, 'foreground_is': fg_what, 'target': target,
                         'contrast_majority': cr(fg, built), 'contrast_override': cr(fg, ov['value'])})
        if role == 'statusbar':   # DEC-15: Android 15+ version (Karl 2026-11-06; confirmed on device 2026-11-10)
            dark = k in OVR['statusbar_icons']['android15']['dark']; ic = '#000000' if dark else '#ffffff'
            ROLE_EXC[-1]['android15'] = {'statusbar': built, 'statusbar_alias': 'navbar', 'icons': 'dark' if dark else 'light',
                                         'icon_hex_for_contrast': ic, 'contrast': cr(ic, built), 'confirmed': dark,
                                         'note': 'Icon colors are drawn by the system; contrast shown for ' + ('black' if dark else 'white') + ' icons.'}
        if not accepted: EXC.append((plat, k, name, role, src, shipped, built))

meta = {'$description': 'Generated by scripts/build_shell_colors.py (DEC-13, DEC-14). Majority values; exceptions in docs/SHELL-EXCEPTIONS.md. Do not edit by hand.'}
json.dump({**meta, 'color': {'brand': core}}, open('tokens/core/shell.tokens.json', 'w'), indent=1)
json.dump({**meta, 'color': {'ios': ios}}, open('tokens/ios/shell.tokens.json', 'w'), indent=1)
json.dump({**meta, 'color': {'android': andr}}, open('tokens/android/shell.tokens.json', 'w'), indent=1)
json.dump({'generated_by': 'scripts/build_shell_colors.py', 'roles': {'ios': list(IOS_ROLES), 'android': list(AND_ROLES)}, 'markets': data,
           'role_exceptions': ROLE_EXC,
           'exceptions': [dict(zip(('platform', 'code', 'market', 'role', 'source', 'shipped', 'built'), e)) for e in EXC]},
          open('data/shell-colors.json', 'w'), indent=1)
L = ['# App shell colors: exception markets', '', 'Generated by `scripts/build_shell_colors.py`. Do not edit by hand.', '',
     'DEC-14 (Karl, 2026-11-04): the app shell is built with the majority value for every role. The markets below ship something else; '
     'they are **documented, not built**. Future: bring them in line or confirm them as a market-specific design.', '',
     '| Platform | Market | Role | Source key | Shipped | Built (majority) |', '|---|---|---|---|---|---|']
for p, k, n, r, src, sh, b in EXC:
    L.append(f'| {p} | {n} ({k.upper()}) | {r} | `{src}` | `{sh}` · {", ".join(map(str, rgb(sh)))} | `{b}` · {", ".join(map(str, rgb(b)))} |')
L += ['', '## Header band (iOS) and status bar (Android): market overrides', '',
      'DEC-15 (Karl, 2026-11-05): `header` and `statusbar` follow the top bar (`navbar`). In these markets the app ships them '
      'different from its own top bar, mostly because the top bar is white, so the majority build fails contrast. '
      '**Karl accepted every suggested override on 2026-11-05** (data/shell-overrides.json): these markets get an override token '
      'with the shipped color (`color.ios.<m>.header` / `color.android.<m>.statusbar`), built in tokens, Swift, Kotlin and Figma. '
      'Drawn majority vs override in Figma (iOS file: Components · App shell › 01 · Header band exceptions; Android file: › 01 · Status bar exceptions, '
      'with an Android 14 and below vs 15+ comparison). Android: the override is what Android 14 and below shows (white icons); on Android 15+ the status bar '
      'is navbar with dark icons in these markets (Ameer M., confirmed on device 2026-11-10; tokens `statusbar.android.<m>.icons` / `icons15`).', '',
      '| Platform | Market | Role | Majority (navbar) | On it | Override (shipped) | On it | Status | Target | Android 15+ |', '|---|---|---|---|---|---|---|---|---|---|']
fx = lambda h: f'`{h}` · {", ".join(map(str, rgb(h)))}'
a15 = lambda e: '—' if 'android15' not in e else f"navbar {fx(e['android15']['statusbar'])}, {e['android15']['icons']} icons: {e['android15']['contrast']}:1 {'✅' if e['android15']['contrast'] >= e['target'] else '❌'}"
for e in ROLE_EXC:
    ok = lambda c: f"{c}:1 {'✅' if c >= e['target'] else '❌'}"
    ovs = fx(e['override']['value']) + (f" (same hex as `{'`, `'.join(e['override']['same_as'])}`)" if e['override']['same_as'] else '')
    L.append(f"| {e['platform']} | {e['market']} ({e['code'].upper()}) | {e['role']} | {fx(e['majority'])} | {ok(e['contrast_majority'])} | {ovs} | {ok(e['contrast_override'])} | {'accepted, built' if e['accepted'] else 'suggested'} | {e['target']}:1 ({e['foreground_is']} {e['foreground']}) | {a15(e)} |")
L += ['', 'Foreground: iOS header text is `Style.json cell-tertiary-headertext` (#ffffff in all 77 markets). Android status-bar icons are '
      'light by default; the main theme never sets `windowLightStatusBar` (MISSING-ASSETS 5.6). '
      'Apps team (Ameer M., 2026-11-05 from code; confirmed on device 2026-11-10): on Android 14 and below the icons are white, so the dark overrides are needed; '
      'on Android 15+ these markets show a white status bar with dark icons (= navbar). Both versions are built (DEC-15): `statusbar` + `icons` (14 and below), '
      'navbar + `icons15` (15+). Every other market keeps navbar with light icons on Android 15+: inferred, not confirmed (MISSING-ASSETS 5.6). '
      'Dark and light icon colors are drawn by the system; the contrast above uses black and white.']
open('docs/SHELL-EXCEPTIONS.md', 'w').write('\n'.join(L) + '\n')
print(len(EXC), 'exceptions documented;', len(ROLE_EXC), 'header/statusbar exceptions,', sum(e['accepted'] for e in ROLE_EXC), 'accepted overrides')
print(len(data), 'markets; iOS roles', len(IOS_ROLES), 'Android roles', len(AND_ROLES))

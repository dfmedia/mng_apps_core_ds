"""Write DTCG design tokens (W3C format) from data/brand-color-resolution.json.
Usage: python3 scripts/build_tokens.py
Outputs:
  tokens/core/brand.tokens.json      color.brand.<market>.<role>  (7 Core roles, all 77 markets)
  tokens/ios/brand.tokens.json       color.ios.<market>.header     (iOS-only role: alias of Core navbar, DEC-15)
  tokens/android/brand.tokens.json   color.android.<market>.statusbar (Android-only role: alias of Core navbar, DEC-15)
                                     statusbar.android.<market>.icons / icons15 (icon style, Android 14 and below / 15+)
  Markets in data/shell-overrides.json (accepted by Karl 2026-11-05) get an override token with the shipped hex instead;
  scripts/build_shell_colors.py documents them in docs/SHELL-EXCEPTIONS.md.
Every token carries hex ($value) and RGB 0-255 in $extensions.mng.rgb, plus how the value was chosen.
Then `npm run build` turns these into Swift and Kotlin (style-dictionary.config.mjs).
"""
import json
R = json.load(open('data/brand-color-resolution.json'))
ROLES = ['navbar', 'navtext', 'tabbar', 'tabactive', 'tabinactive', 'action', 'alert', 'alerttext']
DESC = {'navbar': 'Top bar background', 'navtext': 'Top bar title and icons (on navbar)', 'tabbar': 'Bottom tab bar background',
        'tabactive': 'Selected tab icon/label (on tabbar)', 'tabinactive': 'Unselected tab icon/label (on tabbar)',
        'action': 'Primary button fill (white label); buy and continue alias this', 'alert': 'Breaking-news banner (one Core red, DEC-05)', 'alerttext': 'Text on the breaking-news banner (white, 5.74:1 WCAG AA)'}
rgb = lambda h: [int(h[i:i+2], 16) for i in (1, 3, 5)]
def tok(hexv, desc, ext): return {'$value': hexv, '$type': 'color', '$description': desc, '$extensions': {'mng': dict(rgb=rgb(hexv), **ext)}}
OVR = json.load(open('data/shell-overrides.json'))
core, ios, andr = {}, {}, {}
for m in sorted(R['markets'], key=lambda m: m['code']):
    k = m['code'].lower(); ro = m['roles']
    core[k] = {r: tok(ro[r]['value'], DESC[r], {'market': m['name'], 'evidence': ro[r]['evidence'],
               'shipped': {'ios': ro[r]['ios'], 'android': ro[r]['android']}, 'fix': ro[r]['fix'], 'provisional': bool(m.get('provisional'))}) for r in ROLES}
    core[k]['buy'] = {'$value': '{color.brand.%s.action}' % k, '$type': 'color', '$description': 'Alias of action (PLAT-04)'}
    core[k]['continue'] = {'$value': '{color.brand.%s.action}' % k, '$type': 'color', '$description': 'Alias of action (PLAT-04)'}
    h = m['platform_only']['ios']['header']; s = m['platform_only']['android']['statusbar']
    # DEC-15: both follow the top bar (iOS ships header = navbar in 69/77, Android statusbar = top bar in 70/77)
    # accepted market overrides (data/shell-overrides.json) keep the shipped hex instead
    ios[k] = {'header': tok(h, 'Section-front header band (iOS only): market override, shipped value (DEC-15, accepted 2026-11-05)',
                            {'owner': 'ios', 'override': True, 'shipped': h}) if k in OVR['header'] else
                        {'$value': '{color.brand.%s.navbar}' % k, '$type': 'color',
                         '$description': 'Section-front header band (iOS only): alias of navbar (DEC-15)',
                         '$extensions': {'mng': {'owner': 'ios', 'follows': 'navbar', 'shipped': h}}}}
    andr[k] = {'statusbar': tok(s, 'Status bar (Android only): market override, shipped value (DEC-15, accepted 2026-11-05)',
                                {'owner': 'android', 'override': True, 'shipped': s}) if k in OVR['statusbar'] else
                            {'$value': '{color.brand.%s.navbar}' % k, '$type': 'color',
                             '$description': 'Status bar (Android only): alias of navbar (DEC-15)',
                             '$extensions': {'mng': {'owner': 'android', 'follows': 'navbar', 'shipped': s}}}}
# DEC-15 (Karl 2026-11-06, confirmed on device 2026-11-10): status-bar icon style per Android version.
# Android 14 and below: statusbar (override or navbar) with light icons. Android 15+: navbar, dark icons in the white-top-bar markets.
SBI = OVR['statusbar_icons']; sbar = {}
for k in andr:
    dark15 = k in SBI['android15']['dark']
    sbar[k] = {'icons': {'$value': SBI['android14']['all'], '$type': 'string',
                         '$description': 'Status-bar icon style on Android 14 and below (light = white icons). Status bar color: statusbar.',
                         '$extensions': {'mng': {'owner': 'android', 'android': '14 and below', 'confirmed': SBI['android14']['confirmed']}}},
               'icons15': {'$value': 'dark' if dark15 else SBI['android15']['others'], '$type': 'string',
                           '$description': 'Status-bar icon style on Android 15+ (API 35). Status bar color on 15+: navbar (DEC-15).',
                           '$extensions': {'mng': {'owner': 'android', 'android': '15+', 'statusbar': 'navbar',
                                                   'confirmed': SBI['android15']['dark_confirmed'] if dark15 else None,
                                                   **({} if dark15 else {'note': SBI['android15']['others_note']})}}}}
meta = {'$description': 'Generated by scripts/build_tokens.py from data/brand-color-resolution.json (DEC-01..03). Do not edit by hand.'}
json.dump({**meta, 'color': {'brand': core}}, open('tokens/core/brand.tokens.json', 'w'), indent=1)
json.dump({**meta, 'color': {'ios': ios}}, open('tokens/ios/brand.tokens.json', 'w'), indent=1)
json.dump({**meta, 'color': {'android': andr}, 'statusbar': {'android': sbar}}, open('tokens/android/brand.tokens.json', 'w'), indent=1)
print(len(core), 'markets ->', len(core) * len(ROLES), 'core tokens')

# docs/BRAND-COLORS.md: every brand color as hex and RGB
EV = {'sheet': 'migration sheet', 'sheet+drift': 'migration sheet', 'agree+sheet': 'same on both + sheet', 'agree': 'same on both',
      'drift-rule': 'Android (iOS rounding)', 'ios-close': 'iOS (DEC-08, close, unconfirmed)', 'core-alert': 'Core red (DEC-05)', 'new-market': 'provisional (new market)', 'web-close': 'Cluster Audit (DEC-02)', 'ios-default': 'iOS (DEC-03)', 'follows-navbar': 'follows navbar'}
f = lambda h: f"`{h}` · {', '.join(map(str, rgb(h)))}"
L = ['# Brand colors — hex and RGB', '', 'Generated by `scripts/build_tokens.py` from `data/brand-color-resolution.json`. Do not edit by hand.',
     'Each cell: hex · R, G, B (0–255). Tokens: `tokens/core/brand.tokens.json` (`color.brand.<code>.<role>`). Swift: `MNGBrandPalettes.<code>`. Kotlin: `MngBrandPalettes.<CODE>`.',
     '`buy` and `continue` are aliases of `action`. `header` (iOS only) and `statusbar` (Android only) are aliases of `navbar` (DEC-15) '
     'except in the accepted override markets (data/shell-overrides.json), which keep the shipped value shown below; details in docs/SHELL-EXCEPTIONS.md.', '',
     '| Code | Market | ' + ' | '.join(ROLES) + ' | header (iOS, shipped) | statusbar (Android, shipped) |', '|' + '---|' * (len(ROLES) + 4)]
for m in sorted(R['markets'], key=lambda m: m['code']):
    ro = m['roles']
    L.append(f"| {m['code']} | {m['name']} | " + ' | '.join(f(ro[r]['value']) for r in ROLES) + f" | {f(m['platform_only']['ios']['header'])} | {f(m['platform_only']['android']['statusbar'])} |")
L += ['', '## How each value was chosen', '', '| Code | ' + ' | '.join(ROLES) + ' |', '|' + '---|' * (len(ROLES) + 1)]
for m in sorted(R['markets'], key=lambda m: m['code']):
    L.append(f"| {m['code']} | " + ' | '.join(EV.get(m['roles'][r]['evidence'], m['roles'][r]['evidence']) for r in ROLES) + ' |')
# DEC-16: the Android launcher-icon backdrop is a market brand asset, documented here, not a system color or token
_A = json.load(open('data/source/android-markets.json')); _i = _A['tokens'].index('ic_launcher_background')
def _argb(v):
    if not v: return None
    v = v.lower()
    return ('#' + v[3:] if v[1:3] == 'ff' else '#' + v[3:] + v[1:3]) if len(v) == 9 else v
_LB = {m['code']: _argb(m['values'][_i]) for m in _A['markets']}
L += ['', '## Android app icon background (market brand asset)', '',
      'DEC-16 (Karl, 2026-11-10): `ic_launcher_background` is the background layer of the Android adaptive app icon (the home-screen icon), '
      'behind the logo layer. It is documented here as part of each market\'s brand, **not** as a system color or token. '
      'Source: android-tribpub @ 1cfb069a6. 8-digit values carry alpha (`#00000000` = transparent). iOS app icons are complete images, so iOS has no equivalent.', '',
      '| Code | Market | App icon background (Android) |', '|---|---|---|']
for m in sorted(R['markets'], key=lambda m: m['code']):
    v = _LB.get(m['code'])
    cell = 'not in the Android export' if v is None else (f'`{v}` · transparent' if v == '#00000000' else (f"`{v}` · " + ', '.join(str(int(v[i:i + 2], 16)) for i in (1, 3, 5)) + (f', alpha {round(int(v[7:], 16) / 255, 2)}' if len(v) == 9 else '')))
    L.append(f"| {m['code']} | {m['name']} | {cell} |")
open('docs/BRAND-COLORS.md', 'w').write('\n'.join(L) + '\n')
print('wrote docs/BRAND-COLORS.md')

"""Controls and subscription option (DEC-14): tokens for the majority value, exceptions documented only.
Usage: python3 scripts/build_control_tokens.py   (after build_tokens.py; then `npm run build`)
Reads:  data/source/markets.json (iOS), data/source/android-markets.json, tokens/core/brand.tokens.json
Writes: tokens/ios/controls.tokens.json, tokens/android/controls.tokens.json
        data/control-colors.json      majority rule per color: which role it follows, and the markets that ship something else
        docs/CONTROL-EXCEPTIONS.md    those exception markets (documented, not built: Karl, DEC-14)
Rule (Karl, 2026-11-03): build each color for the majority of markets and only note the exceptions.
Per-market tints that follow each app's own primary-button color follow the Core `action` role (same role the Brand theme
binds), so they need no new per-market tokens. Constant colors (one value in most markets) become platform tokens.
"""
import json
from collections import Counter

def load(fn):
    d = json.load(open(fn)); T = {t: i for i, t in enumerate(d['tokens'])}
    return {m['code']: {k: (m['values'][i] or '').lower() for k, i in T.items()} for m in d['markets']}
I, A = load('data/source/markets.json'), load('data/source/android-markets.json')
h6 = lambda v: '#' + v.lstrip('#')[-6:] if v and v != 'null' else None
rgb = lambda h: [int(h[i:i + 2], 16) for i in (1, 3, 5)]

# (platform, key, compared with, what it colors)
FOLLOW = [
 ('ios', 'subscriptionTintColor', 'paywallPrimaryActionColor', 'Subscription option fill'),
 ('ios', 'pushNotificationPromptYesButtonBackgroundColor', 'paywallPrimaryActionColor', 'Notification prompt Yes fill'),
 ('ios', 'settingsSwitchTintColor', 'paywallPrimaryActionColor', 'Settings switch (on)'),
 ('ios', 'alertTopicCellSwitchTint', 'paywallPrimaryActionColor', 'Alert topic switch (on)'),
 ('ios', 'offlineViewSwitchTintColor', 'paywallPrimaryActionColor', 'Offline mode switch (on)'),
 ('ios', 'settingsSliderThumbTintColor', 'paywallPrimaryActionColor', 'Text size slider thumb'),
 ('ios', 'enableNotificationViewButtonBackgroundColor', 'paywallPrimaryActionColor', 'Enable notifications button fill'),
 ('android', 'Paywall_BuyButton_Background', 'Paywall_PurchaseButton_Background', 'Subscription option fill'),
 ('android', 'btn_continue', 'Paywall_PurchaseButton_Background', 'Your News Continue fill, checked topic checkbox'),
 ('android', 'Alerts_Enable_Button_Background', 'Paywall_PurchaseButton_Background', 'Alerts enable button fill'),
 ('android', 'MainStyle_Accent', 'Paywall_PurchaseButton_Background', 'Alert topic switch (on), accent (PLAT-10)'),
]
CONST = [
 ('ios', 'subscriptionInactiveColor', 'Subscription option, unselected background'),
 ('ios', 'paywallPrimaryTextColor', 'Subscription option and primary button text'),
 ('ios', 'pushNotificationPromptYesButtonTextColor', 'Notification prompt Yes text'),
 ('ios', 'pushNotificationPromptNoButtonTextColor', 'Notification prompt No text'),
 ('ios', 'settingsSliderMinimumTrackTintColor', 'Text size slider track'),
 ('ios', 'settingsSliderTickMarkTint', 'Text size slider tick marks'),
 ('android', 'Paywall_Button_TextColor', 'Subscription option and primary button text'),
 ('android', 'Alerts_Enable_Button_Text', 'Alerts enable button text'),
]
# Android values the style guide gives as fixed (not per-market keys)
ANDROID_FIXED = {
 'switch-off-thumb': ('#e5e5e5', 'Settings switch thumb, off (SwitchCompat)'),
 'switch-off-track': ('#b9b9b9', 'Settings switch track, off (SwitchCompat)'),
 'checkbox-unchecked': ('#757575', 'Your News topic checkbox, unchecked (checkbox_tint)'),
 'savings-label-text': ('#004e87', 'Savings label text on the subscription screen'),
}
# iOS system colors the native controls use when the app does not set one (Apple defaults, sRGB)
IOS_SYSTEM = {'switch-off-track': ('#e9e9ea', 'UISwitch track, off (system default; the app sets only the on tint)'),
              'switch-thumb': ('#ffffff', 'UISwitch thumb (system default)')}

out = {'follow': [], 'const': []}
for plat, key, base, what in FOLLOW:
    M = I if plat == 'ios' else A
    exc = sorted(k for k in M if h6(M[k][key]) != h6(M[k][base]))
    out['follow'].append({'platform': plat, 'key': key, 'what': what, 'follows': 'action', 'majority': len(M) - len(exc), 'of': len(M),
                          'exceptions': {k: h6(M[k][key]) for k in exc}})
for plat, key, what in CONST:
    M = I if plat == 'ios' else A
    c = Counter(h6(M[k][key]) for k in M); val, n = c.most_common(1)[0]
    out['const'].append({'platform': plat, 'key': key, 'what': what, 'value': val, 'majority': n, 'of': len(M),
                         'exceptions': {k: h6(M[k][key]) for k in sorted(M) if h6(M[k][key]) != val}})

def ctok(h, desc, **ext): return {'$value': h, '$type': 'color', '$description': desc, '$extensions': {'mng': dict(rgb=rgb(h), **ext)}}
slug = {'subscriptionInactiveColor': 'subscription-option.unselected-fill', 'paywallPrimaryTextColor': 'subscription-option.label',
        'pushNotificationPromptYesButtonTextColor': 'permission-prompt.yes-label', 'pushNotificationPromptNoButtonTextColor': 'permission-prompt.no-label',
        'settingsSliderMinimumTrackTintColor': 'text-size-slider.track', 'settingsSliderTickMarkTint': 'text-size-slider.tick',
        'Paywall_Button_TextColor': 'subscription-option.label', 'Alerts_Enable_Button_Text': 'alerts-enable.label'}
ios, andr = {}, {}
def put(tree, path, t):
    *head, last = path.split('.')
    for p in head: tree = tree.setdefault(p, {})
    tree[last] = t
for c in out['const']:
    tree = ios if c['platform'] == 'ios' else andr
    put(tree, f"color.{c['platform']}-control.{slug[c['key']]}", ctok(c['value'], f"{c['what']} ({c['key']}; {c['majority']} of {c['of']} markets; exceptions documented only, DEC-14)", source=c['key']))
for k, (h, d) in ANDROID_FIXED.items(): put(andr, f'color.android-control.{k}', ctok(h, d + ' (DEC-14)', source='style guide'))
for k, (h, d) in IOS_SYSTEM.items(): put(ios, f'color.ios-control.{k}', ctok(h, d + ' (DEC-14)', source='system'))
# typography for the subscription option label
put(ios, 'type.ios-control.subscription-option', {'$value': {'fontFamily': 'Open Sans', 'fontWeight': 700, 'fontSize': '16px'}, '$type': 'typography',
    '$description': 'Subscription option label: OpenSans-Bold 16 (SubscriptionOptionButton.xib)', '$extensions': {'mng': {'postscript': 'OpenSans-Bold'}}})
put(andr, 'type.android-control.subscription-option', {'$value': {'fontFamily': 'Roboto', 'fontWeight': 400, 'fontSize': '16px'}, '$type': 'typography',
    '$description': 'Subscription option text: system font 16sp; the Monthly line is bold', '$extensions': {'mng': {'boldFirstLine': True}}})

meta = {'$description': 'Generated by scripts/build_control_tokens.py (DEC-14). Majority values; exceptions in docs/CONTROL-EXCEPTIONS.md. Do not edit by hand.'}
json.dump({**meta, **ios}, open('tokens/ios/controls.tokens.json', 'w'), indent=1)
json.dump({**meta, **andr}, open('tokens/android/controls.tokens.json', 'w'), indent=1)
json.dump({'generated_by': 'scripts/build_control_tokens.py', **out}, open('data/control-colors.json', 'w'), indent=1)

L = ['# Control and button colors: exception markets', '',
     'Generated by `scripts/build_control_tokens.py`. Do not edit by hand.', '',
     'DEC-14 (Karl, 2026-11-03): each color is built for the majority of markets; the markets that ship something else are listed here and **not built**.', '',
     '## Tints that follow the primary-button color (Core `action`)', '', '| Platform | What | Source key | Follows action in | Exceptions (shipped value) |', '|---|---|---|---|---|']
for f in out['follow']:
    ex = ', '.join(f'{k} `{v}`' for k, v in f['exceptions'].items()) or '—'
    L.append(f"| {'iOS' if f['platform'] == 'ios' else 'Android'} | {f['what']} | `{f['key']}` | {f['majority']} of {f['of']} | {ex} |")
L += ['', '## Fixed colors', '', '| Platform | What | Source key | Value | Markets | Exceptions |', '|---|---|---|---|---|---|']
for c in out['const']:
    ex = ', '.join(f'{k} `{v}`' for k, v in c['exceptions'].items()) or '—'
    L.append(f"| {'iOS' if c['platform'] == 'ios' else 'Android'} | {c['what']} | `{c['key']}` | `{c['value']}` · {', '.join(map(str, rgb(c['value'])))} | {c['majority']} of {c['of']} | {ex} |")
open('docs/CONTROL-EXCEPTIONS.md', 'w').write('\n'.join(L) + '\n')
for f in out['follow']: print(f"{f['platform']:8} {f['key']:48} action {f['majority']}/{f['of']}")

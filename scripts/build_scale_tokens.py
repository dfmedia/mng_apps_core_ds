"""Scales (DEC-11, DEC-12): layout spacing, touch targets, breakpoints and every component metric as tokens.
Usage: python3 scripts/build_scale_tokens.py   (after compare_scales.py; then `npm run build`)
Reads:  data/scale-comparison.json
Writes: tokens/core/scale.tokens.json      space.* / grid.*                values both apps ship the same
        tokens/ios/scale.tokens.json       space.ios.* size.ios.* breakpoint.ios.* component.ios.*
        tokens/android/scale.tokens.json   space.android.* size.android.* breakpoint.android.* component.android.*
Every value is the production value. Breakpoints are kept as shipped (DEC-12): iOS has two sets (front and item widths, LAY-01),
Android picks section-front width classes by physical screen width in inches, plus two dp resource breakpoints.
The iOS legacy-template radius is not a token (DEC-10).
"""
import json
C = {r['role']: r for r in json.load(open('data/scale-comparison.json'))['roles']}
num = lambda t: float(str(t['value']).split()[0].replace('px', '').replace('dp', '').replace('in', ''))

def tok(t, desc, platform, unit='px', typ='dimension', value=None):
    v = value if value is not None else num(t)
    return {'$value': f'{v:g}{unit}' if typ == 'dimension' else v, '$type': typ, '$description': desc,
            '$extensions': {'mng': {'source': t['name'], 'usage': t['usage'], 'platform': platform, 'unit': unit or 'count'}}}

def put(tree, path, t):
    *head, last = path.split('.')
    for p in head: tree = tree.setdefault(p, {})
    tree[last] = t

core, ios, andr = {}, {}, {}
side = lambda role, s: C[role][s]

# ---- Core (same on both apps)
for role, path, desc in [('Section-front cell margin', 'space.cell.margin', 'Outer margin of a section-front cell (both apps 16)'),
                         ('Section-front cell gap', 'space.cell.gap', 'Space between elements inside a section-front cell (both apps 8)'),
                         ('Article side margin, phone', 'space.article.side', 'Article side margin on phones (both apps 16; iOS grows with width, Android 30 landscape / 75 tablet)')]:
    assert C[role]['match'] == 'same', role
    put(core, path, tok(side(role, 'ios'), desc, 'core'))
put(core, 'grid.columns', tok(side('Section-front grid columns', 'ios'), 'Section-front items are sized in twelfths (both apps)', 'core', typ='number', value=12))

# ---- iOS (pt)
IOS = [
 ('Article top margin, phone', 'space.ios.article.top', 'Article card top margin, iPhone'),
 ('Article top margin, tablet', 'space.ios.article.top-tablet', 'Article card top margin, iPad'),
 ('Minimum touch target', 'size.ios.touch-min', 'Apple minimum touch target (not enforced in the app today)'),
 ('Width class: small', 'breakpoint.ios.front.small', 'Section front: x-small → small at this window width'),
 ('Width class: medium', 'breakpoint.ios.front.medium', 'Section front: small → medium'),
 ('Width class: large', 'breakpoint.ios.front.large', 'Section front: medium → large (12.9-inch iPad landscape)'),
 ('Item width class: medium', 'breakpoint.ios.item.medium', 'Section-front item widths: medium step (differs from front medium, LAY-01)'),
 ('Item width class: large', 'breakpoint.ios.item.large', 'Section-front item widths: large step (differs from front large, LAY-01)'),
 ('Subscription option inset', 'component.ios.subscription-option.inset', 'Subscription option button inner padding'),
 ('Subscription option radius', 'component.ios.subscription-option.radius', 'Subscription option button corner radius'),
 ('Google sign-in radius', 'component.ios.google-sign-in.radius', 'Sign in with Google button corner radius (TroncKit default)'),
 ('Your News checkbox', 'component.ios.checkbox.size', 'Your News topic checkbox, square (below the touch minimum)'),
 ('Social sign-in icon', 'component.ios.social-sign-in.icon', 'Icon inside social sign-in buttons'),
]
for role, path, desc in IOS: put(ios, path, tok(side(role, 'ios'), desc, 'ios'))
# push-prompt Yes/No buttons ship radius 5 in every market (the same value the legacy template uses for paywall buttons)
put(ios, 'component.ios.permission-prompt.radius', tok(side('Primary button radius, legacy template', 'ios'), 'Notification prompt Yes / No buttons corner radius (PushNotificationOptInView.xib)', 'ios'))
tab = side('Tab bar icon', 'ios'); w, h = [float(x.replace('px', '')) for x in str(tab['value']).split()]
put(ios, 'component.ios.tab-bar.icon-width', tok(tab, 'Tab bar icon width (Font Awesome, 26 x 23)', 'ios', value=w))
put(ios, 'component.ios.tab-bar.icon-height', tok(tab, 'Tab bar icon height (Font Awesome, 26 x 23)', 'ios', value=h))

# ---- Android (dp; width classes in physical inches)
AND = [
 ('Article side margin, landscape', 'space.android.article.side-landscape', 'Article side padding, phone landscape', 'px'),
 ('Article side margin, tablet', 'space.android.article.side-tablet', 'Article side padding at sw600dp and up', 'px'),
 ('Minimum touch target', 'size.android.touch-min', 'Android minimum touch target (not enforced in the app today)', 'px'),
 ('Width class: x-small', 'breakpoint.android.width.xsmall', 'Section front: XSMALL below this physical screen width (inches)', 'in'),
 ('Width class: small', 'breakpoint.android.width.small', 'Section front: SMALL below this physical screen width (inches)', 'in'),
 ('Width class: medium', 'breakpoint.android.width.medium', 'Section front: MEDIUM below this physical screen width (inches)', 'in'),
 ('Width class: large', 'breakpoint.android.width.large', 'Section front: LARGE below, XLARGE above this physical screen width (inches)', 'in'),
 ('Tablet remote config', 'breakpoint.android.tablet-config', 'sw500dp: tablet remote config, is_phone = false', 'px'),
 ('Tablet resources (article padding, type)', 'breakpoint.android.tablet-resources', 'sw600dp: tablet article padding and type', 'px'),
 ('Paywall login button side margin', 'component.android.paywall-login.side-margin', 'Side margins of paywall login buttons (LoginButtonStyle)', 'px'),
 ("What's New Continue / outlined sheet button radius", 'component.android.whats-new-continue.radius', "What's New Continue button and outlined sheet buttons", 'px'),
 ('Your News Continue radius', 'component.android.continue.radius', 'Your News Continue button corner radius', 'px'),
 ('Manage subscription / delete account radius', 'component.android.account-button.radius', 'Manage subscription and delete account buttons', 'px'),
 ('Savings label radius', 'component.android.savings-label.radius', 'Savings label on the subscription screen', 'px'),
 ('Tab bar icon', 'component.android.tab-bar.icon-height', 'Bottom-nav icon height', 'px'),
 ('Audio player control', 'component.android.audio-player.control', 'Persistent audio player play/pause and close (below the touch minimum)', 'px'),
 ('Author contact icon', 'component.android.author.contact-icon', 'Author contact icons (below the touch minimum)', 'px'),
 ('Overlay close button', 'component.android.overlay.close', 'Breaking-news and live-video overlay close button (below the touch minimum)', 'px'),
]
for role, path, desc, unit in AND:
    t = side(role, 'android')
    put(andr, path, tok(t, desc, 'android', unit=unit) if unit == 'px' else
        {**tok(t, desc, 'android', typ='number', value=num(t)), '$extensions': {'mng': {'source': t['name'], 'usage': t['usage'], 'platform': 'android', 'unit': 'in'}}})
# Continue button, as shipped per platform (Karl, 2026-11-04; DEC-14)
SRC = lambda s, u, p: {'$extensions': {'mng': {'source': s, 'platform': p, 'unit': u}}}
put(ios, 'component.ios.continue.width', {'$value': '159px', '$type': 'dimension', '$description': 'Your News Continue button width (Continue-* PNG image, 159 x 55 pt)', **SRC('Continue-* PNGs', 'px', 'ios')})
put(ios, 'component.ios.continue.height', {'$value': '55px', '$type': 'dimension', '$description': 'Your News Continue button height (Continue-* PNG image, 159 x 55 pt)', **SRC('Continue-* PNGs', 'px', 'ios')})
put(andr, 'component.android.continue.width', {'$value': '152px', '$type': 'dimension', '$description': 'Your News Continue button width (bg_continue.xml, 152 x 54 dp)', **SRC('bg_continue.xml', 'px', 'android')})
put(andr, 'component.android.continue.height', {'$value': '54px', '$type': 'dimension', '$description': 'Your News Continue button height (bg_continue.xml, 152 x 54 dp)', **SRC('bg_continue.xml', 'px', 'android')})
put(andr, 'component.android.subscription-option.inset', {'$value': '14px', '$type': 'dimension',
    '$description': 'Subscription option inner padding (controls notes: 14dp padding)', '$extensions': {'mng': {'source': 'paywall subscription option (5-controls.md)', 'platform': 'android', 'unit': 'px'}}})

meta = {'$description': 'Generated by scripts/build_scale_tokens.py (DEC-11, DEC-12). Production values. Do not edit by hand.'}
for f, t in (('tokens/core/scale.tokens.json', core), ('tokens/ios/scale.tokens.json', ios), ('tokens/android/scale.tokens.json', andr)):
    json.dump({**meta, **t}, open(f, 'w'), indent=1, ensure_ascii=False)
count = lambda d: sum(count(v) for v in d.values()) if '$value' not in d else 1
print('core', count(core), 'ios', count(ios), 'android', count(andr))

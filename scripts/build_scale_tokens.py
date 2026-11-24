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
 ('Social sign-in icon', 'component.ios.social-sign-in.icon', 'Icon inside social sign-in buttons (native Arc login, not shown in production)'),
 # f79fe3339 export (DREAMT-4718, 2026-11-19)
 ('Top bar height', 'component.ios.top-bar.height', 'Navigation bar height (iOS default; logo at natural size)'),
 ('Section tab height', 'component.ios.section-tabs.height', 'Section tabs bar height'),
 ('Section tab gap', 'component.ios.section-tabs.gap', 'Gap between section tabs; half pads each end'),
 ('Section tab indicator', 'component.ios.section-tabs.indicator', 'Selected section tab underline, full tab width, fades in over 0.32 s'),
 ('Breaking-news banner height', 'component.ios.breaking-news-banner.height', 'Breaking-news banner height'),
 ('Section header band height', 'component.ios.section-header-band.height', 'Section header band height'),
 ('Section header band text inset', 'component.ios.section-header-band.inset', 'Section header band left and right text inset'),
 ('Segmented control band height', 'component.ios.segmented-control.band-height', 'Band holding the For You / Saved / Alerts segmented control'),
 ('Settings header band height', 'component.ios.settings-header.height', 'Settings section header band height'),
 ('Savings label radius', 'component.ios.savings-label.radius', 'Savings pill corner radius'),
 ('Savings label inset, phone', 'component.ios.savings-label.inset', 'Savings pill inset from the yearly option trailing edge, iPhone'),
 ('Savings label inset, tablet', 'component.ios.savings-label.inset-tablet', 'Savings pill inset from the yearly option trailing edge, iPad'),
 ('Push prompt button height', 'component.ios.permission-prompt.height', 'Notification prompt Yes / No button height'),
 ('Modal button height', 'component.ios.modal-button.height', 'Manage App Subscription and Cancel buttons height'),
 ('Newsletters button height', 'component.ios.newsletters-button.height', 'Newsletters buttons minimum height (incl. Apple / Google sign-in)'),
 ('Newsletters button radius', 'component.ios.newsletters-button.radius', 'Newsletters buttons corner radius'),
 ('Newsletters sign-in icon', 'component.ios.newsletters-button.icon', 'Apple / Google icon inside Newsletters sign-in buttons'),
 ('Newsletters button icon gap', 'component.ios.newsletters-button.icon-gap', 'Gap between icon and label in Newsletters buttons'),
 ('Loading indicator card radius', 'component.ios.loading-indicator.radius', 'Loading indicator card corner radius'),
 ('Tournament loading symbol', 'component.ios.tournament-loading.icon', 'Sport symbol in tournament loading (SF Symbols)'),
]
for role, path, desc in IOS: put(ios, path, tok(side(role, 'ios'), desc, 'ios'))
# push-prompt Yes/No buttons ship radius 5 in every market (the same value the legacy template uses for paywall buttons)
put(ios, 'component.ios.permission-prompt.radius', tok(side('Primary button radius, legacy template', 'ios'), 'Notification prompt Yes / No buttons corner radius (PushNotificationOptInView.xib)', 'ios'))
tab = side('Tab bar icon', 'ios'); w, h = [float(x.replace('px', '')) for x in str(tab['value']).split()]
put(ios, 'component.ios.tab-bar.icon-width', tok(tab, 'Tab bar icon width (Font Awesome, 26 x 23)', 'ios', value=w))
put(ios, 'component.ios.tab-bar.icon-height', tok(tab, 'Tab bar icon height (Font Awesome, 26 x 23)', 'ios', value=h))
sav = side('Savings label size', 'ios'); w, h = [float(x.replace('px', '')) for x in str(sav['value']).split()]
put(ios, 'component.ios.savings-label.width', tok(sav, 'Savings pill width (110 x 30)', 'ios', value=w))
put(ios, 'component.ios.savings-label.height', tok(sav, 'Savings pill height (110 x 30)', 'ios', value=h))

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
 ('Top bar height', 'component.android.top-bar.height', 'Top app bar height on phones (?actionBarSize)', 'px'),
 ('Top bar height, tablet', 'component.android.top-bar.height-tablet', 'Top app bar height at sw600dp and up', 'px'),
 ('Section tab height', 'component.android.section-tabs.height', 'Section tab height (Material TabLayout default)', 'px'),
 ('Section tab indicator', 'component.android.section-tabs.indicator', 'Section tab selected indicator height', 'px'),
 ('Bottom navigation height', 'component.android.bottom-nav.height', 'Bottom navigation height, phones and tablets', 'px'),
 ('Widget minimum width', 'component.android.widget.min-width', 'Home-screen widget minWidth (2 x 1 cells, not resizable)', 'px'),
 ('Widget minimum height', 'component.android.widget.min-height', 'Home-screen widget minHeight', 'px'),
 ('Elevation: top bar (scrolled)', 'component.android.elevation.toolbar', 'Top bar elevation when content scrolls under it (0 at rest)', 'px'),
 ('Elevation: secondary top bars', 'component.android.elevation.toolbar-secondary', 'Settings, web view and login toolbar elevation', 'px'),
 ('Elevation: section tabs', 'component.android.elevation.section-tabs', 'Section tab strip elevation', 'px'),
 ('Elevation: cards', 'component.android.elevation.card', 'Card elevation (special-section cards 4dp)', 'px'),
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
SAVP = json.load(open('data/source/apps-team-answers/2026-11-24-DREAMT-4719-android.json'))['savings_label']   # DEC-25
for k, v, d in [('padding-horizontal', SAVP['pill']['padding_horizontal'], 'Savings label left and right padding (the pill wraps its text)'),
                ('padding-vertical', SAVP['pill']['padding_vertical'], 'Savings label top and bottom padding (about 29dp tall)'),
                ('border-width', SAVP['pill']['border_width'], 'Savings label outline width (buy color)'),
                ('end-margin', SAVP['position']['end_margin'], 'Savings label distance from the right edge; it overlaps the top edge of the Yearly option')]:
    put(andr, f'component.android.savings-label.{k}', {'$value': f'{v}px', '$type': 'dimension', '$description': d + ' (DEC-25, Apps team, DREAMT-4719, 2026-11-24)',
        '$extensions': {'mng': {'source': 'Apps team answer (paywall discount label layout)', 'platform': 'android', 'unit': 'px'}}})
put(andr, 'component.android.subscription-option.inset', {'$value': '14px', '$type': 'dimension',
    '$description': 'Subscription option inner padding (controls notes: 14dp padding)', '$extensions': {'mng': {'source': 'paywall subscription option (5-controls.md)', 'platform': 'android', 'unit': 'px'}}})

# iOS shadows as shipped (f79fe3339 export, `shadow` group; Apps team 5.1): no shared scale, one token per place it is used.
import re
SH = json.load(open('data/source/ios-tokens.json'))['shadow']
shadow = {}
for t in SH['tokens']:
    u = t['usage']; m = re.search(r'opacity ([\d.]+), radius ([\d.]+), offset (?:not set so the iOS default )?(-?[\d.]+),(-?[\d.]+)', u)
    op, rad, ox, oy = map(float, m.groups())
    key = t['name'].replace('shadow-', '')
    shadow[key] = {'$value': {'color': '#000000', 'offsetX': f'{ox:g}px', 'offsetY': f'{oy:g}px', 'blur': f'{2 * rad:g}px', 'spread': '0px'}, '$type': 'shadow',
                   '$description': u.split('. iOS:')[0] + f'. iOS layer: black, opacity {op:g}, radius {rad:g}, offset {ox:g},{oy:g} (blur = 2 x radius).',
                   '$extensions': {'mng': {'platform': 'ios', 'opacity': op, 'radius': rad, 'offsetX': ox, 'offsetY': oy, 'source': (re.search(r'(\w+\.swift:\d+)', u) or [None, 'f79fe3339'])[1], 'css': t['value']}}}
json.dump({'$description': 'Generated by scripts/build_scale_tokens.py from the iOS export (TroncKit f79fe3339, shadow group). ' + SH['note'] + ' Do not edit by hand.', 'shadow': {'ios': shadow}},
          open('tokens/ios/shadow.tokens.json', 'w'), indent=1, ensure_ascii=False)
meta = {'$description': 'Generated by scripts/build_scale_tokens.py (DEC-11, DEC-12). Production values. Do not edit by hand.'}
for f, t in (('tokens/core/scale.tokens.json', core), ('tokens/ios/scale.tokens.json', ios), ('tokens/android/scale.tokens.json', andr)):
    json.dump({**meta, **t}, open(f, 'w'), indent=1, ensure_ascii=False)
count = lambda d: sum(count(v) for v in d.values()) if '$value' not in d else 1
print('core', count(core), 'ios', count(ios), 'android', count(andr))

"""App shell sizes, elevation, motion and other controls as shipped, iOS next to Android (documented only, DEC-09).
Usage: python3 scripts/build_shipped_specs.py   (after build_scale_tokens.py; then figma_shipped_specs.py)
Reads:  data/source/apps-team-answers/2026-11-18-DREAMT-4718-ios.json + 2026-11-19 corrections (iOS, TroncKit f79fe3339 answers)
        data/source/apps-team-answers/2026-11-19-DREAMT-4719-android.json (Android answers + style guide 1795110354-0c21)
        data/source/apps-team-answers/2026-11-23-DREAMT-4719-android.json (5.6 follow-ups + style guide 1795459789-4808)
        data/source/android-scales.json (Android size and elevation tokens), data/component-platform-map.json (owner buckets)
Writes: data/shipped-specs.json, docs/SHIPPED-SPECS.md
Every value comes from the Apps team's answers or the Android style guide. iOS values are from f79fe3339; since the
f79fe3339 export (2026-11-19) the iOS sizes are also tokens (component.ios.*, tokens/ios/scale.tokens.json).
"""
import json

I = json.load(open('data/source/apps-team-answers/2026-11-18-DREAMT-4718-ios.json'))
I2 = json.load(open('data/source/apps-team-answers/2026-11-19-DREAMT-4718-ios.json'))   # corrections (spinner colors, paywall text)
A = json.load(open('data/source/apps-team-answers/2026-11-19-DREAMT-4719-android.json'))
A3 = json.load(open('data/source/apps-team-answers/2026-11-23-DREAMT-4719-android.json'))   # 5.6 follow-ups (Alerts fill, bottom sheets)
SC = json.load(open('data/source/android-scales.json'))
OWN = {i['id']: i['owner'] for i in json.load(open('data/component-platform-map.json'))['items']}
TOK = {t['name']: t['value'].replace('px', '') for k in ('size', 'elevation') for t in SC.get(k, {}).get('tokens', [])}
BUCKET = {'core': 'Core', 'core+variant': 'Core, per-platform value', 'ios': 'iOS only', 'android': 'Android only'}
SRC_I = 'Apps team, DREAMT-4718 (TroncKit f79fe3339)'
SRC_A = f"Apps team, DREAMT-4719 + Android style guide {A['style_guide_update']['version']} (5.6 follow-ups: 1795459789-4808)"

sh, ash = I['shell'], A['shell']
g = A['style_guide_update']
shell = [
    {'id': 'nav-bar', 'what': 'Top bar', 'ios': f"{sh['nav_bar']['height']} pt; {sh['nav_bar']['note']}",
     'android': f"{TOK['size-toolbar']}dp phone / {TOK['size-toolbar-tablet']}dp tablet; title {ash['top_bar']['title']}; elevation {TOK['elevation-toolbar']}dp when scrolled",
     'tokens': 'component.android.top-bar.height / height-tablet'},
    {'id': 'section-tabs', 'what': 'Section tabs', 'ios': f"{sh['section_tabs']['height']} pt, {sh['section_tabs']['gap']} pt between tabs, {sh['section_tabs']['indicator']} pt underline fading in over {sh['section_tabs']['indicator_fade_s']} s; {sh['section_tabs']['label']}",
     'android': f"{TOK['size-section-tab']}dp, 12dp side padding, scrollable, {TOK['size-tab-indicator']}dp indicator; {ash['section_tabs']['label']}; elevation {TOK['elevation-section-tabs']}dp",
     'tokens': 'component.android.section-tabs.height / indicator'},
    {'id': 'tab-bar', 'what': 'Bottom tab bar', 'ios': f"{sh['tab_bar']['height']} height; {sh['tab_bar']['label']}",
     'android': f"{TOK['size-bottom-nav']}dp, {ash['bottom_nav']['icon']}dp icons, label {ash['bottom_nav']['label']} 2dp below the icon",
     'tokens': 'component.android.bottom-nav.height, component.android.tab-bar.icon-height'},
    {'id': 'breaking-banner', 'what': 'Breaking-news banner', 'ios': f"{sh['breaking_news']['height']} pt; {sh['breaking_news']['label']}",
     'android': g['breaking_news'], 'tokens': 'component.android.overlay.close (40dp close)'},
    {'id': 'section-header', 'what': 'Section header band', 'ios': f"{sh['section_header']['height']} pt, {sh['section_header']['inset']} pt text inset", 'android': '—', 'tokens': ''},
    {'id': 'status-bar', 'what': 'Status bar', 'ios': 'System; takes the nav bar color', 'android': 'System; color and icon style per Android version (DEC-15, Components · App shell › 01)', 'tokens': 'statusbar.android.*'},
]
for r in shell: r['bucket'] = BUCKET[OWN[r['id']]]

elevation = {'ios': I['shadows'], 'ios_note': I['shadows_note'], 'android': A['elevation']}
motion = {'ios': I['motion'], 'android': A['motion']}

C, ac = I['controls'], A
lo = I2['loading']['spinner']   # 2026-11-19 correction: 11 colors (TDP orange, MC, NYDN, OS, SS added)
controls = [
    {'id': 'segmented', 'what': 'Segmented control (For You / Saved / Alerts)',
     'ios': f"{C['segmented']['style']}: selected {C['segmented']['selected']} on {C['segmented']['track']}, {C['segmented']['label']}, {C['segmented']['band']} pt band",
     'android': f"MaterialButtonToggleGroup: track {ac['segmented']['track']} radius {ac['segmented']['track_radius']}dp; selected {ac['segmented']['selected_fill']} (TSAR {ac['segmented']['selected_fill_tsar']}) with {ac['segmented']['selected_text']} text; unselected {ac['segmented']['unselected_fill']} with {ac['segmented']['unselected_text']} text; {ac['segmented']['label']}",
     'swatches': {'ios': [C['segmented']['selected'], C['segmented']['track']], 'android': [ac['segmented']['track'], ac['segmented']['selected_fill'], ac['segmented']['unselected_text']]}},
    {'id': 'loading', 'what': 'Loading indicator',
     'ios': f"{C['loading']['style']}; spinner {lo['majority']} in {lo['majority_markets']} markets; " + ', '.join(f"{k} {v}" for k, v in lo['exceptions'].items()),
     'android': 'Full-screen progress dialog. ' + '; '.join(f"{x['where']} {x['value']}" + (f" ({x['size']})" if x.get('size') else '') for x in ac['loading']),
     'swatches': {'ios': [lo['majority']], 'android': ['#D5D5D5', '#2A2A2A', '#1E88E5']}},
    {'id': 'permission-prompt', 'what': 'Notification prompt buttons',
     'ios': f"Yes {C['push_prompt']['yes']} (filled) / No {C['push_prompt']['no']}; {C['push_prompt']['height']} pt, radius {C['push_prompt']['radius']}",
     'android': f"CUSTOMIZE: {ac['alerts_enable']['label']}, about {ac['alerts_enable']['height_approx']}dp, {ac['alerts_enable']['width']}, square; fill Alerts_Enable_Button_Background per market: the market action in 58 of 77, #DAA520 in 15, DP #4FA8D1, TPD #000000, OS and TSAR the default #FF6859 (Apps team, 2026-11-23). NO, THANKS: {ac['alerts_enable']['no_thanks']}",
     'swatches': {'android': ['#DAA520', '#4FA8D1', '#FF6859']}},
    {'id': 'savings-badge', 'what': 'Savings label',
     'ios': f"{C['savings_pill']['width']} × {C['savings_pill']['height']} pt, {C['savings_pill']['fill']}, {C['savings_pill']['border']}, radius {C['savings_pill']['radius']}; {C['savings_pill']['label']}; inset {C['savings_pill']['inset']}",
     'android': 'White, 2dp stroke in the buy color, radius 15, text in the market color (VP screenshot, 2026-11-19; the style guide says #004e87); font, size and padding asked (MISSING-ASSETS 5.6)'},
    {'id': 'button-account', 'what': 'Manage subscription buttons (split, DEC-21)',
     'ios': f"Modal: {C['manage_subscription_modal']['height']} pt, radius {C['manage_subscription_modal']['radius']}; {C['manage_subscription_modal']['buttons']} (white on white in 7 markets, DSC-34)",
     'android': (lambda b: f"Bottom sheets, device default button style (not Material): {b['label']}; Open Play Store filled {b['open_play_store']['fill']}, text {b['open_play_store']['text']}, radius {b['open_play_store']['radius']}; {b['outlined']['buttons']} outlined, {b['outlined']['stroke']}, radius {b['outlined']['radius']}; Delete account's Cancel filled {b['delete_account_cancel']['fill']}, white text; Delete account buttons {b['height']['delete_account']}dp, Manage subscription at least {b['height']['manage_subscription_min']}dp (Apps team, 2026-11-23)")(A3['account_bottom_sheets'])},
    {'id': 'social-signin', 'what': 'Social sign-in',
     'ios': f"{C['social_signin']['where']}: {C['social_signin']['height']} pt, radius {C['social_signin']['radius']}, {C['social_signin']['label']}, {C['social_signin']['outline']} pt outline, {C['social_signin']['icon']} pt icon, {C['social_signin']['gap']} pt gap",
     'android': 'None in the app: login is the Auth0 hosted page'},
]
SPLIT = 'Split: iOS only + Android only'   # DEC-21: the apps do different things
for r in controls: r['bucket'] = BUCKET[OWN[r['id']]] if r['id'] in OWN else SPLIT

out = {'generated_by': 'scripts/build_shipped_specs.py', 'sources': {'ios': SRC_I, 'android': SRC_A},
       'rule': 'Documented as shipped (DEC-09). iOS sizes are tokens since the f79fe3339 export (component.ios.*).',
       'shell': shell, 'elevation': elevation, 'motion': motion, 'controls': controls}
json.dump(out, open('data/shipped-specs.json', 'w'), indent=1, ensure_ascii=False)

L = ['# Shipped specs: app shell, elevation, motion, controls (generated)', '',
     f"Generated by `scripts/build_shipped_specs.py`. iOS: {SRC_I}. Android: {SRC_A}. Documented as shipped (DEC-09); "
     "iOS sizes are tokens since the f79fe3339 export (`component.ios.*`, tokens/ios/scale.tokens.json). Figma: Core Layout · iOS vs Android › 03, 04; Core Components · Controls › 01.", '',
     '## App shell sizes', '', '| Part | Owner | iOS | Android | Android tokens |', '|---|---|---|---|---|']
L += [f"| {r['what']} | {r['bucket']} | {r['ios']} | {r['android']} | {r['tokens'] or '—'} |" for r in shell]
L += ['', '## Elevation and shadows', '', f"iOS: {I['shadows_note']} Tokens: `shadow.ios.*` (Swift `MNGShadowTokens`, from the f79fe3339 export).", '', '| iOS (where) | Opacity | Radius | Offset |', '|---|---|---|---|']
L += [f"| {s['where']} | {s['opacity']} | {s['radius']} | {s['offset']} |" for s in I['shadows']]
L += ['', '| Android (where) | Elevation |', '|---|---|'] + [f"| {e['where']} | {e['dp']} (dp) |" for e in A['elevation']]
L += ['', '## Motion', '', '| iOS (where) | Duration |', '|---|---|'] + [f"| {m['where']} | {m['duration']} |" for m in I['motion']]
L += ['', '| Android (where) | Duration |', '|---|---|'] + [f"| {m['where']} | {m['duration']} |" for m in A['motion']]
L += ['', '## Other controls', '', '| Control | Owner | iOS | Android |', '|---|---|---|---|']
L += [f"| {r['what']} | {r['bucket']} | {r['ios']} | {r['android']} |" for r in controls]
open('docs/SHIPPED-SPECS.md', 'w').write('\n'.join(L) + '\n')
print(f"shell {len(shell)}, shadows {len(I['shadows'])}/{len(A['elevation'])}, motion {len(I['motion'])}/{len(A['motion'])}, controls {len(controls)}")

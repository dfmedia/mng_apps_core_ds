"""Style-guide items that were not tracked yet, documented as shipped (Karl, 2026-11-10: document only, design nothing new).
Usage: python3 scripts/build_guide_extras.py   (then npm run build; the registry rows live in scripts/component_platform_map.py)
Reads  data/source/style-guide-extras.json (copied from both style guides), data/system-color-comparison.json,
       data/system-tokens.json, data/type-font-exceptions.json
Writes data/guide-extras.json, docs/GUIDE-EXTRAS.md, tokens/android/guide-extras.tokens.json
Tokens (DEC-12): Android ad slot sizes as component metrics (component.android.ad.*); the four fixed PageSuite eEdition colors
as Android system colors (color.android-system.eedition.*, DEC-16 fixed colors). Everything else already has a token
(whats-new-button-color, widget-*, Core ad/background and ad/label, component.android.whats-new-continue.radius) or is unknown.
"""
import json

S = json.load(open('data/source/style-guide-extras.json'))
SYS = json.load(open('data/system-color-comparison.json'))
TOK = {t['name']: t for t in json.load(open('data/system-tokens.json'))['tokens']}
FONTS = json.load(open('data/type-font-exceptions.json'))


def find(o, key):
    if isinstance(o, dict):
        if o.get('key') == key and 'majority' in o: return o
        for v in o.values():
            r = find(v, key)
            if r: return r
    if isinstance(o, list):
        for v in o:
            r = find(v, key)
            if r: return r
    return None


def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)


rgb = lambda h: ', '.join(str(int(h[i:i + 2], 16)) for i in (1, 3, 5))
hexrgb = lambda h: f'`{h}` · {rgb(h)}'

# ---- What's New Continue: shipped fill per market = drawable override, else whats_new_button_color
W = S['whats_new_continue']
wn = find(SYS, W['fill']['key'])
font = find(FONTS, W['label']['font_key'])
fills = {}
for v in wn['values']:
    for m in v['markets']: fills[m] = v['value']
shipped = {m: W['drawable_overrides'].get(m, h) for m, h in fills.items()}
groups = {}
for m, h in sorted(shipped.items()): groups.setdefault(h, []).append(m)
fill_rows = sorted(({'value': h, 'markets': ms, 'count': len(ms), 'white_label_contrast': ratio('#ffffff', h),
                     'kind': 'majority (token whats-new-button-color)' if h == wn['majority'] else '; '.join(
                         f"{k} ({', '.join(x)})" if len(groups[h]) > 1 else k for k, x in (
                             ('drawable override', [m for m in ms if m in W['drawable_overrides']]),
                             ('exception, documented only', [m for m in ms if m not in W['drawable_overrides']])) if x)}
                    for h, ms in groups.items()), key=lambda r: -r['count'])
whats_new = {'platform': 'android', 'evidence': W['evidence'], 'token_fill': 'whats-new-button-color', 'majority': wn['majority'],
             'majority_markets': wn['majority_markets'], 'fills': fill_rows,
             'color_resource_vs_drawable': {m: {'color_resource': fills[m], 'drawable': h} for m, h in W['drawable_overrides'].items()},
             'label': {**W['label'], 'font': font['majority'] if font else None, 'font_markets': font['majority_markets'] if font else None},
             'radius': {'value': W['radius']['value'], 'token': 'component.android.whats-new-continue.radius'},
             'unknown': W['unknown'], 'ios': W['ios']}

# ---- Ad slots
A = S['ad_slots']
ad_tokens = {k: {'width': v['width'], 'height': v['height'], 'token': f'component.android.ad.{k}'} for k, v in A['android']['sizes'].items()}
ads = {'android': {**A['android'], 'tokens': ad_tokens}, 'ios': A['ios'],
       'colors_core': [{'name': n, 'value': next(t for t in json.load(open('data/system-tokens.json'))['tokens'] if t['name'] == n)['values']} for n in A['colors_core']],
       'ios_adhesion': TOK.get('adhesion-banner-background')}

# ---- Widget, eEdition
WG = S['widget']
widget = {**WG, 'day_tokens': [{'name': TOK[k.replace('_', '-')]['name'], 'value': TOK[k.replace('_', '-')]['value'], 'source': k} for k in WG['day_keys']]}
E = S['eedition']
eedition = {**E, 'colors': [{**c, 'token': f"color.android-system.eedition.{c['id']}"} for c in E['colors']],
            'contrast': {'tab text on tab container': ratio('#ffffff', '#ffffff'), 'inactive tab text on tab container': ratio('#999999', '#ffffff')}}

out = {'generated_by': 'scripts/build_guide_extras.py', 'sources': S['sources'],
       'rule': 'Documented as shipped (DEC-09). Majority values only; exceptions documented, not built (DEC-14/16). Nothing new designed.',
       'whats_new_continue': whats_new, 'alerts_enable': S['alerts_enable'], 'ad_slots': ads, 'widget': widget, 'eedition': eedition,
       'images': S['images']}
json.dump(out, open('data/guide-extras.json', 'w'), indent=1, ensure_ascii=False)

# ---- Tokens: tokens/android/guide-extras.tokens.json
ext = lambda **k: {'mng': {'platform': 'android', **k}}
tok = {'$description': 'Generated by scripts/build_guide_extras.py from data/source/style-guide-extras.json (Android style guide). Do not edit.',
       'component': {'android': {'ad': {}}}, 'color': {'android-system': {'eedition': {}}}}
use = {k: ', '.join(s['name'].lower() + (' (phone)' if s['phone'] == k and s['tablet'] != k else ' (tablet)' if s['tablet'] == k and s['phone'] != k else '')
                    for s in A['android']['slots'] if k in (s['phone'], s['tablet'])) for k in A['android']['sizes']}
for k, v in A['android']['sizes'].items():
    tok['component']['android']['ad'][k] = {
        d: {'$value': f"{v[d]}px", '$type': 'dimension', '$description': f"Ad slot {k} {d}: {use[k]}",
            '$extensions': ext(source='AdsUtil.getAdSizesListOfAdPos', usage=f"{v['width']}x{v['height']} dp: {use[k]} ({A['android']['evidence']})", unit='px')}
        for d in ('width', 'height')}
for c in eedition['colors']:
    tok['color']['android-system']['eedition'][c['id']] = {
        '$type': 'color', '$value': c['value'],
        '$description': f"PageSuite eEdition {c['what'].lower()} (Android): same in all 77 markets" + (f" (passed as {c['shipped_as']})" if c.get('shipped_as') else ''),
        '$extensions': ext(source=f"PageSuite SDK ({E['sdk']})", kind='fixed', markets=77, exceptions={}, rgb=[int(c['value'][i:i + 2], 16) for i in (1, 3, 5)], owner='android')}
json.dump(tok, open('tokens/android/guide-extras.tokens.json', 'w'), indent=1, ensure_ascii=False)

# ---- Doc
L = ['# Style-guide extras (as shipped)', '',
     'Generated by `scripts/build_guide_extras.py` from `data/source/style-guide-extras.json`. Do not edit by hand.', '',
     'Items from the two Apps team style guides that were not tracked before (docs/STYLE-GUIDE-INVENTORY.md). ' + out['rule'], '',
     f"Sources: iOS {S['sources']['ios']}; Android {S['sources']['android']}.", '',
     '## Ad slots (Core: both apps show ads)', '',
     f"Colors are Core tokens (DEC-16): " + '; '.join(f"`{c['name']}` {hexrgb(c['value']['ios'])}" for c in ads['colors_core']) + '. '
     f"iOS also has the adhesion (sticky) banner background `adhesion-banner-background` {hexrgb(ads['ios_adhesion']['value'])}.", '',
     f"**Android sizes** (dp, tokens `component.android.ad.*`, source: {A['android']['evidence']}):", '',
     '| Slot | Phone | Tablet |', '|---|---|---|']
sz = lambda k: f"{A['android']['sizes'][k]['width']} × {A['android']['sizes'][k]['height']} (`{k}`)"
for s in A['android']['slots']:
    L.append(f"| {s['name']}{' · ' + s['where'] if s.get('where') else ''} | {sz(s['phone'])} | {sz(s['tablet'])} |")
L += [''] + [f'- {r}' for r in A['android']['rules']] + ['',
      f"**iOS:** {A['ios']['unknown']} (unknown, ask Apps team: MISSING-ASSETS 5.8). What ships: " + '; '.join(A['ios']['known']) + '.', '',
      "## What's New Continue button (Android only)", '',
      f"Source: {W['evidence']}. Not in the iOS guide. Label {hexrgb(W['label']['color'])}, {W['label']['case']}, "
      f"`{W['label']['font_key']}` = {whats_new['label']['font']} in {whats_new['label']['font_markets']} of 77 markets. "
      f"Radius {W['radius']['value']} (`{whats_new['radius']['token']}`). Unknown: {', '.join(W['unknown'])} (MISSING-ASSETS 5.6).", '',
      f"Fill: token `whats-new-button-color` {hexrgb(wn['majority'])} in {wn['majority_markets']} of 77 markets. "
      "CT, NYDN and VP override the button drawable, so the drawable color is what ships there (their color resource is not used on this button). "
      "White-label contrast is shown as shipped; below 4.5:1 fails for text.", '',
      '| Fill (as shipped) | Markets | White label contrast | Kind |', '|---|---|---|---|']
for r in fill_rows:
    L.append(f"| {hexrgb(r['value'])} | {r['count']}: {', '.join(r['markets']) if r['count'] < 20 else 'majority'} | {r['white_label_contrast']}:1 | {r['kind']} |")
L += ['', '| Market | Color resource `whats_new_button_color` | Drawable (ships) |', '|---|---|---|']
for m, v in whats_new['color_resource_vs_drawable'].items():
    L.append(f"| {m} | {hexrgb(v['color_resource'])} | {hexrgb(v['drawable'])} |")
AE = S['alerts_enable']
L += ['', '## Alerts enable button (Android)', '',
      f"Already tracked: {AE['registry']}. Fill `{AE['fill']['key']}` (control token, 58 of 77 markets follow Core action, docs/CONTROL-EXCEPTIONS.md), label {hexrgb(AE['label']['color'])}, {AE['shape'].lower()} corners. Font and height: MISSING-ASSETS 5.6.", '',
      '## Home-screen widget (Android only)', '',
      f"Source: {WG['evidence']}. {WG['ios']}.", '',
      '| Color | Day value (token) | Night value |', '|---|---|---|']
for t in widget['day_tokens']:
    L.append(f"| `{t['source']}` | {hexrgb(t['value'])} (`{t['name']}`, System colors · Android) | unknown, ask Apps team (5.9) |")
L += ['', f"- {WG['night']}", f"- {WG['logo']}", f"- {WG['icons']}", f"- Unknown: {', '.join(WG['unknown'])} (MISSING-ASSETS 5.9).", '',
      '## eEdition (PageSuite) colors (Android only)', '',
      f"Source: {E['evidence']}. {E['sdk']}. {' '.join(E['rules'])} {E['ios']}.", '',
      '| Color | Value | Token |', '|---|---|---|']
for c in eedition['colors']:
    L.append(f"| {c['what']} | {hexrgb(c['value'])}{' (passed as ' + c['shipped_as'] + ')' if c.get('shipped_as') else ''} | `{c['token']}` |")
L += ['', 'Contrast as shipped (how the SDK paints these is not in the guide): ' + '; '.join(f'{k} {v}:1' for k, v in eedition['contrast'].items()) + '.', '',
      '## Non-icon images (as shipped, not built)', '',
      'Per-market artwork, not reusable design-system parts. Tracked here and in the registry; vector masters are MISSING-ASSETS 2.1 / 2.2. Not drawn in Figma.', '',
      '| Platform | Group | What | Files |', '|---|---|---|---|']
for p in ('ios', 'android'):
    for g in S['images'][p]['groups']:
        L.append(f"| {'iOS' if p == 'ios' else 'Android'} | {g['group']} | {g['what']} | {', '.join(g['files']) if g['files'] else 'not in the guide'} |")
L += ['', f"Android: {S['images']['android']['note']}"]
open('docs/GUIDE-EXTRAS.md', 'w').write('\n'.join(L) + '\n')
print(f"What's New fills: {[(r['value'], r['count']) for r in fill_rows]}")
print(f"ad tokens: {list(ad_tokens)}; eEdition tokens: {[c['id'] for c in eedition['colors']]}")

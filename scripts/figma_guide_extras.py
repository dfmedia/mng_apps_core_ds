"""Emit the Figma builds for the style-guide extras (data/guide-extras.json, scripts/build_guide_extras.py). Prints JS for figma_execute.
Usage: python3 scripts/figma_guide_extras.py MODE [ad-background-key]
  vars                      Android file: ad size variables (Components · Android) + eEdition colors (System colors · Android)
  core-ads                  Core file:    Layout · iOS vs Android › 02 · Ad slots (table, colors bound to System colors)
  android-ads <key>         Android file: Layout · Ads, widget, eEdition › 01 · Ad slots (slots bound to the size variables;
                            fill = Core library ad/background, <key> = that variable's key in the Core file)
  android-widget            Android file: › 02 · Home-screen widget colors (bound to System colors · Android)
  android-eedition          Android file: › 03 · eEdition (PageSuite) colors (bound to System colors · Android)
  whats-new                 Android file: Components · Button › 04 · What's New Continue (as shipped)
Run `vars` before the Android sections that bind to the new variables.
"""
import json, sys

D = json.load(open('data/guide-extras.json'))
MODE = sys.argv[1]
rgb = lambda h: ', '.join(str(int(h[i:i + 2], 16)) for i in (1, 3, 5))
hx = lambda h: f'{h} · {rgb(h)}'
SRC = f"Source: Android {D['sources']['android'].split(' (')[0]} · iOS {D['sources']['ios'].split(' (')[0]} · data/guide-extras.json · docs/GUIDE-EXTRAS.md."
TABLE = open('scripts/figma/build_table_section.js').read()
EXTRAS = open('scripts/figma/build_guide_extras.js').read()
AP = 'Layout · Ads, widget, eEdition'
A = D['ad_slots']['android']; SZ = A['sizes']
sz = lambda k: f"{SZ[k]['width']} × {SZ[k]['height']}"
SYSA = 'System colors · Android::'


def table(page, T):
    return f"const PAGE = {json.dumps(page)}; const T = {json.dumps(T, ensure_ascii=False, separators=(',', ':'))};\n" + TABLE


def extras(mode, data):
    return f"const MODE = {json.dumps(mode)}; const D = {json.dumps(data, ensure_ascii=False, separators=(',', ':'))};\n" + EXTRAS


uses = {k: '; '.join(f"{s['name']}{' (' + s['where'] + ')' if s.get('where') else ''}, {'phone' if s['phone'] == k else ''}{' and ' if s['phone'] == k and s['tablet'] == k else ''}{'tablet' if s['tablet'] == k else ''}"
                     for s in A['slots'] if k in (s['phone'], s['tablet'])) for k in SZ}

if MODE == 'vars':
    floats = [{'name': f'ad/{k}/{d}', 'value': v[d], 'desc': f"Ad slot {k} {d}: {v['width']} × {v['height']} dp. {uses[k]}. AdsUtil.getAdSizesListOfAdPos (Android style guide 4-layout.md). Token component.android.ad.{k}.{d} (DEC-12)."}
              for k, v in SZ.items() for d in ('width', 'height')]
    colors = [{'name': f"eedition-{c['id']}", 'value': c['value'], 'desc': f"PageSuite eEdition {c['what'].lower()}: same in all 77 markets ({D['eedition']['sdk']}). Token {c['token']} (DEC-16)."}
              for c in D['eedition']['colors']]
    print(extras('vars', {'floats': floats, 'colors': colors}))

elif MODE == 'core-ads':
    I = D['ad_slots']['ios']; col = {c['name']: c for c in D['ad_slots']['colors_core']}
    ANS = json.load(open('data/source/apps-team-answers/2026-11-18-DREAMT-4718-ios.json'))['ad_slots']
    isz = lambda k: f"{ANS['sizes'][k]['width']} × {ANS['sizes'][k]['height']}"
    ios_slot = {x['id']: x for x in ANS['slots']}
    rows = [{'group': 'Colors · Core tokens (DEC-16)'}]
    for n, what, si, sa in (('ad/background', 'Ad slot background', 'cellAdBackgroundColor', 'ad_background'), ('ad/label', "'Advertisement' label", 'adLabelTextColor', 'advertisement_title')):
        v = col[n]['value']
        rows.append([{'t': what, 'b': True}, {'t': f"{hx(v['ios'])} · {si}", 'sw': v['ios'], 'v': f'System colors::{n}'},
                     {'t': f"{hx(v['android'])} · {sa}", 'sw': v['android'], 'v': f'System colors::{n}'}, f'{n} (System colors)', {'chip': 'Core'}])
    ad = D['ad_slots']['ios_adhesion']
    rows.append([{'t': 'Adhesion (sticky) banner background', 'b': True}, f"{hx(ad['value'])} · {ad['source']} (iOS token {ad['name']}, iOS file). {ANS['adhesion_note']}", '—', ad['name'] + ' (System colors · iOS)', {'chip': 'iOS only'}])
    rows.append({'group': 'Sizes · iOS pt, Android dp'})
    for s in A['slots']:
        andr = f"{sz(s['phone'])} phone · {sz(s['tablet'])} tablet" if s['phone'] != s['tablet'] else f"{sz(s['phone'])} phone and tablet"
        toks = ' / '.join(dict.fromkeys(f"component.android.ad.{k}" for k in (s['phone'], s['tablet'])))
        if s['id'] == 'sticky-footer':
            ios, chip = 'None: iOS has no adhesion (sticky) banner (Apps team, 2026-11-18)', 'Android only'
        else:
            x = ios_slot['first' if s['id'] == 'first' else 'other']
            ios = (f"{isz(x['phone'])} phone · {isz(x['tablet'])} tablet" if x['phone'] != x['tablet'] else f"{isz(x['phone'])} phone and tablet") + ' (Apps team, 2026-11-18)'
            chip = 'Core'
        rows.append([{'t': s['name'] + (f" · {s['where']}" if s.get('where') else ''), 'b': True}, ios, andr, toks, {'chip': chip}])
    rows.append({'group': 'Rules and assets'})
    for r in A['rules']:
        rows.append(['Android rule', '—', r, '—', {'chip': 'Android only'}])
    rows.append(['iOS rule', ANS['rules'][1], '—', '—', {'chip': 'iOS only'}])
    for k in I['known'][:2]:
        rows.append(['iOS asset', k, '—', '—', {'chip': 'iOS only'}])
    T = {'name': '02 · Ad slots', 'title': 'Ad slots (as shipped)',
         'intro': ('Both apps show ads. The two ad colors are Core tokens. Android sets its slot sizes in code (first slot and sticky footer: banner, '
                   'other slots: 300 × 250); iOS uses the same sizes and has no sticky banner (Apps team, 2026-11-18). The Android slots are drawn from their tokens in the '
                   f'Android file ({AP} › 01). Documented as shipped, nothing new designed. ' + SRC),
         'columns': [{'name': 'Item', 'w': 220}, {'name': 'iOS', 'w': 380}, {'name': 'Android', 'w': 380}, {'name': 'Token', 'w': 280}, {'name': 'Ownership', 'w': 180}],
         'rows': rows}
    print(table('Layout · iOS vs Android', T))

elif MODE == 'android-ads':
    key = sys.argv[2]
    slots = [{'id': k, 'width': v['width'], 'height': v['height'], 'uses': uses[k]} for k, v in SZ.items()]
    print(extras('ads', {'page': AP, 'name': '01 · Ad slots', 'title': 'Ad slots (as shipped)', 'width': 1300, 'bgKey': key, 'slots': slots,
                         'rules': A['rules'],
                         'intro': ('Each slot is sized by its Components · Android variables (ad/<size>/width, height) and filled with the Core '
                                   'System colors ad/background. The dashed outline only marks the edge. Phone vs tablet comes from is_phone. ' + SRC)}))

elif MODE == 'android-widget':
    W = D['widget']
    rows = [[{'t': t['source'], 'b': True}, {'t': hx(t['value']), 'sw': t['value'], 'v': SYSA + t['name']}, {'t': hx(t['night'].lower()), 'sw': t['night'].lower()}, f"{t['name']} · {t['night_token']}"]
            for t in W['day_tokens']]
    rows += [{'group': 'Size and layout (Apps team, DREAMT-4719, 2026-11-19)'}, ['Size', W['answered']['size'], '—', '—'], ['Layout', W['answered']['layout'], '—', '—'],
             {'group': 'Also on the widget'}, ['Logo', W['logo'], '—', '—'], ['Icons', W['icons'], '—', '—']]
    T = {'name': '02 · Home-screen widget colors', 'title': 'Home-screen widget colors (as shipped)',
         'intro': ("Android only. Day colors are System colors · Android tokens, the same in all 77 markets. values-night changes only these four colors, "
                   "with no market overrides; night values and the size and layout come from the Apps team (DREAMT-4719, 2026-11-19), night tokens color.android-system.widget-night.*. " + SRC),
         'columns': [{'name': 'Color', 'w': 200}, {'name': 'Day value', 'w': 460}, {'name': 'Night value (values-night)', 'w': 360}, {'name': 'Token', 'w': 220}],
         'rows': rows}
    print(table(AP, T))

elif MODE == 'android-eedition':
    E = D['eedition']
    rows = [[{'t': c['what'], 'b': True}, {'t': hx(c['value']) + (f" (passed as {c['shipped_as']})" if c.get('shipped_as') else ''), 'sw': c['value'], 'v': SYSA + 'eedition-' + c['id']}, c['token']]
            for c in E['colors']]
    rows += [{'group': 'Contrast as shipped'}] + [[k.capitalize(), f'{v}:1', 'How the SDK paints these is not in the guide'] for k, v in E['contrast'].items()]
    T = {'name': '03 · eEdition (PageSuite) colors', 'title': 'eEdition (PageSuite) colors (as shipped)',
         'intro': f"Android only. {E['sdk']}. {' '.join(E['rules'])} iOS has its own eNewspaper viewer. " + SRC,
         'columns': [{'name': 'Color', 'w': 220}, {'name': 'Value', 'w': 480}, {'name': 'Token', 'w': 540}],
         'rows': rows}
    print(table(AP, T))

elif MODE == 'whats-new':
    W = D['whats_new_continue']
    rows = [{'group': 'Fill as shipped (majority = token; exceptions documented, not built, DEC-14)'}]
    for r in W['fills']:
        cell = {'t': hx(r['value']), 'sw': r['value']}
        if r['value'] == W['majority']: cell['v'] = SYSA + W['token_fill']
        rows.append([cell, f"{r['count']}: " + (', '.join(r['markets']) if r['count'] < 20 else 'majority'), f"{r['white_label_contrast']}:1", r['kind']])
    rows += [{'group': 'Shape and label'},
             [{'t': 'Radius', 'b': True}, f"{W['radius']['value']} dp", '—', f"{W['radius']['token']} (Components · Android whats-new-continue/radius)"],
             [{'t': 'Label', 'b': True}, f"{hx(W['label']['color'])}, {W['label']['case']}, {W['label']['font']} ({W['label']['font_key']}, {W['label']['font_markets']} of 77)", '—', W['answered']['label'] + ' (Apps team)'],
             [{'t': 'Height', 'b': True}, f"{W['answered']['padding']} dp padding, about {W['answered']['height_approx']} dp tall", '—', 'Apps team, DREAMT-4719, 2026-11-19'],
             [{'t': 'To clarify', 'b': True}, W['ask'], '—', 'Not drawn as a component until the fill is confirmed']]
    T = {'name': "04 · What's New Continue (as shipped)", 'title': "What's New Continue button (as shipped)",
         'intro': ("Android only (not in the iOS guide). CT, NYDN and VP override the button drawable, so their drawable color ships, not the color resource. "
                   "White-label contrast below 4.5:1 fails for text; values are kept as shipped. Label size and height: Apps team (DREAMT-4719, 2026-11-19). "
                   "The answer names whats_new_button_color as the fill in every market, which disagrees with the drawable overrides, so that is asked again (MISSING-ASSETS 5.6). " + SRC),
         'columns': [{'name': 'Fill / property', 'w': 300}, {'name': 'Markets / value', 'w': 560}, {'name': 'White label contrast', 'w': 180}, {'name': 'Kind / token', 'w': 360}],
         'rows': rows}
    print(table('Components · Button', T))
else:
    sys.exit(__doc__)

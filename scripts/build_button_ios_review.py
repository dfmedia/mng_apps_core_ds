"""iOS primary button review (Karl, 2026-11-18): our DEC-07 iOS spec next to the buttons iOS actually shows.
Findings only; nothing is rebuilt. Usage: python3 scripts/build_button_ios_review.py
Reads:  data/source/button-shipped.json (e30ad2585 style guide), data/button-decisions.json (DEC-07),
        data/source/apps-team-answers/2026-11-18-DREAMT-4718-ios.json (f79fe3339)
Writes: data/button-ios-review.json (read by scripts/figma_button_ios_review.py)
"""
import json
SHIP = json.load(open('data/source/button-shipped.json'))['primary']['ios']
LINK = json.load(open('data/source/button-shipped.json'))['text_link']['ios']
DEC = json.load(open('data/button-decisions.json'))
ANS = json.load(open('data/source/apps-team-answers/2026-11-18-DREAMT-4718-ios.json'))
B = ANS['buttons']
purchase = next(b for b in B['shipped'] if b['id'] == 'meter-purchase')
ex = B['log_in_link']['size_exceptions']
ex_txt = '; '.join(f"{sz} in {', '.join(ms)}" for sz, ms in ex.items())
comparison = [
 # property, our spec, shipped purchase button, verdict
 ('Based on', f"{SHIP['where']} (style guide, TroncKit e30ad2585)", f"{purchase['name']} (Apps team, f79fe3339)", 'Differs', 'Our source button is never shown: ' + B['login']),
 ('Fill', 'Brand theme action', f"{purchase['fill']} (= action)", 'Same', ''),
 ('Label font', f"{SHIP['font']['family']} {SHIP['font']['weight']} {SHIP['font']['size']}", purchase['label'], 'Same', ''),
 ('Label case', 'Always uppercase', purchase['text'], 'Unclear', 'Forced uppercase, or the text each market sets?'),
 ('Label color', SHIP['label_color'], 'Not stated', 'Unclear', 'Probably white; to confirm'),
 ('Radius', f"{SHIP['radius']} pt (legacy markets {SHIP['radius_legacy']} pt + {SHIP['border_legacy']} pt border)", f"{purchase['radius']} pt", 'Differs', 'Does the purchase button have a legacy-market variant?'),
 ('Height', f"{DEC['provisional']['ios_height']['value']} pt, provisional", purchase['height'], 'Differs', 'Fixed 45, or content-driven? ' + B['guideline']),
 ('Pressed', 'Native platform feedback', B['pressed'], 'Same', ''),
 ('Disabled', f"{DEC['provisional']['disabled']['fill']} / {DEC['provisional']['disabled']['label']} (Android values, new on iOS)", 'Not stated; not shipped on iOS', 'Unclear', ''),
 ('Text link font', f"{DEC['provisional']['ios_link_font']['postscript']} {DEC['provisional']['ios_link_font']['size']}, provisional", f"{B['log_in_link']['font']}; {ex_txt}", 'Differs', '8 markets use a smaller size'),
 ('Text link underline', 'None' if not LINK['underline'] else 'Underlined', B['log_in_link']['underline'] + ' in the default text', 'Differs', 'TDP screenshot: its own text is underlined throughout'),
]
out = {'generated_by': 'scripts/build_button_ios_review.py', 'status': 'Findings only. Karl, 2026-11-19: no rebuild until the Apps team answers MISSING-ASSETS 5.10', 'screenshot': 'TDP-6-paywall (f79fe3339): about 44–45 pt tall, radius about 8 pt, white bold uppercase label; the whole Log In text underlined',
       'sources': {'spec': 'DEC-07, data/source/button-shipped.json (TroncKit e30ad2585)', 'shipped': ANS['source']},
       'login': B['login'], 'single_primary': B['single_primary'], 'pressed': B['pressed'],
       'shipped': B['shipped'] + [{'id': 'subscription-option', 'name': 'Subscription option (earlier guide, e30ad2585)', 'height': None, 'radius': 8, 'label': 'Open Sans Bold 16', 'fill': 'subscriptionTintColor', 'text': None}],
       'not_shown': [{'name': SHIP['where'], 'why': B['login']}, {'name': 'Social sign-in row (Facebook, Google, Amazon)', 'why': B['login']}],
       'comparison': [dict(zip(('property', 'spec', 'shipped', 'verdict', 'note'), r)) for r in comparison],
       'questions': ['Is the purchase button label forced to uppercase, or the text each market sets?',
                     'Is the height fixed at 45 pt or content-driven (at least 45)?',
                     'Do the legacy-template markets (BS, DP, HC, MC, OS, SS, VP) draw the purchase button differently?',
                     'Is the label always white?']}
json.dump(out, open('data/button-ios-review.json', 'w'), indent=1, ensure_ascii=False)
print(len(out['shipped']), 'shipped buttons;', sum(r['verdict'] == 'Differs' for r in out['comparison']), 'differences;', len(out['questions']), 'questions')

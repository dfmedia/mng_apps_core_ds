"""Typography step 1: compare the shipped iOS and Android type styles by role (read-only review).
Usage: python3 scripts/compare_type.py
Reads:  data/source/ios-type.json, data/source/android-type.json (copied from the two style-guide artifacts)
Writes: data/type-comparison.json, docs/TYPE-COMPARISON.md
Values are read from the sources; only the role mapping below (which iOS style does the same job as which
Android style) is hand-made. Families are the majority-market font; per-market exceptions stay in each style's note.
Match:  same     same family, weight and size
        close    same family; size within 2 or weight differs
        differs  different family, or same family with size and weight both different
        ios-only / android-only   the other app has no such style
        unknown  the other app has the element, but its font is not in the export (MISSING-ASSETS 4.4)
                 (also when a style's size is known but its font is not, e.g. Android article-subhead)
"""
import json, re

IOS = json.load(open('data/source/ios-type.json'))
AND = json.load(open('data/source/android-type.json'))
FAM = {'sans': 'Open Sans', 'condensed': 'Open Sans Condensed', 'serif': 'PT Serif', 'display': 'Spectral',
       'spectral': 'Spectral', 'roboto': 'Roboto', 'playfair': 'Playfair Display'}
PARSE = [('Open Sans Condensed', 'Open Sans Condensed'), ('OpenSans', 'Open Sans'), ('Open Sans', 'Open Sans'),
         ('PT Serif', 'PT Serif'), ('Spectral', 'Spectral'), ('Roboto', 'Roboto'), ('Playfair', 'Playfair Display')]
LEGACY = 'BS, DP, HC, MC, OS, SS, VP'

def index(src):
    out = {}
    for g in src['groups']:
        for s in g['styles']:
            fam = FAM.get(s.get('family'))
            if not fam:   # Android styles without a family key name it in the usage text: majority font first, exceptions after
                u = s.get('usage', ''); hits = [(u.find(k), -len(k), v) for k, v in PARSE if k in u]
                fam = min(hits)[2] if hits else None
            out[s['name']] = {'style': s['name'], 'group': g['name'], 'family': fam, 'weight': int(s['fontWeight']),
                              'size': float(str(s['fontSize']).replace('px', '')), 'lineHeight': s.get('lineHeight'),
                              'letterSpacing': s.get('letterSpacing'), 'usage': s.get('usage', ''),
                              'legacy': 'legacy template only' in s.get('usage', ''),
                              'uppercase': bool(re.search(r'all caps|uppercase', s.get('usage', ''), re.I))}
    return out
I, A = index(IOS), index(AND)
# Android heading series: h2-h4 say "Same fonts as article-h1" (h4 is the same series: "h5 is 17sp, h6 16sp")
for h in ('article-h2', 'article-h3', 'article-h4'):
    A[h]['family'] = A['article-h1']['family']
# sf-headline says "same fonts" as the highlight headline
if 'same fonts' in A['sf-headline']['usage']: A['sf-headline']['family'] = A['sf-headline-highlight']['family']

# role, group, iOS style, Android style, note.  '?' = the app has the element but the export has no font for it.
ROLES = [
 ('Article headline', 'Article', 'page-title', 'article-headline', ''),
 ('Article headline, tablet', 'Article', 'page-title-tablet', None, ''),
 ('Article body', 'Article', 'page-body', 'article-body', ''),
 ('Article body bold', 'Article', 'page-body-bold', None, 'Android uses the article bold font only for headings'),
 ('Article body italic', 'Article', 'page-body-italic', None, ''),
 ('Article body bold italic', 'Article', 'page-body-bolditalic', None, ''),
 ('Article body light italic', 'Article', 'page-body-lightitalic', None, ''),
 ('Article subhead', 'Article', 'page-subhead', 'article-subhead', ''),
 ('Article heading h1', 'Article', None, 'article-h1', 'h2 20, h3 19, h4 18, h5 17, h6 16 follow the same font'),
 ('Article heading h2', 'Article', None, 'article-h2', ''),
 ('Article heading h3', 'Article', None, 'article-h3', ''),
 ('Article heading h4', 'Article', None, 'article-h4', ''),
 ('Article deck', 'Article', 'page-deck', None, ''),
 ('Article kicker', 'Article', 'page-kicker', None, ''),
 ('Article byline', 'Article', 'page-byline', 'article-byline', ''),
 ('Article dateline', 'Article', None, 'article-dateline', ''),
 ('Image caption', 'Article', 'page-caption', 'article-caption', ''),
 ('Image credit', 'Article', None, 'article-image-credit', ''),
 ('Pull quote', 'Article', None, 'article-pullquote', ''),
 ('Author bio', 'Article', 'page-bio', None, ''),
 ('Gallery title', 'Article', 'page-gallery', None, ''),
 ('Slogan', 'Article', 'page-slogan', None, ''),
 ('Section-front headline', 'Section front', 'cell-headline', 'sf-headline', 'Android: base size; PageBuilder multiplies it (normal x1.18, about 19sp on phones)'),
 ('Section-front headline, highlight', 'Section front', 'cell-headline-highlight', 'sf-headline-highlight', 'Android: base size x PageBuilder size'),
 ('Section-front headline, thin', 'Section front', 'cell-headline-thin', 'sf-headline-thin', ''),
 ('Section-front blurb', 'Section front', 'cell-body', 'sf-blurb', ''),
 ('Section-front byline / timestamp', 'Section front', 'cell-timestamp', 'sf-byline', ''),
 ('Section-front label (kicker)', 'Section front', 'cell-label-bold-large', 'sf-label', ''),
 ('Section-front caption', 'Section front', 'cell-caption', None, ''),
 ('Section-front deck', 'Section front', 'cell-deck', None, ''),
 ('Headline, media above', 'Section front', 'cell-headline-media-above', None, ''),
 ('Headline, media bottom', 'Section front', 'cell-headline-media-bottom', None, ''),
 ('Headline, media left', 'Section front', 'cell-headline-media-left', None, ''),
 ('Headline, media left (regular)', 'Section front', 'cell-headline-media-left-normalfont', None, ''),
 ('Headline, bullets', 'Section front', 'cell-headline-bullets', None, ''),
 ('Label, light large', 'Section front', 'cell-label-light-large', None, ''),
 ('Label, bold small', 'Section front', 'cell-label-bold-small', None, ''),
 ('Label, light small', 'Section front', 'cell-label-light-small', None, 'Named light, ships Bold'),
 ('Score', 'Section front', 'cell-score', None, ''),
 ('Tertiary headline', 'Section front', 'cell-tertiary', None, ''),
 ('Tertiary header text', 'Section front', 'cell-tertiary-headertext', None, ''),
 ('Tertiary timestamp', 'Section front', 'cell-timestamp-tertiary', None, ''),
 ('AR headline', 'Section front', 'ar-headline', None, ''),
 ('Legacy: headline default', 'Section front', 'cell-headline-default', None, ''),
 ('Legacy: blurb', 'Section front', 'cell-blurb', None, ''),
 ('Legacy: card text', 'Section front', 'cell-card-text-default', None, ''),
 ('Legacy: label default', 'Section front', 'cell-label-default', None, ''),
 ('Legacy: signature', 'Section front', 'cell-signature', None, ''),
 ('Legacy: kicker left', 'Section front', 'label-kicker-left', None, ''),
 ('Legacy: label small left', 'Section front', 'label-normal-small-left', None, ''),
 ('Top bar title', 'App', 'nav-title', '?', ''),
 ('Bottom tab label', 'App', 'tab-item', 'nav-label', ''),
 ('Section tabs', 'App', '?', 'section-tab', 'Android size: 12sp in articles, 14sp in notifications'),
 ('Sections list header', 'App', 'section-list-header', None, ''),
 ('Menu header', 'App', 'menu-header', None, ''),
 ('Menu item', 'App', 'menu-text', None, ''),
 ('Settings row', 'App', '?', 'settings-item', ''),
 ('Settings header', 'App', '?', 'settings-category', ''),
 ('Search result headline', 'App', '?', 'search-headline', ''),
 ('Shared headline (TroncAppThemeable)', 'App', 'headline', None, 'iOS generic fonts every market defines'),
 ('Shared body', 'App', 'body', None, ''),
 ('Shared body bold', 'App', 'body-bold', None, ''),
 ('Shared caption', 'App', 'caption', None, ''),
 ('Shared caption bold', 'App', 'caption-bold', None, ''),
 ('Paywall heading', 'Paywall', 'blocker-header', 'paywall-heading', ''),
 ('Paywall heading, large', 'Paywall', 'blocker-header-regular', None, ''),
 ('Paywall body', 'Paywall', 'blocker-description', 'paywall-text', ''),
 ('Paywall buy text', 'Paywall', 'blocker-buy', None, ''),
 ('Paywall buy text, large', 'Paywall', 'blocker-buy-regular', None, ''),
 ('Paywall store policy header', 'Paywall', 'blocker-store-policy-header', None, ''),
 ('Paywall log-in text', 'Paywall', 'blocker-login', None, ''),
 ('Paywall log-in text, large', 'Paywall', 'blocker-login-regular', None, ''),
 ('Paywall price', 'Paywall', 'blocker-price', None, ''),
 ('Paywall plan name', 'Paywall', 'blocker-name', None, ''),
 ('Continue button label', 'Paywall', None, 'continue-label', 'iOS draws Continue as PNG images (DSC-24)'),
]

def match(i, a):
    if i == '?' or a == '?': return 'unknown'
    if not a: return 'ios-only'
    if not i: return 'android-only'
    if i['family'] is None or a['family'] is None: return 'unknown'
    if i['family'] != a['family']: return 'differs'
    if i['weight'] == a['weight'] and i['size'] == a['size']: return 'same'
    if i['weight'] == a['weight'] and abs(i['size'] - a['size']) <= 2: return 'close'
    if i['size'] == a['size']: return 'close'
    return 'differs'

used_i, used_a, rows = set(), set(), []
for role, group, si, sa, note in ROLES:
    i = I[si] if si not in (None, '?') else si
    a = A[sa] if sa not in (None, '?') else sa
    if isinstance(i, dict): used_i.add(si)
    if isinstance(a, dict): used_a.add(sa)
    rows.append({'role': role, 'group': group, 'ios': i, 'android': a, 'match': match(i, a), 'note': note})
missing = sorted(set(I) - used_i) + sorted(set(A) - used_a)
assert not missing, f'styles not mapped to a role: {missing}'

fams = lambda X: sorted({s['family'] for s in X.values() if s['family']})
counts = {}
for r in rows: counts[r['match']] = counts.get(r['match'], 0) + 1
out = {'generated_by': 'scripts/compare_type.py', 'counts': counts, 'families': {'ios': fams(I), 'android': fams(A)},
       'styles': {'ios': len(I), 'android': len(A)}, 'legacy_markets': LEGACY, 'roles': rows}
json.dump(out, open('data/type-comparison.json', 'w'), indent=1, ensure_ascii=False)

# docs/TYPE-COMPARISON.md
W = {200: 'ExtraLight', 300: 'Light', 400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}
def fmt(s):
    if s == '?': return 'not in the export'
    if not s: return '—'
    n = f"{s['family'] or 'font not in the export,'} {W[s['weight']]} {s['size']:g}"
    if s['uppercase']: n += ', caps'
    if s['lineHeight']: n += f", line x{s['lineHeight']}"
    return f"{n} (`{s['style']}`)"
LABEL = {'same': '✅ same', 'close': '🟡 close', 'differs': '🔴 differs', 'ios-only': 'iOS only', 'android-only': 'Android only', 'unknown': '❓ unknown'}
L = ['# Typography: iOS vs Android', '',
     'Generated by `scripts/compare_type.py` from `data/source/ios-type.json` and `data/source/android-type.json`. Do not edit by hand. Step 1 of the typography work: a read-only review, nothing decided yet.', '',
     f"iOS ships {len(I)} styles (TroncKit Style.json + TroncAppThemeable); Android ships {len(A)} (styles and dimens in android-tribpub). Sizes are pt on iOS and sp on Android. Fonts are the majority-market value; per-market exceptions are in each style's source note.", '',
     '## Summary', '', '| Match | Roles |', '|---|---|'] + [f'| {LABEL[k]} | {counts.get(k, 0)} |' for k in LABEL] + ['',
     '## Font families', '',
     f"- **iOS:** {', '.join(fams(I))}. Standard template: Spectral for headlines and article body, Open Sans for UI and labels, PT Serif for some cell headlines.",
     f"- **Android:** {', '.join(fams(A))}. PT Serif for headlines and article body in most markets, Open Sans for UI, Roboto (system) for settings and paywall text, Playfair Display for the paywall heading.",
     '- **Biggest difference:** the serif. iOS sets headlines and article text in Spectral; Android sets them in PT Serif. Both apps bundle both fonts.',
     f"- **Legacy template (iOS, {LEGACY}):** 7 extra styles plus different values for many others (see each note).", '']
for g in dict.fromkeys(r['group'] for r in rows):
    L += [f'## {g}', '', '| Role | iOS | Android | Match | Note |', '|---|---|---|---|---|']
    for r in rows:
        if r['group'] == g:
            L.append(f"| {r['role']} | {fmt(r['ios'])} | {fmt(r['android'])} | {LABEL[r['match']]} | {r['note']} |")
    L.append('')
open('docs/TYPE-COMPARISON.md', 'w').write('\n'.join(L))
print(len(rows), 'roles:', counts)

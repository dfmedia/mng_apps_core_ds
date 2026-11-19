"""Bug report for the Apps team: production problems the design-system work found, per app, with evidence and a suggested fix.
Usage: python3 scripts/build_bug_report.py   (after the token and comparison scripts)
Reads:  data/source/markets.json (iOS f79fe3339), data/source/android-markets.json (1cfb069a6), data/palette-analysis.json,
        data/button-spec.json, data/shell-colors.json, data/source/apps-team-answers/*.json
Writes: docs/BUG-REPORT.md (written for the Apps team: no internal file paths in the rows; our IDs only in the last column)
Every number is computed here from the data; the wording of each bug is hand-written below.
"""
import json

def load(fn):
    d = json.load(open(fn)); T = {t: i for i, t in enumerate(d['tokens'])}
    return {m['code']: {k: (m['values'][i] or '') for k, i in T.items()} for m in d['markets']}
I, A = load('data/source/markets.json'), load('data/source/android-markets.json')
PA = {m['code']: m for m in json.load(open('data/palette-analysis.json'))['markets']}
BS = json.load(open('data/button-spec.json'))
SH = json.load(open('data/shell-colors.json'))
ANS_I = json.load(open('data/source/apps-team-answers/2026-11-19-DREAMT-4718-ios.json'))
h6 = lambda v: ('#' + v.lstrip('#')[-6:]).lower() if v else None
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def ratio(a, b):
    x, y = lum(a), lum(b); return round((max(x, y) + 0.05) / (min(x, y) + 0.05), 2)
fails = lambda cid: sorted(c for c in PA if not next(x for x in PA[c]['checks'] if x['id'] == cid)['pass'])
lst = lambda xs: ', '.join(xs)

# ---- computed evidence
white_nav = sorted(c for c in I if h6(I[c]['navigationBarBackgroundColor']) == '#ffffff')
alert_ff = fails('alert')
tivdb_alert_text = h6(I['TIVDB']['breakingNewsBannerTextColor'])
spin = ANS_I['loading']['spinner']
spin_all = {**{c: spin['majority'] for c in I}, **spin['exceptions']}
spin_low = sorted((c, v, ratio(v.lower(), '#ffffff')) for c, v in spin['exceptions'].items() if ratio(v.lower(), '#ffffff') < 3)
alink = {c: h6(A[c]['Paywall_LoginButton_Text']) for c in A}
alink_invisible = sorted(c for c, v in alink.items() if ratio(v, '#ffffff') < 1.5)
alink_low = sorted(c for c, v in alink.items() if 1.5 <= ratio(v, '#ffffff') < 4.5)
label_fail = BS['summary']['label_fail']; ios_link_fail = BS['summary']['ios_link_fail']
tsar15 = next(e['android15'] for e in SH['role_exceptions'] if e['code'] == 'tsar' and e.get('android15'))

S, M, L_ = 'High', 'Medium', 'Low'
BUGS = {'iOS': [
  (S, 'Manage App Subscription button is white on white', f"In the {len(white_nav)} markets with a white nav bar ({lst(white_nav)}) the button is filled with the nav bar color and has white text, so it can't be read.",
   'Apps team answer (code, not checked on a device).', 'Use a fill that gives white text 4.5:1 in every market (for example the market action color), or dark text on white.', 'DSC-34'),
  (M, 'Breaking-news banner text fails contrast', f"White on #ff0000 is {ratio('#ffffff', '#ff0000')}:1 (needs 4.5:1) in {len(alert_ff)} markets. Android uses #cf000e ({ratio('#ffffff', '#cf000e')}:1).",
   'Export (breakingNewsBannerBackgroundColor).', 'Use #cf000e, like Android.', 'DSC-15'),
  (L_, 'TIVDB breaking-news text is black', f"Black text ({tivdb_alert_text}) passes on today's #ff0000 ({ratio(tivdb_alert_text or '#000000', '#ff0000')}:1) but fails on #cf000e ({ratio(tivdb_alert_text or '#000000', '#cf000e')}:1), so it breaks when the red is fixed (item above).",
   'Export (breakingNewsBannerTextColor).', 'White text, like every other market, together with the red fix.', 'DSC-19'),
  (M, 'Loading spinner hard to see in some markets', 'The spinner sits on a white card. ' + '; '.join(f'{c} {v} is {r}:1' for c, v, r in spin_low) + ' (graphics need 3:1).',
   'Apps team answer (spinner colors, corrected list).', 'Use a darker spinner color in these markets (or the default #004E87).', ''),
  (M, 'Blank logo on the Manage Subscription screen', 'The 100 pt logo at the top of the Manage Subscription modal (ManageSubscriptionIcon) has no image file, so the area is empty in every market.',
   'Apps team answer.', 'Add the market logo, or remove the empty space.', 'ICON-04'),
  (M, 'Paywall Log In link fails contrast', f"The link color (paywallLinkColor) is under 4.5:1 on the white paywall in {len(ios_link_fail)} markets: {lst(ios_link_fail)}.",
   'Export.', 'Darken the link color in those markets.', 'CLR-04'),
  (L_, 'Brand colors copied from the wrong market', 'TLR uses Lowell Sun red #ab4021 (should be #4e5dca); TUDJ uses Vacaville blue #408fcc (should be #32408f); TBE uses #0070b8 (should be #4351af). Android and the migration sheet agree on the right value.',
   'Export vs Android and the migration sheet.', 'Set the right brand color in those three markets.', 'DSC-02, DSC-03, DSC-04'),
  (L_, 'Brand colors off by one in a color channel', 'TroncKit stores each channel as a 2-decimal fraction, so many colors come back 1 off (for example #22 becomes #21). Invisible, but the values no longer match the brand.',
   'Export vs Android and the migration sheet (36 markets).', 'Store colors as hex.', 'DSC-01'),
  (L_, 'Unused code and assets', 'UIImage(systemName: "saved") in updateTabBasedOnIsPagesuite() (never called; "saved" is not an SF Symbol) and the tab-newspaper image set (only referenced by an unused property).',
   'Apps team answers.', 'Remove them.', ''),
], 'Android': [
  (S, 'Paywall Log In link may be invisible in OS, SS and TSAR', f"The link uses Paywall_LoginButton_Text, which is {', '.join(f'{c} {alink[c].upper()}' for c in alink_invisible)}: white on the white paywall.",
   'Export; screenshots show the link in this color in TDP and NYDN.', 'Use a dark or brand color in those markets. (Asked as question 5.11.)', 'MISSING-ASSETS 5.11'),
  (M, 'Paywall Log In link fails contrast everywhere else', f"{len(alink_low)} markets use a color under 4.5:1 on white; most use #56A1DD ({ratio('#56a1dd', '#ffffff')}:1).",
   'Export and screenshots.', 'Darken the link (or use the market action color where it passes).', 'CLR-04'),
  (M, 'TSAR status bar icons invisible on Android 15+', f"The status bar is {tsar15['statusbar'].upper()} with white icons: {tsar15['contrast']}:1.",
   'Confirmed in production (Apps team).', 'Use dark icons when the bar is light, not only when it is exactly #FFFFFF.', 'CLR-09'),
  (M, 'Article text size is not remembered, and the Settings entry does nothing', 'The chosen size is not re-applied after a cold start (FontSizeManager.init() is never called), and the Settings text-size entry is in no preference XML and has an empty handler. Steps are raw px, so they shrink on denser screens.',
   'Android style guide and Apps team answer.', 'Call FontSizeManager.init() at start-up; wire or remove the Settings entry; scale in sp or a percentage.', 'TYPE-07'),
  (L_, 'NYDN font file name typo', 'StreamModule_Font_Time_And_Blurb points to OpenSansCondensed-Bold.ttff (double f), so the time / blurb line falls back to Roboto.',
   'Apps team answer.', 'Rename to OpenSansCondensed-Bold.ttf. (MC also has two unused strings pointing to OpenSans-Semibold.ttf; delete them.)', 'TYPE-06'),
  (L_, 'Brand colors that differ from iOS and the migration sheet', 'MC primary button uses Hartford blue #4fa8d1 (should be #539cc4); TEPTG uses green #3e8e75 (should be #32408f); SIT selected tab #149ce5 (should be #ffea00).',
   'Export vs iOS and the migration sheet.', 'Set the right brand color in those markets.', 'DSC-05, DSC-07, DSC-08'),
], 'Both apps': [
  (M, 'White text on the primary button fails contrast', f"White on the market action color is under 4.5:1 in {len(label_fail)} markets: {lst(label_fail)}.",
   'Export (both apps ship white on action).', 'Darken action in those markets (suggested values in the design system), or use black text.', 'CLR-04'),
  (M, 'Nav bar title, selected tab and section header fail contrast in some iOS markets', f"Nav title under 4.5:1 in {len(fails('nav'))} ({lst(fails('nav'))}); selected tab under 3:1 in {len(fails('tab'))}; header text under 4.5:1 in {len(fails('header'))}.",
   'Export (iOS values; Android mostly the same colors).', 'Darken those market colors.', 'CLR-02, CLR-03, CLR-05'),
], 'Style guides': [
  (L_, 'Android guide: savings label text color', 'The guide says #004E87; the VP screenshot shows the text and 2dp outline in the market color.', 'Screenshots (5.3).', 'Correct the guide. (Asked on the Android ticket.)', ''),
  (L_, 'Android guide: Log In link color', "The Buttons table says #000000 (Paywall_Text); production uses Paywall_LoginButton_Text.", 'Screenshots (5.3).', 'Correct the guide.', ''),
]}

L = ['# Bug report: what the design-system work found in the apps', '',
     'Generated by `scripts/build_bug_report.py` from the app exports (iOS TroncKit `f79fe3339`, Android android-tribpub `1cfb069a6`), the Apps team answers (DREAMT-4718, DREAMT-4719) and the Android screenshots. Do not edit by hand.', '',
     'Written for the Apps team. Each row is something that ships today and looks wrong: what it is, which markets, how we know, and a suggested fix. '
     'Contrast targets: text 4.5:1, icons and large text 3:1 (WCAG AA). The design system documents these values as shipped and does not change the apps; open questions stay in docs/MISSING-ASSETS.md.', '',
     f"**Summary:** {sum(len(v) for v in BUGS.values())} items: " + ', '.join(f"{k} {len(v)}" for k, v in BUGS.items()) + '. '
     + ', '.join(f"{sum(1 for v in BUGS.values() for b in v if b[0] == s)} {s.lower()}" for s in (S, M, L_)) + '.', '',
     'Priority: **High** = can\'t be read or used · **Medium** = fails contrast or misbehaves · **Low** = data or naming, no visible harm.', '']
for app, bugs in BUGS.items():
    L += [f'## {app}', '', '| # | Priority | Bug | Details | Evidence | Suggested fix | Our ref |', '|---|---|---|---|---|---|---|']
    n = 0
    for pr, title, det, ev, fix, ref in sorted(bugs, key=lambda b: (S, M, L_).index(b[0])):
        n += 1; L.append(f"| {n} | {pr} | {title} | {det} | {ev} | {fix} | {ref or '—'} |")
    L.append('')
open('docs/BUG-REPORT.md', 'w').write('\n'.join(L) + '\n')
print(f"{sum(len(v) for v in BUGS.values())} bugs; white nav {len(white_nav)}, alert {len(alert_ff)}, android link invisible {alink_invisible}, low {len(alink_low)}, spinner low {spin_low}")

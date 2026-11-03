"""Typography step 2 (DEC-09): every shipped text style as a token, per platform, exactly as in production.
Usage: python3 scripts/build_type_tokens.py   (after compare_type.py; then `npm run build`)
Reads:  data/source/ios-type.json, data/source/android-type.json, data/type-comparison.json (role names)
Writes: tokens/ios/type.tokens.json       type.ios.<role>       (63 iOS styles; legacy-template values in $extensions.mng.legacy)
        tokens/android/type.tokens.json   type.android.<role>   (26 Android styles; asset file names for TypefaceCache)
        data/type-styles.json             the Figma text styles to build in the iOS and Android files
        docs/TYPE-STYLES.md               every style with its Figma name, token and code name (generated)
Values are the majority-market production values. Per-market font exceptions (NYDN, VP, the Android Open Sans group…)
are kept as text in $extensions.mng.exceptions; they are not tokens yet (backlog: foundation/type-markets).
"""
import json, re

IOS = json.load(open('data/source/ios-type.json'))
AND = json.load(open('data/source/android-type.json'))
CMP = json.load(open('data/type-comparison.json'))
LEGACY = ['BS', 'DP', 'HC', 'MC', 'OS', 'SS', 'VP']

PS_FAMILY = [('OpenSansCondensed', 'Open Sans Condensed'), ('OpenSans_Condensed', 'Open Sans Condensed'), ('OpenSans', 'Open Sans'),
             ('PTSerif', 'PT Serif'), ('Spectral', 'Spectral'), ('Open Sans', 'Open Sans')]
PS_WEIGHT = {'ExtraLight': 200, 'Light': 300, 'Regular': 400, 'Medium': 500, 'SemiBold': 600, 'Semibold': 600, 'Bold': 700, 'ExtraBold': 800}
FIGMA_STYLE = {200: 'ExtraLight', 300: 'Light', 400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}

def from_postscript(ps):
    """'Spectral-BoldItalic' -> ('Spectral', 700, True); 'Open Sans' -> ('Open Sans', 400, False)"""
    fam = next(v for k, v in PS_FAMILY if ps.startswith(k))
    suffix = ps.split('-', 1)[1] if '-' in ps else 'Regular'
    italic = suffix.endswith('Italic')
    w = suffix[:-6] if italic else suffix
    return fam, PS_WEIGHT.get(w or 'Regular', 400), italic

def figma_style(w, italic):
    s = FIGMA_STYLE[w]
    if italic: s = 'Italic' if s == 'Regular' else s + ' Italic'
    return s

def slug(role):
    return re.sub(r'[^a-z0-9]+', '-', role.lower()).strip('-')
def short(role, group):
    """Figma name inside its group: 'Article headline' in Article -> 'Headline'; drops '(TroncAppThemeable)' and 'Legacy: '."""
    r = re.sub(r'\s*\(TroncAppThemeable\)', '', role).replace('Legacy: ', '')
    for p in (group, group.replace(' ', '-')):
        if r.lower().startswith(p.lower() + ' '):
            r = r[len(p) + 1:]
            break
    return r[:1].upper() + r[1:]
def camel(role):
    parts = re.sub(r'[^A-Za-z0-9]+', ' ', role).split()
    return parts[0].lower() + ''.join(p[:1].upper() + p[1:] for p in parts[1:])

role_of = {}
for r in CMP['roles']:
    for side in ('ios', 'android'):
        if isinstance(r[side], dict): role_of[(side, r[side]['style'])] = (r['role'], r['group'])

def styles(src):
    for g in src['groups']:
        for s in g['styles']: yield g['name'], s

def tok(value, desc, **ext):
    return {'$value': value, '$type': 'typography', '$description': desc, '$extensions': {'mng': ext}}

ios_tokens, and_tokens, figma, legacy_rows = {}, {}, [], []

# ---- iOS: the font comes from the production postscript name in the source note
for gname, s in styles(IOS):
    u = s['usage']
    m = re.search(r'((?:OpenSans|OpenSansCondensed|OpenSans_Condensed|PTSerif|Spectral)-[A-Za-z]+|Open Sans) (\d+(?:\.\d+)?) in \d+ of \d+', u)
    ps, size = m.group(1), float(m.group(2))
    fam, w, it = from_postscript(ps)
    role, group = role_of[('ios', s['name'])]
    legacy_only = 'legacy template only' in u
    lm = re.search(r'Legacy template \([^)]*\): ([A-Za-z_-]+) (\d+(?:\.\d+)?)', u)
    legacy = None
    if lm:
        lf, lw, li = from_postscript(lm.group(1))
        legacy = {'postscript': lm.group(1), 'fontFamily': lf, 'fontWeight': lw, 'italic': li, 'fontSize': float(lm.group(2)), 'markets': LEGACY}
    exc = '; '.join(x.group(0) for x in re.finditer(r'(Exceptions|Other values): [^.]*', u))
    key = slug(role)
    # DEC-10: the iOS legacy template is acknowledged only (data/legacy-template.json, docs/LEGACY-TEMPLATE.md), not built
    if legacy_only or legacy:
        lv = legacy or {'postscript': ps, 'fontSize': size}
        legacy_rows.append({'role': role, 'group': group, 'style': s['name'], 'legacyOnly': legacy_only,
                            'standard': None if legacy_only else f'{ps} {size:g}', 'legacy': f"{lv['postscript']} {lv['fontSize']:g}"})
    if legacy_only:
        continue
    ios_tokens[key] = tok({'fontFamily': fam, 'fontWeight': w, 'fontSize': f'{size:g}px', 'fontStyle': 'italic' if it else 'normal'},
                          f'{role} (iOS `{s["name"]}`): {ps} {size:g} pt',
                          role=role, group=group, style=s['name'], postscript=ps, code=camel(role),
                          exceptions=exc, source='TroncKit Style.json / TroncAppThemeable')
    base = {'platform': 'ios', 'token': f'type.ios.{key}', 'family': fam, 'figmaStyle': figma_style(w, it), 'size': size,
            'lineHeight': None, 'letterSpacingEm': None, 'uppercase': False, 'style': s['name'], 'postscript': ps}
    figma.append({**base, 'name': f'{group}/{short(role, group)}', 'legacy': False})

# ---- Android: family + asset file from the bundled font list
FILES = {(f['family'], int(f['weight']), f['style'] == 'italic'): f['file'].split('/')[-1] for f in AND['fonts']}
FAM = {'sans': 'Open Sans', 'condensed': 'Open Sans Condensed', 'serif': 'PT Serif', 'spectral': 'Spectral', 'roboto': 'Roboto', 'playfair': 'Playfair Display'}
cmp_android = {r['android']['style']: r['android'] for r in CMP['roles'] if isinstance(r['android'], dict)}
for gname, s in styles(AND):
    c = cmp_android[s['name']]
    fam, w, size = c['family'], int(s['fontWeight']), float(str(s['fontSize']).replace('px', ''))
    role, group = role_of[('android', s['name'])]
    asset = FILES.get((fam, w, False)) if fam and fam != 'Roboto' else None
    if fam == 'Open Sans Condensed' and w == 300: asset = 'OpenSans-Regular-Condensed.ttf'   # production file name (see source note)
    ls = float(s['letterSpacing'].replace('em', '')) if s.get('letterSpacing') else None
    caps = bool(re.search(r'all caps', s['usage'], re.I))
    lh = float(s['lineHeight']) if s.get('lineHeight') else None
    exc = re.search(r'(?:;|\.) ([^.;]*in (?:DP|CT|NYDN|MC|HC|SS)[^.]*)', s['usage'])
    key = slug(role)
    val = {'fontFamily': fam or 'unknown', 'fontWeight': w, 'fontSize': f'{size:g}px'}
    if lh: val['lineHeight'] = lh
    if ls: val['letterSpacing'] = f'{ls}em'
    and_tokens[key] = tok(val, f'{role} (Android `{s["name"]}`): {fam or "font not in the export"} {FIGMA_STYLE[w]} {size:g}sp',
                          role=role, group=group, style=s['name'], asset=asset, system=fam == 'Roboto', code=camel(role), uppercase=caps,
                          fontKnown=fam is not None, exceptions=exc.group(1) if exc else '', source='android-tribpub styles/dimens')
    figma.append({'platform': 'android', 'token': f'type.android.{key}', 'name': f'{group}/{short(role, group)}', 'family': fam, 'figmaStyle': FIGMA_STYLE[w],
                  'size': size, 'lineHeight': lh, 'letterSpacingEm': ls, 'uppercase': caps, 'style': s['name'], 'asset': asset, 'legacy': False})

meta = {'$description': 'Generated by scripts/build_type_tokens.py (DEC-09). Production values per platform. Do not edit by hand.'}
json.dump({**meta, 'type': {'ios': ios_tokens}}, open('tokens/ios/type.tokens.json', 'w'), indent=1, ensure_ascii=False)
json.dump({**meta, 'type': {'android': and_tokens}}, open('tokens/android/type.tokens.json', 'w'), indent=1, ensure_ascii=False)
json.dump({'generated_by': 'scripts/build_type_tokens.py', 'styles': figma}, open('data/type-styles.json', 'w'), indent=1, ensure_ascii=False)
json.dump({'generated_by': 'scripts/build_type_tokens.py', 'markets': LEGACY, 'type': legacy_rows}, open('data/legacy-template-type.json', 'w'), indent=1, ensure_ascii=False)

L = ['# Text styles (production values)', '',
     'Generated by `scripts/build_type_tokens.py` (DEC-09). Do not edit by hand. Each app keeps its own fonts and sizes, exactly as shipped; Core defines the role names, which are the same in both Figma files so mockups can swap between libraries. Comparison: docs/TYPE-COMPARISON.md.', '',
     '- **iOS:** text styles in the MNG iOS Figma file; tokens `type.ios.*`; Swift `MNGTextStyle.<name>` (Tokens/MNGTypeStyles.swift).',
     f'- **iOS legacy template ({", ".join(LEGACY)}):** acknowledged only, not built (DEC-10). Its values are listed in docs/LEGACY-TEMPLATE.md.',
     '- **Android:** text styles in the MNG Android Figma file; tokens `type.android.*`; Kotlin `MngTypeStyles.<NAME>` (tokens/MngTypeStyles.kt) with the asset file the app loads through TypefaceCache.', '',
     '| Platform | Figma style | Font | Size | Extras | Code | Source style |', '|---|---|---|---|---|---|---|']
for f in figma:
    tk = (ios_tokens if f['platform'] == 'ios' else and_tokens)[f['token'].split('.')[-1]]['$extensions']['mng']
    extras = ', '.join(x for x in [f'line ×{f["lineHeight"]:g}' if f['lineHeight'] else '', f'tracking {f["letterSpacingEm"]}em' if f['letterSpacingEm'] else '', 'caps' if f['uppercase'] else ''] if x)
    font = f"{f['family'] or 'not in the export'} {f['figmaStyle']}"
    L.append(f"| {'iOS' if f['platform'] == 'ios' else 'Android'} | {f['name']} | {font} | {f['size']:g} | {extras} | `{tk['code']}` | `{f['style']}` |")
open('docs/TYPE-STYLES.md', 'w').write('\n'.join(L) + '\n')
print(f"legacy (acknowledged only): {len(legacy_rows)} rows; iOS {len(ios_tokens)} tokens, Android {len(and_tokens)} tokens, Figma styles: iOS {sum(f['platform']=='ios' for f in figma)} (legacy {sum(f['legacy'] for f in figma)}), Android {sum(f['platform']=='android' for f in figma)}")

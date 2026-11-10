"""System colors step 2 (DEC-16): majority tokens for the themed colors, every market documented, exceptions not built.

Usage: python3 scripts/build_system_tokens.py   (after scripts/compare_system_colors.py, before npm run build)
Reads:  data/system-color-comparison.json, data/system-color-pairs.json
Writes: tokens/core/system.tokens.json      Core: the 11 approved pairs (5 same value, 6 with a value per platform)
        tokens/ios/system.tokens.json       iOS-only system colors
        tokens/android/system.tokens.json   Android-only system colors
        data/system-tokens.json             flat list for the Figma build (scripts/figma/build_system_variables.js)
        docs/SYSTEM-TOKENS.md               every token: value, source key, kind, markets, exceptions

Rules (DEC-14 / DEC-16):
  fixed     one value (same in all 77 markets)
  majority  the majority value; the markets that ship something else are listed in $extensions.mng.exceptions (documented, not built)
  follows   no value of its own: it is the market's brand role (`action`, `navbar`, `navtext`; Android `accent` = action per DEC-14).
            Listed in the group's `$extensions.mng.follows` (not a token); code reads the brand palette, Figma aliases the Core Brand theme variable.
  not set   iOS leaves it to UIKit: the UIKit default is named (`uikit`), with its light-mode value for Figma.
Colors that already have tokens (brand, app shell, controls, buttons) and the Android launcher icon background (DEC-16) are skipped.
"""
import json, re

C = json.load(open('data/system-color-comparison.json'))
PAIRS = json.load(open('data/system-color-pairs.json'))['pairs']
P = C['platforms']
# UIKit defaults used when iOS leaves a color unset (light mode). Named so Swift uses the system color itself.
UIKIT = {'sectionListSectionSeparatorColor': ('separator', '#3c3c4349', 'UITableView default separator (UIColor.separator, light: 60, 60, 67 at 29%)'),
         'trackingConsentSwitchOnTintColor': ('systemGreen', '#34c759', 'UISwitch default on tint (UIColor.systemGreen, light)')}
ROLE = {'action': 'action', 'navbar': 'navbar', 'navtext': 'navtext', 'accent': 'action'}   # DEC-14: Android accent is built as action

def kebab(key, plat):
    if plat == 'ios':
        key = re.sub(r'Color$', '', key)
        key = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', '-', key)          # HUDBackground -> HUD-Background
        return re.sub(r'(?<=[a-z0-9])([A-Z])', r'-\1', key).lower()
    return key.replace('_', '-').lower()
def rgb(h):
    if not h or not h.startswith('#'): return None
    out = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
    return out + [round(int(h[7:], 16) / 255, 2)] if len(h) == 9 else out
def desc(c, plat, extra=''):
    k = c['kind']
    n = c['follows_markets'] if k == 'follows' else c['majority_markets']
    base = {'fixed': 'same in all 77 markets', 'majority': f'{n} of 77 markets; exceptions documented only (DEC-16)',
            'follows': f"follows {c['follows']} in {n} of 77 markets; exceptions documented only (DEC-16)"}.get(k, k)
    return f"`{c['key']}` ({'iOS' if plat == 'ios' else 'Android'}): {base}{extra}"

def token(c, plat, value=None):
    v = c['majority'] if value is None else value
    ext = {'source': c['key'], 'platform': plat, 'kind': c['kind'], 'markets': c['follows_markets'] if c['kind'] == 'follows' else c['majority_markets'],
           'exceptions': c['exceptions'], 'not_set_markets': c['not_set_markets']}
    if c['kind'] == 'follows':
        ext['follows'] = ROLE[c['follows']]
        if c['follows'] != ROLE[c['follows']]: ext['follows_note'] = f"{c['follows']} is built as {ROLE[c['follows']]} (DEC-14)"
        return {'$type': 'color', '$value': None, '$description': desc(c, plat), '$extensions': {'mng': ext}}
    if v is None:                                   # not set: UIKit default
        name, hexv, why = UIKIT[c['key']]
        ext['uikit'] = name
        return {'$type': 'color', '$value': hexv, '$description': desc(c, plat, f'; not set by the app: {why}'), '$extensions': {'mng': {**ext, 'rgb': rgb(hexv)}}}
    return {'$type': 'color', '$value': v, '$description': desc(c, plat), '$extensions': {'mng': {**ext, 'rgb': rgb(v)}}}

def put(tree, path, tok):
    *g, leaf = path
    for p in g: tree = tree.setdefault(p, {})
    tree[leaf] = tok

flat = []
by = {plat: {c['key']: c for c in P[plat]['colors']} for plat in ('ios', 'android')}
paired = {'ios': {p['ios'] for p in PAIRS}, 'android': {p['android'] for p in PAIRS}}

# Core: one token per approved pair
core = {}
for p in PAIRS:
    a, b = by['ios'][p['ios']], by['android'][p['android']]
    ta, tb = token(a, 'ios'), token(b, 'android')
    same = ta['$value'] == tb['$value'] and a['kind'] != 'follows' and b['kind'] != 'follows'
    path = ['color', 'system'] + p['name'].split('/')
    if same:
        t = {'$type': 'color', '$value': ta['$value'], '$description': f"{p['what']}: same on both apps. {ta['$description']}; {tb['$description']}",
             '$extensions': {'mng': {'owner': 'core', 'rgb': rgb(ta['$value']), 'ios': ta['$extensions']['mng'], 'android': tb['$extensions']['mng']}}}
        put(core, path, t)
        flat.append({'collection': 'core', 'name': p['name'], 'what': p['what'], 'values': {'ios': ta['$value'], 'android': tb['$value']}, 'same': True,
                     'sources': {'ios': a['key'], 'android': b['key']}})
    else:   # Core, per-platform value: one Core name, a value per platform (like the Core Button collection)
        for plat, t, c in (('ios', ta, a), ('android', tb, b)):
            t = json.loads(json.dumps(t)); t['$extensions']['mng']['owner'] = 'core (per-platform value)'
            t['$description'] = f"{p['what']} (Core, per-platform value): {t['$description']}"
            put(core, ['color', f'system-{plat}'] + p['name'].split('/'), t)
        flat.append({'collection': 'core', 'name': p['name'], 'what': p['what'], 'values': {'ios': ta['$value'], 'android': tb['$value']}, 'same': False,
                     'uikit': ta['$extensions']['mng'].get('uikit'), 'sources': {'ios': a['key'], 'android': b['key']}})

camel = lambda n: ''.join(w if i == 0 else w[:1].upper() + w[1:] for i, w in enumerate(re.split(r'[-/.]', n)) if w)
CORE_CAMEL = {camel(p['name']) for p in PAIRS}
plats = {}
for plat in ('ios', 'android'):
    tree = {}
    for c in sorted(P[plat]['colors'], key=lambda c: c['key']):
        if c['covered_by'] or c['key'] in paired[plat]: continue
        name = kebab(c['key'], plat)
        if camel(name) in CORE_CAMEL: name += '-alt'      # e.g. Android section_front_background (#f7f7f7) vs Core section-front/background
        t = token(c, plat); t['$extensions']['mng']['owner'] = plat
        if c['kind'] == 'follows':   # no value of its own: listed on the group, read from the brand palette by the code formats
            grp = tree.setdefault('color', {}).setdefault(f'{plat}-system', {})
            grp.setdefault('$extensions', {'mng': {'follows': {}}})['mng']['follows'][name] = {'$description': t['$description'], **t['$extensions']['mng']}
        else:
            put(tree, ['color', f'{plat}-system', name], t)
        flat.append({'collection': plat, 'name': name, 'source': c['key'], 'kind': c['kind'], 'value': t['$value'],
                     'follows': t['$extensions']['mng'].get('follows'), 'uikit': t['$extensions']['mng'].get('uikit'),
                     'markets': t['$extensions']['mng']['markets'], 'exceptions': len(c['exceptions'])})
    plats[plat] = tree

names = [f"{f['collection']}:{f['name']}" for f in flat]
assert len(names) == len(set(names)), 'duplicate token names'
meta = '$description'
json.dump({meta: 'Generated by scripts/build_system_tokens.py (DEC-16): Core system colors (approved iOS/Android pairs). Majority values; exceptions documented only. Do not edit by hand.', **core},
          open('tokens/core/system.tokens.json', 'w'), indent=1)
for plat in ('ios', 'android'):
    json.dump({meta: f'Generated by scripts/build_system_tokens.py (DEC-16): {plat} system colors. Majority values; follows = brand role; exceptions documented only. Do not edit by hand.', **plats[plat]},
              open(f'tokens/{plat}/system.tokens.json', 'w'), indent=1)
json.dump({'generated_by': 'scripts/build_system_tokens.py', 'tokens': flat}, open('data/system-tokens.json', 'w'), indent=1)

# docs/SYSTEM-TOKENS.md
fx = lambda h: '—' if not h else (f'`{h}` · ' + ', '.join(map(str, rgb(h))))
L = ['# System color tokens', '', 'Generated by `scripts/build_system_tokens.py` from `data/system-color-comparison.json`. Do not edit by hand.', '',
     'DEC-16 (Karl, 2026-11-10): majority values; colors that follow a brand role read the market palette; every exception is documented '
     '(per market in `docs/SYSTEM-COLORS.md`, and in each token\'s `$extensions.mng.exceptions`) but not built.', '',
     f"Core: {sum(1 for f in flat if f['collection'] == 'core')} · iOS: {sum(1 for f in flat if f['collection'] == 'ios')} · Android: {sum(1 for f in flat if f['collection'] == 'android')}", '',
     '## Core (same screen element on both apps)', '', '| Token | What | iOS | Android | Sources |', '|---|---|---|---|---|']
for f in flat:
    if f['collection'] != 'core': continue
    ios = fx(f['values']['ios']) + (f" (UIKit `{f['uikit']}`)" if f.get('uikit') else '')
    L.append(f"| `{f['name']}` | {f['what']} | {ios} | {fx(f['values']['android'])} | `{f['sources']['ios']}` / `{f['sources']['android']}` |")
for plat, title in (('ios', 'iOS only'), ('android', 'Android only')):
    L += ['', f'## {title}', '', '| Token | Value | Kind | Markets | Exceptions (documented) | Source |', '|---|---|---|---|---|---|']
    for f in flat:
        if f['collection'] != plat: continue
        v = f"= `{f['follows']}` (market brand color)" if f['follows'] else fx(f['value']) + (f" (UIKit `{f['uikit']}`)" if f['uikit'] else '')
        L.append(f"| `{f['name']}` | {v} | {f['kind']} | {f['markets']} | {f['exceptions'] or '—'} | `{f['source']}` |")
open('docs/SYSTEM-TOKENS.md', 'w').write('\n'.join(L) + '\n')
print({k: sum(1 for f in flat if f['collection'] == k) for k in ('core', 'ios', 'android')}, 'follows:', sum(1 for f in flat if f.get('follows')))

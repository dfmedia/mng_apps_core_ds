"""Combined icon name list: one name per icon purpose, with what each app ships today (DEC-17).
Usage: python3 scripts/build_icon_names.py   (after scripts/icon_platform_map.py)
Reads  data/icon-platform-map.json (TroncKit @ e30ad2585, android-tribpub @ 1cfb069a6)
       data/icon-comparison.json (reference glyphs: nearest SF Symbol / Material Symbol / Font Awesome, and the Oct 2026 recommendation)
Writes data/icon-names.json, docs/ICON-NAMES.md
Documents what ships, nothing new: the glyphs stay as each app ships them (DEC-09, DEC-17). Only the shared
name is new. Reference glyphs (nearest SF Symbol / Material / Font Awesome) and the earlier
recommendations are kept in a separate `reference` block, labeled as such, so one combined list carries everything (Karl, 2026-11-10).
Naming: lowercase words joined by hyphens, named for what the icon does, not what it looks like.
        Prefixes: tab- (bottom tab bar), enews- (eNewspaper viewer), brand- (logos).
"""
import json

M = json.load(open('data/icon-platform-map.json'))
# purpose -> (name, note). Purposes that share a meaning share a name (DEC-17: one set of icon names).
NAME = {
    'Search': ('search', ''), 'Settings': ('settings', ''), 'Share': ('share', ''),
    'Save (not saved)': ('save', ''), 'Saved': ('saved', 'Android also shows a star in special sections (see below), same name (DEC-17).'),
    'Home tab': ('tab-home', ''), 'Sections / menu': ('menu', 'Sections tab and the eNewspaper menu.'),
    'Alerts tab': ('tab-alerts', ''), 'For You / Your News tab': ('tab-for-you', ''), 'eNewspaper tab': ('tab-enewspaper', ''),
    'Games tab': ('tab-games', ''), 'Digital tab': ('tab-digital', ''),
    'Expand / show more': ('expand', ''), 'Collapse / show less': ('collapse', ''), 'Back': ('back', ''),
    'Forward / disclosure': ('forward', ''), 'Close': ('close', ''), 'Close (circle)': ('close-circle', ''),
    'Account': ('account', ''), 'Warning': ('warning', ''), 'Email': ('email', ''), 'Refresh': ('refresh', ''), 'Filter': ('filter', ''),
    'Text size smaller': ('text-size-smaller', 'iOS variant of text-size; Android ships one text-size icon (DEC-17, PLAT-08).'),
    'Text size larger': ('text-size-larger', 'iOS variant of text-size; Android ships one text-size icon (DEC-17, PLAT-08).'),
    'Follow topic': ('follow-topic', ''), 'Unfollow topic': ('unfollow-topic', ''), 'Checked': ('checked', ''), 'Unchecked': ('unchecked', ''),
    'Continue': ('continue', ''),
    'Expand page': ('enews-expand-page', ''), 'Fit to screen': ('enews-fit-to-screen', ''), 'Previous page': ('enews-previous-page', ''), 'Next page': ('enews-next-page', ''),
    'Play': ('play', ''), 'Pause': ('pause', ''), 'Skip back 15 s': ('skip-back-15', ''), 'Skip forward 15 s': ('skip-forward-15', ''),
    'Rewind': ('rewind', ''), 'Fast forward': ('fast-forward', ''), '3D embed': ('embed-3d', ''), 'Tournament sport symbols (6)': ('tournament-sport', 'Six symbols; names unknown.'),
    'Rating star (empty)': ('rating-star-empty', ''), 'Rating star (half)': ('rating-star-half', ''), 'Rating star (full)': ('rating-star-full', ''),
    'Like / favorite': ('like', 'Tweet embeds.'), 'Repost': ('repost', 'Tweet embeds.'), 'Verified': ('verified', 'Tweet embeds.'),
    'Apple': ('brand-apple', ''), 'Google': ('brand-google', ''), 'Facebook': ('brand-facebook', ''), 'X (Twitter)': ('brand-x', ''),
    'Bluesky': ('brand-bluesky', ''), 'Instagram': ('brand-instagram', ''), 'YouTube': ('brand-youtube', ''), 'Vimeo': ('brand-vimeo', ''),
    'Amazon (sign-in)': ('brand-amazon', ''), '1Password': ('brand-1password', ''), 'Outbrain': ('brand-outbrain', ''),
    'Notification small icon': ('notification', 'Android platform requirement (monochrome, per market).'),
    'Save star (special sections)': ('saved', "Android's glyph for saved in special sections; iOS shows the bookmark. Both kept (DEC-17, PLAT-09 rejected)."),
}
# open Apps team questions per purpose (docs/MISSING-ASSETS.md §1)
ASK = {
    'Saved': '1.3 (iOS "saved" SF Symbol renders nothing), 1.6 (per-market copies)', 'Home tab': '1.4 (market tab-bar overrides)',
    'For You / Your News tab': '1.6, 1.8 (no master vector)', 'Games tab': '1.5 (no clear source)', 'Digital tab': '1.9 (what does it open?)',
    'Filter': '1.5', 'Text size smaller': '1.5', 'Text size larger': '1.5', 'Follow topic': '1.5', 'Unfollow topic': '1.5',
    'Checked': '1.6 (per-market copies)', 'Unchecked': '1.6 (per-market copies)', 'Continue': '1.6 (per-market copies)',
    'Skip back 15 s': '1.5, 1.11 (15 s on Android?)', 'Skip forward 15 s': '1.5, 1.11 (15 s on Android?)', 'Tournament sport symbols (6)': '1.10 (symbol names)',
}
BUCKET = {'core': 'Core', 'core-variant': 'Core, per-platform value', 'ios-only': 'iOS only', 'android-only': 'Android only'}
missing = [p['purpose'] for p in M['purposes'] if p['purpose'] not in NAME]
assert not missing, f'no name for: {missing}'

# icon-comparison.json rows: [group, purpose, ios_today, sf_symbol, [material, style], [fa, code, style], recommendation]
REF = {c[1]: {'sf_symbol': c[3] or None, 'material': (c[4] or [None])[0], 'font_awesome': (c[5] or [None])[0], 'recommendation': c[6] or None}
       for c in json.load(open('data/icon-comparison.json'))}
rows = []
for p in M['purposes']:
    name, note = NAME[p['purpose']]
    ask = ASK.get(p['purpose'], '1.12 (brand vectors)' if p['group'] == 'Brands' else '')
    rows.append({'name': name, 'purpose': p['purpose'], 'group': p['group'], 'bucket': BUCKET[p['bucket']],
                 'ios': p['ios_today'] or None, 'android': p['android_today'] or None,
                 'note': note, 'apps_team': ask,
                 'reference': {**REF.get(p['purpose'], {'sf_symbol': None, 'material': None, 'font_awesome': None, 'recommendation': None}),
                               'ownership_note': p['note'] or None}})   # factual notes only; recommendations stay in data/icon-platform-map.json
names = sorted({r['name'] for r in rows})
shared = {n: [r['purpose'] for r in rows if r['name'] == n] for n in names if sum(r['name'] == n for r in rows) > 1}
out = {'generated_by': 'scripts/build_icon_names.py', 'source': M['source'], 'decision': 'DEC-17',
       'rule': 'One name per icon purpose, glyphs as each app ships them. Lowercase, hyphens, named for the job. Prefixes tab-, enews-, brand-.',
       'status': 'names approved by Karl 2026-11-11 (DEC-17); glyphs documented as shipped',
       'summary': {'purposes': len(rows), 'names': len(names), 'shared_names': shared,
                   'by_bucket': {b: sum(r['bucket'] == b for r in rows) for b in BUCKET.values()}},
       'icons': rows}
json.dump(out, open('data/icon-names.json', 'w'), indent=1, ensure_ascii=False)

cell = lambda s: (s or '—').replace('|', '\\|')
L = ['# Icon names (combined iOS + Android)', '', 'Generated by `scripts/build_icon_names.py` from `data/icon-platform-map.json` '
     f"(iOS {M['source']['ios']}, Android {M['source']['android']}). Do not edit by hand.", '',
     '**What this is (DEC-17):** one shared name for each icon purpose, next to what each app ships today. Nothing is redesigned: '
     'each app keeps its own glyphs; only the name is shared. Names approved by Karl on 2026-11-11 (DEC-17).', '',
     '**Naming rule:** lowercase words joined by hyphens, named for what the icon does, not what it looks like. '
     'Prefixes: `tab-` (bottom tab bar), `enews-` (eNewspaper viewer), `brand-` (logos).', '',
     f"**Count:** {len(rows)} purposes → {len(names)} names. " + ' · '.join(f'{b}: {n}' for b, n in out['summary']['by_bucket'].items()) + '.',
     'Names shared by more than one purpose: ' + '; '.join(f"`{n}` ({', '.join(ps)})" for n, ps in shared.items()) + '.', '',
     'Open questions for the Apps team are the numbers in docs/MISSING-ASSETS.md §1. The Android icon set has not been extracted yet (1.7).',
     '**Reference columns** (not what ships): the nearest SF Symbol, Material Symbol and Font Awesome 5.15.1 glyph, and the earlier recommendation '
     'from the October comparison and ownership pages. They are kept for context; nothing in them is decided.', '']
for g in dict.fromkeys(r['group'] for r in rows):
    L += [f'## {g}', '', '| Name | Purpose | Bucket | iOS ships | Android ships | Note | Apps team | Reference: SF / Material / FA | Earlier recommendation (Oct 2026, not decided) |', '|---|---|---|---|---|---|---|---|---|']
    for r in [r for r in rows if r['group'] == g]:
        rf = r['reference']; refs = ' / '.join(x or '—' for x in (rf['sf_symbol'], rf['material'], rf['font_awesome']))
        rec = ' · '.join(x for x in (rf['recommendation'], rf['ownership_note']) if x)
        L.append(f"| `{r['name']}` | {r['purpose']} | {r['bucket']} | {cell(r['ios'])} | {cell(r['android'])} | {cell(r['note'])} | {cell(r['apps_team'])} | {cell(refs)} | {cell(rec)} |")
    L.append('')
open('docs/ICON-NAMES.md', 'w').write('\n'.join(L))
print(len(rows), 'purposes ->', len(names), 'names; shared:', shared)

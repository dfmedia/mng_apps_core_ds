#!/usr/bin/env python3
"""Professional vector for every shipped UI icon (DEC-29): the closest platform symbol, never a trace.

Usage: python3 scripts/build_icon_replacements.py      (after build_icon_sources.py and match_material_icons.py)
Reads  data/icon-sources.json, data/icon-names.json, data/icon-material-matches.json (shape ranking that helped pick),
       @material-symbols/svg-400 from npm (Apache-2.0).
Writes data/icon-replacements.json, docs/ICON-REPLACEMENTS.md,
       icons/material/*.svg in this repo (Core names) and ../mng_apps_android_ds/icons/material/*.svg (Android-only names),
       each folder with the Material licence and a manifest.json.
Picks: chosen by eye on 2026-11-25 from the shipped PNG beside the 5 closest Material Symbols by shape and the reference
symbol (sheets from match_material_icons.py --sheets). The SF Symbol column is the iOS vector: the matching symbol
from scripts/sf_symbols_vectors.swift (exported on Karl's Mac; git-ignored while the repos are public).
`weak` marks picks that are only roughly like the shipped glyph: Karl to confirm.
"""
import json, os, shutil, subprocess, tempfile
from collections import OrderedDict, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VERSION = '0.49.0'

# icon name -> Material Symbol (outlined, weight 400; "-fill" = filled). None = no Material equivalent.
MATERIAL = {
    'back': 'chevron_left', 'forward': 'chevron_right', 'checked': 'check_circle-fill', 'unchecked': 'radio_button_unchecked',
    'close': 'close', 'close-circle': 'cancel-fill', 'collapse': 'keyboard_arrow_down', 'expand': 'keyboard_arrow_up',
    'continue': 'arrow_circle_right-fill', 'email': 'mail-fill', 'embed-3d': 'deployed_code',
    'enews-expand-page': 'open_in_full', 'enews-fit-to-screen': 'close_fullscreen',
    'enews-next-page': 'arrow_forward_ios', 'enews-previous-page': 'arrow_back_ios_new', 'exit-full-screen': 'close_fullscreen',
    'filter': None, 'follow-topic': 'format_list_bulleted_add', 'unfollow-topic': None,
    'like': 'favorite-fill', 'menu': 'menu', 'pause': 'pause-fill', 'play': 'play_arrow-fill', 'player-error': 'error-fill',
    'rating-star-empty': 'star', 'rating-star-full': 'star-fill', 'rating-star-half': 'star_half-fill',
    'refresh': 'refresh', 'repost': 'repeat', 'save': 'bookmark', 'saved': 'bookmark-fill', 'search': 'search',
    'settings': 'settings', 'share': 'share', 'tab-alerts': 'notifications', 'tab-enewspaper': None,
    'tab-for-you': None, 'tab-games': 'extension', 'tab-home': 'home', 'text-size': 'format_size',
    'text-size-larger': 'text_increase', 'text-size-smaller': 'text_decrease', 'verified': 'verified-fill',
    'warning': 'warning-fill', 'account': 'account_circle', 'skip-back-10': 'replay_10', 'skip-forward-10': 'forward_10',
    'skip-back-15': None, 'skip-forward-15': None, 'tournament-sport': None, 'enews-coach-arrow': None, 'notification': None,
}
# shipped file -> Material Symbol, where that file's drawing differs from the name's default
BY_FILE = {
    'ic_check.png': 'check_circle', 'WhiteCheckmark.png': 'check_circle', 'ic_topic_selected.png': 'check', 'GreyCheckmark.png': 'check',
    'radio_button_on.png': 'radio_button_checked', 'ic_ad_close.png': 'cancel-fill',
    'Plus-CT.png': 'add_circle', 'Minus-CT.png': 'do_not_disturb_on', 'liveblog_arrow.png': 'arrow_circle_right-fill',
    'btn_play_large.png': 'play_circle-fill', 'ic_play_btn.png': 'play_circle-fill', 'embed-play.png': 'play_circle-fill',
    'button-play.png': 'play_circle-fill', 'button-play-medium.png': 'play_circle-fill', 'button-play-small.png': 'play_circle-fill',
    'button-pause.png': 'pause_circle-fill', 'button-pause-medium.png': 'pause_circle-fill', 'button-pause-small.png': 'pause_circle-fill',
    'mc_tab_icon_alerts.png': 'notifications-fill', 'card_star_default.png': 'star', 'star_on_card_saved_state.png': 'star-fill',
    'nav-share.png': 'ios_share', 'tab-newspaper.png': None, 'mc_tab_icon_latestnews.png': None,
}
# Material Symbol -> SF Symbol (the iOS vector for the same drawing)
SF = {
    'chevron_left': 'chevron.left', 'chevron_right': 'chevron.right', 'check_circle-fill': 'checkmark.circle.fill',
    'check_circle': 'checkmark.circle', 'check': 'checkmark', 'radio_button_checked': 'smallcircle.filled.circle',
    'radio_button_unchecked': 'circle', 'close': 'xmark', 'cancel-fill': 'xmark.circle.fill',
    'keyboard_arrow_down': 'chevron.down', 'keyboard_arrow_up': 'chevron.up', 'arrow_circle_right-fill': 'arrow.right.circle.fill',
    'mail-fill': 'envelope.fill', 'deployed_code': 'cube', 'open_in_full': 'arrow.up.left.and.arrow.down.right',
    'close_fullscreen': 'arrow.down.right.and.arrow.up.left', 'arrow_forward_ios': 'chevron.right', 'arrow_back_ios_new': 'chevron.left',
    'page_info': 'slider.horizontal.3', 'format_list_bulleted_add': 'text.badge.plus', 'playlist_remove': 'text.badge.minus',
    'add_circle': 'plus.circle', 'do_not_disturb_on': 'minus.circle', 'favorite-fill': 'heart.fill', 'menu': 'line.3.horizontal',
    'pause-fill': 'pause.fill', 'play_arrow-fill': 'play.fill', 'play_circle-fill': 'play.circle.fill', 'pause_circle-fill': 'pause.circle.fill',
    'error-fill': 'exclamationmark.circle.fill', 'star': 'star', 'star-fill': 'star.fill', 'star_half-fill': 'star.leadinghalf.filled',
    'refresh': 'arrow.clockwise', 'repeat': 'arrow.2.squarepath', 'bookmark': 'bookmark', 'bookmark-fill': 'bookmark.fill',
    'search': 'magnifyingglass', 'settings': 'gearshape', 'share': 'square.and.arrow.up', 'ios_share': 'square.and.arrow.up',
    'notifications': 'bell', 'notifications-fill': 'bell.fill', 'newsmode': 'newspaper', 'menu_book': 'book',
    'patient_list-fill': None, 'extension': 'puzzlepiece', 'home': 'house', 'format_size': 'textformat.size',
    'text_increase': 'textformat.size.larger', 'text_decrease': 'textformat.size.smaller', 'verified-fill': 'checkmark.seal.fill',
    'warning-fill': 'exclamationmark.triangle.fill', 'account_circle': 'person.circle.fill',
}
SF_BY_FILE = {'UnFollowTopic.png': 'text.badge.minus', 'BTN_UnFollowTopic.png': 'text.badge.minus'}   # iOS pair of text.badge.plus
SF_BY_NAME = {'skip-back-15': 'gobackward.15', 'skip-forward-15': 'goforward.15',
              'tournament-sport': 'soccerball.inverse · american.football.fill · baseball.fill · basketball.fill · hockey.puck.fill · sportscourt.fill'}
# Karl's review of the picks (2026-11-25)
OPEN = {   # still to decide
    'embed-3d': 'Shipped: a wireframe cube with "VIEW IN 3D" under it, in the PostKit (Washington Post SDK) image set; where it shows is asked (MISSING-ASSETS 1.4). '
                'Material deployed_code / SF cube is the cube alone.',
}
REDRAW = {   # no good stock symbol: redraw cleanly in vector (the shipped PNG is only a guide)
    'filter': 'Redrawn: three sliders with round knobs (approved by Karl, 2026-11-25).',
    'tab-enewspaper': "Karl redraws (Illustrator): Patrick Carr's newspaper icon (NewspaperFinal.png = shipped iOS tab-enews and Android mc_tab_icon_newspaper, same drawing); no vector exists. "
                      'iOS tab-newspaper is never shown (Apps team, 2026-11-19): not carried into the DS.',
    'tab-for-you': 'Karl redraws (Illustrator): person beside a list; no stock symbol matches and no master exists (Apps team, 2026-11-18).',
    'unfollow-topic': 'iOS only. List version: SF text.badge.minus (exported 2026-11-25) is the shipped drawing (minus in a circle beside the list), '
                      'so iOS may need no redraw: Karl to confirm. Circle version (Minus-CT): do_not_disturb_on / SF minus.circle (Karl: good).',
    'enews-coach-arrow': 'Redrawn: a clean dotted curve with an arrowhead (approved by Karl, 2026-11-25; where it is used: MISSING-ASSETS 1.2).',
    'tab-home': 'Market home icons (mastheads) are marks, not symbols: redraw per market. home is the generic icon.',
}
CONFIRMED = {   # Karl: good
    'follow-topic': 'Karl: good (list: format_list_bulleted_add / SF text.badge.plus; circle: add_circle / SF plus.circle).',
    'repost': 'Karl: good (repeat / SF arrow.2.squarepath).',
    'text-size': 'Android only. Material format_size (T T) replaces the shipped serif A A (Karl, 2026-11-25).',
    'text-size-larger': 'iOS only (DEC-21): SF textformat.size.larger (Karl: good). Android has no such icon: it uses text-size.',
    'text-size-smaller': 'iOS only (DEC-21): SF textformat.size.smaller (Karl: good). Android has no such icon: it uses text-size.',
}
OTHER = {
    'notification': 'Per-market notification icons: asked of the Apps team (MISSING-ASSETS 1.3).',
    'skip-back-15': 'iOS only: SF gobackward.15 (Material has 5, 10 and 30 only).',
    'skip-forward-15': 'iOS only: SF goforward.15 (Material has 5, 10 and 30 only).',
    'tournament-sport': 'iOS only: SF Symbols as shipped.',
}

SF_DIR = os.path.join(ROOT, 'assets', 'sf-symbols', 'vector')   # git-ignored; Karl's export (scripts/sf_symbols_vectors.swift)

def material_pkg(t):
    subprocess.run(['npm', 'pack', f'@material-symbols/svg-400@{VERSION}', '-q'], cwd=t, check=True, capture_output=True)
    subprocess.run(['tar', 'xzf', f'material-symbols-svg-400-{VERSION}.tgz'], cwd=t, check=True)
    return os.path.join(t, 'package')

def main():
    names = {i['name']: i for i in json.load(open(os.path.join(ROOT, 'data', 'icon-names.json')))['icons']}
    src = json.load(open(os.path.join(ROOT, 'data', 'icon-sources.json')))['assets']
    matches = {(m['name'], m['master']): m for m in json.load(open(os.path.join(ROOT, 'data', 'icon-material-matches.json')))['matches']}
    missing = sorted(n for n in names if n not in MATERIAL and not n.startswith('brand-'))
    assert not missing, f'no Material decision for: {missing}'
    bucket = {}
    for i in json.load(open(os.path.join(ROOT, 'data', 'icon-names.json')))['icons']:   # a name shared by purposes: Core wins
        b = bucket.get(i['name'])
        bucket[i['name']] = i['bucket'] if b is None or not b.startswith('Core') and i['bucket'].startswith('Core') else b
    # per shipped file
    files = []
    for r in src:
        if r['kind'] != 'icon' or not r['name'] or r['name'].startswith('brand-') or r['vector'] == 'drop':
            continue
        mat = BY_FILE[r['file']] if r['file'] in BY_FILE else MATERIAL.get(r['name'])
        m = matches.get((r['name'], r['master']))
        score = None
        if m and mat:
            score = next((t['score'] for t in m['top'] if t['symbol'] == mat), m['reference_score'] if m['reference'] == mat else None)
        files.append(OrderedDict(platform=r['platform'], folder=r['folder'], file=r['file'], name=r['name'],
                                 material=mat, sf=SF.get(mat) if mat else SF_BY_FILE.get(r['file']) or SF_BY_NAME.get(r['name']),
                                 shape_rank=score))
    _rp = os.path.join(ROOT, 'data', 'icon-redraws.json')
    redraws = defaultdict(list)
    for r in (json.load(open(_rp))['redraws'] if os.path.exists(_rp) else []):
        redraws[r['name']].append(r['svg'])
    # per name
    rows = []
    for n in sorted(MATERIAL):
        fs = [f for f in files if f['name'] == n]
        mats = sorted({f['material'] for f in fs if f['material']} | ({MATERIAL[n]} if MATERIAL[n] else set()))
        sfs = sorted({f['sf'] for f in fs if f['sf']} | ({SF.get(MATERIAL[n]) or SF_BY_NAME.get(n)} - {None}))
        status = 'open' if n in OPEN else 'partly-redraw' if n in REDRAW and (MATERIAL[n] or any(f['material'] for f in fs)) else 'redraw' if n in REDRAW \
            else 'ask' if n == 'notification' else 'symbol'
        rows.append(OrderedDict(name=n, bucket=bucket.get(n), material=mats, sf=sfs, status=status,
                                note=OPEN.get(n) or REDRAW.get(n) or CONFIRMED.get(n) or OTHER.get(n) or '', redrawn=redraws.get(n, []), shipped_files=len(fs)))
    # copy Material SVGs: Core and core-variant names -> this repo; Android only -> Android repo; iOS only -> none (SF on iOS)
    dest = {'core': os.path.join(ROOT, 'icons', 'material'), 'android': os.path.join(ROOT, '..', 'mng_apps_android_ds', 'icons', 'material')}
    want = defaultdict(set)
    for r in rows:
        b = r['bucket'] or ''
        where = 'android' if b == 'Android only' else 'core' if b.startswith('Core') else None
        if where:   # the name's default symbol, plus per-file picks for Android files (iOS files use SF Symbols)
            want[where] |= {MATERIAL[r['name']]} - {None}
            want[where] |= {f['material'] for f in files if f['name'] == r['name'] and f['platform'] == 'android' and f['material']}
    with tempfile.TemporaryDirectory() as t:
        pkg = material_pkg(t)
        for where, syms in want.items():
            d = dest[where]
            if os.path.isdir(d):
                for f in os.listdir(d):
                    os.remove(os.path.join(d, f))
            os.makedirs(d, exist_ok=True)
            for s in sorted(syms):
                shutil.copy(os.path.join(pkg, 'outlined', f'{s}.svg'), os.path.join(d, f'{s}.svg'))
            shutil.copy(os.path.join(pkg, 'LICENSE'), os.path.join(d, 'LICENSE'))
            json.dump({'generated_by': 'scripts/build_icon_replacements.py', 'package': f'@material-symbols/svg-400@{VERSION}',
                       'style': 'outlined, weight 400 ("-fill" = filled)', 'license': 'Apache-2.0',
                       'symbols': sorted(syms)},
                      open(os.path.join(d, 'manifest.json'), 'w'), indent=1)
    sf_all = sorted({s for r in rows for x in r['sf'] for s in x.split(' · ')})
    out = OrderedDict(generated_by='scripts/build_icon_replacements.py', decision='DEC-29',
                      material=f'@material-symbols/svg-400@{VERSION}',
                      summary=OrderedDict(names=len(rows), by_status={s: sum(r['status'] == s for r in rows) for s in STATUS},
                                          material_svgs={k: len(v) for k, v in want.items()}, sf_symbols=len(sf_all), shipped_files=len(files)),
                      sf_symbols_needed=sf_all,
                      sf_symbols_exported=sorted(x for x in sf_all if os.path.exists(os.path.join(SF_DIR, x + '.svg'))) if os.path.isdir(SF_DIR) else None,
                      names=rows, files=files)
    json.dump(out, open(os.path.join(ROOT, 'data', 'icon-replacements.json'), 'w'), indent=1)
    write_md(out)
    print(json.dumps(out['summary']))

STATUS = {'symbol': 'Stock symbol', 'partly-redraw': 'Stock symbol for some files, redraw for others', 'redraw': 'Redraw', 'open': 'Open: Karl to decide', 'ask': 'Asked of the Apps team'}

def write_md(out):
    s = out['summary']
    L = ['# Icon replacements (DEC-29)', '',
         'Generated by `scripts/build_icon_replacements.py`. Do not edit by hand.', '',
         'Every shipped UI icon gets a professionally drawn vector: the closest **Material Symbol** (Android and Core; Apache-2.0, '
         'so the SVGs live in the repos) and the closest **SF Symbol** (iOS; exported on Karl\'s Mac by `scripts/sf_symbols_vectors.swift`, '
         'kept out of the repos while they are public). Shipped PNGs are not traced (DEC-29). What ships today stays documented in '
         'docs/ICON-NAMES.md and docs/ICON-SOURCES.md (rule 1).', '',
         f"**{s['names']} icon names:** " + ', '.join(f"{v} {STATUS[k].lower()}" for k, v in s['by_status'].items()) + '. '
         f"Material SVGs: {s['material_svgs'].get('core', 0)} in `icons/material/` (Core), {s['material_svgs'].get('android', 0)} in "
         f"`mng_apps_android_ds/icons/material/` (Android only). SF Symbols needed: {s['sf_symbols']}.", '',
         'Brand marks (`brand-*`) are not here: they stay the brands\' own artwork (DEC-26).', '',
         '## By icon name', '', '| Name | Owner | Material Symbol | SF Symbol | Status | Redrawn SVG | Note |', '|---|---|---|---|---|---|---|']
    for r in out['names']:
        L.append(f"| `{r['name']}` | {r['bucket'] or '—'} | {', '.join('`'+m+'`' for m in r['material']) or '—'} | "
                 f"{', '.join('`'+m+'`' for m in r['sf']) or '—'} | {STATUS[r['status']]} | {', '.join('`'+x+'`' for x in r['redrawn']) or '—'} | {r['note'] or '—'} |")
    L += ['', '## By shipped file', '', 'Which symbol replaces each shipped file. Shape rank: how close the Material Symbol is to the shipped '
          'drawing (soft IoU of the ink, 0–1; blank where the pick was not in the top 5, e.g. a white glyph on a colored circle).', '',
          '| Platform | File | Name | Material | SF | Shape rank |', '|---|---|---|---|---|---|']
    for f in sorted(out['files'], key=lambda f: (f['name'], f['platform'], f['file'])):
        L.append(f"| {f['platform']} | `{f['file']}` | `{f['name']}` | {('`'+f['material']+'`') if f['material'] else '—'} | "
                 f"{('`'+f['sf']+'`') if f['sf'] else '—'} | {f['shape_rank'] if f['shape_rank'] is not None else ''} |")
    ex = out['sf_symbols_exported']
    L += ['', '## SF Symbols', '', f"{len(out['sf_symbols_needed'])} needed: " + ', '.join(f'`{x}`' for x in out['sf_symbols_needed']) + '.', '',
          ('All exported as true vectors by scripts/sf_symbols_vectors.swift on Karl\'s Mac (2026-11-25, macOS 15.5, from the SF Pro font), '
           'checked by eye against Apple\'s rendering. They are in assets/sf-symbols/vector/ (git-ignored while the repos are public).'
           if ex is not None and len(ex) == len(out['sf_symbols_needed']) else
           f"Exported: {len(ex) if ex is not None else 'unknown (folder not here)'}; missing: " + ', '.join(sorted(set(out['sf_symbols_needed']) - set(ex or [])))), '']
    open(os.path.join(ROOT, 'docs', 'ICON-REPLACEMENTS.md'), 'w').write('\n'.join(L))

if __name__ == '__main__':
    main()

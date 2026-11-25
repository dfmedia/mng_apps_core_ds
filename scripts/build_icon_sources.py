#!/usr/bin/env python3
"""Icon and graphic inventory of both style guides (DEC-26 step 1).

For every image the Apps team exported (data/source/style-guide-assets.json, measured from
downloads/style-guides/) this records:
  - kind: icon · market-icon · logo · button-image · image
  - name: the DEC-17 icon name (docs/ICON-NAMES.md) the file belongs to, where it has one
  - shape: files that are the same drawing in another colour share one shape id (one vector + a colour token)
  - colours: mono · two-tone · multi (multi = photo, gradient or texture: tracing will not match)
  - vector: how the DS gets a professional vector (DEC-29): UI icons are replaced by the closest Material Symbol /
    SF Symbol (scripts/build_icon_replacements.py); market marks, logos and simple artwork with no stock symbol are
    redrawn cleanly (the PNG is only a guide); photos stay raster; pictures of buttons become the Button component.
    Shipped SVGs are used as they are. Nothing is traced.
Writes data/icon-sources.json and docs/ICON-SOURCES.md. Needs downloads/style-guides/ for the shape
comparison (git-ignored); without it, shapes fall back to one per file.
"""
import json, os, re
from collections import defaultdict, OrderedDict

ROOT = os.path.join(os.path.dirname(__file__), '..')
SG = os.path.join(ROOT, 'downloads', 'style-guides')
SRC = json.load(open(os.path.join(ROOT, 'data', 'source', 'style-guide-assets.json')))
NAMES = json.load(open(os.path.join(ROOT, 'data', 'icon-names.json')))
NAME_SET = {i['name'] for i in NAMES['icons']}

# ---------------------------------------------------------------- kind
IMAGES = {  # photos, illustrations, placeholders
    'ad-bigbox-offline-250.jpg', 'cover-placeholder.png', 'eNewspaper-overlay.png', 'menu-line.png',
    'AccountDeletionImage.png', 'mng-top-image-view.png', 'player-placeholder-compact.png',
    'player-placeholder-regular.png', 'recirculationPlaceholder.png', 'your_news_image.png'}
BUTTON_IMAGES = re.compile(r'^(Continue-|TopicSelection-|ButtonWithCheckmark|apple_button|fb_button|google_button|twitter_button)')
LOGOS = re.compile(r'^(outbrainLogo|Masthead|instagram-logo|twitter-logo|twp-slogan|youtube-logo|vimeo-logo|paywall-logo|paywall-1password|'
                   r'AppleIcon|GoogleIcon|FacebookIcon|TwitterIcon|tweet-logo|ic_amazon|ic_fb|ic_twitter|author_contact_|AuthorContact|'
                   r'.*-logo(-white)?\.png|logo-bs-white)')
IOS_MARKET_TABS = {'tab-baltimoresun.png', 'tab-dailypress.png', 'tab-hart.png', 'tab-home.png', 'tab-morningcall.png',
                   'tab-os.png', 'tab-sunsentinel.png', 'tab-viginia.png', 'tab-nydn-active.png'}

def kind_of(a):
    f, folder = a['file'], a['folder']
    if f in IMAGES or (a['platform'] == 'ios' and folder == 'Onboarding' and re.fullmatch(r'[A-Z]+\.png', f)):
        return 'image'
    if BUTTON_IMAGES.match(f):
        return 'button-image'
    if folder == 'Home tab by market' or f in IOS_MARKET_TABS:
        return 'market-icon'
    if LOGOS.match(f):
        return 'logo'
    return 'icon'

# ---------------------------------------------------------------- DEC-17 name
# (regex on file name, name). First match wins. None = no DEC-17 name (images, wordmarks).
NAME_RULES = [
    # Android
    (r'^mc_alert_bell|^mc_tab_icon_alerts|^bell\.png|^tab-alerts', 'tab-alerts'),
    (r'^mc_tab_icon_for_you|^For-You|^tab-foryou|^YourNews-', 'tab-for-you'),
    (r'^mc_tab_icon_games|^ic_games|^tab-games', 'tab-games'),
    (r'^mc_tab_icon_newspaper|^ic_newspaper|^tab-enews|^tab-newspaper', 'tab-enewspaper'),
    (r'^mc_tab_icon_sections|^tab-sections|^black_menu|^menu\.png', 'menu'),
    (r'^menu-line', 'enews-coach-arrow'),
    (r'^video-fullscreen-close', 'exit-full-screen'),
    (r'^player-error-image|^player-offline-image', 'player-error'),
    (r'^mc_tab_icon_latestnews', 'tab-home'),
    (r'^ic_bookmark_outline|^ic_btn_unsave|^nav-save-unfilled|^Unsaved-Article|^Saved-Unfilled-', 'save'),
    (r'^mc_tab_icon_saved|^ic_bookmark\.png|^ic_btn_save|^card_star_default|^star_on_card|^nav-save-filled|^Saved-Article|'
     r'^Saved-Filled-|^Saved--|^Saved-CT|^tab-saved', 'saved'),
    (r'^ic_clear_search|^button-miniplayer-close', 'close-circle'),
    (r'^ic_filter|^icon_filter', 'filter'),
    (r'^ic_font_size|^ic_textsize_change', 'text-size'),
    (r'^ic_share|^nav-share', 'share'),
    (r'^ic_wc_refresh', 'refresh'),
    (r'^mc_ic_search|^nav-search|^black_search|^search\.png', 'search'),
    (r'^mc_ic_settings|^nav-settings', 'settings'),
    (r'^web_view_navigation_back', 'back'),
    (r'^web_view_navigation_forward|^game_open_arrow|^ic_arrow\.png|^liveblog_arrow', 'forward'),
    (r'^btn_play_large|^ic_play_btn|^play_player_button|^ic_persistent_player_play|^button-play|^button-miniplayer-play|'
     r'^embed-play', 'play'),
    (r'^pause_player_button|^ic_persistent_player_pause|^button-pause|^button-miniplayer-pause', 'pause'),
    (r'^close_player_button|^ic_persistent_player_close|^ic_ad_close|^ic_close_white|^xbutton|^CloseButton|'
     r'^BannerCloseLight|^overlay-close', 'close'),
    (r'^arrow_circle_right|^Continue-', 'continue'),
    (r'^icon_downarrow|^Chevron---Down|^chevron_down|^button-downarrow', 'collapse'),
    (r'^icon_uparrow|^Chevron---Up|^chevron_up', 'expand'),
    (r'^ic_check\.png|^ic_topic_selected|^radio_button_on|^Checked|^Checkmark-|^GreyCheckmark|^WhiteCheckmark|'
     r'^ButtonWithCheckmark|^TopicSelection-', 'checked'),
    (r'^radio_button_off|^Uncheck', 'unchecked'),
    (r'^ic_follow_topic|^BTN_FollowTopic|^FollowTopic|^Plus-CT', 'follow-topic'),
    (r'^ic_unfollow_topic|^BTN_UnFollowTopic|^UnFollowTopic|^Minus-CT', 'unfollow-topic'),
    (r'^ic_email', 'email'),
    (r'^exclamation-icon', 'warning'),
    (r'^black_expand-paper|^expand-paper', 'enews-expand-page'),
    (r'^black_fit-to-screen|^fit-to-screen', 'enews-fit-to-screen'),
    (r'^black_left-arrow|^left-arrow', 'enews-previous-page'),
    (r'^black_right-arrow|^right-arrow', 'enews-next-page'),
    (r'^textsizelarge', 'text-size-larger'),
    (r'^textsizesmall', 'text-size-smaller'),
    (r'^button-rewind', 'skip-back-15'),
    (r'^button-fastforward', 'skip-forward-15'),
    (r'^embed-3d', 'embed-3d'),
    (r'^rating-star-empty', 'rating-star-empty'),
    (r'^rating-star-half', 'rating-star-half'),
    (r'^rating-star-full', 'rating-star-full'),
    (r'^tweet-favorite', 'like'),
    (r'^tweet-retweet', 'repost'),
    (r'^tweet-verified', 'verified'),
    (r'^apple_button|^AppleIcon', 'brand-apple'),
    (r'^google_button|^GoogleIcon', 'brand-google'),
    (r'^fb_button|^ic_fb|^FacebookIcon|^author_contact_facebook|^AuthorContactFacebook', 'brand-facebook'),
    (r'^twitter_button|^ic_twitter|^TwitterIcon|^tweet-logo|^twitter-logo|^author_contact_x|^AuthorContactX', 'brand-x'),
    (r'^author_contact_bluesky|^AuthorContactBluesky', 'brand-bluesky'),
    (r'^author_contact_instagram|^AuthorContactInstagram|^instagram-logo', 'brand-instagram'),
    (r'^youtube-logo', 'brand-youtube'),
    (r'^vimeo-logo', 'brand-vimeo'),
    (r'^paywall-1password', 'brand-1password'),
    (r'^outbrainLogo', 'brand-outbrain'),
]

# Notes on single files: what the picture shows where the file name misleads, and Karl's call on it (DEC-28, 2026-11-25).
NOTES = {
    'button-fastforward.png': 'PostKit player: a clockwise arrow with "15", not a fast-forward glyph. Named skip-forward-15, iOS only; vector SF goforward.15 (DEC-29).',
    'button-rewind.png': 'PostKit player: a counter-clockwise arrow with "15", not a rewind glyph. Named skip-back-15, iOS only; vector SF gobackward.15 (DEC-29).',
    'video-fullscreen-close.png': 'Two arrows pointing inward (exit full screen), not an X. Own name exit-full-screen; vector Material close_fullscreen / SF arrow.down.right.and.arrow.up.left (DEC-29).',
    'gif-play.png': 'A "GIF" badge, not a play button. Not carried into the DS; reported as a bug to delete; where it shows is asked (DEC-28).',
    'menu-line.png': 'A dotted curved arrow, not a menu icon. Own name enews-coach-arrow; to be redrawn cleanly (no stock symbol); where and how it is applied is asked (DEC-28).',
    'overlay-close.png': 'An X with the word "Close" baked into the image (text in a PNG).',
    'player-error-image.png': 'Exclamation in a dark circle. Same drawing as player-offline-image: one icon, player-error, for both (DEC-28): Material error-fill / SF exclamationmark.circle.fill (DEC-29).',
    'player-offline-image.png': 'Same drawing as player-error-image: uses player-error (DEC-28).',
    'tab-digital.png': 'A phone outline; not listed in ICON-NAMES (no tab uses it per the Apps team tab list).',
    'tab-home.png': 'The Chicago Tribune "C" (white): CT\'s market home icon, not the generic home.',
    'ic_amazon.png': 'Never shown on either app (Apps team, 2026-11-23): not carried into the DS.',
    'tab-newspaper.png': 'An open newspaper; never shown (Apps team, 2026-11-19: only an unused property refers to it). Not carried into the DS (Karl, 2026-11-25).',
}
DROP = {'ic_amazon.png', 'gif-play.png', 'tab-newspaper.png'}
# Names with no style-guide file: where their SVG comes from (DEC-28). SF Symbol SVGs come from Karl's Mac
# (scripts/sf_symbols_vectors.swift → assets/sf-symbols/vector/, git-ignored while the repos are public: Apple licence).
SF = 'SF Symbol SVG from scripts/sf_symbols_vectors.swift (Karl\'s Mac; git-ignored while the repos are public)'
NO_FILE_SVG = {
    'account': ('iOS', 'SF person.circle.fill', SF + '; Material account_circle as reference'),
    'tournament-sport': ('iOS', 'SF soccerball.inverse, american.football.fill, baseball.fill, basketball.fill, hockey.puck.fill; fallback sportscourt.fill', SF),
    'skip-back-15': ('iOS', 'SF gobackward.15 (main player); PostKit player ships button-rewind', SF),
    'skip-forward-15': ('iOS', 'SF goforward.15 (main player); PostKit player ships button-fastforward', SF),
    'skip-back-10': ('Android', 'Media3 skip_back_10', 'Material Symbols replay_10: mng_apps_android_ds/icons/material/replay_10.svg'),
    'skip-forward-10': ('Android', 'Media3 skip_forward_10', 'Material Symbols forward_10: mng_apps_android_ds/icons/material/forward_10.svg'),
    'notification': ('Android', 'per-market monochrome notification icons', 'Not in either style guide: asked of the Apps team (1.3)'),
}

# Origin notes for graphics that come from the Washington Post PostKit SDK inside TroncKit.
WAPO = re.compile(r'^(Masthead|twp-slogan|paywall-logo|player-placeholder|recirculationPlaceholder|ad-bigbox)')

def name_of(a):
    if a['file'] in ('tab-home.png', 'ic_amazon.png', 'tab-digital.png', 'gif-play.png'):
        return None
    if a['folder'] == 'Home tab by market' or a['file'] in IOS_MARKET_TABS:
        return 'tab-home'
    for rx, n in NAME_RULES:
        if re.search(rx, a['file']):
            return n
    return None

# ---------------------------------------------------------------- colours
def colours(a):
    if a['format'] == 'svg':
        return 'mono' if len(a['fills']) <= 1 else 'two-tone'
    shares = [i['share'] for i in a['ink']]
    big = [s for s in shares if s >= 0.05]
    if a['ink_buckets'] <= 1 or len(big) == 1:
        return 'mono'
    if a['ink_buckets'] <= 3 and len(big) <= 2:
        return 'two-tone'
    return 'multi'

# ---------------------------------------------------------------- shapes
def shape_groups(assets):
    """Same drawing in another colour → same shape id. Compares the opaque mask and the light-ink mask
    (so a white glyph on different coloured buttons only matches when the glyph matches)."""
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        return {}
    def masks(a):
        p = os.path.join(SG, a['platform'], a['folder'], a['file'])
        if not os.path.exists(p):
            return None
        im = np.asarray(Image.open(p).convert('RGBA')).astype(int)
        op = im[:, :, 3] >= 128
        luma = (im[:, :, 0] * 299 + im[:, :, 1] * 587 + im[:, :, 2] * 114) // 1000
        light = op & (luma >= 215)
        return op, light
    def iou(x, y):
        u = (x | y).sum()
        return 1.0 if u == 0 else (x & y).sum() / u
    groups, out = [], {}
    for a in assets:
        if a['format'] != 'png':
            continue
        m = masks(a)
        if m is None:
            continue
        for g in groups:
            b, mb = g['first'], g['masks']
            if (a['width'], a['height']) != (b['width'], b['height']):
                continue
            if iou(m[0], mb[0]) > 0.97 and iou(m[1], mb[1]) > 0.9 and \
               (a['transparent_share'] > 0.05 or iou(m[1], mb[1]) > 0.97):
                g['members'].append(a); break
        else:
            groups.append({'first': a, 'masks': m, 'members': [a]})
    for gi, g in enumerate(groups):
        for a in g['members']:
            out[(a['platform'], a['folder'], a['file'])] = gi
    return out

# ---------------------------------------------------------------- vector plan
def vector_plan(a, kind, col):
    if a['format'] == 'svg':
        return 'shipped-svg'
    if kind == 'icon':
        return 'symbol'
    if kind == 'image':
        return 'keep-raster' if col == 'multi' else 'redraw'
    if kind == 'button-image':
        return 'component'
    if a['file'] in DROP:
        return 'drop'
    return 'redraw' if col in ('mono', 'two-tone') else 'review'

def main():
    assets = SRC['assets']
    shapes = shape_groups(assets)
    rows = []
    for a in assets:
        k = kind_of(a)
        n = name_of(a)
        col = colours(a)
        f = NOTES.get(a['file'])
        row = OrderedDict(
            platform=a['platform'], folder=a['folder'], file=a['file'], kind=k, name=n,
            format=a['format'], size=(a.get('viewBox') if a['format'] == 'svg' else f"{a['width']}x{a['height']}"),
            colours=col,
            ink=[i['hex'] for i in a.get('ink', []) if i['share'] >= 0.05] or a.get('fills', []),
            shape=None, vector=vector_plan(a, k, col),
            note=f,
            origin='Washington Post PostKit (in TroncKit)' if WAPO.match(a['file']) else None,
            sha256=a['sha256'])
        rows.append(row)
    # shape ids: number groups in file order; SVGs that share a path with a PNG are not merged (different formats)
    ids, nxt = {}, 1
    for r in rows:
        key = (r['platform'], r['folder'], r['file'])
        g = shapes.get(key)
        if g is None:
            r['shape'] = f's{nxt:03d}'; nxt += 1; continue
        if g not in ids:
            ids[g] = f's{nxt:03d}'; nxt += 1
        r['shape'] = ids[g]
    # identical SVGs across platforms (author contact icons): same shape id
    svg_by_hash = {}
    for r, a in zip(rows, assets):
        if a['format'] == 'svg':
            path = os.path.join(SG, a['platform'], a['folder'], a['file'])
            d = re.findall(r'\sd="([^"]+)"', open(path).read()) if os.path.exists(path) else [a['sha256']]
            key = '|'.join(d)
            if key in svg_by_hash:
                r['shape'] = svg_by_hash[key]
            else:
                svg_by_hash[key] = r['shape']
    # master per shape: shipped SVG if any, else the largest PNG
    by_shape = defaultdict(list)
    for r in rows:
        by_shape[r['shape']].append(r)
    for sid, members in by_shape.items():
        svg = [m for m in members if m['format'] == 'svg']
        def px(m):
            w, h = m['size'].split('x'); return int(w) * int(h)
        master = svg[0] if svg else max(members, key=px)
        for m in members:
            m['master'] = f"{master['platform']}/{master['folder']}/{master['file']}"
            m['variants'] = len(members)

    summary = OrderedDict()
    summary['files'] = len(rows)
    for key in ('kind', 'vector', 'colours', 'platform'):
        c = defaultdict(int)
        for r in rows:
            c[r[key]] += 1
        summary[f'by_{key}'] = dict(sorted(c.items(), key=lambda x: -x[1]))
    summary['shapes_to_redraw'] = len({r['shape'] for r in rows if r['vector'] == 'redraw'})
    summary['shapes_to_redraw_by_kind'] = {k: len({r['shape'] for r in rows if r['vector'] == 'redraw' and r['kind'] == k})
                                          for k in ('market-icon', 'logo', 'image')}
    summary['icon_shapes'] = len({r['shape'] for r in rows if r['vector'] == 'symbol'})
    summary['shipped_svgs'] = sum(1 for r in rows if r['vector'] == 'shipped-svg')
    summary['names_covered'] = sorted({r['name'] for r in rows if r['name']})
    summary['names_without_style_guide_file'] = sorted(NAME_SET - set(summary['names_covered']))
    summary['notes'] = sum(1 for r in rows if r['note'])

    out = OrderedDict(generated_by='scripts/build_icon_sources.py', source=SRC['source'],
                      decision='DEC-26 (vectors only), DEC-29 (platform symbols, no traces), DEC-17 (names)',
                      summary=summary, assets=rows)
    json.dump(out, open(os.path.join(ROOT, 'data', 'icon-sources.json'), 'w'), indent=1)
    write_md(out, by_shape)
    print(json.dumps(summary, indent=1))

KIND_TEXT = {
    'icon': 'UI icon', 'market-icon': 'Market home-tab icon (per market)', 'logo': 'Logo or brand mark',
    'button-image': 'Picture of a button', 'image': 'Photo, illustration or placeholder'}
VECTOR_TEXT = {
    'shipped-svg': 'Already a vector (shipped SVG): use as is',
    'symbol': 'UI icon: replaced by the closest Material Symbol / SF Symbol (docs/ICON-REPLACEMENTS.md)',
    'redraw': 'No stock symbol (market marks, logos, simple artwork): redraw cleanly in vector, using the PNG only as a guide',
    'review': 'Photo-like or many colours: tracing will not match; Karl decides (keep raster or redraw)',
    'keep-raster': 'Photo: stays a raster image (not an icon)',
    'component': 'Rebuild as the Button component (text + icon), not an image',
    'drop': 'Not carried into the DS (never shown, or to be deleted from the app)'}

def write_md(out, by_shape):
    s = out['summary']; rows = out['assets']
    L = ['# Icon and graphic sources (DEC-26 inventory)', '',
         'Generated by `scripts/build_icon_sources.py` from `data/source/style-guide-assets.json` (every file in the two Apps team '
         'style guides, downloaded 2026-11-25) and `data/icon-names.json` (DEC-17). Do not edit by hand.', '',
         '**What this is:** every image the apps ship, as exported in the style guides, with the icon name it belongs to, '
         'whether it is the same drawing as another file in a different colour, and how the design system gets a vector for it '
         '(DEC-26: every icon and graphic is a vector; DEC-29: from the platform symbol sets or a clean redraw, never a trace).', '',
         f"**Count:** {s['files']} files (Android {s['by_platform'].get('android', 0)}, iOS {s['by_platform'].get('ios', 0)}). "
         f"{s['shipped_svgs']} are already SVG. {s['icon_shapes']} distinct UI icon drawings are replaced by platform symbols "
         f"(docs/ICON-REPLACEMENTS.md, DEC-29); {s['shapes_to_redraw']} drawings with no stock symbol need a clean redraw "
         f"({s['shapes_to_redraw_by_kind']['market-icon']} market icons, {s['shapes_to_redraw_by_kind']['logo']} logos, "
         f"{s['shapes_to_redraw_by_kind']['image']} simple illustrations). Nothing is traced (DEC-29).", '',
         '## Summary', '', '| Kind | Files |', '|---|---|']
    for k, v in s['by_kind'].items():
        L.append(f'| {KIND_TEXT[k]} | {v} |')
    L += ['', '| How we get the vector | Files |', '|---|---|']
    for k, v in s['by_vector'].items():
        L.append(f'| {VECTOR_TEXT[k]} | {v} |')
    L += ['', '## Icon names with no file in the style guides', '',
          'These are drawn by the system at runtime (SF Symbols on iOS, Material / Media3 on Android), so no image ships. '
          'Each still gets a vector in the design system, in the platform that uses it (DEC-28).', '',
          '| Name | Platform | What ships | SVG |', '|---|---|---|---|']
    for n in s['names_without_style_guide_file']:
        plat, ships, svg = NO_FILE_SVG.get(n, ('?', '?', 'unknown'))
        L.append(f'| `{n}` | {plat} | {ships} | {svg} |')
    # notes
    L += ['', '## Notes on single files', '', 'Files whose name misleads, or that need a decision. Decisions: DEC-28 (2026-11-25).', '',
          '| Platform | File | Name | Note | Vector |', '|---|---|---|---|---|']
    for r in [r for r in rows if r['note']]:
        L.append(f"| {r['platform']} | `{r['file']}` | {('`'+r['name']+'`') if r['name'] else '—'} | {r['note']} | {r['vector']} |")
    # same drawing, many colours
    L += ['', '## Same drawing, different colours', '',
          'Each line is one vector plus a colour per file: the colours become tokens, the files go away.', '',
          '| Name | Files | Colours | Master |', '|---|---|---|---|']
    for sid, members in sorted(by_shape.items()):
        if len(members) < 2:
            continue
        cols = sorted({c for m in members for c in m['ink'][:1]})
        L.append(f"| {('`'+members[0]['name']+'`') if members[0]['name'] else members[0]['kind']} | "
                 f"{', '.join(m['file'] for m in members)} | {' '.join(cols)} | {members[0]['master'].split('/')[-1]} |")
    # per name
    L += ['', '## By icon name', '']
    byname = defaultdict(list)
    for r in rows:
        byname[r['name'] or f"(no name: {r['kind']})"].append(r)
    for n in sorted(byname, key=lambda x: (x.startswith('('), x)):
        rs = byname[n]
        L += [f'### {n if n.startswith("(") else "`"+n+"`"}', '',
              '| Platform | Folder | File | Size | Colours | Ink | Shape | Vector |', '|---|---|---|---|---|---|---|---|']
        for r in rs:
            L.append(f"| {r['platform']} | {r['folder']} | `{r['file']}` | {r['size']} | {r['colours']} | {' '.join(r['ink'][:2])} | "
                     f"{r['shape']}{' ×'+str(r['variants']) if r['variants'] > 1 else ''} | {r['vector']} |")
        L.append('')
    L += ['## Legend', '']
    for k, v in VECTOR_TEXT.items():
        L.append(f'- **{k}**: {v}')
    L += ['- **Colours**: mono = one ink colour; two-tone = two inks (e.g. white glyph on a coloured circle); '
          'multi = photo, gradient or texture.',
          '- **Shape**: files with the same shape id are the same drawing; ×n = how many files share it.']
    open(os.path.join(ROOT, 'docs', 'ICON-SOURCES.md'), 'w').write('\n'.join(L) + '\n')

if __name__ == '__main__':
    main()

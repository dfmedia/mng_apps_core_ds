#!/usr/bin/env python3
"""Clean vector redraws for the icons with no matching stock symbol (DEC-29).

Usage: python3 scripts/redraw_icons.py [--preview FILE]
Writes icons/redrawn/<name>.svg in the repo that owns the icon (this repo for Core names, ../mng_apps_ios_ds for iOS-only)
and data/icon-redraws.json. --preview writes a PNG: shipped PNG | redraw at shipped size | redraw large.

Drawn on the Material Symbols grid (viewBox 0 -960 960 960, content inside 80..880, 60-unit strokes = weight 400), so the
redraws sit with the Material Symbols they appear beside. Geometry is written here from the shipped PNG's proportions
(the PNG is only a guide; nothing is traced). Strokes are converted to filled outlines with picosvg, so every file is
plain filled paths. The eNewspaper coach arrow is an illustration (dotted line), so it keeps its dashed stroke.
"""
import json, os, sys, io, re, subprocess
from collections import OrderedDict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPO = {'core': ROOT, 'ios': os.path.join(ROOT, '..', 'mng_apps_ios_ds')}
MATERIAL_PKG = '/tmp/material-symbols-0.49.0/package/outlined'   # from scripts/match_material_icons.py
VB = 'viewBox="0 -960 960 960"'

def svg(body, title, vb=VB, size=(24, 24)):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" {vb}>'
            f'<title>{title}</title>{body}</svg>\n')

def outline(svg_text):
    """Strokes -> filled outlines, one path per shape (picosvg)."""
    from picosvg.svg import SVG
    pico = SVG.fromstring(svg_text).topicosvg(allow_text=True)
    out = pico.tostring(pretty_print=False)
    return out

# ---- filter: three sliders with round knobs (shipped: knobs left, right, middle)
def filter_icon():
    rows = [(-720, 300), (-480, 640), (-240, 440)]   # (y, knob x)
    r_out, r_in, t = 125, 65, 60
    parts = []
    for y, cx in rows:
        if cx - r_out > 120:
            parts.append(f'<rect x="120" y="{y - t // 2}" width="{cx - r_out - 120}" height="{t}"/>')
        if 840 - (cx + r_out) > 0:
            parts.append(f'<rect x="{cx + r_out}" y="{y - t // 2}" width="{840 - cx - r_out}" height="{t}"/>')
        parts.append(f'<circle cx="{cx}" cy="{y}" r="{(r_out + r_in) / 2}" fill="none" stroke="#000" stroke-width="{r_out - r_in}"/>')
    return ''.join(parts)

# ---- tab-for-you: a person beside a three-row list (filled = selected / Android; outline body = iOS unselected)
BODY = 'M200 -544H410Q470 -544 480 -484L530 -140Q538 -80 478 -80H132Q72 -80 80 -140L130 -484Q140 -544 200 -544Z'
BODY_IN = 'M205 -514H405Q448 -514 452 -478L498 -146Q503 -110 465 -110H145Q107 -110 112 -146L158 -478Q162 -514 205 -514Z'
def for_you(filled):
    head = '<circle cx="305" cy="-704" r="144"/>'
    body = f'<path d="{BODY}"/>' if filled else f'<path d="{BODY_IN}" fill="none" stroke="#000" stroke-width="60" stroke-linejoin="round"/>'
    rows = ''.join(f'<circle cx="615" cy="{y}" r="34"/><rect x="685" y="{y - 26}" width="195" height="52" rx="26"/>' for y in (-790, -685, -580))
    return head + body + rows

# ---- unfollow-topic (list): Material format_list_bulleted_add with the plus replaced by a minus (pair of follow-topic)
def unfollow_list():
    d = re.search(r' d="([^"]+)"', open(os.path.join(MATERIAL_PKG, 'format_list_bulleted_add.svg')).read()).group(1)
    plus = 'M718-134h33v-110h110v-33H751v-110h-33v110H608v33h110v110Z'
    assert d.startswith(plus), 'Material path changed: check the plus sub-path'
    minus = 'M608-244h253v-33H608v33Z'
    rest = d[len(plus):]
    assert rest.startswith('m14.5 60'), 'Material path changed: check the circle sub-path'
    rest = 'M732.5-74' + rest[len('m14.5 60'):]   # the circle starts relative to the plus's end point: make it absolute
    return f'<path fill-rule="evenodd" d="{minus}{rest}"/>'

# ---- tab-enewspaper: Patrick Carr's newspaper (= shipped iOS tab-enews / Android mc_tab_icon_newspaper)
def newspaper():
    page = 'M240 -790H840Q880 -790 880 -750V-210Q880 -170 840 -170H240Q200 -170 200 -210V-750Q200 -790 240 -790Z'
    strip = 'M80 -560H150V-215Q150 -170 115 -170Q80 -170 80 -215Z'
    block_out = 'M300 -690H520V-470H300Z'
    block_in = 'M345 -645H475V-515H345Z'
    lines = ''.join(f'M570 {y - 22}H780V{y + 22}H570Z' for y in (-668, -580, -492))
    long_line = 'M300 -402H780V-358H300Z'
    return (f'<path d="{strip}"/>'
            f'<path fill-rule="evenodd" d="{page}{block_out}{block_in}{lines}{long_line}"/>')

# ---- enews-coach-arrow: dotted curve with an arrowhead (illustration, 294 x 333 as shipped, #004E87)
def coach_arrow():
    curve = 'M18 325C40 232 118 200 168 166S246 110 258 52'
    head = 'M246 44L275 12L282 55Z'
    return (f'<path d="{curve}" fill="none" stroke="#004E87" stroke-width="6" stroke-dasharray="7 6"/>'
            f'<path d="{head}" fill="#004E87"/>')

ICONS = [
    # name, owner, file, body, filled-outline?, viewBox, size, shipped PNG for the preview
    ('filter', 'core', 'filter.svg', filter_icon, True, VB, (24, 24), 'android/Toolbar/ic_filter.png'),
    ('tab-for-you', 'core', 'tab-for-you-fill.svg', lambda: for_you(True), True, VB, (24, 24), 'android/Bottom nav/mc_tab_icon_for_you.png'),
    ('tab-for-you', 'core', 'tab-for-you.svg', lambda: for_you(False), True, VB, (24, 24), 'ios/Tab Bar/tab-foryou.png'),
    ('tab-enewspaper', 'core', 'tab-enewspaper.svg', newspaper, False, VB, (24, 24), 'android/Bottom nav/mc_tab_icon_newspaper.png'),
    ('unfollow-topic', 'ios', 'unfollow-topic.svg', unfollow_list, False, VB, (24, 24), 'android/Save and select/ic_unfollow_topic.png'),
    ('enews-coach-arrow', 'ios', 'enews-coach-arrow.svg', coach_arrow, False, 'viewBox="0 0 294 333"', (294, 333), 'ios/ENewspaper/menu-line.png'),
]

def main():
    rows = []
    for name, owner, fname, fn, conv, vb, size, shipped in ICONS:
        text = svg(fn(), f'{name} (redrawn, DEC-29)', vb, size)
        if conv:
            text = outline(text)
        d = os.path.join(REPO[owner], 'icons', 'redrawn')
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, fname), 'w').write(text)
        rows.append(OrderedDict(name=name, owner=owner, svg=os.path.relpath(os.path.join(d, fname), os.path.join(ROOT, '..')),
                                guide=shipped, note='derived from Material format_list_bulleted_add (Apache-2.0)' if name == 'unfollow-topic' else ''))
    json.dump({'generated_by': 'scripts/redraw_icons.py', 'decision': 'DEC-29', 'grid': 'Material Symbols 960 grid, 60-unit strokes',
               'redraws': rows}, open(os.path.join(ROOT, 'data', 'icon-redraws.json'), 'w'), indent=1)
    print(len(rows), 'redraws')
    if '--preview' in sys.argv:
        preview(rows, sys.argv[sys.argv.index('--preview') + 1])

def preview(rows, out):
    import cairosvg
    from PIL import Image, ImageDraw
    SG = os.path.join(ROOT, 'downloads', 'style-guides')
    T = 180
    sheet = Image.new('RGB', (4 * (T + 10) + 10, len(rows) * (T + 24)), (255, 255, 255))
    dr = ImageDraw.Draw(sheet)
    for i, r in enumerate(rows):
        y = i * (T + 24)
        dr.text((4, y + 2), f"{r['name']}  ({os.path.basename(r['svg'])})   shipped PNG | redraw at shipped size | redraw large | Material neighbour", fill=(0, 0, 0))
        plat, folder, f = r['guide'].split('/', 2)
        png = Image.open(os.path.join(SG, plat, folder, f)).convert('RGBA')
        svgp = os.path.join(ROOT, '..', r['svg'])
        rs = lambda p, w, h: Image.open(io.BytesIO(subprocess.run(['rsvg-convert', '-w', str(w), '-h', str(h), '--keep-aspect-ratio', p], capture_output=True, check=True).stdout)).convert('RGBA')
        small = rs(svgp, png.width, png.height)
        big = rs(svgp, T - 10, T - 10)
        neighbour = {'unfollow-topic': 'format_list_bulleted_add', 'filter': 'page_info'}.get(r['name'])
        tiles = [png, small, big]
        if neighbour:
            tiles.append(rs(os.path.join(MATERIAL_PKG, neighbour + '.svg'), T - 10, T - 10))
        for j, t in enumerate(tiles):
            t = t.copy(); t.thumbnail((T - 10, T - 10), Image.LANCZOS)
            bg = Image.new('RGBA', (T, T), (225, 225, 225, 255) if j == 0 else (255, 255, 255, 255))
            bg.alpha_composite(t, ((T - t.width) // 2, (T - t.height) // 2))
            sheet.paste(bg.convert('RGB'), (10 + j * (T + 10), y + 18))
    sheet.save(out)

if __name__ == '__main__':
    main()

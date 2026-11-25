#!/usr/bin/env python3
"""Trace shipped PNG icons to SVG and check each trace against the PNG at its shipped size (DEC-26, DEC-28).

Usage: python3 scripts/trace_icons.py [name ...]      (default: every entry in TRACE below)
Reads  downloads/style-guides/<platform>/<folder>/<file> (git-ignored; Karl's local copy of the two style guides)
Writes <repo>/icons/traced/<name>.svg in the platform repo that owns the icon (../mng_apps_ios_ds or ../mng_apps_android_ds,
       or this repo for Core), and data/icon-traces.json (the overlay check for every trace).

How: each ink layer of the PNG (opaque area, or the light glyph on a dark shape) is upscaled 8x, thresholded at 50 %
and traced with potrace (pip install potracer). Colors are the PNG's own ink (exact hex, no rounding). The SVG keeps
the PNG's pixel grid as its viewBox. The check renders the SVG at the PNG's size (rsvg-convert) and compares
coverage: soft IoU (overlap of per-pixel coverage, so a half-covered edge pixel counts half). A trace passes at soft IoU >= 0.90
(two-tone icons: the light glyph also >= 0.90). The 50 % mask IoU is reported too but not used: thin strokes with edges on
half pixels swing it (exit-full-screen, 2026-11-25);
a failing trace is written anyway and flagged for Karl (DEC-26: mismatches go to Karl, not into the DS).
"""
import json, os, subprocess, sys, io
import numpy as np
from PIL import Image
import potrace

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SG = os.path.join(ROOT, 'downloads', 'style-guides')
REPO = {'core': ROOT, 'ios': os.path.join(ROOT, '..', 'mng_apps_ios_ds'), 'android': os.path.join(ROOT, '..', 'mng_apps_android_ds')}

# name: (owner, platform, folder, file, layers). Layers: 'ink' = whole opaque area in one color;
# 'ink+light' = opaque area in its dark ink, plus the light glyph on top in the light ink.
TRACE = {
    'skip-back-15':        ('ios', 'ios', 'PostKit', 'button-rewind.png', 'ink'),
    'skip-forward-15':     ('ios', 'ios', 'PostKit', 'button-fastforward.png', 'ink'),
    'exit-full-screen':    ('ios', 'ios', 'PostKit', 'video-fullscreen-close.png', 'ink', 0.0),   # straight edges, square corners
    'player-error':        ('ios', 'ios', 'PostKit', 'player-error-image.png', 'ink+light'),
    'enews-coach-arrow':   ('ios', 'ios', 'ENewspaper', 'menu-line.png', 'ink'),
}
K = 8

def dominant(rgba, mask):
    px = rgba[mask][:, :3]
    if not len(px):
        return '#000000'
    q = (px // 4) * 4
    vals, counts = np.unique(q, axis=0, return_counts=True)
    top = vals[counts.argmax()]
    near = px[(np.abs(q - top) <= 4).all(axis=1)]
    vals, counts = np.unique(near, axis=0, return_counts=True)
    r, g, b = vals[counts.argmax()]
    return '#%02X%02X%02X' % (r, g, b)

def trace(cov, w, h, alphamax=1.0):
    """cov: float coverage 0..1 at shipped size -> SVG path d in shipped pixel units."""
    big = np.asarray(Image.fromarray((cov * 255).astype(np.uint8)).resize((w * K, h * K), Image.LANCZOS)) >= 128
    plist = potrace.Bitmap(~big).trace(turdsize=2 * K, alphamax=alphamax, opticurve=True, opttolerance=0.2)
    f = lambda p: f"{p.x / K:.2f} {p.y / K:.2f}"
    d = []
    for curve in plist:
        d.append('M' + f(curve.start_point))
        for s in curve.segments:
            d.append(('L' + f(s.c) + ' L' + f(s.end_point)) if s.is_corner else ('C' + f(s.c1) + ' ' + f(s.c2) + ' ' + f(s.end_point)))
        d.append('Z')
    return ''.join(d)

def build(name):
    owner, plat, folder, file, layers, *opt = TRACE[name]
    am = opt[0] if opt else 1.0
    im = Image.open(os.path.join(SG, plat, folder, file)).convert('RGBA')
    w, h = im.size
    rgba = np.asarray(im).astype(int)
    alpha = rgba[:, :, 3] / 255.0
    luma = (rgba[:, :, 0] * 299 + rgba[:, :, 1] * 587 + rgba[:, :, 2] * 114) / 1000.0
    paths = []
    if layers == 'ink':
        ink = dominant(rgba, alpha >= 0.5)
        paths.append((trace(alpha, w, h, am), ink))
    else:
        dark = dominant(rgba, (alpha >= 0.5) & (luma < 128))
        light = dominant(rgba, (alpha >= 0.5) & (luma >= 215))
        # light glyph coverage: how far each pixel is from the dark ink toward the light ink
        ld, ll = int(dark[1:3], 16) * 0.299 + int(dark[3:5], 16) * 0.587 + int(dark[5:7], 16) * 0.114, \
                 int(light[1:3], 16) * 0.299 + int(light[3:5], 16) * 0.587 + int(light[5:7], 16) * 0.114
        glyph = np.clip((luma - ld) / max(1, ll - ld), 0, 1) * alpha
        paths.append((trace(alpha, w, h), dark))
        paths.append((trace(glyph, w, h), light))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
           f'  <title>{name} (traced from {file}, {w}x{h}, DEC-26)</title>\n'
           + ''.join(f'  <path fill="{c}" fill-rule="evenodd" d="{d}"/>\n' for d, c in paths) + '</svg>\n')
    out_dir = os.path.join(REPO[owner], 'icons', 'traced')
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f'{name}.svg')
    open(out, 'w').write(svg)
    # overlay check at shipped size
    png = subprocess.run(['rsvg-convert', '-w', str(w), '-h', str(h), out], capture_output=True, check=True).stdout
    r = np.asarray(Image.open(io.BytesIO(png)).convert('RGBA')).astype(int)
    ra = r[:, :, 3] / 255.0
    a, b = alpha >= 0.5, ra >= 0.5
    iou = float((a & b).sum() / max(1, (a | b).sum()))
    diff = float(np.abs(alpha - ra).mean() / max(alpha.mean(), 1e-6))
    soft = float(np.minimum(alpha, ra).sum() / max(1e-6, np.maximum(alpha, ra).sum()))   # soft IoU: edge pixels count by coverage
    res = {'name': name, 'owner': owner, 'source': f'{plat}/{folder}/{file}', 'size': f'{w}x{h}',
           'colors': [c for _, c in paths], 'svg': os.path.relpath(out, os.path.join(ROOT, '..')),
           'bytes': len(svg), 'soft_iou': round(soft, 4), 'iou': round(iou, 4), 'coverage_diff': round(diff, 4)}
    if layers == 'ink+light':   # the glyph must match too
        lum_r = (r[:, :, 0] * 299 + r[:, :, 1] * 587 + r[:, :, 2] * 114) / 1000.0
        g1, g2 = (luma >= 160) & (alpha >= 0.5), (lum_r >= 160) & b
        res['glyph_iou'] = round(float((g1 & g2).sum() / max(1, (g1 | g2).sum())), 4)
    res['pass'] = res['soft_iou'] >= 0.90 and res.get('glyph_iou', 1) >= 0.9
    return res

def main():
    names = sys.argv[1:] or list(TRACE)
    path = os.path.join(ROOT, 'data', 'icon-traces.json')
    prev = json.load(open(path))['traces'] if os.path.exists(path) else []
    keep = {t['name']: t for t in prev if t['name'] not in names}
    for n in names:
        keep[n] = build(n)
        t = keep[n]
        print(f"{'PASS' if t['pass'] else 'FAIL'} {n:20} soft IoU {t['soft_iou']:.3f} IoU {t['iou']:.3f} diff {t['coverage_diff']:.3f}"
              + (f" glyph {t['glyph_iou']:.3f}" if 'glyph_iou' in t else '') + f"  {t['svg']} ({t['bytes']} B)")
    json.dump({'generated_by': 'scripts/trace_icons.py', 'decision': 'DEC-26, DEC-28',
               'check': 'rendered at shipped size: soft IoU (coverage overlap) >= 0.90; two-tone icons also glyph IoU >= 0.90. IoU of 50% masks and mean coverage difference are reported, not gated (they swing on half-pixel edges of thin strokes)',
               'traces': sorted(keep.values(), key=lambda t: t['name'])}, open(path, 'w'), indent=1)

if __name__ == '__main__':
    main()

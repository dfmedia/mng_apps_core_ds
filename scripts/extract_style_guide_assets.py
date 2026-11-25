#!/usr/bin/env python3
"""Measure every image exported in the two Apps team style guides.

Input:  downloads/style-guides/{android,ios}/<guide folder>/<file> (git-ignored; Karl's local copies of the
        style-guide Files, downloaded 2026-11-25) and downloads/style-guides/manifest.json (the guides' own
        file lists, from each guide's project/design-system.json).
Output: data/source/style-guide-assets.json — one row per file: platform, guide folder, file, bytes, sha256,
        pixel size, alpha, ink colours. No image data goes into the repo (rule 6: data first; repos are public).
"""
import hashlib, json, os, re, sys
from collections import Counter
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..')
SG = os.path.join(ROOT, 'downloads', 'style-guides')
OUT = os.path.join(ROOT, 'data', 'source', 'style-guide-assets.json')

def hexc(rgb): return '#%02X%02X%02X' % rgb[:3]

def png_info(path):
    im = Image.open(path)
    info = {'format': im.format.lower(), 'width': im.width, 'height': im.height, 'mode': im.mode}
    rgba = im.convert('RGBA')
    px = list(rgba.get_flattened_data() if hasattr(rgba, 'get_flattened_data') else rgba.getdata())
    n = len(px)
    alpha0 = sum(1 for p in px if p[3] == 0)
    opaque = [p for p in px if p[3] >= 128]
    info['transparent_share'] = round(alpha0 / n, 3)
    info['has_alpha'] = alpha0 > 0 or any(p[3] < 255 for p in px[:: max(1, n // 4000)])
    # ink colours: quantise to 4 bits per channel so anti-aliasing does not split a colour
    q = Counter((p[0] >> 4, p[1] >> 4, p[2] >> 4) for p in opaque)
    total = sum(q.values()) or 1
    top = []
    for (r, g, b), c in q.most_common(4):
        exact = Counter(p[:3] for p in opaque if (p[0] >> 4, p[1] >> 4, p[2] >> 4) == (r, g, b)).most_common(1)[0][0]
        top.append({'hex': hexc(exact), 'share': round(c / total, 3)})
    info['ink'] = top
    info['ink_buckets'] = len([1 for c in q.values() if c / total >= 0.01])
    return info

def svg_info(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    vb = re.search(r'viewBox="([^"]+)"', s)
    w = re.search(r'\bwidth="([\d.]+)', s); h = re.search(r'\bheight="([\d.]+)', s)
    fills = sorted(set(re.findall(r'(?:fill|android:fillColor)="(#[0-9A-Fa-f]{3,8})"', s)))
    return {'format': 'svg', 'viewBox': vb.group(1) if vb else None,
            'width': float(w.group(1)) if w else None, 'height': float(h.group(1)) if h else None,
            'fills': fills, 'paths': s.count('<path')}

def main():
    man = json.load(open(os.path.join(SG, 'manifest.json')))
    rows, missing = [], []
    for plat, folder, name, _size in man:
        p = os.path.join(SG, plat, folder, name)
        if not os.path.exists(p):
            missing.append(f'{plat}/{folder}/{name}'); continue
        b = open(p, 'rb').read()
        row = {'platform': plat, 'folder': folder, 'file': name, 'bytes': len(b),
               'sha256': hashlib.sha256(b).hexdigest()}
        row.update(svg_info(p) if name.endswith('.svg') else png_info(p))
        rows.append(row)
    out = {'generated_by': 'scripts/extract_style_guide_assets.py',
           'source': {'ios': 'MNG iOS Style Guide (claude.ai/artifact/V364juyHFU3STfVZ6EgjMc), Files › assets',
                      'android': 'MNG Android Style Guide (claude.ai/artifact/5MyLP13QSt52WGRgXW35ZJ), Files › assets',
                      'downloaded': '2026-11-25'},
           'count': len(rows), 'missing': missing, 'assets': rows}
    json.dump(out, open(OUT, 'w'), indent=1)
    print(f'{len(rows)} assets, {len(missing)} missing → {OUT}')

if __name__ == '__main__':
    main()

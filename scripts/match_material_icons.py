#!/usr/bin/env python3
"""Closest Material Symbols for every shipped UI icon (DEC-29 step 1).

Usage: python3 scripts/match_material_icons.py [--sheets DIR]
Reads  data/icon-sources.json (the inventory), data/icon-names.json (reference Material symbol per name),
       downloads/style-guides/ (shipped PNGs, git-ignored), @material-symbols/svg-400 from npm (Apache-2.0).
Writes data/icon-material-matches.json: per icon name and platform, the shipped master file and the 5 closest
       Material Symbols (outlined and filled, weight 400) by shape, plus the score of the reference symbol.
       With --sheets DIR, also contact sheets (shipped PNG | reference | top 5) as PNGs in DIR (not in the repo:
       they contain the shipped images).
Shape score: both images cropped to their ink, fitted into 48 x 48, blurred by 1 px, soft IoU. It ranks
candidates; Karl's picks (scripts/build_icon_replacements.py) are made by eye from the sheets.
"""
import json, os, sys, subprocess, tempfile, io
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SG = os.path.join(ROOT, 'downloads', 'style-guides')
VERSION = '0.49.0'
CACHE = os.path.join(tempfile.gettempdir(), f'material-symbols-{VERSION}')
N, FIT = 48, 40

def material_pkg():
    pkg = os.path.join(CACHE, 'package')
    if not os.path.isdir(pkg):
        os.makedirs(CACHE, exist_ok=True)
        subprocess.run(['npm', 'pack', f'@material-symbols/svg-400@{VERSION}', '-q'], cwd=CACHE, check=True, capture_output=True)
        subprocess.run(['tar', 'xzf', f'material-symbols-svg-400-{VERSION}.tgz'], cwd=CACHE, check=True)
    return pkg

def norm(alpha):
    """float alpha 0..1 -> normalised 48x48 float mask (ink cropped, fitted, centred, blurred 1 px)."""
    m = alpha >= 0.5
    if not m.any():
        return np.zeros((N, N))
    ys, xs = np.where(m)
    crop = alpha[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = crop.shape
    s = FIT / max(h, w)
    im = Image.fromarray((crop * 255).astype(np.uint8)).resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
    c = Image.new('L', (N, N), 0)
    c.paste(im, ((N - im.width) // 2, (N - im.height) // 2))
    return np.asarray(c.filter(ImageFilter.GaussianBlur(1))) / 255.0

def soft_iou(a, b):
    return float(np.minimum(a, b).sum() / max(1e-6, np.maximum(a, b).sum()))

def render_svg(path, px=96):
    import cairosvg
    png = cairosvg.svg2png(url=path, output_width=px, output_height=px)
    return np.asarray(Image.open(io.BytesIO(png)).convert('RGBA'))[:, :, 3] / 255.0

def material_masks(pkg):
    cache = os.path.join(CACHE, 'masks.npz')
    if os.path.exists(cache):
        d = np.load(cache)
        return list(d['names']), d['masks']
    names, masks = [], []
    for f in sorted(os.listdir(os.path.join(pkg, 'outlined'))):
        if f.endswith('.svg'):
            names.append(f[:-4]); masks.append(norm(render_svg(os.path.join(pkg, 'outlined', f))))
    masks = np.stack(masks).astype(np.float32)
    np.savez_compressed(cache, names=np.array(names), masks=masks)
    return names, masks

def main():
    sheets = sys.argv[sys.argv.index('--sheets') + 1] if '--sheets' in sys.argv else None
    pkg = material_pkg()
    names, masks = material_masks(pkg)
    flat = masks.reshape(len(names), -1)
    idx = {n: i for i, n in enumerate(names)}
    src = json.load(open(os.path.join(ROOT, 'data', 'icon-sources.json')))['assets']
    ref = {i['name']: (i['reference'] or {}).get('material') for i in json.load(open(os.path.join(ROOT, 'data', 'icon-names.json')))['icons']}
    # one shipped master per (name, platform, shape): the largest file of that drawing
    seen, items = set(), []
    for r in src:
        if r['kind'] != 'icon' or not r['name'] or r['name'].startswith('brand-') or r['vector'] == 'drop':
            continue
        master = r['master'].split('/', 2)
        key = (r['name'], master[0], r['shape'])
        if key in seen or master[0] != r['platform']:
            continue
        seen.add(key)
        items.append({'name': r['name'], 'platform': r['platform'], 'master': r['master'], 'shape': r['shape'], 'variants': r['variants']})
    out = []
    for it in items:
        plat, folder, file = it['master'].split('/', 2)
        p = os.path.join(SG, plat, folder, file)
        alpha = render_svg(p) if p.endswith('.svg') else np.asarray(Image.open(p).convert('RGBA'))[:, :, 3] / 255.0
        q = norm(alpha).reshape(-1)
        mn = np.minimum(flat, q).sum(1); mx = np.maximum(flat, q).sum(1)
        sc = mn / np.maximum(mx, 1e-6)
        top = np.argsort(-sc)[:5]
        r_name = ref.get(it['name'])
        r_score = None
        if r_name:
            r_name = r_name.replace(' ', '_')
            if r_name not in idx:
                r_name = None
            else:
                r_score = round(float(sc[idx[r_name]]), 3)
                f = r_name + '-fill'
                if f in idx and sc[idx[f]] > sc[idx[r_name]]:
                    r_name, r_score = f, round(float(sc[idx[f]]), 3)
        it.update(reference=r_name, reference_score=r_score,
                  top=[{'symbol': names[i], 'score': round(float(sc[i]), 3)} for i in top])
        out.append(it)
    out.sort(key=lambda x: (x['name'], x['platform']))
    json.dump({'generated_by': 'scripts/match_material_icons.py', 'material': f'@material-symbols/svg-400@{VERSION} (outlined, weight 400; -fill = filled)',
               'score': 'soft IoU of ink-fitted 48 x 48 masks, 1 px blur', 'matches': out},
              open(os.path.join(ROOT, 'data', 'icon-material-matches.json'), 'w'), indent=1)
    print(len(out), 'shipped masters matched')
    if sheets:
        os.makedirs(sheets, exist_ok=True)
        T = 84
        def tile(alpha):
            im = Image.fromarray((np.clip(alpha, 0, 1) * 255).astype(np.uint8))
            im.thumbnail((T - 8, T - 8), Image.LANCZOS)
            t = Image.new('L', (T, T), 255)
            t.paste(Image.new('L', im.size, 0), ((T - im.width) // 2, (T - im.height) // 2), im)
            return t
        per = 12
        for si in range(0, len(out), per):
            chunk = out[si:si + per]
            sheet = Image.new('L', (7 * (T + 6) + 200, len(chunk) * (T + 18)), 255)
            d = ImageDraw.Draw(sheet)
            for ri, it in enumerate(chunk):
                y = ri * (T + 18)
                plat, folder, file = it['master'].split('/', 2)
                p = os.path.join(SG, plat, folder, file)
                a = render_svg(p) if p.endswith('.svg') else np.asarray(Image.open(p).convert('RGBA'))[:, :, 3] / 255.0
                d.text((2, y + 2), f"{si + ri}. {it['name']}", fill=0)
                d.text((2, y + 16), f"{plat}: {file[:26]}", fill=0)
                d.text((2, y + 30), f"x{it['variants']}", fill=0)
                cells = [('shipped', a)]
                cells.append((f"ref {it['reference'] or '—'} {it['reference_score'] or ''}",
                              render_svg(os.path.join(pkg, 'outlined', it['reference'] + '.svg')) if it['reference'] else np.zeros((4, 4))))
                for t in it['top']:
                    cells.append((f"{t['symbol']} {t['score']}", render_svg(os.path.join(pkg, 'outlined', t['symbol'] + '.svg'))))
                for ci, (lab, al) in enumerate(cells):
                    x = 200 + ci * (T + 6)
                    sheet.paste(tile(al), (x, y))
                    d.text((x, y + T + 2), lab[:16], fill=0)
            sheet.save(os.path.join(sheets, f'match-{si // per:02d}.png'))
        print('sheets in', sheets)

if __name__ == '__main__':
    main()

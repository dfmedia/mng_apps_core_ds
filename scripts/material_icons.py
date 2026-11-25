#!/usr/bin/env python3
"""Material Symbols SVGs for icon names whose Android glyph is a stock Material symbol (DEC-28).

Usage: python3 scripts/material_icons.py
Gets @material-symbols/svg-400 (Apache-2.0) from npm into a temp folder and copies the listed symbols to
../mng_apps_android_ds/icons/material/<icon name>.svg, with the package LICENSE next to them.
Material Symbols are Apache-2.0, so unlike SF Symbols they can live in the public repos.
"""
import os, shutil, subprocess, tempfile, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VERSION = '0.49.0'
STYLE = 'outlined'   # the Material Symbols default; the Apps team said replay_10 / forward_10 "work as is" (2026-11-19)
# icon name -> Material symbol (what Android ships: Media3 skip_back_10 / skip_forward_10 draw these glyphs)
SYMBOLS = {'skip-back-10': 'replay_10', 'skip-forward-10': 'forward_10'}

out = os.path.join(ROOT, '..', 'mng_apps_android_ds', 'icons', 'material')
os.makedirs(out, exist_ok=True)
with tempfile.TemporaryDirectory() as t:
    subprocess.run(['npm', 'pack', f'@material-symbols/svg-400@{VERSION}', '-q'], cwd=t, check=True, capture_output=True)
    subprocess.run(['tar', 'xzf', f'material-symbols-svg-400-{VERSION}.tgz'], cwd=t, check=True)
    pkg = os.path.join(t, 'package')
    for name, sym in SYMBOLS.items():
        shutil.copy(os.path.join(pkg, STYLE, f'{sym}.svg'), os.path.join(out, f'{name}.svg'))
    shutil.copy(os.path.join(pkg, 'LICENSE'), os.path.join(out, 'LICENSE'))
json.dump({'generated_by': 'scripts/material_icons.py', 'package': f'@material-symbols/svg-400@{VERSION}', 'style': STYLE,
           'license': 'Apache-2.0', 'icons': SYMBOLS}, open(os.path.join(out, 'manifest.json'), 'w'), indent=1)
print(f'{len(SYMBOLS)} Material Symbols -> {os.path.relpath(out, ROOT)}')

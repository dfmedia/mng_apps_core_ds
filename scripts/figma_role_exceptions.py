"""Emit the Figma build for the header band (iOS) / status bar (Android) exception samples (DEC-15).
Usage: python3 scripts/figma_role_exceptions.py ios|android  ->  prints JS (PLATFORM + DATA + scripts/figma/build_role_exceptions.js)
       to run with figma_execute in that platform's file (iOS uNxwBNoP4ODDUFGByi73mZ, Android FGUeuRYhGudxo0VQdToZT9).
Data: data/shell-colors.json `role_exceptions` (scripts/build_shell_colors.py).
"""
import json, sys
plat = {'ios': 'iOS', 'android': 'Android'}[sys.argv[1]]
D = json.load(open('data/shell-colors.json'))
DATA = [{'code': e['code'], 'market': e['market'], 'built': e['majority'], 'navbar': e['majority'], 'navtext': e['navtext'],
         'override': e['override']['value'], 'accepted': e['accepted'], 'foreground': e['foreground'], 'target': e['target'],
         'contrast_built': e['contrast_majority'], 'contrast_override': e['contrast_override'],
         **({'android15': e['android15']} if 'android15' in e else {})}
        for e in D['role_exceptions'] if e['platform'] == plat]
print(f"const PLATFORM = {json.dumps(plat)};\nconst DATA = {json.dumps(DATA)};\n" + open('scripts/figma/build_role_exceptions.js').read())

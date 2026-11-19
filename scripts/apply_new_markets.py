"""Add markets that have no Android build yet (TDH ships on iOS since f79fe3339; others have no app at all) (data/source/new-markets.json) to the resolution, marked provisional.
Usage: python3 scripts/apply_new_markets.py data/brand-color-resolution.json data/source/new-markets.json
Run after apply_core_alert.py.
"""
import json, sys
res_path, new_path = sys.argv[1:3]
R = json.load(open(res_path)); N = json.load(open(new_path))['markets']
rgb = lambda h: [int(h[i:i+2], 16) for i in (1, 3, 5)]
R['markets'] = [m for m in R['markets'] if not m.get('provisional')]
for n in N:
    R['markets'].append({'code': n['code'], 'name': n['name'], 'cluster': n['cluster'], 'provisional': True, 'status': 'ios-only' if n.get('ios_shipped') else 'provisional', 'ios_shipped': n.get('ios_shipped'),
        'roles': {k: {'ios': v if n.get('ios_shipped') and k != 'alert' else None, 'android': None, 'sheet': None, 'value': v, 'value_rgb': rgb(v),
                      'evidence': ('core-alert' if k == 'alert' else 'ios-only-market') if n.get('ios_shipped') else 'new-market', 'fix': None, 'note': n['source']} for k, v in n['roles'].items()},
        'platform_only': n['platform_only']})
json.dump(R, open(res_path, 'w'), indent=1)
print('added', [n['code'] for n in N])

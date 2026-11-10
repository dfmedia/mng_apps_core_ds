"""Emit the Figma build for the Core page "Color · System colors" from data/system-color-comparison.json.
Usage: python3 scripts/figma_system_colors.py <n>   ->  prints JS (PAGE + T + scripts/figma/build_table_section.js)
       to run with figma_execute in the Core file. n = 1..8 (one section per call; sections stack in order).
"""
import json, sys
D = json.load(open('data/system-color-comparison.json')); P = D['platforms']
PAGE = 'Color · System colors'
sw = lambda h: {'sw': h if (h and h.startswith('#')) else None, 't': (h or 'not set') + ('' if not h or not h.startswith('#') else ' · ' + ', '.join(str(int(h[i:i+2], 16)) for i in (1, 3, 5)) + (f', alpha {round(int(h[7:], 16) / 255, 2)}' if len(h) == 9 else ''))}
chip = lambda b: {'chip': b.replace(' (until pairing confirmed)', '')} if b else ''
KIND = {'fixed': 'Fixed: same in all 77 markets → one System variable', 'follows': 'Follows a brand role → alias', 'majority': 'Majority value → exceptions documented', 'per-market': 'Per market: no value in 39+ markets'}

def colors(plat):
    rows = []; cs = P[plat]['colors']
    for kind in ('fixed', 'follows', 'majority', 'per-market'):
        sel = sorted([c for c in cs if c['kind'] == kind and not c['covered_by']], key=lambda c: c['key'])
        if not sel: continue
        rows.append({'group': f'{KIND[kind]} ({len(sel)})'})
        for c in sel:
            exc = c['exceptions'] if kind in ('follows', 'majority') else {}
            if kind == 'per-market': ex = f"{len(c['values'])} values: " + '; '.join(f"{g['value']} ×{len(g['markets'])}" for g in c['values'][:4])
            else: ex = ', '.join(f"{k} {v or 'not set'}" for k, v in list(sorted(exc.items()))[:6]) + (f" … +{len(exc) - 6}" if len(exc) > 6 else '')
            val = {'t': '= ' + c['follows'] + ' (market brand color)', 'sw': None} if kind == 'follows' else sw(c['majority'])
            n = c['follows_markets'] if kind == 'follows' else c['majority_markets']
            rows.append([{'t': c['key'], 'b': True}, val, str(n), ex or '—', chip(c['bucket'])])
    cov = sorted([c for c in cs if c['covered_by']], key=lambda c: c['key'])
    rows.append({'group': f'Already tokens or not system colors: brand roles, app shell, controls, buttons, brand assets ({len(cov)})'})
    for c in cov: rows.append([{'t': c['key'], 'b': True}, {'t': '= ' + c['follows'], 'sw': None} if c['kind'] == 'follows' else sw(c['majority']), str(c['follows_markets'] if c['kind'] == 'follows' else c['majority_markets']), '—', 'token: ' + c['covered_by']])
    return rows

def palettes(plat):
    nm = P[plat]['markets']; tpl = P[plat]['templates'] or {}
    rows = []
    for g in P[plat]['palettes']:
        d = g['differences_from_majority']
        rows.append([{'t': g['id'], 'b': True}, ', '.join(f"{c}{' (legacy)' if tpl.get(c) == 'legacy' else ''}" for c in g['markets']), str(len(g['markets'])),
                     'majority palette' if not d else f"{len(d)}: " + ', '.join(list(d)[:5]) + (' …' if len(d) > 5 else '')])
    return rows

BRAND = json.load(open('tokens/core/brand.tokens.json'))['color']['brand']
def palette_values(plat):
    """07/08: every exception palette's actual values next to the majority value (DEC-16; data/system-color-comparison.json)."""
    nm = P[plat]['markets']; tpl = P[plat]['templates'] or {}; mp = P[plat]['majority_palette']
    rows = []
    for g in P[plat]['palettes'][1:]:
        d = g['differences_from_majority']; ms = g['markets']
        names = ', '.join(f"{c} {nm.get(c, '')}{' (legacy)' if tpl.get(c) == 'legacy' else ''}".strip() for c in ms)
        rows.append({'group': f"{g['id']} · {len(ms)} market{'s' if len(ms) > 1 else ''}: {names} · {len(d)} color{'s differ' if len(d) != 1 else ' differs'}"})
        for key in sorted(d):
            maj = mp.get(key)
            if isinstance(maj, str) and maj.startswith('='):
                role = maj[1:]; tok = BRAND.get(ms[0].lower(), {}).get(role) if len(ms) == 1 else None
                majc = ({'sw': tok['$value'], 't': f"= {role} → {sw(tok['$value'])['t']} ({ms[0]} brand token)"} if tok and str(tok.get('$value', '')).startswith('#')
                        else {'sw': None, 't': f"= {role} (the market's brand color)"})
            else:
                majc = sw(maj)
            rows.append([{'t': key, 'b': True}, majc, sw(d[key])])
    return rows

S = P['ios']['summary'], P['android']['summary']
SEC = {
 1: dict(name='01 · Summary', title='System colors · iOS vs Android',
         intro='Every themed color both apps ship, in all 77 markets, from data/system-color-comparison.json (scripts/compare_system_colors.py; TroncKit @ e30ad2585, android-tribpub @ 1cfb069a6). DEC-16 (2026-11-10): tokens hold the majority values (Core: System colors collection; iOS and Android: System colors · iOS / · Android; docs/SYSTEM-TOKENS.md). Every market palette is documented here and in docs/SYSTEM-COLORS.md; exceptions are not built.',
         columns=[{'name': '', 'w': 560}, {'name': 'iOS', 'w': 200}, {'name': 'Android', 'w': 200}],
         rows=[[lab, str(S[0].get(k, 0)), str(S[1].get(k, 0))] for k, lab in [('colors', 'Themed colors in the export'), ('covered', 'Already tokens, or brand assets (not system colors)'), ('fixed', 'Fixed: same in all 77 markets'), ('follows', 'Follows a brand role (alias)'), ('majority', 'Majority value + exceptions'), ('per-market', 'Per market'), ('palettes', 'Distinct market palettes')]]
              + [['iOS ↔ Android pairs (approved 2026-11-10)', str(len(D['pairs'])), str(len(D['pairs']))]]),
 2: dict(name='02 · iOS ↔ Android pairs', title='iOS ↔ Android pairs (approved)',
         intro='Matched by name and screen (data/system-color-pairs.json), then compared market by market (same < 0.012 ΔE, close < 0.05). Approved by Karl 2026-11-10: each pair is one Core token. Not pairs (different designs, platform-only): alert topic rows ×4 and the offline header.',
         columns=[{'name': 'What', 'w': 280}, {'name': 'iOS', 'w': 320}, {'name': 'iOS value', 'w': 240}, {'name': 'Android', 'w': 260}, {'name': 'Android value', 'w': 240}, {'name': 'Same / close / differ', 'w': 150}, {'name': 'Bucket', 'w': 220}, {'name': 'Check', 'w': 280}],
         rows=[[p['what'], {'t': p['ios'], 'b': True}, sw(p['ios_majority']) if p['ios_kind'] != 'follows' else '= role', {'t': p['android'], 'b': True}, sw(p['android_majority']) if p['android_kind'] != 'follows' else '= role',
                f"{p['same']} / {p['close']} / {p['differ']}", chip(p['bucket']), p['check'] or '—'] for p in D['pairs']]),
 3: dict(name='03 · iOS colors', title='iOS · every themed color', intro='Value = the majority value (or the brand role it follows). Exceptions: market and the value it ships instead (first six; all in docs/SYSTEM-COLORS.md). "not set" = UIKit system default (MISSING-ASSETS 3.1).',
         columns=[{'name': 'Color', 'w': 380}, {'name': 'Value', 'w': 280}, {'name': 'Markets', 'w': 90}, {'name': 'Exceptions', 'w': 560}, {'name': 'Bucket', 'w': 280}], rows=colors('ios')),
 4: dict(name='04 · Android colors', title='Android · every themed color', intro='Value = the majority value (or the brand role it follows). Exceptions: market and the value it ships instead (first six; all in docs/SYSTEM-COLORS.md). 8-digit values carry alpha.',
         columns=[{'name': 'Color', 'w': 380}, {'name': 'Value', 'w': 280}, {'name': 'Markets', 'w': 90}, {'name': 'Exceptions', 'w': 560}, {'name': 'Bucket', 'w': 280}], rows=colors('android')),
 5: dict(name='05 · iOS market palettes', title='iOS · market palettes', intro=f"Every market is in exactly one palette. Markets in a palette ship identical system colors (brand-following colors compared as the role). The differences are listed in docs/SYSTEM-COLORS.md. {S[0]['palettes']} palettes for 77 markets.",
         columns=[{'name': 'Palette', 'w': 100}, {'name': 'Markets', 'w': 900}, {'name': 'Count', 'w': 80}, {'name': 'Differences from the majority palette', 'w': 600}], rows=palettes('ios')),
 6: dict(name='06 · Android market palettes', title='Android · market palettes', intro=f"Every market is in exactly one palette. Markets in a palette ship identical system colors (brand-following colors compared as the role). The differences are listed in docs/SYSTEM-COLORS.md. {S[1]['palettes']} palettes for 77 markets. ic_launcher_background (app icon background) is a market brand asset, not a system color (DEC-16, docs/BRAND-COLORS.md).",
         columns=[{'name': 'Palette', 'w': 100}, {'name': 'Markets', 'w': 900}, {'name': 'Count', 'w': 80}, {'name': 'Differences from the majority palette', 'w': 600}], rows=palettes('android')),
 7: dict(name='07 · iOS palette values', title='iOS · palette values (I02–I19)',
         intro=f"Each exception palette's actual system colors, next to the majority value (palette I01, {len(P['ios']['palettes'][0]['markets'])} markets). Only the colors that differ are listed. Tokens hold the majority value; these are documented, not built (DEC-16). '= role' = the color follows a brand role; for a one-market palette the market's Core brand token is shown. Source: data/system-color-comparison.json (TroncKit @ e30ad2585) · docs/SYSTEM-COLORS.md.",
         columns=[{'name': 'Color', 'w': 380}, {'name': 'Majority value', 'w': 420}, {'name': 'This palette ships', 'w': 300}], rows=palette_values('ios')),
 8: dict(name='08 · Android palette values', title='Android · palette values (A02–A29)',
         intro=f"Each exception palette's actual system colors, next to the majority value (palette A01, {len(P['android']['palettes'][0]['markets'])} markets). Only the colors that differ are listed. Tokens hold the majority value; these are documented, not built (DEC-16). '= role' = the color follows a brand role; for a one-market palette the market's Core brand token is shown (accent: Android role, not resolved). Same hex on both sides (TPD) = the market ships a fixed color where the majority follows the role; today they match. 8-digit values carry alpha. Source: data/system-color-comparison.json (android-tribpub @ 1cfb069a6) · docs/SYSTEM-COLORS.md.",
         columns=[{'name': 'Color', 'w': 380}, {'name': 'Majority value', 'w': 420}, {'name': 'This palette ships', 'w': 300}], rows=palette_values('android')),
}
n = int(sys.argv[1])
if n in (7, 8):
    # long tables: send a compact form (key, majority, palette value) and expand hex -> "hex · R, G, B" in Figma (EXPAND below)
    def cc(c):
        if c.get('sw') is None: return c['t']                                   # '= role (...)' text
        return c['sw'] if '→' not in c['t'] else c['sw'] + '|' + c['t'].split(' → ')[0][2:] + '|' + c['t'].split('(')[-1].split(' ')[0]
    C = dict(SEC[n], rows=[r['group'] if isinstance(r, dict) else [r[0]['t'], cc(r[1]), r[2]['sw']] for r in SEC[n]['rows']])
    EXPAND = """const rgbT = (h) => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)).join(', ') + (h.length === 9 ? `, alpha ${Math.round(parseInt(h.slice(7), 16) / 255 * 100) / 100}` : '');
const swT = (h) => ({ sw: h, t: `${h} · ${rgbT(h)}` });
const majT = (m) => !m.startsWith('#') ? { sw: null, t: m } : m.includes('|') ? (([h, role, mk]) => ({ sw: h, t: `= ${role} → ${h} · ${rgbT(h)} (${mk} brand token)` }))(m.split('|')) : swT(m);
const T = { ...C, rows: C.rows.map(r => typeof r === 'string' ? { group: r } : [{ t: r[0], b: true }, majT(r[1]), swT(r[2])]) };
"""
    print(f"const PAGE = {json.dumps(PAGE)}; const C = {json.dumps(C, ensure_ascii=False, separators=(',', ':'))};\n" + EXPAND + open('scripts/figma/build_table_section.js').read())
else:
    print(f"const PAGE = {json.dumps(PAGE)}; const T = {json.dumps(SEC[n], ensure_ascii=False)};\n" + open('scripts/figma/build_table_section.js').read())

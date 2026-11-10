"""Emit the Figma build for Core page "Type · iOS vs Android" › 04 · iOS per-market fonts / 05 · Android per-market fonts.
Usage: python3 scripts/figma_font_exceptions.py 4|5  ->  prints JS (PAGE + T + scripts/figma/build_table_section.js) for figma_execute in the Core file.
Data: data/type-font-exceptions.json (scripts/build_font_exceptions.py).
"""
import json, sys
D = json.load(open('data/type-font-exceptions.json')); n = int(sys.argv[1])
def market_rows(P):
    rows = []
    for r in P['by_market']:
        rows.append({'group': f"{r['market']} · {r['name']} · {r['keys']} key{'s' if r['keys'] != 1 else ''} differ{'s' if r['keys'] == 1 else ''}"})
        for s in r['swaps']:
            rows.append([{'t': s['from'], 'b': True}, {'t': s['to'], 'b': True}, str(len(s['keys'])), ', '.join(s['keys'])])
    return rows
cols = [{'name': 'Majority font (what the text styles use)', 'w': 300}, {'name': 'This market ships', 'w': 300}, {'name': 'Keys', 'w': 70}, {'name': 'Font keys', 'w': 800}]
SEC = {
 4: dict(name='04 · iOS per-market fonts', title='iOS · per-market fonts (as shipped)',
         intro=(f"{D['ios']['keys_with_exceptions']} of {D['ios']['keys']} AppThemeable font keys differ in at least one market (font name and size). "
                f"Text styles use the majority value (DEC-09); these exceptions are documented, not built. {D['ios']['legacy_template']}. "
                f"Source: {D['source']['ios']} · data/type-font-exceptions.json · docs/TYPE-FONT-EXCEPTIONS.md. Future: IMPROVEMENTS TYPE-05."),
         columns=cols, rows=market_rows(D['ios'])),
 5: dict(name='05 · Android per-market fonts', title='Android · per-market fonts (as shipped)',
         intro=(f"{D['android']['keys_with_exceptions']} of {D['android']['keys']} font keys differ in at least one market; {len(D['android']['by_market'])} markets ship a different font file somewhere. "
                f"Text styles use the majority file per key (DEC-09); these exceptions are documented, not built. Note: OpenSans-Regular-Condensed.ttf is Open Sans Condensed Light (300). "
                f"Source: {D['source']['android']} · data/type-font-exceptions.json · docs/TYPE-FONT-EXCEPTIONS.md. Future: IMPROVEMENTS TYPE-05."),
         columns=cols, rows=market_rows(D['android'])),
}
print(f"const PAGE = {json.dumps('Type · iOS vs Android')}; const T = {json.dumps(SEC[n], ensure_ascii=False, separators=(',', ':'))};\n" + open('scripts/figma/build_table_section.js').read())

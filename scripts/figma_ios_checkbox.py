"""Emit the Figma build for the iOS file: Components · Controls › 02 · Checkbox (as shipped).
Usage: python3 scripts/figma_ios_checkbox.py list            ->  the 17 image files with byte length and FNV-1a hash
       python3 scripts/figma_ios_checkbox.py upload <file>   ->  JS that uploads one image (base64) and refuses it if the
                                                                 decoded bytes don't match the local file
       python3 scripts/figma_ios_checkbox.py build           ->  JS that builds the section from the uploaded images
Run in the iOS file (uNxwBNoP4ODDUFGByi73mZ) with figma_execute. Data: data/ios-checkbox.json; images: data/source/ios-assets/checkbox/.
The Desktop Bridge plugin cannot download from GitHub, so images travel as base64, one per call. Each upload is checked
(length + FNV-1a) because a long base64 string pasted into a call can arrive altered; a mismatch is refused, not stored.
"""
import json, base64, sys
SRC = 'data/source/ios-assets/checkbox'
D = json.load(open('data/ios-checkbox.json'))
files = sorted({s['checked']['file'] for s in D['sets']} | {s['unchecked']['file'] for s in D['sets']} | {e['file'] for e in D['not_mapped']})
slim = {k: D[k] for k in ('source', 'control_size_pt', 'image_placement')}
slim['sets'] = [{'set': s['set'], 'checked': {'file': s['checked']['file']}, 'unchecked': {'file': s['unchecked']['file']}, 'markets': s['markets']} for s in D['sets']]
slim['not_mapped'] = [{'file': e['file'], 'note': e['note']} for e in D['not_mapped']]


def fnv(b):
    x = 2166136261
    for c in b: x = ((x ^ c) * 16777619) & 0xffffffff
    return x


UPLOAD = '''const F=%s, LEN=%d, FNV=%d, B64=%s;
const b=figma.base64Decode(B64); let x=2166136261>>>0; for (const c of b){x^=c; x=Math.imul(x,16777619)>>>0;}
if (b.length!==LEN || x!==FNV) return {file:F, error:'mismatch, not stored', len:b.length, fnv:x};
const KEY='mng-ios-checkbox-images', TEMP='_checkbox images (temporary)';
const pg=figma.root.children.find(p=>p.name==='Components · Controls'); await pg.loadAsync();
let tmp=pg.children.find(n=>n.name===TEMP); if(!tmp){tmp=figma.createFrame(); tmp.name=TEMP; tmp.x=-2000; tmp.resize(800,40); pg.appendChild(tmp);}
const h=figma.createImage(b).hash; const r=figma.createRectangle(); r.name=F; r.resize(17,18); r.fills=[{type:'IMAGE',imageHash:h,scaleMode:'FILL'}]; tmp.appendChild(r);
const hash=JSON.parse(figma.root.getPluginData(KEY)||'{}'); hash[F]=h; figma.root.setPluginData(KEY, JSON.stringify(hash)); return {ok:F};'''

if sys.argv[1] == 'list':
    for f in files:
        b = open(f'{SRC}/{f}', 'rb').read(); print(f, len(b), fnv(b))
elif sys.argv[1] == 'upload':
    f = sys.argv[2]; assert f in files, f'unknown file {f}'
    b = open(f'{SRC}/{f}', 'rb').read()
    print(UPLOAD % (json.dumps(f), len(b), fnv(b), json.dumps(base64.b64encode(b).decode())))
else:
    print(f"const DATA = {json.dumps(slim, separators=(',', ':'))};\n" + open('scripts/figma/build_ios_checkbox.js').read())

// Exports TRUE VECTOR SVGs of the SF Symbols used on the Icons page.
// Run on a Mac from the repo root:   swift scripts/sf_symbols_vectors.swift
//
// How: SF Symbols live as glyphs in the system font (SF Pro) at private-use code points.
// Apple doesn't publish the name → code point map, so this script renders each symbol by
// name (NSImage systemSymbolName) and finds the system-font glyph that looks identical,
// then writes that glyph's outline as an SVG path.
//
// Run from anywhere: output paths are taken from this script's location (2026-11-25: a run from another folder wrote nothing to the repo).
// Two methods, both run every time:
//   A. glyph outlines from a font that carries the symbol glyphs (system font, SF Pro, or any font inside SF Symbols.app);
//   (2026-11-25: drawing NSImage symbols into a PDF gives bitmaps, not vectors, so that route is gone.)
//   Each symbol is first looked up by glyph name in that font (exact); only if the font has no glyph of that name is it
//   matched by shape against every symbol glyph.
// Everything printed is also written to assets/sf-symbols/vector/_log.txt.
// Output: assets/sf-symbols/vector/<name>.svg   (Regular weight, 40 pt, black fill)
//         assets/sf-symbols/vector/<name>@<weight>.svg   (Medium … Heavy, for the WEIGHTED symbols only)
//         assets/sf-symbols/vector/_codepoints.json  (name → code point + match score)
// DEC-26 (2026-11-25): the list covers every SF Symbol iOS ships plus the candidates that replace the 7 Font Awesome
// glyphs (with filled versions and heavier weights, so Karl can pick the closest). The output folder is git-ignored
// while the repos are public (Apple licence); it moves into the repo once they are private.
// SF Symbols licence: use only in mockups of apps for Apple platforms.
import AppKit
import CoreText

let names = ["magnifyingglass", "gearshape", "square.and.arrow.up", "bookmark", "bookmark.fill", "house", "line.3.horizontal", "bell", "newspaper", "gamecontroller.fill", "chevron.up", "chevron.down", "chevron.left", "chevron.right", "xmark", "xmark.circle.fill", "person.circle.fill", "exclamationmark.triangle.fill", "envelope.fill", "arrow.clockwise", "line.3.horizontal.decrease", "textformat.size.smaller", "textformat.size.larger", "plus.circle", "minus.circle", "checkmark.circle.fill", "circle", "arrow.right.circle.fill", "arrow.up.left.and.arrow.down.right", "arrow.down.right.and.arrow.up.left", "arrow.left", "arrow.right", "play.fill", "pause.fill", "gobackward.15", "goforward.15", "backward.fill", "forward.fill", "cube", "star", "star.leadinghalf.filled", "star.fill", "heart", "arrow.2.squarepath", "checkmark.seal.fill", "apple.logo",
             // DEC-26: filled candidates for the Font Awesome replacements, and the tournament-loading symbols iOS ships
             "house.fill", "bell.fill", "soccerball.inverse", "american.football.fill", "baseball.fill", "basketball.fill", "hockey.puck.fill", "sportscourt.fill",
             // DEC-29: every SF Symbol docs/ICON-REPLACEMENTS.md picks (data/icon-replacements.json sf_symbols_needed)
             "book", "checkmark", "checkmark.circle", "exclamationmark.circle.fill", "heart.fill", "pause.circle.fill", "play.circle.fill", "puzzlepiece", "slider.horizontal.3", "smallcircle.filled.circle", "text.badge.minus", "text.badge.plus", "textformat.size"]

// The 7 Font Awesome replacements (DEC-26): also exported at heavier weights, because Font Awesome is solid and heavy.
let weighted = ["magnifyingglass", "bookmark", "bookmark.fill", "house", "house.fill", "line.3.horizontal", "bell", "bell.fill", "chevron.up", "chevron.down"]
let weights: [(String, NSFont.Weight)] = [("medium", .medium), ("semibold", .semibold), ("bold", .bold), ("heavy", .heavy)]

let scriptURL = URL(fileURLWithPath: CommandLine.arguments[0], relativeTo: URL(fileURLWithPath: FileManager.default.currentDirectoryPath)).standardizedFileURL
let repoRoot = scriptURL.deletingLastPathComponent().deletingLastPathComponent()
let outDir = repoRoot.appendingPathComponent("assets/sf-symbols/vector")
try! FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)
var logText = ""
func say(_ s: String) { print(s); logText += s + "\n"; try? logText.write(to: outDir.appendingPathComponent("_log.txt"), atomically: true, encoding: .utf8) }
say("Repo: \(repoRoot.path)  macOS \(ProcessInfo.processInfo.operatingSystemVersionString)")

let S = 112          // render canvas (px)
let N = 28           // signature grid
let fontSize: CGFloat = 40
var font = NSFont.systemFont(ofSize: fontSize, weight: .regular) as CTFont
// If the system font has no symbol glyphs, fall back to the font bundled with the SF Symbols app.
func hasSymbolGlyph(_ f: CTFont) -> Bool {
    var u = Array(String(UnicodeScalar(UInt32(0x100000))!).utf16); var g = [CGGlyph](repeating: 0, count: u.count)
    return CTFontGetGlyphsForCharacters(f, &u, &g, u.count) && g[0] != 0
}
var glyphFontFound = hasSymbolGlyph(font)
if glyphFontFound { say("Symbol glyphs: system font") }
if !glyphFontFound {   // SF Pro installed as a font
    for n in ["SF Pro", "SF Pro Text", "SF Pro Display", "SFPro-Regular", "SFProText-Regular"] {
        if let f = NSFont(name: n, size: fontSize), hasSymbolGlyph(f as CTFont) { font = f as CTFont; glyphFontFound = true; say("Symbol glyphs: font \(n)"); break }
    }
}
if !glyphFontFound {   // any font file inside the SF Symbols app
    let res = "/Applications/SF Symbols.app/Contents/Resources"
    let files = (FileManager.default.enumerator(atPath: res)?.allObjects as? [String] ?? []).filter { $0.hasSuffix(".otf") || $0.hasSuffix(".ttf") }
    say("SF Symbols.app font files: \(files.isEmpty ? "none found" : files.joined(separator: ", "))")
    for rel in files {
        let url = URL(fileURLWithPath: res + "/" + rel) as CFURL
        for d in (CTFontManagerCreateFontDescriptorsFromURL(url) as? [CTFontDescriptor] ?? []) {
            let f = CTFontCreateWithFontDescriptor(d, fontSize, nil)
            if hasSymbolGlyph(f) { font = f; glyphFontFound = true; say("Symbol glyphs: \(rel)"); break }
        }
        if glyphFontFound { break }
    }
}
if !glyphFontFound { say("No font with symbol glyphs found. Install SF Pro (developer.apple.com/fonts) or the SF Symbols app and run again."); exit(1) }


struct Sig { var v: [Float]; var aspect: Float }

// Render into an 8-bit gray canvas (coverage 0…255) and reduce to an N×N signature of the ink bbox.
// invert: the drawing is dark ink on white (a symbol image drawn as is) instead of white ink on black.
func signature(invert: Bool = false, _ draw: (CGContext) -> Void) -> Sig? {
    var buf = [UInt8](repeating: 0, count: S * S)
    let ok: Bool = buf.withUnsafeMutableBytes { raw -> Bool in
        guard let ctx = CGContext(data: raw.baseAddress, width: S, height: S, bitsPerComponent: 8,
                                  bytesPerRow: S, space: CGColorSpaceCreateDeviceGray(),
                                  bitmapInfo: CGImageAlphaInfo.none.rawValue) else { return false }
        ctx.setFillColor(gray: invert ? 1 : 0, alpha: 1); ctx.fill(CGRect(x: 0, y: 0, width: S, height: S))
        draw(ctx); return true
    }
    if !ok { return nil }
    if invert { for i in 0..<buf.count { buf[i] = 255 - buf[i] } }
    var x0 = S, y0 = S, x1 = -1, y1 = -1
    for y in 0..<S { for x in 0..<S where buf[y * S + x] > 40 {
        x0 = min(x0, x); x1 = max(x1, x); y0 = min(y0, y); y1 = max(y1, y) } }
    if x1 < 0 { return nil }
    let bw = Float(x1 - x0 + 1), bh = Float(y1 - y0 + 1)
    var v = [Float](repeating: 0, count: N * N)
    for gy in 0..<N { for gx in 0..<N {
        let sx0 = x0 + Int(Float(gx) * bw / Float(N)), sx1 = max(sx0 + 1, x0 + Int(Float(gx + 1) * bw / Float(N)))
        let sy0 = y0 + Int(Float(gy) * bh / Float(N)), sy1 = max(sy0 + 1, y0 + Int(Float(gy + 1) * bh / Float(N)))
        var sum: Float = 0, n: Float = 0
        for y in sy0..<min(sy1, S) { for x in sx0..<min(sx1, S) { sum += Float(buf[y * S + x]); n += 1 } }
        v[gy * N + gx] = n > 0 ? sum / n / 255 : 0
    } }
    return Sig(v: v, aspect: bw / bh)
}

func symbolSig(_ name: String) -> Sig? {
    guard let base = NSImage(systemSymbolName: name, accessibilityDescription: nil),
          let img = base.withSymbolConfiguration(
              NSImage.SymbolConfiguration(pointSize: fontSize, weight: .regular).applying(.preferringMonochrome()))
    else { return nil }
    // 2026-11-25: drawing through an NSImage drawing-handler block crashes the swift interpreter (trace trap in
    // NSCustomImageRep). Take the symbol's CGImage instead and draw it with Core Graphics only (black ink on white).
    var rect = CGRect(origin: .zero, size: img.size)
    guard let cg = img.cgImage(forProposedRect: &rect, context: nil, hints: nil) else { return nil }
    let w = img.size.width, h = img.size.height
    return signature(invert: true) { ctx in
        ctx.draw(cg, in: CGRect(x: (CGFloat(S) - w) / 2, y: (CGFloat(S) - h) / 2, width: w, height: h))
    }
}

func glyphPath(_ cp: UInt32, in f: CTFont? = nil) -> CGPath? {
    let f = f ?? font
    var units = Array(String(UnicodeScalar(cp)!).utf16)
    var glyphs = [CGGlyph](repeating: 0, count: units.count)
    guard CTFontGetGlyphsForCharacters(f, &units, &glyphs, units.count), glyphs[0] != 0 else { return nil }
    return CTFontCreatePathForGlyph(f, glyphs[0], nil)
}

func glyphSig(_ path: CGPath) -> Sig? {
    let b = path.boundingBoxOfPath
    if b.isEmpty || b.width > CGFloat(S) - 4 || b.height > CGFloat(S) - 4 { return nil }
    return signature { ctx in
        ctx.translateBy(x: (CGFloat(S) - b.width) / 2 - b.minX, y: (CGFloat(S) - b.height) / 2 - b.minY)
        ctx.addPath(path); ctx.setFillColor(gray: 1, alpha: 1); ctx.fillPath(using: .winding)
    }
}

func score(_ a: Sig, _ b: Sig) -> Float {
    var d: Float = 0
    for i in 0..<(N * N) { d += abs(a.v[i] - b.v[i]) }
    return d / Float(N * N) + abs(log(a.aspect / b.aspect))
}

// Index every private-use glyph in the system font.
var candidates: [(cp: UInt32, path: CGPath, sig: Sig)] = []
if glyphFontFound {
    say("Method A: indexing symbol glyphs…")
    for cp in UInt32(0x100000)..<UInt32(0x104000) {
        if let p = glyphPath(cp), let s = glyphSig(p) { candidates.append((cp, p, s)) }
    }
    say("  \(candidates.count) glyphs")
}
if candidates.isEmpty { say("No symbol glyphs in the font: stopping."); exit(1) }

func svg(_ path: CGPath) -> String {
    let b = path.boundingBoxOfPath
    var t = CGAffineTransform(translationX: -b.minX, y: b.maxY).scaledBy(x: 1, y: -1)
    let p = path.copy(using: &t)!
    var d = ""
    func f(_ v: CGFloat) -> String { String(format: "%.3f", Double(v)) }
    p.applyWithBlock { el in
        let e = el.pointee, pt = e.points
        switch e.type {
        case .moveToPoint: d += "M\(f(pt[0].x)) \(f(pt[0].y))"
        case .addLineToPoint: d += "L\(f(pt[0].x)) \(f(pt[0].y))"
        case .addQuadCurveToPoint: d += "Q\(f(pt[0].x)) \(f(pt[0].y)) \(f(pt[1].x)) \(f(pt[1].y))"
        case .addCurveToPoint: d += "C\(f(pt[0].x)) \(f(pt[0].y)) \(f(pt[1].x)) \(f(pt[1].y)) \(f(pt[2].x)) \(f(pt[2].y))"
        case .closeSubpath: d += "Z"
        @unknown default: break
        }
    }
    return "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"\(f(b.width))\" height=\"\(f(b.height))\" viewBox=\"0 0 \(f(b.width)) \(f(b.height))\"><path fill=\"#000\" fill-rule=\"nonzero\" d=\"\(d)\"/></svg>\n"
}

var report: [String: Any] = [:]
var weak: [String] = []
func glyphByName(_ name: String, in f: CTFont? = nil) -> CGPath? {
    let f = f ?? font
    let g = CTFontGetGlyphWithName(f, name as CFString)
    return g == 0 ? nil : CTFontCreatePathForGlyph(f, g, nil)
}
for name in names {
    say("… \(name)")
    if let p = glyphByName(name) {   // exact: the font names the glyph after the symbol
        try! svg(p).write(to: outDir.appendingPathComponent("\(name).svg"), atomically: true, encoding: .utf8)
        var done: [String] = []
        if weighted.contains(name) {
            for (wn, w) in weights {
                let wf = NSFont.systemFont(ofSize: fontSize, weight: w) as CTFont
                if let wp = glyphByName(name, in: wf) {
                    try! svg(wp).write(to: outDir.appendingPathComponent("\(name)@\(wn).svg"), atomically: true, encoding: .utf8); done.append(wn)
                }
            }
        }
        report[name] = ["method": "glyph name", "weights": done] as [String: Any]
        say("    by glyph name\(done.isEmpty ? "" : " (+ " + done.joined(separator: ", ") + ")")")
        continue
    }
    guard let s = symbolSig(name) else { say("    MISSING (not an SF Symbol on this macOS?)"); continue }
    var best: (Float, Int) = (.infinity, -1), second: Float = .infinity
    for (i, c) in candidates.enumerated() {
        var sc = score(s, c.sig)
        if sc.isNaN { sc = .infinity }
        if sc < best.0 { second = best.0; best = (sc, i) } else if sc < second { second = sc }
    }
    guard best.1 >= 0 else { say("    NO MATCH"); continue }
    let c = candidates[best.1]
    try! svg(c.path).write(to: outDir.appendingPathComponent("\(name).svg"), atomically: true, encoding: .utf8)
    let cpHex = String(format: "U+%06X", c.cp)
    var done: [String] = []
    if weighted.contains(name) {   // same code point, heavier system-font weights (the SF Symbols app font has one weight only)
        for (wn, w) in weights {
            let wf = NSFont.systemFont(ofSize: fontSize, weight: w) as CTFont
            if hasSymbolGlyph(wf), let p = glyphPath(c.cp, in: wf) {
                try! svg(p).write(to: outDir.appendingPathComponent("\(name)@\(wn).svg"), atomically: true, encoding: .utf8); done.append(wn)
            }
        }
        if done.isEmpty { say("  (no weights for \(name): the system font has no symbol glyphs)") }
    }
    report[name] = ["method": "shape match", "codepoint": cpHex, "score": best.0, "runnerUp": second, "weights": done] as [String: Any]
    let flag = best.0 > 0.08 || second - best.0 < 0.01 ? "  <-- CHECK" : ""
    if !flag.isEmpty { weak.append(name) }
    say(String(format: "%@  %@  score %.3f  next %.3f%@", cpHex, name, best.0, second, flag))
}
try! JSONSerialization.data(withJSONObject: report, options: [.prettyPrinted, .sortedKeys])
    .write(to: outDir.appendingPathComponent("_codepoints.json"))
say("Done: \(report.count) SVGs in assets/sf-symbols/vector/. Weak matches to eyeball: \(weak.isEmpty ? "none" : weak.joined(separator: ", "))")

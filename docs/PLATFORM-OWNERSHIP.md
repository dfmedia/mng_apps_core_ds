# Platform ownership — Core vs iOS vs Android

What belongs in Core and what belongs in a platform file, based on the shipped code of both apps. This is the starting point for splitting the Core file into the iOS and Android files.

- iOS: TroncKit @ `e30ad2585` · Android: android-tribpub @ `1cfb069a6` (2026-10-15)
- Figma (Core file): **Icons · System Comparison → 04 · Platform ownership** and **Color · Market Palettes → 05 · iOS vs Android**
- Data: `data/icon-platform-map.json`, `data/color-platform-comparison.json`

Status key: `PROPOSED` · `WAITING` (on Apps team) · `APPROVED` · `REJECTED` · `DONE`

## Icons — 61 purposes

| Bucket | Count | What's in it |
|--------|-------|--------------|
| Core | 32 | Search, settings, share, save/saved, all tabs except Digital, arrows, close, play/pause, check/uncheck, continue, email, refresh, filter, warning, brands used by both (Google, Facebook, X, Bluesky, Instagram, Amazon) |
| Core + platform variant | 2 | Text size: Android has one icon that opens a 4-step list; iOS has smaller and larger glyphs |
| iOS only | 25 | Digital tab, account, follow/unfollow topic, 4 eNewspaper viewer controls (Android uses the PageSuite SDK), skip 15 s, rewind, fast forward, 3D embed, tournament symbols, 3 rating stars, 3 tweet-embed icons, Apple, YouTube, Vimeo, 1Password, Outbrain |
| Android only | 2 | Notification small icon (a platform requirement); special-section save star (same meaning as Saved; kept as Android's glyph, DEC-17) |

Most iOS-only items are **features** Android doesn't have, not icon disagreements. If Android adds the feature, the icon moves to Core.

## Colors — brand roles

| Role | Bucket | Same / close / differs (of 77) | Note |
|------|--------|-------------------------------|------|
| navbar | Core | 55 / 5 / 17 | 39 of the 55 are near-identical hexes (#4351af vs #4252b0) |
| navtext | Core | 75 / 0 / 2 | TIVDB, OS |
| tabbar | Core | 54 / 5 / 18 | Android always = navbar; iOS too except BS |
| tabactive | Core | 54 / 2 / 21 | |
| tabinactive | Core | 73 / 0 / 4 | Android reuses navtext |
| action | Core | 49 / 6 / 22 | Primary / Subscribe button |
| alert | Core (one value) | 0 / 6 / 71 | Android #cf000e everywhere; iOS #ff0000 (71) and #d80000 (6) |
| buy | Core alias → action | 48 / 6 / 23 | = action in 77/77 iOS and 74/77 Android markets |
| continue | Core alias → action | — | Android only as a color; = action in 70/77. iOS uses pre-colored PNGs |
| statusbar | Android only | — | = navbar in 70/77; default alias to navbar |
| header | iOS only | — | = navbar in 66/77; default alias to navbar |
| accent | Android only | 43 / 3 / 31 | Theme accent for switches; 19 markets still use template gold #daa520 |

- **43 markets** match on all six bar/tab/button roles and can share one Core palette now.
- **34 markets** have at least one real difference (listed in Figma section 05).
- Hexes: 63 on Android, 59 on iOS. 16 are identical; 34 more Android values are near-identical to an iOS value (off by 1 in one channel; invisible). They appear in 40 of the 77 brands.

## Decisions for Karl

| ID | Decision | Recommendation | Status |
|----|----------|----------------|--------|
| PLAT-01 | Adopt the ownership buckets as the rule | The five buckets in CLAUDE.md (Core, Core per-platform value, Core alias, iOS only, Android only); the "Core + platform variant" rows on this page = Core per-platform value | APPROVED 2026-11-10 → DEC-17 |
| PLAT-02 | Near-identical hexes: which value is official | Migration sheet wins when it matches an app; otherwise Android, because iOS rounds each channel to 2 decimals (explains 32 of 34 sheet-checked pairs). See DISCREPANCIES DSC-01 | APPROVED 2026-10-21 → DEC-01 in docs/DECISIONS.md |
| PLAT-03 | One Core `alert` color for both apps and all markets | #cf000e: passes 4.5:1 with white (5.74:1); iOS #ff0000 fails (4.0:1). Covers CLR-01 | APPROVED 2026-10-21 → DEC-05 |
| PLAT-04 | Fold `buy` and `continue` into `action` | Yes, as aliases (removes 2 roles × 77 markets) | SETTLED 2026-11-10 by what's built (Karl): `buy` and `continue` colors are aliases of `action` in tokens, Swift, Kotlin and the Figma Brand theme (DEC-04, DEC-06); Android ships them = action in 74 and 70 of 77 markets, exceptions documented, not built (DEC-14). The Continue **button** itself stays as shipped per platform (DEC-14, IMPROVEMENTS BTN-03) |
| PLAT-05 | `statusbar` (Android) and `header` (iOS) default to `navbar` | Platform files only store the exceptions (7 and 11 markets) | APPROVED 2026-11-05 → DEC-15 (aliases of navbar; 8 iOS + 7 Android exceptions documented with suggested overrides, not built) |
| PLAT-06 | 10 markets where iOS shows template blue #004e87 and Android shows the market's own color (TBAN, TBH, TCE, TDB, TDF, TLBPT, TMI, TRDF, TSPPP, TT) | Ask Apps team which is intended. Likely Android | RESOLVED 2026-10-26: iOS value (DEC-03, DEC-08) |
| PLAT-07 | Big brand differences: TLR (iOS rust vs Android blue), TEPTG (navy vs green), TSV (black vs blue), TUDJ, SGVT/PSN/TPE/TSBS/TWDN (orange action on iOS) | Ask brand owners for the correct color per market | RESOLVED 2026-10-26: migration sheet where it covers the market, otherwise iOS (DEC-01, DEC-03, DEC-08) |
| PLAT-08 | Text size icons: one Core "text size" glyph; iOS keeps smaller/larger as a platform variant | Yes | APPROVED 2026-11-10 → DEC-17 (built with the icons, after MISSING-ASSETS §1) |
| PLAT-09 | Drop the Android special-section save star; use Core Saved | Yes | REJECTED 2026-11-10 → DEC-17: the Android star and the iOS bookmark are platform-specific for now; keep both, one icon name |
| PLAT-10 | Android `accent`: decide the switch-on color (today the Material default in Settings, accent on alert topics) | Map to `action` or `tabactive` and retire gold #daa520 | SETTLED 2026-11-10 by what's built (Karl): `accent` follows Core `action`, the value 52 of 77 Android markets ship (DEC-14). The 25 exceptions, including template gold #daa520, are documented in docs/CONTROL-EXCEPTIONS.md, not built; the apps still ship them until the Apps team changes them |

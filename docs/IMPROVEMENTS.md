# Improvements Log — MNG Apps Core Design System

Things we could improve in the apps. **The design system documents shipped values exactly as they are**, including failing ones; every proposed change lives here and is shown beside the shipped value in Figma (Color Palettes page → "Suggested" rows). Nothing here is applied to the shipped tokens until the Apps team approves it.

Status key: `PROPOSED` · `REQUIRED` (Karl: must be fixed in the apps; the design system keeps the shipped value) · `FUTURE` (agreed direction, not scheduled) · `APPROVED` · `REJECTED` · `DONE`
Source: iOS TroncKit @ `e30ad2585` (via the App iOS Design System artifact). Data and math: `data/palette-analysis.json`, `scripts/analyze_palettes.py`.

## Summary

| ID | Area | Improvement | Impact | Status |
|----|------|-------------|--------|--------|
| ICON-01 | Icons | Consolidate three icon systems (Font Awesome, TroncKit PNGs, SF Symbols) into one semantic icon set | All 77 apps, ~250 icon files | PROPOSED |
| ICON-02 | Icons | Replace per-market recolored icon copies with one tinted icon | ~60 duplicate PNGs | PROPOSED |
| ICON-03 | Icons | Remove dead `"saved"` SF Symbol reference | 1 call site | PROPOSED |
| CLR-01 | Color | Breaking-news red fails 4.5:1 with white text | 70 markets | APPROVED (DEC-05) |
| CLR-02 | Color | Nav bar title contrast | 6 markets | PROPOSED |
| CLR-03 | Color | Selected tab icon contrast | 34 markets | PROPOSED |
| CLR-04 | Color | White label on primary button; iOS text link on white | 15 + 9 markets | REQUIRED (DEC-07) |
| CLR-05 | Color | White text on section header band | 6 markets | PROPOSED |
| CLR-06 | Color | Merge near-duplicate brand hexes | 59 → ~45 unique values | PROPOSED |
| CLR-07 | Color | Collapse identical market palettes into shared themes | 77 markets → 45 palettes | PROPOSED |
| CTRL-01 | Controls | Bring touch targets to 44 pt | Checkbox (30), social icons (24) | PROPOSED |
| CTRL-02 | Buttons | Add Secondary, Text, Disabled and Loading button states | All markets | PROPOSED (pilot adds Disabled and Text link, DEC-07) |
| BTN-01 | Buttons | One primary button height for both apps (iOS 44 provisional, Android 60) | All markets | FUTURE (DEC-07) |
| BTN-02 | Buttons | One button label style for both apps (iOS Open Sans Bold 14, Android system font) | All markets | FUTURE (DEC-07) |
| TYPE-03 | Type | One serif for both apps | — | REJECTED (Karl 2026-10-30: fonts stay per platform) |
| TYPE-04 | Type | Shared type scale: one set of sizes for both apps, each in its own fonts | All markets | FUTURE (DEC-09) |
| TYPE-05 | Type | Remove per-market font exceptions (iOS NYDN, VP…; Android Open Sans group, NYDN, CT, MC…) | ~13 markets | FUTURE (DEC-09) |
| LAY-01 | Layout | Reconcile the two breakpoint sets (668/835/1113 vs 668/769/1025) | iPad section fronts | PROPOSED |
| TYPE-01 | Type | Retire the legacy Style.json template (7 markets) | BS, DP, HC, MC, OS, SS, VP | PROPOSED |
| TYPE-02 | Type | Remove font fallbacks that change size (e.g. 12 → 10) | `AppThemeable.swift:630` | PROPOSED |

---

## Icons

### ICON-01 · One semantic icon system — `PROPOSED`

**Today:** iOS draws icons from three unrelated sources: Font Awesome 5.15.1 (7 glyphs), 218 TroncKit images (mostly PNG), and ~21 SF Symbols. The same idea often exists in all three (e.g. Saved = FA `bookmark` + `Saved-*` PNGs + `nav-save-*` PNGs).

**Can it be one system?** Yes — as one *semantic* system, not one glyph file. SF Symbols are Apple-only (licence limits them to Apple-platform UI), and Android's native equivalent is Material Symbols, so a single shared glyph set across both platforms would mean giving up native icons. Recommended structure:

1. **Core DS defines the icon *names and meanings*** — `icon/search`, `icon/share`, `icon/bookmark`, `icon/bookmark-filled`, `icon/settings`, `icon/close`, `icon/play`, … one entry per purpose, with size and color tokens.
2. **Each platform file supplies the glyph**:
   - iOS → SF Symbols wherever one exists (search → `magnifyingglass`, share → `square.and.arrow.up`, settings → `gearshape`, bookmark → `bookmark` / `bookmark.fill`, home → `house`, sections → `line.3.horizontal`, alerts → `bell`, close → `xmark`, play/pause, `gobackward.15` / `goforward.15`, rating → `star` / `star.fill` / `star.leadinghalf.filled`, text size → `textformat.size`, checkbox → `checkmark.circle.fill` / `circle`).
   - Android → Material Symbols for the same names.
3. **A small custom vector set in Core only for what neither platform provides**: social/brand marks (Facebook, Google, Apple, X, Bluesky, Instagram, YouTube, Vimeo — use each brand's official asset), eNewspaper-specific controls, Your News, follow/unfollow topic.
4. **Retire Font Awesome** from the iOS app (7 glyphs; all have SF Symbol equivalents).

Result: one icon list to design and review, native look on each platform, no raster icons.

### ICON-02 · One tinted icon instead of per-market copies — `PROPOSED`

`Saved-Filled-*` / `Saved-Unfilled-*` (9 markets each), `Checkmark-*`, `Uncheck-*`, `YourNews-*`, `Continue-*`, `TopicSelection-*`, `Saved - *` tab icons are the same glyph exported in different colors. Replace each family with one template icon tinted by the market's color token (`tabactive`, `action`, …).

### ICON-03 · Dead `"saved"` SF Symbol — `PROPOSED`

`CoreTabBarViewController.swift:140` asks for `"saved"`, which is not an SF Symbol. Point it at `bookmark` / `bookmark.fill` (see MISSING-ASSETS 1.3).

---

## Color — contrast

Shipped values stay in the design system as-is. The suggestions below change **only lightness** (OKLCH) of the one color that needs to move, keeping hue, so each brand still reads the same. Targets: 4.5:1 for text (WCAG 2.2 AA, SC 1.4.3) and 3:1 for icons/UI (SC 1.4.11). Each suggestion is the smallest lightness change that clears the target, so margins are thin (≈4.56–4.65:1, ≈3.06–3.1:1). Not AAA.

> **Known limitation — revisit later (decision 2026-10-16):** the selected-tab suggestions are checked at 3:1 as icons. Tab *labels* are text and would need 4.5:1; suggestions at ~3.1:1 (P03, P11, P13, P14, P25, P39, P40) and the dimmed unselected-tab values (~3.06:1) pass for the icon but not the label. The "white selected tab" fixes pass both.

### CLR-01 · Breaking-news banner (target 4.5:1) — darken `alert` — `APPROVED` 2026-10-21 as DEC-05: one Core red `#cf000e`, white text 5.74:1

70 markets fail.

| Shipped (fg on bg) | Ratio | Suggested | New ratio | Markets |
|---|---|---|---|---|
| `#ffffff` on `#ff0000` | 4.0:1 | `alert` `#ff0000` → `#e81b12` | 4.57:1 | TBAN, TBH, TBHS, TBCP, TBE, TB, TCCDR, CT, TCE, TCHW, TDB, TDF, TDLW, TDCD, TDPS, TEPTG, TETS, TFMT, TGT, TJA, TLBPT, TLTC, TLADN, TLR, TLS, TMD, TMI, TMCH, NYDN, TOD, OCR, OS, PSN, PAC, TRE, TRDF, TRH, TROT, SGVT, TSCS, TSAR, TSEB, TSV, SIT, TSPPP, TCV, TDC, TDP, TEBT, TMN, TMJ, TMS, TNH, TOP, TPM, TPD, TPE, TR, TSBS, SDUT, TSS, TTH, TT, TRR, TTT, TUDJ, TVR, TVTH, TWDN, TWDD |

### CLR-02 · Nav bar title (target 4.5:1) — darken `navbar`

In these markets `navbar`, `tabbar`, `header` and `action` are the same color today. If `navbar` is darkened, `tabbar` should most likely follow so the top and bottom bars still match (it is shown unchanged on the Figma page because the tab bar itself passes).

6 markets fail.

| Shipped (fg on bg) | Ratio | Suggested | New ratio | Markets |
|---|---|---|---|---|
| `#ffffff` on `#408fcc` | 3.49:1 | `navbar` `#408fcc` → `#287ab5` | 4.62:1 | TUDJ, TVR |
| `#ffffff` on `#1591b7` | 3.64:1 | `navbar` `#1591b7` → `#147fa1` | 4.59:1 | TDLW |
| `#ffffff` on `#5b9bc8` | 3.01:1 | `navbar` `#5b9bc8` → `#3b7ba6` | 4.6:1 | TDCD |
| `#ffffff` on `#c75c14` | 4.23:1 | `navbar` `#c75c14` → `#c05606` | 4.59:1 | TDPS |
| `#ffffff` on `#5480ba` | 4.06:1 | `navbar` `#5480ba` → `#4b77b0` | 4.6:1 | TEBT |

### CLR-03 · Selected tab on tab bar (target 3:1)

34 markets fail.

| Shipped (fg on bg) | Ratio | Suggested | New ratio | Markets |
|---|---|---|---|---|
| `#000000` on `#004e87` | 2.44:1 | `tabactive` `#000000` → `#ffffff` + unselected `#ffffff`→`#759fbe` (3.06:1) | 8.61:1 | TBAN, TCE, TLBPT, TMI, TSPPP, TMN, TT |
| `#000000` on `#36408a` | 2.26:1 | `tabactive` `#000000` → `#ffffff` + unselected `#ffffff`→`#8c92bc` (3.08:1) | 9.3:1 | TCCDR, TCHW, TETS, TJA, TSCS |
| `#ff6900` on `#b01f36` | 2.35:1 | `tabactive` `#ff6900` → `#fc9364` | 3.07:1 | PSN, SGVT, TPE, TSBS, TWDN |
| `#000000` on `#424a54` | 2.34:1 | `tabactive` `#000000` → `#ffffff` + unselected `#ffffff`→`#93989e` (3.09:1) | 8.98:1 | TRH, TCV, TSS, TTT |
| `#000000` on `#33408f` | 2.27:1 | `tabactive` `#000000` → `#ffffff` + unselected `#ffffff`→`#8b92bf` (3.07:1) | 9.25:1 | TEPTG, TFMT |
| `#000000` on `#405278` | 2.7:1 | `tabactive` `#000000` → `#ffffff` + unselected `#ffffff`→`#9aa3b7` (3.08:1) | 7.79:1 | TMD, TMS |
| `#004e87` on `#000000` | 2.44:1 | `tabactive` `#004e87` → `#1a5e98` | 3.1:1 | TRE, TSV |
| `#daa520` on `#ffffff` | 2.24:1 | `tabactive` `#daa520` → `#ba8c13` | 3.07:1 | BS |
| `#004e87` on `#b01f36` | 1.27:1 | `tabactive` `#004e87` → `#000000` | 3.1:1 | TBHS |
| `#000000` on `#004e87` | 2.44:1 | `tabactive` `#000000` → `#9a9a9a` | 3.06:1 | TIVDB |
| `#000000` on `#003b66` | 1.82:1 | `tabactive` `#000000` → `#ffffff` + unselected `#ffffff`→`#6689a3` (3.12:1) | 11.55:1 | TROT |
| `#6bd1e6` on `#5480ba` | 2.3:1 | `tabactive` `#6bd1e6` → `#98edff` | 3.07:1 | TEBT |
| `#004e87` on `#0b151e` | 2.14:1 | `tabactive` `#004e87` → `#2467a2` | 3.1:1 | TOP |
| `#000000` on `#8c0a2e` | 2.2:1 | `tabactive` `#000000` → `#ffffff` + unselected `#ffffff`→`#c38092` (3.1:1) | 9.55:1 | TVTH |

### CLR-04 · White label on primary button (target 4.5:1) — `REQUIRED`

The first pass (iOS shipped values, 2026-10-16) found 22 markets. Since then DEC-01…03 settled the Core `action` colors, so the list below is regenerated from the Core values on every build.

<!-- BUTTON-CLR-04:START generated by scripts/build_button_tokens.py; do not edit inside -->
**REQUIRED** (Karl, DEC-07, 2026-10-26): the design system keeps the shipped colors, and these markets must be fixed in the apps. Checked against the Core `action` values (tokens/core/brand.tokens.json). 15 of 78 markets fail.

| Market | Shipped `action` | White label | Suggested `action` | New ratio | Black label instead |
|---|---|---|---|---|---|
| BS | `#daa520` · 218, 165, 32 | 2.24:1 | `#9f6d00` · 159, 109, 0 | 4.5:1 | 9.38:1 |
| CT | `#9dd1f5` · 157, 209, 245 | 1.63:1 | `#4b7c9d` · 75, 124, 157 | 4.5:1 | 12.87:1 |
| HC | `#4fa8d1` · 79, 168, 209 | 2.67:1 | `#1e7fa6` · 30, 127, 166 | 4.52:1 | 7.85:1 |
| MC | `#539cc4` · 83, 156, 196 | 3.03:1 | `#337ea5` · 51, 126, 165 | 4.5:1 | 6.92:1 |
| NYDN | `#4492e0` · 68, 146, 224 | 3.26:1 | `#2979c5` · 41, 121, 197 | 4.53:1 | 6.43:1 |
| OS | `#15919d` · 21, 145, 157 | 3.77:1 | `#00838f` · 0, 131, 143 | 4.52:1 | 5.57:1 |
| SGVT | `#ff6900` · 255, 105, 0 | 2.89:1 | `#d64200` · 214, 66, 0 | 4.53:1 | 7.27:1 |
| TDB | `#9dd1f5` · 157, 209, 245 | 1.63:1 | `#4b7c9d` · 75, 124, 157 | 4.5:1 | 12.87:1 |
| TDCD | `#5b9bc8` · 91, 155, 200 | 3.01:1 | `#3c7ca8` · 60, 124, 168 | 4.53:1 | 6.97:1 |
| TDF | `#9dd1f5` · 157, 209, 245 | 1.63:1 | `#4b7c9d` · 75, 124, 157 | 4.5:1 | 12.87:1 |
| TDLW | `#1591b7` · 21, 145, 183 | 3.64:1 | `#0080a6` · 0, 128, 166 | 4.53:1 | 5.77:1 |
| TDP | `#f7a430` · 247, 164, 48 | 2.04:1 | `#b16300` · 177, 99, 0 | 4.51:1 | 10.31:1 |
| TDPS | `#c75c14` · 199, 92, 20 | 4.23:1 | `#c25709` · 194, 87, 9 | 4.51:1 | 4.97:1 |
| TEBT | `#6bd1e6` · 107, 209, 230 | 1.77:1 | `#008296` · 0, 130, 150 | 4.53:1 | 11.89:1 |
| TVR | `#408fcb` · 64, 143, 203 | 3.49:1 | `#2b7cb7` · 43, 124, 183 | 4.5:1 | 6.01:1 |

iOS text link (`paywallLinkColor`) on the white paywall, target 4.5:1. 9 markets fail.

| Market | Shipped link | Ratio | Suggested | New ratio |
|---|---|---|---|---|
| HC | `#4fa8d1` · 79, 168, 209 | 2.67:1 | `#1e7fa6` · 30, 127, 166 | 4.52:1 |
| MC | `#539cc4` · 83, 156, 196 | 3.03:1 | `#337ea5` · 51, 126, 165 | 4.5:1 |
| NYDN | `#4591e0` · 69, 145, 224 | 3.29:1 | `#2c79c7` · 44, 121, 199 | 4.5:1 |
| TDCD | `#5b9bc8` · 91, 155, 200 | 3.01:1 | `#3c7ca8` · 60, 124, 168 | 4.53:1 |
| TDLW | `#1591b7` · 21, 145, 183 | 3.64:1 | `#0080a6` · 0, 128, 166 | 4.53:1 |
| TDPS | `#c75c14` · 199, 92, 20 | 4.23:1 | `#c25709` · 194, 87, 9 | 4.51:1 |
| TEBT | `#5480ba` · 84, 128, 186 | 4.06:1 | `#4d78b2` · 77, 120, 178 | 4.52:1 |
| TUDJ | `#408fcc` · 64, 143, 204 | 3.49:1 | `#2a7bb7` · 42, 123, 183 | 4.55:1 |
| TVR | `#408fcc` · 64, 143, 204 | 3.49:1 | `#2a7bb7` · 42, 123, 183 | 4.55:1 |
<!-- BUTTON-CLR-04:END -->

### CLR-05 · White text on section header band (target 4.5:1) — darken `header`

6 markets fail.

| Shipped (fg on bg) | Ratio | Suggested | New ratio | Markets |
|---|---|---|---|---|
| `#ffffff` on `#408fcc` | 3.49:1 | `header` `#408fcc` → `#287ab5` | 4.62:1 | TUDJ, TVR |
| `#ffffff` on `#1591b7` | 3.64:1 | `header` `#1591b7` → `#147fa1` | 4.59:1 | TDLW |
| `#ffffff` on `#5b9bc8` | 3.01:1 | `header` `#5b9bc8` → `#3b7ba6` | 4.6:1 | TDCD |
| `#ffffff` on `#c75c14` | 4.23:1 | `header` `#c75c14` → `#c05606` | 4.59:1 | TDPS |
| `#ffffff` on `#547fba` | 4.1:1 | `header` `#547fba` → `#4d77b2` | 4.57:1 | TEBT |

---

## Color — consolidation

### CLR-06 · Merge near-duplicate hexes — `PROPOSED`

The 539 brand tokens use 59 unique hex values. Several are visually identical (ΔE OKLab < 0.01) and look like typos or rounding:

| Keep | Merge in | Notes |
|------|----------|-------|
| `#b01f36` | `#b01e35` | TBHS `action` |
| `#36408a` | `#363e8a`, `#33408f` | TCHW `header`; 8 uses of `#33408f` |
| `#4050b6` | `#3f50b6`, `#4052b5`, `#4252b0` | VP header; Boulder/Buffzone family |
| `#0f73a8` | `#0f73a9` | SIT `header` |
| `#5c5b59` | `#5d5b59` | MC / TSAR header |
| `#ffeb00` | `#ffea00` | SIT / PAC `tabactive` |
| `#5480ba` | `#547fba` | TEBT `header` |
| `#007538` | `#007739` | TDC / TWDD |
| `#5b9bc8` | `#539cc4` | TDCD / MC (review — slightly more visible) |

**Decision 2026-10-16:** keep shipped values as-is for now; merges not applied. Revisit when building the color variables.

### CLR-07 · Shared themes instead of 77 one-off palettes — `PROPOSED`

77 markets use only **45 unique 7-color palettes** (the largest shared by 7 markets). Figma allows 20 modes per collection on our plan, so grouping markets into shared themes is also what makes variable modes workable. **Decision 2026-10-16:** revisit later.

---

## Controls, layout, type

### CTRL-01 · 44 pt touch targets — `PROPOSED`
Your News checkbox is 30 × 30 and social login icons are 24 pt. Keep the visual size, extend the hit area to `size-touch-min` (44).

### CTRL-02 · Missing button states — `PROPOSED`
Only Primary exists. Disabled is styled only on tracking-consent Continue; loading is a full-screen overlay. Propose Secondary, Text, Disabled and inline Loading variants.

### BTN-01 · One primary button height — `FUTURE`
Decided 2026-10-26 (DEC-07): keep each app's height for now, as tokens: iOS `button.ios.primary.height` 44 pt (provisional; not in the source, MISSING-ASSETS 5.5), Android `button.android.primary.height` 60 dp (`paywall_button_height`). Future change: one height for both, at least 48 so it meets both apps' touch minimums (44 pt / 48 dp).

### BTN-02 · One button label style — `FUTURE`
Decided 2026-10-26 (DEC-07): the Button is a Core component, but the label font stays per platform for now: iOS Open Sans Bold 14 uppercase, Android system font uppercase (Roboto Medium 14sp, provisional). Future change: one label style in Core so the platform files no longer need their own label.

### LAY-01 · One breakpoint set — `PROPOSED`
`FrontWidth.swift` uses 668 / 835 / 1113; `PageItem.swift` uses 668 / 769 / 1025. Pick one.

### TYPE-01 · Retire the legacy Style.json template — `PROPOSED`
7 markets (BS, DP, HC, MC, OS, SS, VP) run an older 60–61-key template with different label fonts. Moving them to the standard 51-key template removes a whole set of type styles.

### TYPE-02 · Size-changing font fallbacks — `PROPOSED`
`UIFont(name:size:) ?? .systemFont(ofSize:)` fallbacks sometimes change size (12 → 10, `AppThemeable.swift:630`). Fallbacks should keep the size.

### TYPE-03 · One serif — `REJECTED`
Karl, 2026-10-30: the fonts can't be unified across iOS and Android and stay separate (iOS Spectral, Android PT Serif for headlines and article text).

### TYPE-04 · Shared type scale — `FUTURE`
One set of sizes for both apps, each app keeping its own fonts. Until then (DEC-09) each app keeps its shipped sizes. Only 1 of 19 shared roles matches today (Section-front label, Open Sans Bold 14).

### TYPE-05 · Remove per-market font exceptions — `FUTURE`
Some markets override the standard fonts: iOS NYDN (Open Sans Condensed) and VP (Open Sans), plus single-market values in a few cell and paywall styles; Android DP, SIT, TOD, TTT, VP (Open Sans for headlines and article text), NYDN, CT, MC, HC, OS, SS (byline, settings, search). Every market should use its platform's standard styles. Today they are tracked as notes on each type token (docs/TYPE-STYLES.md source notes).

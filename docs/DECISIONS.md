# Decisions

Design-system decisions with the rule, the date, who made it and what changed. Proposed decisions still under discussion are in `docs/PLATFORM-OWNERSHIP.md` (PLAT-) and `docs/IMPROVEMENTS.md`. Fixes the apps need are in `docs/DISCREPANCIES.md`.

| ID | Decision | Date | By |
|---|---|---|---|
| DEC-01 | Brand colors: the migration sheet wins when it matches an app; otherwise Android, because iOS rounds each color channel to 2 decimals | 2026-10-21 | Karl |
| DEC-02 | Brand colors: where the Cluster Audit web color is close to our value (ΔE < 0.05), use the web color. Where it's far, keep our earlier choice. Where neither settles it, the brand stays open | 2026-10-21 | Karl |
| DEC-03 | Brand colors: any color still unresolved after DEC-01 and DEC-02 takes the iOS value | 2026-10-21 | Karl |
| DEC-04 | Colors are managed as design tokens: one DTCG source in Core, Style Dictionary generates Swift and Kotlin; every color is documented as hex and RGB | 2026-10-21 | Karl |
| DEC-05 | One breaking-news red for every market and both apps: `#cf000e` with white text (5.74:1, WCAG AA). Fix on iOS ASAP | 2026-10-21 | Karl |
| DEC-06 | Figma color variables: a **Brand colors** collection with every market as plain variables (no modes), plus a **Brand theme** collection with 20 modes (the plan limit) for the required markets, one per cluster and the most different ones. Daily Herald added as a provisional market | 2026-10-21 | Karl |
| DEC-13 | App shell: build waits for the Apps team's production sizes; colors are each platform's production values (new roles for section tabs and Android tab labels; navicon = navtext); icons are swappable slots until the icon set exists | 2026-11-03 | Karl |
| DEC-12 | Everything is linked to tokens: breakpoints as shipped per platform, every component metric as a platform token, and every component property in Figma bound to a variable | 2026-11-03 | Karl |
| DEC-11 | Layout spacing: the values both apps ship the same become Core tokens (cell margin 16, cell gap 8, article side 16, 12-column grid); platform-only layout values and touch targets become platform tokens; component-specific radii and sizes stay raw production values (DEC-09) | 2026-11-03 | Claude, under DEC-09 (Karl to confirm) |
| DEC-10 | The iOS legacy theme template (BS, DP, HC, MC, OS, SS, VP) is acknowledged only: documented, but not built in Figma, tokens or code | 2026-11-03 | Karl |
| DEC-09 | Typography and components match production: each app keeps its own fonts (permanently) and sizes; every shipped style is built, one-app styles and the iOS legacy template included; raw production values where no token exists yet | 2026-10-30 | Karl |
| DEC-08 | Brand colors: iOS is the default for every iOS/Android mismatch that no source confirms, including close ones (the drift rule no longer picks Android on its own). DEC-03 is final: no Apps team confirmation needed | 2026-10-26 | Karl |
| DEC-07 | Button pilot: one Core Button component that keeps each app's shipped values. Colors, radius and height stay as shipped (as per-platform tokens); the label font stays per platform. Contrast failures are required app fixes; height and label font are future changes | 2026-10-26 | Karl |

## DEC-01 · Migration sheet + iOS drift rule

- **Source:** "Tribpub-MNG App Migrations" → Production → Primary / Secondary color (`data/source/migration-sheet-brand-colors.json`; project reference `references/migration-sheet-brand-colors.md`).
- **Rule:** 1) If the sheet's color matches either app, it is the value. 2) If iOS equals Android after rounding each channel to 2 decimals (`0x22` → 0.13 → `0x21`), Android holds the authored value. 3) Otherwise open.
- **Amended by DEC-08 (2026-10-26):** step 2 now applies only where the sheet confirms the value. Without the sheet, the iOS value is used.
- **Why:** the sheet matched Android in every near-identical pair it covered; the rounding explains 32 of the 34 pairs it could check.
- **Applied by:** `scripts/resolve_brand_colors.py` → `data/brand-color-resolution.json`. Replaces proposal PLAT-02.

## DEC-02 · Align with Cluster Audit web colors when close

- **Source:** "_Adabel's Cluster Audit - MAIN" → colors → `{{PropertyColor}}` (WordPress / ARC web colors), read once on 2026-10-21 (`data/source/cluster-audit-web-colors.json`). Not a live source; don't re-read it without a new decision.
- **Rule:** applied to each brand's main color (bar, or the button for the legacy Tribune markets whose bar is white/black). The button follows the bar where the app already uses the same color for both.
  - Close (OKLab ΔE < 0.05, same color family, slightly different shade) → use the web color.
  - Far (ΔE ≥ 0.05) → keep the DEC-01 value.
  - Brand still open and web color far from both apps → stays open.
- **Why:** moves the apps toward the shared web theme colors (fewer palettes to manage) without changing any brand to a visibly different color.
- **Applied by:** `scripts/apply_web_alignment.py` (run after `resolve_brand_colors.py`). Each changed role keeps the earlier value under `previous`.

### Changed to the web color (27)

| Code | Brand | Role | Was | Now | ΔE | Was open? |
|---|---|---|---|---|---|---|
| TBH | Boston Herald | navbar | — (open) | #00538a | 0.015 | yes |
| TCCDR | Canon City Daily Record | navbar | #353f8a | #32408f | 0.009 |  |
| TCE | Chico Enterprise Record | navbar | — (open) | #32408f | 0.046 | yes |
| TETS | Eureka Times Standard | navbar | #353f8a | #32408f | 0.009 |  |
| TGT | Greeley Tribune | navbar | #536e7f | #44687f | 0.028 |  |
| TJA | Journal Advocate | navbar | #353f8a | #32408f | 0.009 |  |
| TLBPT | Long Beach Press-Telegram | navbar | — (open) | #32408f | 0.032 | yes |
| TLADN | Los Angeles Daily News | navbar | #ab4022 | #b93611 | 0.029 |  |
| TLS | Lowell Sun News for Mobile | navbar | #ab4022 | #b93611 | 0.029 |  |
| TMD | Macomb Daily | navbar | #3f5177 | #3a527a | 0.008 |  |
| TMI | Marin Independent Journal News | navbar | — (open) | #32408f | 0.046 | yes |
| NYDN | New York Daily News | action | #4591e0 | #4492e0 | 0.003 |  |
| TOD | Oneida Daily Dispatch | navbar | #b92111 | #b93611 | 0.028 |  |
| OS | Orlando Sentinel | action | — (open) | #15919d | 0.0 | yes |
| PSN | Pasadena Star News | navbar | — (open) | #b93611 | 0.038 | yes |
| TRDF | Redlands Daily Facts | navbar | — (open) | #32408f | 0.032 | yes |
| TSCS | Santa Cruz Sentinel | navbar | #353f8a | #32408f | 0.009 |  |
| TSEB | Sentinel and Enterprise | navbar | #bc3b10 | #b93611 | 0.011 |  |
| TMJ | The Morning Journal | navbar | #bc3b10 | #b93611 | 0.011 |  |
| TMS | The Morning Sun | navbar | #3f5177 | #3a527a | 0.008 |  |
| TNH | The News Herald | navbar | #ab4022 | #b93611 | 0.029 |  |
| TPM | The Pottstown Mercury | navbar | #bc3b10 | #b93611 | 0.011 |  |
| TPE | The Press-Enterprise | navbar | — (open) | #b93611 | 0.038 | yes |
| TSBS | The San Bernardino Sun | navbar | — (open) | #b93611 | 0.038 | yes |
| TTH | The Times Herald | navbar | #bc3b10 | #b93611 | 0.011 |  |
| TRR | The Troy Record | navbar | #bc3b10 | #b93611 | 0.011 |  |
| TWDN | Whittier Daily News | navbar | — (open) | #b93611 | 0.038 | yes |

### Already identical (10)

BS, CT, DP, TEPTG, TFMT, HC, MC, SS, TUDJ, VP

### Kept: web color too far (15)

| Code | Brand | Kept | Web | ΔE |
|---|---|---|---|---|
| TIVDB | Inland Valley Daily Bulletin | #004e87 | #32408f | 0.052 |
| TLTC | Longmont Times-Call for Mobile | #007cba | #32408f | 0.169 |
| TLR | Loveland Reporter Herald | #4e5dca | #32408f | 0.126 |
| TMCH | Monterey County Herald | #3c6292 | #32408f | 0.099 |
| TRE | Reading Eagle | #004e87 | #b93611 | 0.298 |
| TROT | Royal Oak Tribune | #013a67 | #3a527a | 0.099 |
| SGVT | San Gabriel Valley Tribune | #b11e35 | #b93611 | 0.058 |
| TSAR | Saratogian | #f5f5f5 | #b93611 | 0.477 |
| TDC | The Daily Camera | #007639 | #32408f | 0.244 |
| TEBT | The East Bay Times | #557fba | #006394 | 0.119 |
| TMN | The Mercury News | #004e87 | #006394 | 0.064 |
| TR | The Reporter for Mobile | #007cba | #b93611 | 0.299 |
| TVR | Vacaville Reporter | #408fcb | #32408f | 0.229 |
| TVTH | Vallejo Times Herald News | #8d092d | #32408f | 0.229 |
| TWDD | Woodland Daily Democrat | #007639 | #32408f | 0.244 |

### Still open: web color far from both apps (9)

| Code | Brand | iOS | Android | Web | ΔE to nearest |
|---|---|---|---|---|---|
| TDB | Daily Breeze | #004e87 | #2e6c90 | #0a5962 | 0.079 |
| TDF | Daily Freeman | #004e87 | #1b6bad | #b93611 | 0.289 |
| TDLW | Daily Local Weschester | #1591b7 | #1591b5 | #b93611 | 0.296 |
| TDCD | Delaware County Daily Times | #5b9bc8 | #4891b3 | #b93611 | 0.278 |
| OCR | Orange County Register | #b04f0f | #ac4e0f | #0a5962 | 0.235 |
| TSPPP | St. Paul Pioneer Press | #004e87 | #557fba | #0065a8 | 0.08 |
| TDP | The Denver Post | #f7a430 | #daa520 | #7d161e | 0.393 |
| TOP | The Oakland Press | #0b151e | #0b151d | #3a527a | 0.252 |
| TT | The Trentonian | #004e87 | #357dad | #b93611 | 0.273 |

## DEC-03 · Defer to iOS when nothing else settles it

- **Rule:** after DEC-01 (migration sheet, iOS rounding) and DEC-02 (Cluster Audit when close), any brand color where the apps still differ takes the **iOS** value. Android gets the fix.
- **Also covers** the shared roles not checked by DEC-01/02: bar text, unselected tab, tab bar (the tab bar follows the bar color wherever both apps already do that) and the breaking-news red.
- **Applied by:** `scripts/apply_ios_default.py` (after `apply_web_alignment.py`). Each changed role keeps the earlier state under `previous`.
- **Result:** every one of the 77 markets now has a value for all 7 Core roles.

### Brand roles set to iOS (56)

| Code | Brand | Role | iOS (chosen) | Android (needs fix) |
|---|---|---|---|---|
| BS | Baltimore Sun | tabbar | #ffffff | #000000 |
| BS | Baltimore Sun | tabinactive | #000000 | #ffffff |
| TBAN | Bay Area News | navbar | #004e87 | #152c4f |
| TBAN | Bay Area News | action | #004e87 | #152c4f |
| TBAN | Bay Area News | tabactive | #000000 | #9fbfef |
| TBH | Boston Herald | tabactive | #9dd1f5 | #000000 |
| TBHS | Boston Herald Sports | navbar | #b01f36 | #c00030 |
| TBHS | Boston Herald Sports | action | #b01e35 | #c00030 |
| TBHS | Boston Herald Sports | tabactive | #004e87 | #000000 |
| TDB | Daily Breeze | navbar | #004e87 | #2e6c90 |
| TDB | Daily Breeze | action | #9dd1f5 | #2e6c90 |
| TDB | Daily Breeze | tabactive | #9dd1f5 | #6bd1e6 |
| TDF | Daily Freeman | navbar | #004e87 | #1b6bad |
| TDF | Daily Freeman | action | #9dd1f5 | #1b6bad |
| TDF | Daily Freeman | tabactive | #9dd1f5 | #000000 |
| TDLW | Daily Local Weschester | navbar | #1591b7 | #1591b5 |
| TDLW | Daily Local Weschester | action | #1591b7 | #1591b5 |
| DP | Daily Press | tabactive | #005f7e | #4fa8d1 |
| TDCD | Delaware County Daily Times | navbar | #5b9bc8 | #4891b3 |
| TDCD | Delaware County Daily Times | action | #5b9bc8 | #4891b3 |
| TIVDB | Inland Valley Daily Bulletin | tabactive | #000000 | #807c7c |
| TIVDB | Inland Valley Daily Bulletin | navtext | #cccccc | #ffffff |
| TIVDB | Inland Valley Daily Bulletin | tabinactive | #cccccc | #ffffff |
| TLBPT | Long Beach Press-Telegram | tabactive | #000000 | #97b8ed |
| MC | Morning Call | tabactive | #539cc4 | #4fa8d1 |
| OCR | Orange County Register | navbar | #b04f0f | #ac4e0f |
| OCR | Orange County Register | action | #b04f0f | #ac4e0f |
| OS | Orlando Sentinel | tabactive | #15919d | #00919e |
| OS | Orlando Sentinel | navtext | #333333 | #000000 |
| OS | Orlando Sentinel | tabinactive | #333333 | #000000 |
| PSN | Pasadena Star News | tabactive | #ff6900 | #000000 |
| TRDF | Redlands Daily Facts | tabactive | #9dd1f5 | #97b8ed |
| SGVT | San Gabriel Valley Tribune | action | #ff6900 | #b11e35 |
| SGVT | San Gabriel Valley Tribune | tabactive | #ff6900 | #daa520 |
| TSAR | Saratogian | action | #004e87 | #00919e |
| TSV | Silicon Valley | navbar | #000000 | #557fba |
| TSV | Silicon Valley | action | #004e87 | #557fba |
| TSV | Silicon Valley | tabactive | #004e87 | #6bd1e6 |
| TSPPP | St. Paul Pioneer Press | navbar | #004e87 | #557fba |
| TSPPP | St. Paul Pioneer Press | action | #004e87 | #557fba |
| TSPPP | St. Paul Pioneer Press | tabactive | #000000 | #6bd1e6 |
| TDP | The Denver Post | action | #f7a430 | #daa520 |
| TDP | The Denver Post | tabactive | #f7a430 | #daa520 |
| TDP | The Denver Post | tabinactive | #999999 | #ffffff |
| TEBT | The East Bay Times | action | #6bd1e6 | #557fba |
| TMN | The Mercury News | tabactive | #000000 | #6bd1e6 |
| TOP | The Oakland Press | navbar | #0b151e | #0b151d |
| TOP | The Oakland Press | action | #004e87 | #5ab1c3 |
| TOP | The Oakland Press | tabactive | #004e87 | #5ab1c3 |
| TPD | The Press Democrat | action | #000000 | #999999 |
| TPE | The Press-Enterprise | tabactive | #ff6900 | #000000 |
| TSBS | The San Bernardino Sun | tabactive | #ff6900 | #000000 |
| TT | The Trentonian | navbar | #004e87 | #357dad |
| TT | The Trentonian | action | #004e87 | #357dad |
| TT | The Trentonian | tabactive | #000000 | #0d0d0e |
| TWDN | Whittier Daily News | tabactive | #ff6900 | #040404 |

### Breaking-news red

All 77 markets differ (Android `#cf000e` everywhere). By DEC-03 the Core value is the iOS one: `#d80000` in 6, `#ff0000` in 71. **Flag:** `#ff0000` fails 4.5:1 with white text (4.0:1). **Superseded by DEC-05:** all 77 markets now use `#cf000e`.

## DEC-04 · Design tokens for Swift and Kotlin

- **Source of truth:** DTCG (W3C Design Tokens) JSON in `tokens/`: `tokens/core/brand.tokens.json` (`color.brand.<market>.<role>`, 7 Core roles + `buy`/`continue` aliases), `tokens/ios/` (iOS-only `header`), `tokens/android/` (Android-only `statusbar`). Generated from `data/brand-color-resolution.json` by `scripts/build_tokens.py`; never edited by hand.
- **Hex and RGB:** every token stores hex as `$value` and RGB (0–255) in `$extensions.mng.rgb`, plus how it was chosen and what each app ships today. `docs/BRAND-COLORS.md` lists every color as hex · R, G, B.
- **Build:** Style Dictionary 4.4.0 (`npm run tokens && npm run build`) writes:
  - iOS: `mng_apps_ios_ds/Tokens/MNGBrandColors.swift`: `MNGBrandPalette` (UIKit `UIColor`, SwiftUI via `color(\.navbar)`), `MNGBrandPalettes.<code>`, `forMarket("TDP")`.
  - Android: `mng_apps_android_ds/tokens/MngBrandColors.kt` (Jetpack Compose `Color`, `MngBrandPalettes.<CODE>`, `forMarket("tdp")`) and `tokens/flavors/<flavor>/res/values/mng_brand_colors.xml` (one per Gradle flavor, `@color/mng_brand_navbar` …).
- **Exact colors:** platform code is written from the hex bytes (`0xRRGGBB`), never from rounded decimals, which removes the cause of the iOS drift (DSC-01).
- **Kotlin package:** `com.mng.designsystem.tokens`, confirmed by Karl 2026-10-29. Generated code is not compiled in an app yet. Figma variables will be built from the same tokens (ARCHITECTURE §3).

## DEC-05 · One breaking-news red (`#cf000e`), WCAG AA

- **Rule:** every market on both apps uses `#cf000e` (rgb 207, 0, 14) for the breaking-news banner, with white `#ffffff` text. The build checks the pair and fails if it drops below WCAG AA for normal text (4.5:1).
- **Contrast:** white on `#cf000e` = **5.74:1** (AA pass; AAA needs 7:1). iOS today: white on `#ff0000` = 4.0:1 (fails AA) in 71 markets; `#d80000` = 5.36:1 in 6. Black text on `#cf000e` would be 3.66:1 (fails), so the text must be white.
- **New Core token:** `alerttext` (white) so the text color is defined, not left to each app.
- **Fix:** iOS, all 77 markets, **ASAP** because of contrast (DSC-15). iOS TIVDB also uses black banner text; change to white (DSC-19). Android already ships `#cf000e`; confirm its banner text is white.
- **Applied by:** `scripts/apply_core_alert.py` (after `apply_ios_default.py`). Replaces proposal PLAT-03 and covers CLR-01.

## DEC-06 · Figma variables: Brand colors + Brand theme (20 modes)

- **Why not modes per market:** the Figma plan allows 20 modes per collection. Splitting 78 markets across four collections breaks component binding (a layer bound to one collection can't switch to a market in another).
- **Brand colors** (Core file): one collection, one mode ("Value"), a folder per market: `TDP/navbar` … 78 markets × 8 roles = 624 variables. Names and code syntax match the tokens: iOS `MNGBrandPalettes.tdp.navbar`, Android `MngBrandPalettes.TDP.navbar`, Web `color.brand.tdp.navbar`. Each description has hex and RGB.
- **Brand theme** (Core file): 10 role variables (`navbar`, `navtext`, `tabbar`, `tabactive`, `tabinactive`, `action`, `alert`, `alerttext`, `buy`, `continue`) with 20 modes. Each mode aliases one market's Brand colors. Components bind to Brand theme; switching a frame's mode recolors the design. Markets without a mode use their Brand colors variables directly, or get swapped into a mode.
- **Picking the 20** (`scripts/select_theme_modes.py` → `data/figma-theme-modes.json`): Karl's required list (OCR, TDP, TCCDR, SS, MC, CT, TMN, TDH, TBH), then the most visually different market from each cluster not yet covered, then the most different overall. Skipped: BS, TB (decommissioned), TBCP, TROT (not using).

| Code | Market | Cluster | Why |
|---|---|---|---|
| OCR | Orange County Register | SCNG | required |
| TDP | The Denver Post | Denver | required |
| TCCDR | Canon City Daily Record | PMP - Weeklies | required |
| SS | Sun Sentinel | Tribune | required |
| MC | Morning Call | Tribune | required |
| CT | Chicago Tribune | Tribune | required |
| TMN | The Mercury News | BANG | required |
| TDH | Daily Herald | Tribune | required |
| TBH | Boston Herald | Boston | required |
| TOP | The Oakland Press | 21C / Mich | covers cluster 21C / Mich |
| TSAR | Saratogian | 21C / New York | covers cluster 21C / New York |
| TDCD | Delaware County Daily Times | 21C / Philly | covers cluster 21C / Philly |
| TTT | Times-Tribune | NEPA | covers cluster NEPA |
| TWDD | Woodland Daily Democrat | Norcal | covers cluster Norcal |
| TGT | Greeley Tribune | PMP | covers cluster PMP |
| TPD | The Press Democrat | Sonoma | covers cluster Sonoma |
| SGVT | San Gabriel Valley Tribune | SCNG | most different remaining |
| HC | Hartford Courant | Tribune | most different remaining |
| OS | Orlando Sentinel | Tribune | most different remaining |
| PAC | Petaluma Argus-Courier | Sonoma | most different remaining |

- **Duplicates skipped (Karl, 2026-10-21):** a cluster whose best pick would nearly duplicate a market already chosen (mean ΔE < 0.03) is skipped: 21C / Ohio (TNH ≈ OCR) and St. Paul (TSPPP = TMN). Their slots went to SGVT and OS. Brands with no cluster in either sheet (TBAN, TBE, TB, TBCP, TBHS, TCHW, TDPS) weren't treated as a cluster.
- **Daily Herald (TDH):** no app build yet, so it's added as a **provisional** market (`data/source/new-markets.json`): migration-sheet primary `#0072b4` plus standard-template defaults. White on `#0072b4` = 5.16:1 (AA); black selected tab on it = 4.07:1 (passes 3:1). Replace when the app ships.
- **Figma page:** Core file → **Color · Brand Theme** shows all 20 modes as mini app chrome bound to the theme variables.

## DEC-07 · Button pilot: Core component, shipped values kept

- **Colors:** keep the shipped colors: fill = Brand theme `action`, white label (`button.primary.label`). White fails 4.5:1 in 15 markets, and the iOS text link fails on white in 9. Both lists are **required changes** for the apps in `docs/IMPROVEMENTS.md` → CLR-04 (regenerated by the build).
- **Radius:** keep each app's shipped radius, as tokens: iOS `button.ios.primary.radius` 4 pt, or 5 pt + 1 pt border in the legacy-template markets (BS, DP, HC, MC, OS, SS, VP); Android `button.android.primary.radius` 0 (square). DSC-20 stays open.
- **Height:** keep each app's height, as tokens: iOS `button.ios.primary.height` 44 pt (**provisional**: not in the source), Android `button.android.primary.height` 60 dp. Future change: one height (IMPROVEMENTS BTN-01).
- **Label font:** the Button is a Core component, but the label stays per platform: iOS Open Sans Bold 14 uppercase, Android system font uppercase (Roboto Medium 14sp, **provisional**). Future change: one label style (IMPROVEMENTS BTN-02).
- **Android code** targets the View-based UI: XML resources and styles, not Compose.
- **Scope of the pilot:** Primary (enabled, pressed, disabled) and Text link. Disabled uses Android's shipped `#c1c8cb` / `#767676` on both apps (new on iOS). Secondary, in-button loading and folding Continue into Primary are later (CTRL-02, DSC-24).
- **Provisional values** (iOS height, Android label weight and size, iOS link font, pressed state) are asked for in `docs/MISSING-ASSETS.md` 5.5.
- **Applied by:** `scripts/build_button_tokens.py` (after `build_tokens.py`) → `tokens/{core,ios,android}/button.tokens.json`, `data/button-spec.json`, `docs/components/BUTTON.md`; then `npm run build` → `MNGButtonTokens.swift` (iOS repo) and `tokens/res/values/mng_button.xml` (Android repo).

## DEC-08 · iOS is the default for unconfirmed mismatches

- **Rule (Karl, 2026-10-26):** wherever iOS and Android ship different brand colors and no source confirms one of them (migration sheet, Cluster Audit within ΔE 0.05), use the **iOS** value. This includes close mismatches (off by 1 in a channel). DEC-03 is final; the Apps team is not asked to confirm it (MISSING-ASSETS 3.3 closed).
- **What changed:** the 4 roles DEC-01's drift rule had set to Android without sheet confirmation now take iOS (`scripts/resolve_brand_colors.py`, evidence `ios-close`). Tab bars that follow the bar color follow along.

| Code | Market | Role | Was (Android) | Now (iOS) |
|---|---|---|---|---|
| SGVT | San Gabriel Valley Tribune | navbar, tabbar | `#b11e35` · 177, 30, 53 | `#b01f36` · 176, 31, 54 |
| TDPS | Denver Post Sports | navbar, tabbar, action | `#c75d14` · 199, 93, 20 | `#c75c14` · 199, 92, 20 |
| TEBT | The East Bay Times | navbar, tabbar | `#557fba` · 85, 127, 186 | `#5480ba` · 84, 128, 186 |

- **Unchanged:** values the migration sheet confirms (DEC-01 steps 1–2 with the sheet), values moved to the web color (DEC-02), and the Core breaking-news red (DEC-05).
- **Applied in:** tokens, Swift, Kotlin, the 3 flavor XML files, docs/BRAND-COLORS.md and the Figma Brand colors variables.

## DEC-09 · Typography (and components) match production

- **Rule (Karl, 2026-10-30):** what we build in Figma, and so what Claude builds from, must match what is in production. If that means rebuilding something exactly as it ships (for example a kicker label or a section-front cell), we rebuild it. Where there is no spacing, size or other token for a value yet, use the raw production value.
- **Fonts stay per platform, permanently** (Karl, 2026-10-30): iOS Spectral, Android PT Serif for headlines and article text, and each app's other fonts. Not a future change (TYPE-03 rejected).
- **Sizes:** each app keeps its shipped sizes (pt / sp) for now. One shared type scale is a future change (TYPE-04).
- **All styles:** all 63 iOS and 26 Android styles become tokens, code and Figma text styles, including the 56 that only one app has.
- **iOS legacy template** (BS, DP, HC, MC, OS, SS, VP): **superseded by DEC-10**: documented only, not built.
- **Naming:** Core owns the role names (`Article/Headline`, `Section front/Blurb` …). The same name exists in the iOS and Android files wherever both apps have the role, so mockups can swap libraries.
- **Not yet covered:** per-market font exceptions (e.g. NYDN, VP on iOS; the Open Sans group DP, SIT, TOD, TTT, VP on Android). They are kept as notes on each token (backlog item foundation/type-markets) and should be removed in the future (IMPROVEMENTS TYPE-05).
- **Applied by:** `scripts/build_type_tokens.py` → `tokens/ios/type.tokens.json`, `tokens/android/type.tokens.json`, `data/type-styles.json`, `docs/TYPE-STYLES.md`; `npm run build` → `MNGTypeStyles.swift` (iOS repo), `MngTypeStyles.kt` (Android repo).

## DEC-10 · iOS legacy template: acknowledged, not built

- **Rule (Karl, 2026-11-03):** the 7 iOS markets on TroncKit's older theme template (BS, DP, HC, MC, OS, SS, VP) are recorded in the design system, but nothing is built for them: no Figma styles, variants or variables, no tokens, no code. The template should go away (IMPROVEMENTS TYPE-01).
- **Where the values live:** `docs/LEGACY-TEMPLATE.md` (generated by `scripts/build_legacy_doc.py` from `data/legacy-template-type.json` and `data/source/button-shipped.json`): 19 text styles with different values, 7 legacy-only styles, and the button's radius 5 + 1 pt border.
- **Removed:** iOS type tokens and Swift `legacySpec` / `font(legacyTemplate:)`; button tokens `radius-legacy` / `border-legacy` and Swift `cornerRadius(forMarket:)` / `borderWidth(forMarket:)`; `MNGButton.swift` legacy border. Figma: iOS `Button/Primary` Template=Legacy variants and the legacy radius/border variables (pending: Figma files were not connected on 2026-11-03).
- **Replaces** the legacy parts of DEC-07 and DEC-09.

## DEC-11 · Layout spacing and touch targets

- **Signed off by Karl, 2026-11-10.**

- **Comparison:** `docs/SCALES-COMPARISON.md` (`scripts/compare_scales.py`): 34 roles; 4 the same on both apps, 1 close, 5 differ, 10 iOS only, 14 Android only. Neither app has a shared spacing scale in code.
- **Core tokens** (same on both apps): `space.cell.margin` 16, `space.cell.gap` 8, `space.article.side` 16, `grid.columns` 12. Figma Core collection **Spacing**.
- **Platform tokens:** iOS `space.ios.article.top` 20 / `top-tablet` 40, `size.ios.touch-min` 44 (collection **Spacing · iOS**); Android `space.android.article.side-landscape` 30 / `side-tablet` 75, `size.android.touch-min` 48 (collection **Spacing · Android**).
- **Not tokens:** radii and sizes that belong to one component (Continue 9, savings label 15, player controls 20, overlay close 40 …). Per DEC-09 they are used as raw production values when that component is built; they stay listed in the comparison.
- **Breakpoints:** not built yet. iOS has two disagreeing sets (LAY-01) and Android picks width classes by physical inches.
- **Code:** `MNGScaleTokens.swift` (`MNGScale`, iOS repo), `tokens/res/values/mng_scale.xml` (Android repo). Applied by `scripts/build_scale_tokens.py`.

## DEC-12 · Everything linked to tokens

- **Rule (Karl, 2026-11-03):** build breakpoints and tokens for each design system and its components, so that everything is linked to tokens. Replaces the "component values stay raw" part of DEC-11.
- **Breakpoints, as shipped** (`breakpoint.ios.*`, `breakpoint.android.*`; Figma collections **Breakpoints · iOS** / **Breakpoints · Android**): iOS front 668 / 835 / 1113 pt and item 769 / 1025 pt (both sets kept until LAY-01 is decided); Android width classes 4.1 / 6.1 / 7.8 / 10.4 inches (physical screen) and sw500dp / sw600dp.
- **Component metrics** (`component.ios.*`, `component.android.*`; Figma **Components · iOS** / **Components · Android**): every component-specific radius, size and inset from the style guides, e.g. Continue radius 9, savings label 15, checkbox 30, tab icons 26 × 23 / 24.
- **Core Button** now has an **iOS** and an **Android** mode in the Button collection (height 44 / 60, radius 4 / 0, label Open Sans Bold / Roboto Medium 14, tracking 0 / 1.25 px); every property of the component is bound. The invented 16 px side padding was removed (no production value).
- **Text links** in both platform files are bound to the platform touch target; code uses `MNGScale.sizeTouchMin` / `@dimen/mng_size_touch_min`.
- **Not tokens:** the iOS legacy template (DEC-10).

## DEC-13 · App shell (top bar, section tabs, bottom tab bar, banner, header band, status bar)

"App shell" is this project's name for what the registry and older docs call "App chrome" (Karl, 2026-11-03).

- **Sizes:** the style guides say bar heights, paddings and fonts in their previews are illustrative, so production sizes are not in the exports. Karl: **wait for the Apps team** (MISSING-ASSETS 5.6) before building the app shell components. Known already: top bar title (iOS Open Sans Bold 16), tab labels (iOS Open Sans Bold 10, Android Roboto 10), Android section tabs (Open Sans SemiBold 12), tab icon sizes (DEC-12).
- **Colors: each platform's production values** (exceptions superseded by DEC-14: majority values only) (`scripts/build_shell_colors.py` → `tokens/*/shell.tokens.json`, `data/shell-colors.json`):
  - **Core `navicon`** (top bar icon tint) = alias of `navtext`: both apps ship them equal in all 77 markets.
  - **iOS section bar** (`sectiontabbar`, `sectiontabtext`, `sectiontabselected`, `sectiontabindicator`): white bar, #333333 text and underline in 74 markets; BS, DP, NYDN use #2c2d2d / #000000. Figma iOS file: **Shell colors · iOS** (per market) + **Shell theme · iOS** (20 modes).
  - **Android section tabs and tab labels** (`sectiontab*`, `tablabelactive`, `tablabelinactive`): Android ships the section tabs in the top-bar colors and the tab labels in the tab-icon colors, so these roles **follow the Core roles** (navbar, navtext, tabactive, tabinactive) and inherit every Core color decision. Where production breaks that pattern the shipped value is kept: CT section tabs (white bar, #2c2d2d text, #004e87 selected); tab labels in DP, MC, NYDN, OS, TSAR. Figma Android file: **Shell colors · Android** (aliases of the Core library's Brand colors) + **Shell theme · Android** (20 modes).
  - Already Core: top bar navbar/navtext, tab bar tabbar/tabactive/tabinactive, banner alert/alerttext, iOS header band `header`, Android `statusbar` (both aliases of navbar since DEC-15).
- **Icons:** swappable icon slots, sized with the icon tokens, until the icon set exists (MISSING-ASSETS §1).


## DEC-14 · Remaining buttons and controls: majority values, native look

- **Majority rule (Karl, 2026-11-03):** build each color for the majority of markets and only note the markets that are exceptions. **Exceptions are not built.** Listed in `docs/CONTROL-EXCEPTIONS.md` (`scripts/build_control_tokens.py` → `tokens/*/controls.tokens.json`, `data/control-colors.json`).
- **Tints follow Core `action`** in most markets, so they need no new per-market tokens: iOS subscription option 74/77, notification Yes 74, settings switch 77, alert switch 77, offline switch 71, slider thumb 75, enable notifications 68; Android Buy 74/77, Continue 70, alerts enable 58, `MainStyle_Accent` 52 (closes PLAT-10 for the majority).
- **Fixed colors become platform tokens** (hex · RGB): iOS unselected option #f1f1f1 · 241, 241, 241; labels #ffffff · 255, 255, 255; notification No #333333 · 51, 51, 51; slider track and ticks #999999 · 153, 153, 153; system switch off-track #e9e9ea · 233, 233, 234 and thumb #ffffff. Android switch off thumb #e5e5e5 · 229, 229, 229 and track #b9b9b9 · 185, 185, 185; unchecked checkbox #757575 · 117, 117, 117; savings label text #004e87 · 0, 78, 135.
- **Built now (fully specified):** Subscription option (Core component, iOS/Android modes in the **Subscription option** collection: radius 8/0, inset 16/14, Open Sans Bold 16 / Roboto 16 with a bold first line); Android Switch and Checkbox (Components · Controls); iOS Switch and Text size slider (pending in Figma, tokens done).
- **Native controls** are drawn to the system look and tinted by tokens (Karl), not redesigned.
- **Asked of the Apps team (MISSING-ASSETS 5.7):** fonts and heights for the notification prompt, account buttons, savings label, social sign-in, Android alerts enable and What's New buttons; colors of the segmented control and loading indicator.
- **Continue button (Karl, 2026-11-04): as shipped on each platform.** iOS: image button 159 x 55 pt (`component.ios.continue.*`), drawn in Figma as the image (action fill, chevron slot). Android: 152 x 54 dp, radius 9 (`component.android.continue.*`), Open Sans SemiBold 15 (`continue-label`), fill = action. Not a Core component. Future: IMPROVEMENTS BTN-03.
- **Code:** `MNGControlTokens.swift` (iOS repo), `tokens/res/values/mng_controls.xml` (Android repo).
- **App shell too (Karl, 2026-11-04):** the DEC-13 exceptions are no longer built. iOS section bar uses the majority values in every market; Android section tabs and tab labels follow the Core roles in every market. The 14 shipped exceptions (iOS BS, DP, NYDN; Android CT, DP, NYDN, TSAR) are in `docs/SHELL-EXCEPTIONS.md`. Future: IMPROVEMENTS CLR-08.


## DEC-15 · Header band (iOS) and status bar (Android) follow the top bar

- **Rule (Karl, 2026-11-05):** iOS `header` (section-front header band) and Android `statusbar` are **aliases of Core `navbar`** in every market (DEC-14 majority rule). Closes PLAT-05.
- **Why:** each app ships them equal to its own top bar in most markets: iOS header = nav bar in 69 of 77 (66 exact + TCHW, SIT, TEBT near-identical), Android status bar = top bar in 70 of 77. The tokens used to hold the raw shipped hex, which no longer matched the decided Core `navbar` in 54 iOS and 47 Android markets.
- **Exceptions (documented, not built):** markets whose app ships them different from its own top bar, mostly white-top-bar markets. iOS: DP, MC, NYDN, OS, SS, TSAR, TPD, VP. Android: DP, MC, NYDN, OS, SS, TSAR, VP. Each has a **suggested override** (the shipped color, which passes contrast) in `docs/SHELL-EXCEPTIONS.md`, and is drawn majority vs override side by side in Figma (iOS: Components · App shell › 01 · Header band exceptions; Android: › 01 · Status bar exceptions) so they read as open items, not just notes. On the majority build, 14 of the 15 fail contrast (white header text or light status-bar icons on a white bar). Future: IMPROVEMENTS CLR-08.
- **Changed:** `scripts/build_tokens.py` (alias tokens, shipped value kept in `$extensions.mng.shipped`), `scripts/build_shell_colors.py` (exceptions, `data/shell-colors.json` `role_exceptions`), Style Dictionary: `MNGBrandPalette.header` is now `navbar` (mng_apps_ios_ds), `MngBrandPalette.statusbar` and `@color/mng_brand_statusbar` → `navbar` (mng_apps_android_ds). Figma Android: `<M>/statusbar` (78, aliases of Core `<M>/navbar`) in Shell colors · Android and `statusbar` in Shell theme · Android. Figma iOS: `<M>/header` (78, aliases of Core `<M>/navbar`) in Shell colors · iOS and `header` in Shell theme · iOS (2026-11-05, once the iOS file was in front).
- **Overrides accepted (Karl, 2026-11-05: "accept everything"):** all 15 markets keep the color their app ships, as market override tokens (`data/shell-overrides.json` → `color.ios.<m>.header` / `color.android.<m>.statusbar` hex instead of the navbar alias). iOS header: DP #4050b6, MC #5c5b59, NYDN #4050b6, OS #1875be, SS #136283, TPD #9e0b0f, TSAR #5d5b59, VP #3f50b6. Android status bar: DP, MC, OS, SS, TSAR, VP #000000; NYDN #333333. Code: `MNGBrandPalette.headerOverride` (nil = navbar) in mng_apps_ios_ds; `MngBrandPalette.statusbarOverride` and the flavor XML in mng_apps_android_ds. Figma: those variables hold the hex; the samples show the majority (Core navbar) next to the accepted override, both live. Every other market still follows navbar, so a future navbar change does not reach these 15.
- **Android status-bar icons (Apps team, Ameer M., 2026-11-05 from code; confirmed on device 2026-11-10):** Android 14 and below: white icons (the main theme never sets `windowLightStatusBar`), so the accepted black/#333333 overrides are what those phones show. Android 15+: white status bar with dark icons in these 7 markets, i.e. the majority (navbar). The tokens describe Android 14 and below for now. **Karl (2026-11-06): build both versions once the Apps team confirms on a device**: keep the dark overrides for Android 14 and below, add a per-market status-bar icon style (light/dark) so Android 15+ uses navbar with dark icons, and add an Android 15+ mock-up to the samples. **Device check done (2026-11-10). Built 2026-11-10:** data/shell-overrides.json `statusbar_icons` → tokens `statusbar.android.<m>.icons` (Android 14 and below: light in all markets) and `icons15` (Android 15+: dark in DP, MC, NYDN, OS, SS, TSAR, VP; light elsewhere, inferred, MISSING-ASSETS 5.6). On Android 15+ the status bar color is navbar in every market. Code (mng_apps_android_ds): `MngBrandPalette.statusbar15`, `statusbarFor(sdkInt)`, `statusbarDarkIconsFor(sdkInt)`; flavor XML `@bool/mng_brand_statusbar_dark_icons` plus `res/values-v35/mng_brand_statusbar.xml` in the 7 markets (Android picks it on API 35+). Figma Android: Components · App shell › 01 now compares Android 14 and below (override variable, white icons) with Android 15+ (Core navbar, dark icons); builder `scripts/figma_role_exceptions.py` + `scripts/figma/build_role_exceptions.js`.


## DEC-16 · System colors: majority tokens, every market documented

- **Rule (Karl, 2026-11-10):** system colors follow the DEC-14 majority rule. One set of tokens holds the majority values: Core where iOS and Android match (the 16 proposed pairs), per-platform otherwise; colors that follow a brand role are aliases of it. **Every market's palette is documented** (majority palette + that market's differences, grouped into palettes I01–I19 / A01–A29) in data, `docs/SYSTEM-COLORS.md` and Figma, but **not built as tokens**. An exception becomes a token only if Karl accepts it as a market override (as in DEC-15). Palette-group tokens were considered and dropped: apart from the majority group, almost every group is a single market.
- **Scale of the exceptions (data/system-color-comparison.json):** iOS 223 market/color exceptions in 36 of 96 system colors (3%), 59 of 77 markets have none, 71% come from the 7 legacy-template markets (BS, DP, HC, MC, OS, SS, VP). Android 228 in 40 of 114 colors (3%), 43 markets have none, 63% from NYDN, TSAR, CT, DP, OS, MC, SS, VP.
- **Android launcher icon background** (`ic_launcher_background`, 23 values) is a **market brand asset**, not a system color: documented per market in `docs/BRAND-COLORS.md`, no token.
- **Pairs (Karl, 2026-11-10):** 11 approved iOS/Android pairs become Core tokens (5 same value, 6 with a value per platform: the 4 settings colors and the sections menu name and divider, the last two logged as DSC-32/33). The alert topic rows (×4) and the offline header are different designs on the two apps: platform-only. MISSING-ASSETS 3.4 closed.
- **Built (step 2):** `scripts/build_system_tokens.py` → `tokens/core/system.tokens.json` (11), `tokens/ios/system.tokens.json` (77 + 8 that follow a brand role), `tokens/android/system.tokens.json` (84 + 19 that follow), `docs/SYSTEM-TOKENS.md`. Brand-following colors are not tokens of their own: the code reads the market palette (Android `accent` is built as `action`, DEC-14). iOS colors the app leaves unset use the UIKit default (`UIColor.separator`, `.systemGreen`). Code: `MNGSystemColors.swift` (mng_apps_ios_ds); `MngSystemColors.kt` and `res/values/mng_system_colors.xml` (mng_apps_android_ds). Figma: Core **System colors** collection (iOS/Android modes), **System colors · iOS** / **· Android** in the platform files (scripts/figma/build_system_variables.js).


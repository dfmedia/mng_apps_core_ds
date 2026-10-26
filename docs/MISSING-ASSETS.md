# Missing Assets — Request List for the Apps Team

**Apps team contacts:** Jess Navaro, Patrick Carr

Things the MNG Apps Core Design System needs but that do not exist in the iOS source (TroncKit @ `e30ad2585`) or exist only in a form we can't build from. Ordered by priority.

Status key: `OPEN` · `REQUESTED` · `RECEIVED` · `NOT NEEDED`

---

## 1. Icons — `OPEN` (highest priority)

The iOS app has no vector icon masters. Everything below is needed before the Icons page can be finished.

| # | Ask | Detail | Status |
|---|-----|--------|--------|
| 1.1 | **Vector source files (SVG or PDF) for the TroncKit image assets** | 213 of 218 images are PNG exports (4 are SVG, 1 JPG). We need the master vectors, or confirmation that none exist so we redraw / replace them. Priority groups: Navigation Bar (11), Tab Bar (19), General (20), PostKit player controls (42). | OPEN |
| 1.2 | **`ManageSubscriptionIcon`** | The image set exists in the asset catalog but has **no image file**. What should it show? | OPEN |
| 1.3 | **The `"saved"` SF Symbol** | `CoreTabBarViewController.swift:140` references `"saved"`, which is not a real SF Symbol, so nothing renders. Which icon was intended? | OPEN |
| 1.4 | **Market tab-bar overrides** | 9 markets ship their own Home tab icon and 2 override the Font Awesome tab icons. Need the list of which markets/which icons and the vector files. | OPEN |
| 1.5 | **Icons with no clear source** | Text size small/large, Games tab, ±15 s skip (currently SF `gobackward.15` / `goforward.15`), the six tournament sport symbols, Your News tab, Filter (`icon_filter`), Follow / Unfollow topic. Need the intended design or approval to use platform-native symbols. | OPEN |
| 1.6 | **Per-market icon variants — confirm intent** | `Saved-*`, `Checkmark-*`, `Uncheck-*`, `YourNews-*`, `Continue-*`, `TopicSelection-*` are the same glyph recolored per market. Confirm they can become one tinted icon (see IMPROVEMENTS.md → ICON-01). | OPEN |
| 1.7 | **Android icon set** | Nothing extracted for Android yet. | OPEN |
| 1.8 | **For You / Your News tab icon** | No equivalent in SF Symbols, Material Symbols or Font Awesome. Need the master vector or a new design. | OPEN |
| 1.9 | **`tab-digital` purpose** | What does the Digital tab open? Needed to pick or draw its icon. | OPEN |
| 1.10 | **Tournament sport symbols** | Names of the six SF Symbols used in tournament loading. | OPEN |
| 1.11 | **15 s skip on Android** | Material Symbols only has 5/10/30 s skip. Confirm 15 s is required on Android (custom vector) or switch to 10/30 s. | OPEN |
| 1.12 | **Brand marks** | Official, current vectors for Apple, Google, Facebook, X, Bluesky, Instagram, YouTube, Vimeo, Amazon, 1Password, Outbrain (none of the platform icon sets include them; Font Awesome 5 still has the old Twitter bird and no X/Bluesky). | OPEN |

## 2. Brand / logo assets — `OPEN`

| # | Ask | Detail | Status |
|---|-----|--------|--------|
| 2.1 | Per-market app catalog logos | App icon, `Main logo`, `Lettermark`, paywall meter logo, masthead — 3–19 files per app × 77 apps. Vector masters preferred. | OPEN |
| 2.2 | Onboarding artwork | 19 Onboarding images exist only for legacy markets (BS, CT, DP, HC, MC, NYDN, OS, SS, VP) plus `mng-top-image-view`. Confirm what the other markets show. | OPEN |

## 3. Color — `OPEN`

| # | Ask | Detail | Status |
|---|-----|--------|--------|
| 3.1 | "Not set" theme colors | Some of the 124 themed colors are `null` in some markets (UIKit falls back to its system default). Confirm whether system default is intended or a value is missing. | OPEN |
| 3.2 | Dark mode | Every app is light-only. Confirm there are no plans/specs for dark mode before we decide the variable mode structure. | OPEN |
| 3.3 | Confirm the iOS-default brand colors | DEC-03 set every remaining difference to the iOS value (list in docs/DECISIONS.md → DEC-03). Ask the Apps team only to confirm, especially TDP (iOS `#f7a430` vs Android `#daa520`), TPD (sheet says `#9e0b0f`, both apps black), SGVT and the SCNG selected tabs (iOS orange `#ff6900`), and the breaking-news red (PLAT-03). | CLOSED 2026-10-26: Karl confirmed iOS as the default (DEC-08); not asking the Apps team |

## 4. Typography — `OPEN`

| # | Ask | Detail | Status |
|---|-----|--------|--------|
| 4.1 | Open Sans Condensed source/licence | Used only by NYDN. Confirm the bundled files and whether Figma's Google Fonts version matches. | OPEN |
| 4.3 | Open Sans Light & ExtraBold in Figma | Figma's Open Sans only offers Regular, Italic, SemiBold, Bold (+ italics). iOS bundles Light, LightItalic, ExtraBold, ExtraBoldItalic too. Need the app's font files installed locally (or confirm which styles are actually used) so text styles render correctly. | OPEN |
| 4.2 | Dynamic Type mapping | Article text has 6 sizes (15% steps) or follows iOS text size; other screens are fixed. Need the intended scale if we want it as tokens. | OPEN |

## 5. Components & states — `OPEN`

| # | Ask | Detail | Status |
|---|-----|--------|--------|
| 5.1 | Missing button states | No Secondary, Text, Disabled (except tracking-consent Continue) or Loading variants exist. Confirm whether these should be designed new. | OPEN |
| 5.2 | Elevation / shadow values | None extracted from code. | OPEN |
| 5.3 | Motion / animation specs | None extracted. | OPEN |
| 5.5 | Button values not in the source | iOS primary button height (pilot uses 44 pt); Android button label weight and size (pilot uses Roboto Medium 14sp, the Material default); iOS paywall Log In link font (pilot uses Open Sans Regular 14); pressed state on both apps. | OPEN |
| 5.4 | Current screenshots | Reference screenshots of key screens for a handful of markets (nav, section front, article, paywall, settings) to check the build against. | OPEN |

## 6. Platform — `OPEN`

| # | Ask | Detail | Status |
|---|-----|--------|--------|
| 6.1 | **Android source** | Tokens, components and assets for Android. Needed before the Android file. | OPEN |
| 6.2 | Source commit | Confirm `e30ad2585` is still current for iOS, or provide the newer ref. | OPEN |

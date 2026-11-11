# Missing Assets — Request List for the Apps Team

**Apps team contacts:** Jess Navaro, Patrick Carr

Things the MNG Apps Core Design System needs but that do not exist in the iOS source (TroncKit @ `e30ad2585`) or exist only in a form we can't build from. Ordered by priority.

Status key: `OPEN` · `REQUESTED` · `RECEIVED` · `NOT NEEDED`

**Combined message to the Apps team, sent 2026-11-11 (#pd-mobile-public, Jess Navaro, Patrick Carr, Ameer M.).** Each question carried its ID in brackets, so answers may come by message number or by ID. Message number → ID: 1 → 5.6 sizes · 2 → 5.6 TSAR production · 3 → 5.5 · 4 → 5.7 · 5 → 5.8 · 6 → 4.4 · 7 → 4.5 · 8 → 3.5 · 9 → 1.1, 1.7 · 10 → 1.2 · 11 → 1.3 · 12 → 1.4 · 13 → 1.5 · 14 → 1.6 · 15 → 1.8 · 16 → 1.9 · 17 → 1.10 · 18 → 1.11 · 19 → 1.12 · 20 → 5.9 · 21 → 5.10 · 22 → 2.1, 2.2 · 23 → 3.1 · 24 → 3.2 · 25 → 4.1, 4.2, 4.3 · 26 → 5.2, 5.3 · 27 → 5.4 · 28 → 6.2. When an answer arrives: set the row to RECEIVED with the date and who answered, put any values in data/source/, re-run the scripts, and unblock the item in data/backlog-status.json.

---

## 1. Icons — `OPEN` (highest priority)

The iOS app has no vector icon masters. Everything below is needed before the Icons page can be finished.

| # | Ask | Detail | Status |
|---|-----|--------|--------|
| 1.1 | **Vector source files (SVG or PDF) for the TroncKit image assets** | 213 of 218 images are PNG exports (4 are SVG, 1 JPG). We need the master vectors, or confirmation that none exist so we redraw / replace them. Priority groups: Navigation Bar (11), Tab Bar (19), General (20), PostKit player controls (42). | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 1.2 | **`ManageSubscriptionIcon`** | The image set exists in the asset catalog but has **no image file**. What should it show? | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 1.3 | **The `"saved"` SF Symbol** | `CoreTabBarViewController.swift:140` references `"saved"`, which is not a real SF Symbol, so nothing renders. Which icon was intended? | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 1.4 | **Market tab-bar overrides** | 9 markets ship their own Home tab icon and 2 override the Font Awesome tab icons. Need the list of which markets/which icons and the vector files. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 1.5 | **Icons with no clear source** | Text size small/large, Games tab, ±15 s skip (currently SF `gobackward.15` / `goforward.15`), the six tournament sport symbols, Your News tab, Filter (`icon_filter`), Follow / Unfollow topic. Need the intended design or approval to use platform-native symbols. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 1.6 | **Per-market icon variants — confirm intent** | `Saved-*`, `Checkmark-*`, `Uncheck-*`, `YourNews-*`, `Continue-*`, `TopicSelection-*` are the same glyph recolored per market. Confirm they can become one tinted icon (see IMPROVEMENTS.md → ICON-01). | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 1.7 | **Android icon set** | Found 2026-11-10: the Android style guide (artifact 5MyLP13QSt52WGRgXW35ZJ) carries 138 shipped assets: 126 PNG (xxxhdpi) and 12 SVG converted from vector drawables (persistent player, author contact, search clear, game arrow…), incl. the 77 market Home tab icons. Exports, not masters: vector masters for the PNGs are still needed (see 1.1). | PARTLY ANSWERED; masters ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 1.8 | **For You / Your News tab icon** | No equivalent in SF Symbols, Material Symbols or Font Awesome. Need the master vector or a new design. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 1.9 | **`tab-digital` purpose** | What does the Digital tab open? Needed to pick or draw its icon. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 1.10 | **Tournament sport symbols** | Names of the six SF Symbols used in tournament loading. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 1.11 | **15 s skip on Android** | Material Symbols only has 5/10/30 s skip. Confirm 15 s is required on Android (custom vector) or switch to 10/30 s. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 1.12 | **Brand marks** | Official, current vectors for Apple, Google, Facebook, X, Bluesky, Instagram, YouTube, Vimeo, Amazon, 1Password, Outbrain (none of the platform icon sets include them; Font Awesome 5 still has the old Twitter bird and no X/Bluesky). | ASKED 2026-11-11 (#pd-mobile-public, combined message) |

## 2. Brand / logo assets — `OPEN`

| # | Ask | Detail | Status |
|---|-----|--------|--------|
| 2.1 | Per-market app catalog logos | App icon, `Main logo`, `Lettermark`, paywall meter logo, masthead — 3–19 files per app × 77 apps. Vector masters preferred. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 2.2 | Onboarding artwork | 19 Onboarding images exist only for legacy markets (BS, CT, DP, HC, MC, NYDN, OS, SS, VP) plus `mng-top-image-view`. Confirm what the other markets show. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |

## 3. Color — `OPEN`

| # | Ask | Detail | Status |
|---|-----|--------|--------|
| 3.1 | "Not set" theme colors | Some of the 124 themed colors are `null` in some markets (UIKit falls back to its system default). Confirm whether system default is intended or a value is missing. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 3.4 | Confirm the iOS ↔ Android system-color pairs | Closed without asking (Karl, 2026-11-10): 11 pairs approved; the alert topic rows (×4) and the offline header are treated as different designs, platform-only (data/system-color-pairs.json `not_pairs`). | CLOSED |
| 3.5 | Android settings colors | The Android export has `Settings_Background` `#333333` (70 of 77 markets) with `Settings_Item`, `Settings_Category_Item` and `Settings_Summary_Item` `#000000` (black text on dark gray, 1.7:1). Where is `Settings_Background` used? Is it the settings list background? Screenshot from the Apps team's Android style guide, Market palette card (Denver Post). Asked 2026-11-10. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 3.2 | Dark mode | Every app is light-only. Confirm there are no plans/specs for dark mode before we decide the variable mode structure. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 3.3 | Confirm the iOS-default brand colors | DEC-03 set every remaining difference to the iOS value (list in docs/DECISIONS.md → DEC-03). Ask the Apps team only to confirm, especially TDP (iOS `#f7a430` vs Android `#daa520`), TPD (sheet says `#9e0b0f`, both apps black), SGVT and the SCNG selected tabs (iOS orange `#ff6900`), and the breaking-news red (PLAT-03). | CLOSED 2026-10-26: Karl confirmed iOS as the default (DEC-08); not asking the Apps team |

## 4. Typography — `OPEN`

| # | Ask | Detail | Status |
|---|-----|--------|--------|
| 4.1 | Open Sans Condensed source/licence | Used only by NYDN. Confirm the bundled files and whether Figma's Google Fonts version matches. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 4.4 | Type styles missing from the exports | iOS: section tabs, settings rows and headers, search result headline. Android: top bar title, article subhead font (style `ArticleText.Subhead.Wapo`, size 14sp known; asked 2026-10-30). Found in the type comparison (docs/TYPE-COMPARISON.md). | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 4.3 | Open Sans Light & ExtraBold in Figma | Figma's Open Sans only offers Regular, Italic, SemiBold, Bold (+ italics). iOS bundles Light, LightItalic, ExtraBold, ExtraBoldItalic too. Need the app's font files installed locally (or confirm which styles are actually used) so text styles render correctly. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 4.2 | Dynamic Type mapping | Article text has 6 sizes (15% steps) or follows iOS text size; other screens are fixed. Need the intended scale if we want it as tokens. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 4.5 | Two Android font file names that may not load | Found 2026-11-10 (docs/TYPE-FONT-EXCEPTIONS.md): NYDN `StreamModule_Font_Time_And_Blurb` points to `OpenSansCondensed-Bold.ttff` (double f); MC `Article_Byline_Regular` and `Article_Dateline_Regular` point to `OpenSans-Semibold.ttf` (lowercase b; the bundled file is `OpenSans-SemiBold.ttf`). Do these load on device, or do they fall back to the system font? Documented as shipped. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |

## 5. Components & states — `OPEN`

| # | Ask | Detail | Status |
|---|-----|--------|--------|
| 5.1 | Missing button states | No Secondary, Text, Disabled (except tracking-consent Continue) or Loading variants exist. Confirm whether these should be designed new. | CLOSED 2026-11-10 (Karl: not designed; CTRL-02 not pursued) |
| 5.2 | Elevation / shadow values | None extracted from code. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 5.3 | Motion / animation specs | None extracted. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 5.5 | Button values not in the source | iOS primary button height (pilot uses 44 pt); Android button label weight and size (pilot uses Roboto Medium 14sp, the Material default); iOS paywall Log In link font (pilot uses Open Sans Regular 14); pressed state on both apps. | ASKED 2026-11-05 (#pd-mobile-public, thread with Jess), again 2026-11-11 (combined message) |
| 5.6 | App shell sizes | Production heights, paddings and title/label sizes for the top bar, section tabs, bottom tab bar, breaking-news banner and (iOS) section header band, on both apps. The style guides only have illustrative values. Blocks the app shell components (DEC-13). Also: does Android set `windowLightStatusBar` (dark status-bar icons) anywhere, e.g. in the white-top-bar markets DP, MC, NYDN, OS, SS, TSAR, VP? Not in the export; the DEC-15 samples assume light icons. Answered by Ameer M. (Apps team, 2026-11-05, from reading the code) and **confirmed on device (Ameer M., 2026-11-10)**: the main theme never sets `windowLightStatusBar` (only splash and onboarding do), so on **Android 14 and below** the icons are white and the black status bar is needed. On **Android 15+** the app shows a white status bar with dark icons in these markets (i.e. it matches the top bar). **Follow-up answered (Ameer M., 2026-11-10):** not a per-market setting. On Android 15+ `EdgeToEdgeUtil.java:30` reads `NavigationBar_Background` (the color behind the status bar); exactly `#FFFFFF` → dark icons, any other color → white icons (checked on the Android 16 emulator with Denver Post: white icons on a black bar). So DP, MC, NYDN, OS, SS, VP get dark icons and every other market white, including **TSAR** (`#F5F5F5`, white icons at 1.09:1). **Karl (2026-11-10):** TSAR should show a white status bar with dark icons on Android 15+; built that way, assuming production has the correction. **Still to confirm with Ameer:** what Saratogian shows in production on Android 15+. | ASKED 2026-11-11 (#pd-mobile-public, combined message) (sizes; TSAR production check); status-bar icons answered 2026-11-10 |
| 5.7 | Remaining buttons and controls | Font, size and height for: iOS notification prompt Yes/No, Manage subscription / delete account buttons, savings label, social sign-in buttons (Apple, Google, Facebook), Android alerts Enable and What's New buttons. Colors for the segmented control and the loading indicator on both apps. Colors are otherwise done (DEC-14). | ASKED 2026-11-05 (#pd-mobile-public, thread with Jess), again 2026-11-11 (combined message) |
| 5.8 | iOS checkbox image placement | The Your News checkbox control is 30 × 30 pt; its images are 17 × 18 pt (51 × 54 px @3x). How are they placed (centered at natural size, or scaled)? And which markets use `Uncheck-Grey`? Drawn centered at natural size for now (docs/components/CHECKBOX-IOS.md). | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 5.9 | iOS ad slot sizes | Android sizes are in its guide (320 × 50 phone / 728 × 90 tablet first slot and sticky footer, 300 × 250 others; docs/GUIDE-EXTRAS.md). The iOS guide has no ad sizes, only the offline placeholder image `ad-bigbox-offline-250.jpg` and the adhesion banner background. What sizes does iOS request for each slot, and does the adhesion banner match the Android sticky footer? Found 2026-11-10. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 5.10 | Android home-screen widget | `values-night` changes only the widget colors, but the night values are not in the Android guide. Need the night values of `widget_bg`, `widget_divider1`, `widget_divider2`, `widget_text_main`, and the widget layout and sizes. Day colors are tokens already (docs/GUIDE-EXTRAS.md). Found 2026-11-10. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |
| 5.4 | Current screenshots | Reference screenshots of key screens for a handful of markets (nav, section front, article, paywall, settings) to check the build against. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |

## 6. Platform — `OPEN`

| # | Ask | Detail | Status |
|---|-----|--------|--------|
| 6.1 | **Android source** | Tokens, components and assets for Android. Needed before the Android file. | CLOSED 2026-11-10: android-tribpub @ 1cfb069a6 export and the Android style guide (artifact 5MyLP13QSt52WGRgXW35ZJ) are in use |
| 6.2 | Source commit | Confirm `e30ad2585` is still current for iOS, or provide the newer ref. | ASKED 2026-11-11 (#pd-mobile-public, combined message) |

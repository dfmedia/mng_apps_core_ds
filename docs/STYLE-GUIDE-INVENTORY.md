# Style guide inventory: what the Apps team documented vs what we have built

Checked 2026-11-10 against the two Apps team style guides (Claude artifacts): iOS https://claude.ai/artifact/V364juyHFU3STfVZ6EgjMc (TroncKit @ e30ad2585) and Android https://claude.ai/artifact/5MyLP13QSt52WGRgXW35ZJ (android-tribpub @ 1cfb069a6). Status of our side: docs/BACKLOG.md (data/backlog-status.json). Hand-written summary; refresh when the guides change.

## What the guides contain

| | iOS guide | Android guide |
|---|---|---|
| Components | App chrome, Buttons (incl. Subscription option), Controls, Icon font, Market palette | App chrome, Buttons, Controls, Market palette; plus Layout (ads), Dark mode notes |
| Asset files (in each guide's asset store) | 218: 213 PNG, 4 SVG (author contact icons), 1 JPG, in 19 groups | 138: 126 PNG, 12 SVG (vector drawables converted), in 8 groups |
| Fonts | Open Sans (+ Condensed, NYDN), Spectral, PT Serif | Same plus Roboto and Playfair Display (one paywall heading) |

## Already built (all three libraries)

Brand colors (78 markets), app shell colors (incl. Android 14 vs 15+ status bar), system colors, control colors, text styles, spacing / radius / size scales, breakpoints and grid, Primary button + Disabled + Text link, Subscription option, Continue (per platform), Switch, Checkbox (Android), Text size slider (iOS) and text size setting, icon names (DEC-17).

## Tracked, waiting on the Apps team

| Item | Library | Waiting on |
|---|---|---|
| Top bar, section tabs, bottom tab bar, breaking-news banner (colors done) | Core + iOS + Android | Sizes, MISSING-ASSETS 5.6 |
| Section header band (iOS) and status bar (Android) drawn as components (colors done) | iOS / Android | Sizes, 5.6 |
| Notification prompt Yes / No, Manage subscription / delete account | Core + iOS + Android | 5.7 |
| Savings label | Android | 5.7 |
| Social sign-in buttons incl. Sign in with Apple | iOS | 5.7 |
| Segmented control, loading indicator | Core | 5.7 (colors) |
| All 61 icon purposes as components | Core + iOS + Android | §1 (vector masters) |

## Tracked, not blocked

| Item | Library | Note |
|---|---|---|
| Per-market font exceptions | Core + iOS + Android | Documented only as notes on each text style; no table yet |
| Checkbox, iOS | iOS | iOS ships images per market (Checked / Unchecked + 7 market sets); not drawn yet |
| Orientation | Core | Same on both (phone portrait, tablet all); not on a Figma page yet |

## In the guides, not tracked anywhere yet

| Item | Platform | From the guide |
|---|---|---|
| What's New Continue button | Android | `whats_new_button_color` per market (CT, NYDN, VP override the drawable), white all caps, radius 6. Asked in 5.7, missing from the registry |
| Alerts enable button | Android | `Alerts_Enable_Button_Background`, white text, square. Asked in 5.7, missing from the registry |
| Non-icon images | iOS | Onboarding art and market logos (19), Masthead, paywall logo, account-deletion image, eNewspaper cover placeholder and overlay, player placeholders (error, offline, compact, regular), recirculation placeholder, offline ad placeholder, Washington Post slogan (light / dark), Your News header, topic selection button backgrounds (10) |
| Non-icon images | Android | Per-market `ic_logo` (home-screen widget, plus a night version), launcher icons (background color already in BRAND-COLORS) |
| Ad slots | Android (iOS: offline placeholder only) | 320×50 phone / 728×90 tablet first slot, 300×250 others, sticky footer banner; hidden when the parent is narrower |
| Home-screen widget | Android | The only place with night colors (`values-night`) |
| eEdition (PageSuite) colors | Android | Fixed for every market: tab container #ffffff, tab text #ffffff, inactive #999999, brand #0a1633 |

## The asset files themselves

Both guides carry the shipped image files, so "as shipped" icons and images can be placed in Figma now as reference: PNGs as image fills, the 16 SVGs as vectors. They are exports, not vector masters (except the 16 SVGs), so MISSING-ASSETS 1.1 (vector masters) still stands for building real icon components. MISSING-ASSETS 1.7 updated: the Android set is in the Android guide.

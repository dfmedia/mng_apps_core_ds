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

None left (2026-11-10). Built since this inventory was written: per-market font exceptions (Core Type · iOS vs Android › 04, 05; docs/TYPE-FONT-EXCEPTIONS.md), iOS checkbox as shipped (iOS file, Components · Controls › 02; docs/components/CHECKBOX-IOS.md), orientation (Core Layout · iOS vs Android › 01; docs/ORIENTATION.md).

## In the guides, not tracked before 2026-11-10 (now tracked)

Karl (2026-11-10): add them to the registry and document them as shipped; design nothing new. Built by `scripts/build_guide_extras.py` from `data/source/style-guide-extras.json` → `data/guide-extras.json`, `docs/GUIDE-EXTRAS.md`.

| Item | Platform | Where it is now | Still unknown |
|---|---|---|---|
| What's New Continue button | Android | Registry `component/button-whats-new`. Fill token `whats-new-button-color` (52 of 77; CT, NYDN, VP ship a drawable color), radius `component.android.whats-new-continue.radius` (6). Android Figma Components · Button › 04 | Height, label size, padding (5.7) |
| Alerts enable button | Android | Was already tracked: Android side of `component/permission-prompt` (Notification prompt buttons). Fill is a control token (58 of 77 follow action) | Font, height (5.7) |
| Ad slots | Core (both apps) | Registry `layout/ad-slots`. Colors Core `ad/background`, `ad/label`; Android sizes `component.android.ad.*` (320 × 50, 728 × 90, 300 × 250). Core Figma Layout · iOS vs Android › 02; Android Figma Layout · Ads, widget, eEdition | iOS sizes (5.9) |
| Home-screen widget | Android | Registry `component/widget`. Day colors are System colors · Android tokens (`widget-*`). Android Figma Layout · Ads, widget, eEdition › 02 | Night colors, layout and sizes (5.10) |
| eEdition (PageSuite) colors | Android | Registry `component/eedition-colors`. Tokens `color.android-system.eedition.*` (4 fixed colors), Kotlin `MngSystemColors.eedition*`. Android Figma › 03 | — |
| Non-icon images | iOS + Android | Registry `component/images`; file list in docs/GUIDE-EXTRAS.md. Not drawn in Figma (per-market artwork) | Vector masters (2.1, 2.2) |

## The asset files themselves

Both guides carry the shipped image files, so "as shipped" icons and images can be placed in Figma now as reference: PNGs as image fills, the 16 SVGs as vectors. They are exports, not vector masters (except the 16 SVGs), so MISSING-ASSETS 1.1 (vector masters) still stands for building real icon components. MISSING-ASSETS 1.7 updated: the Android set is in the Android guide.

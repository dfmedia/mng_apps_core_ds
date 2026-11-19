# Layout & breakpoints

## Phone

- Portrait only (`CoreAppDelegate.swift:184`).
- Section-front cells: `space-cell-margin` (16) on all sides, `space-cell-padding` (8) between elements.
- Article: side margin = 0.3125 × width − 160, never below `space-article-margin-min` (16). Top margin `space-article-top-phone` (20).

## App shell

Checked against `f79fe3339` for DREAMT-4718.

| Bar | Height | Spacing | Text |
| --- | --- | --- | --- |
| Navigation bar | `size-navbar` (44, iOS default) | iOS default | Masthead logo at natural size; title text in the system font |
| Section tabs | `size-sectionbar` (44) | `space-sectionbar-gap` (15) between tabs, 7.5 at each end; tab width fits the text | `section-tab`; selected underline `size-section-underline` (4) |
| Breaking-news banner | `size-banner-breaking` (35) | — | `breaking-banner` (Open Sans Bold 14) |
| Section header band | `size-header-band` (30) | `space-header-band-inset` (10) left and right | Style.json `cell-tertiary-headertext` |
| Tab bar | iOS default | iOS default | Tabs: TOP NEWS · SECTIONS · GAMES · YOUR NEWS · NEWSPAPER in 76 markets (bundled `bottomNavTabs`); TB and TBCP have no list, so they get the default TOP NEWS · SECTIONS · YOUR NEWS · ALERTS · NEWSPAPER. Titles are uppercase, except in OS (title case, "Top News") and NYDN's Sections tab ("Sections"). iOS 18 and earlier: system font. iOS 26: system 9 pt medium, scaled with Dynamic Type; "TOP NEWS" and "YOUR NEWS" show as "NEWS" and "YOU" |

On iOS 26 the tab bar uses the system Liquid Glass material, and unselected tabs use the system label color instead of `tabBarUnselectedTintColor` (`AppChromeAppearance.swift`).

## Ads

- The first article ad slot requests 320 × 50 on iPhone and 728 × 90 on iPad. Every other slot requests 300 × 250. All 78 configs are the same (`adPositionSizing`, `defaultArticleAdSize`).
- When the view is narrower than the requested size, the slot falls back to 320 × 50.
- No adhesion or sticky banner: `usesAdhesionAd` is false in every market.

## Shadows

No shared elevation scale: each shadow is set where it's used. They're in the **shadow** token family, converted to CSS (blur = 2 × the iOS radius). Checked against `f79fe3339`.

| Where | Token | iOS opacity | iOS radius | Offset |
| --- | --- | --- | --- | --- |
| Top banner alert | `shadow-banner` | 0.18 | 14 | 0, 8 |
| Persistent audio player | `shadow-audio-player` | 0.20 | 10 | 0, −2 |
| Web view sheet | `shadow-web-sheet` | 0.15 | 10 | 0, 4 |
| Alert with image | `shadow-image-alert` | 0.5 | 5 | 2, 2 |
| Mini media player | `shadow-mini-player` | 0.3 | 4 | 0, 1 |
| Newsletters back button | `shadow-newsletters-back` | 0.15 | 3 | 0, 1 |
| Photo push transition | `shadow-photo-transition` | 0.4 | 6 | 0, −3 (iOS default) |
| Recirculation cards | from the article style | 1 if unset | 1 if unset | 0, 2 if unset |

All are black. The audio player drops its shadow when it sits in the iOS 26 tab bar accessory.

## Motion

No shared animation spec: durations are set where they're used, mostly with the iOS default ease-in-out curve.

| Duration | Used for |
| --- | --- |
| 0.1 s | Section front top region in and out |
| 0.18 s | Article layout change |
| 0.2 s | Live blog update |
| 0.3 s | Most fades and expands: image load, list and eNewspaper views, web embeds, preference confirmation (shown 2 s, then fades), photo zoom reset |
| 0.32 s | Selected section tab underline fade |
| 0.5 s | Recirculation, games landing, live blog. Section front and Your News: 0.5 s after a 0.2 s delay, ease-out |
| 0.72 s | Tournament loading symbols |
| 1.5 s | Widget loading shimmer, linear, repeating |

## Tablet

- All orientations.
- Article top margin `space-article-top-pad` (40).
- Section fronts change layout by window width, not device:

| Width class | From | Source |
| --- | --- | --- |
| x-small | 0 | FrontWidth.swift |
| small | 668 | `bp-front-small` |
| medium | 835 | `bp-front-medium` |
| large | 1113 | `bp-front-large` |

Item sizing in `PageItem.swift` uses 668 / 769 / 1025 instead (`bp-item-medium`, `bp-item-large`). The two sets disagree.

## Grid

Each section-front item takes a width out of 12 (`grid-columns`) for each width class, set by PageBuilder. Example: `{"x-small":12,"small":6}` is full width on a phone and half width from 668 pt.

## Foldable

No foldable or iPhone Duo handling. See the DREAMT-4649 spike.

The iOS apps are one codebase (TroncKit) shipped as 78 market apps. Each market sets its own colors and a few fonts; layout, components and most type are shared. Every app is light mode only. Values here come from the code at commit `f79fe3339` (re-extracted Nov 19, 2026). Since the first export at `e30ad2585`, the only theme changes are a new market, Daily Herald (TDH), and a new optional `tabBarDarkSelectedTintColor`; every other color and font value is unchanged. Market code `DP` is Daily Press; The Denver Post is `TDP`.

## Color

- Each market has seven brand tokens named `<market code>-<role>`: `navbar`, `navtext`, `tabbar`, `tabactive`, `action`, `header`, `alert`. Example: `tdp-tabactive` is The Denver Post's selected-tab orange.
- Use `<m>-navtext` on `<m>-navbar`, and `<m>-tabactive` on `<m>-tabbar`. Fill primary buttons with `<m>-action` and set the label in white.
- Use `<m>-alert` only for the breaking-news banner.
- Many shipped pairs miss contrast: the selected tab in 34 markets is below 3:1 on its tab bar, and white on the primary button is below 4.5:1 in 22 markets. Each token's note gives its ratio. Values are kept as shipped.
- The full set (124 themed colors, the Style.json palette and each market's named colors) is in the **Market palette** component and `assets/Data/markets.json`.

## Type

- Three bundled families. Open Sans is used for navigation, labels, bylines, captions and article titles. Spectral is used for article body text and the main cell headlines. PT Serif is used for media headlines, bullets and tertiary cells. Open Sans Condensed appears only in NYDN.
- The five shared styles are `headline`, `body`, `body-bold`, `caption` and `caption-bold`. Every market defines them; 76 of 78 match.
- Section fronts and articles use the Style.json styles (`cell-*`, `page-*`). 71 markets share one template. BS, DP, HC, MC, OS, SS and VP share a second, older template; see **Type by market**.

## Iconography

- iOS icons come from three places: Font Awesome 5.15.1 (7 glyphs), images in TroncKit (218: 213 PNG, 4 SVG, 1 JPG), and about 21 SF Symbols.
- iOS does not use the MNG IcoMoon icon font from the web style guide. **Icons** maps each iOS icon to its counterpart in Karl's set.

## Layout

- iPhone is portrait only. iPad allows every orientation.
- Section fronts sit on a 12-column grid (`grid-columns`) and change layout at `bp-front-small`, `bp-front-medium` and `bp-front-large`.
- The nav bar and section tabs are 44 pt (`size-navbar`, `size-sectionbar`), the breaking-news banner is 35 (`size-banner-breaking`) and the section header band is 30 (`size-header-band`). The tab bar is the iOS default; on iOS 26 it uses Liquid Glass with smaller titles.
- Cells use `space-cell-margin` and `space-cell-padding`. Articles keep at least `space-article-margin-min` on each side.

## Controls

- No shared button component exists. Login happens in an Auth0 web view, so iOS shows no native Log In / Register buttons. The closest thing to a primary button is the meter paywall purchase button ("TRY ONE MONTH FREE", uppercase in every market): `<m>-action` fill, white Open Sans Bold 14, `size-button-purchase` (45) and `radius-purchase` (8).
- No button has a custom pressed state. They're iOS system buttons: the title fades while pressed and the fill stays the same.
- Touch targets are not held to `size-touch-min`. The Your News checkbox (`size-checkbox`) and the push prompt buttons (`size-button-push`) are smaller.
- No payment buttons exist on iOS. Subscriptions are App Store purchases shown as **Subscription option** buttons.

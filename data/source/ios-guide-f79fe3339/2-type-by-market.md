# Type by market

All 78 apps bundle identical copies of the same font files: Open Sans (10 weights, plus Medium in all but CT, OCR, TB, TBCP and TDP), Open Sans Condensed (Bold v1.11, Light v1.10, Light Italic v1.10; only NYDN uses them), PT Serif (4) and Spectral (14; NYDN has only Regular, Italic, Bold and Bold Italic). TDP also bundles Open Sans Condensed Regular v3.003. They are under Fonts.

## Shared styles

| Style | 76 markets | NYDN | VP |
| --- | --- | --- | --- |
| headline | Spectral Medium 31 | Open Sans Condensed Light 31 | Open Sans Regular 30 |
| body | Open Sans Regular 14 | same | same |
| body-bold | Open Sans Bold 14 | same | same |
| caption | Open Sans Regular 11 | Open Sans Regular 12 | Open Sans Regular 12 |
| caption-bold | Open Sans Bold 11 | Open Sans Bold 12 | Open Sans Bold 12 |

## Style.json templates

- **Standard** (71 markets): 51 font keys. Navigation in Open Sans. Cell headlines in Spectral and PT Serif. Article body in Spectral 18 (PT Serif 18 in DP, MC, NYDN, OS and VP).
- **Legacy** (BS, DP, HC, MC, OS, SS, VP): 60–61 keys. It adds `cell-headline-default`, `cell-blurb`, `cell-signature`, `label-kicker-left`. Cell labels use PT Serif or Spectral instead of Open Sans.
- Each style's note under Typography lists every market that differs.

## Fallbacks and sizing

- Code pattern: `UIFont(name:size:) ?? .systemFont(ofSize:)`. A few fallbacks change size, for example 12 → 10 (`AppThemeable.swift:630`).
- Style.json lookups fall back to `preferredFont(forTextStyle: .body)`.
- Article text has 6 sizes: ×0.85, ×1.0 (default), ×1.15, ×1.30, ×1.45 and ×1.60 (`FontManager.swift`). When the reader follows the iOS text size setting instead, sizes scale by the system size relative to the "small" text size. Other screens use fixed sizes.

## Controls & settings

These styles are set in code, not Style.json. They're in the **Controls & settings** group under Typography. Checked against `f79fe3339`.

| Style | Default | Markets that differ |
| --- | --- | --- |
| `section-tab` | Open Sans Bold 11 | Open Sans SemiBold 12: BS, CT, DP, HC, MC, NYDN, OS, SS, TDP, TDPS, VP, TIVDB |
| `settings-row` | Open Sans Regular 14 | 11: BS, HC, SS. 12: NYDN |
| `settings-header` | Open Sans Bold 14, uppercase | NYDN: Open Sans Condensed Bold 14 |
| `breaking-banner` | Open Sans Bold 14 | — |
| `paywall-purchase` | Open Sans Bold 14 | — |
| `paywall-login-link` | Open Sans Regular 14 | 11: BS, DP, HC, MC, OS, SS. 12: NYDN, VP |
| `savings-label` | Open Sans Bold 13 | — |
| `push-yes` / `push-no` | Open Sans Bold 14 / Regular 14 | VP: No isn't underlined |
| `newsletters-button` | Open Sans SemiBold 18, Dynamic Type | — |
| `search-section-result` | Open Sans Light 20 | — |

- Search story results use `cell-headline` at the xx-small size.
- Style.json `nav-title`, `tab-item` and `blocker-login` aren't read by any iOS code. The nav bar title and tab titles use the system font.

## Weights in use

- **Open Sans Light** is used in 17 files: the subscription option description (12), section search results (20), and message, empty-state and tracking views.
- **Open Sans ExtraBold** is only used to measure section tab widths in HC, MC, SS and VP. It never renders.
- **Light Italic and ExtraBold Italic** are bundled but not used.
- **Open Sans Condensed:** NYDN bundles Bold, Light and Light Italic.

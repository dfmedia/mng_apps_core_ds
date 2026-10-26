# Discrepancies — iOS vs Android things that should match

Everything that differs between the two apps but **should be the same**. Each row says what the right value is, how we know, and which app needs the fix, so the Apps team can work through it later. Differences that are intentional platform conventions (SF Symbols vs Material, 44 pt vs 48 dp) are not listed here; they live in the registry as "Core + variant".

- Sources: iOS TroncKit @ `e30ad2585` · Android android-tribpub @ `1cfb069a6` · migration sheet "Tribpub-MNG App Migrations" (tab Production, Primary / Secondary color)
- Data: `data/brand-color-resolution.json` (`scripts/resolve_brand_colors.py`), `data/color-platform-comparison.json`
- Figma (Core file): Color · Market Palettes → **06 · Brand color source of truth**

Status: `OPEN` (cause unknown, ask Apps team) · `KNOWN` (right value known, fix not scheduled) · `TICKETED` · `FIXED`
Fix on: `iOS` · `Android` · `both` · `?`

## 🔴 Fix ASAP (parked)

Karl, 2026-10-26: not raised with the Apps team yet; pick up later.

| ID | Why | Fix on |
|----|-----|--------|
| **DSC-15** | Breaking-news banner fails WCAG AA on iOS: white on `#ff0000` = 4.0:1 in 71 markets. Core value `#cf000e` = 5.74:1 (DEC-05). | iOS (all 77 markets) |
| **DSC-19** | iOS TIVDB banner text is black on red (3.66:1 on `#cf000e`, fails AA). Use white. | iOS |

## How we decide the right value

1. **Migration sheet wins.** If the sheet's Primary / Secondary color matches either app, that is the source of truth.
2. **iOS 2-decimal drift.** TroncKit stores each color channel as a 2-decimal fraction, so `0x22` (0.133) becomes 0.13 and comes back as `0x21`. When iOS = Android after that rounding, Android holds the authored value. This explains 32 of the 34 pairs the sheet could check.
3. **Web alignment (DEC-02).** Where the Cluster Audit web color is close (ΔE < 0.05) to our value, the web color becomes the value. Far → keep the earlier choice. See `docs/DECISIONS.md`.
4. **iOS default (DEC-03, DEC-08).** Anything still different that no source confirms takes the iOS value, including close (off-by-1) mismatches; Android gets the fix. Final (Karl, 2026-10-26).

All brand colors are now decided; the values are in `docs/BRAND-COLORS.md` (hex and RGB) and `tokens/core/brand.tokens.json`.

## Brand colors

| ID | What differs | Should be | Fix on | Evidence | Status |
|----|--------------|-----------|--------|----------|--------|
| DSC-01 | iOS brand color off by 1 in a channel (2-decimal drift) in 36 markets: SGVT\*, SIT, TB, TBCP, TCCDR, TCHW, TCV, TDC, TDPS\*, TEBT\*, TETS, TFMT, TGT, TJA, TLADN, TLS, TLTC, TMCH, TMD, TMJ, TMS, TNH, TOD, TPM, TR, TRH, TROT, TRR, TSCS, TSEB, TSS, TTH, TTT, TVR, TVTH, TWDD | Android / sheet hex (e.g. `#ab4022`, not `#ab4021`) | iOS | Sheet matches Android in all sheet-covered markets; the rest follow the drift rule. TWDD is 1 unit off without fitting the rule; sheet confirms Android. \*SGVT bar, TDPS and TEBT bar have no sheet value, so DEC-08 (2026-10-26) uses the iOS value there and Android gets the 1-unit fix. Invisible on screen. Fix: store hex strings instead of 2-decimal floats. Where DEC-02 moved a brand to its web color, the target is now that color (DSC-18). | KNOWN |
| DSC-02 | **TLR** Loveland: iOS uses red `#ab4021` | `#4e5dca` | iOS | Sheet = Android. iOS value is TLS Lowell Sun's red (the next market alphabetically). | KNOWN |
| DSC-03 | **TUDJ** Ukiah: iOS uses `#408fcc` | `#32408f` | iOS | Sheet = Android. iOS value is TVR Vacaville's blue (the next market alphabetically). | KNOWN |
| DSC-04 | **TBE** Broomfield: iOS uses `#0070b8` | `#4351af` | iOS | Sheet = Android. | KNOWN |
| DSC-05 | **TEPTG** Estes Park: Android uses green `#3e8e75`; iOS `#33408f` | `#32408f` | both | Sheet `#32408f`; iOS is that value with 2-decimal drift. | KNOWN |
| DSC-06 | **TSAR** Saratogian: iOS bar `#ffffff`, button and selected tab template blue `#004e87` | Bar `#f5f5f5`, secondary `#00919e` | iOS | Sheet = Android (sheet note: secondary matches the logo). Button color (`action`): iOS value (DEC-03). | KNOWN |
| DSC-07 | **MC** Morning Call: Android button `#4fa8d1` | `#539cc4` | Android | Sheet = iOS. Android value is HC Hartford's blue. Selected-tab color: iOS value (DEC-03). | KNOWN |
| DSC-08 | **SIT** Sonoma Index-Tribune: selected tab Android `#149ce5`, iOS `#ffeb00` | `#ffea00` | both | Sheet secondary `#ffea00`; iOS is it with drift. | KNOWN |
| DSC-09 | Template blue on iOS: TBAN, TDB, TDF, TSPPP, TT show `#004e87` where Android shows each market's own color | iOS value (DEC-03) | Android | Not in the migration sheet; web color far from both apps. (TBH, TCE, TMI, TLBPT, TRDF were settled by DEC-02, see DSC-18.) | KNOWN |
| DSC-10 | SCNG group: bar settled to web `#b93611` for PSN, TPE, TSBS, TWDN (DSC-18). Settled by DEC-03: SGVT button (iOS orange `#ff6900` vs Android `#b11e35`) and the selected tab in all five (iOS orange vs Android black) | iOS value (DEC-03) | Android | Web color only covers the bar. | KNOWN |
| DSC-11 | Smaller open differences: TBHS bar `#b01f36` vs `#c00030`; TDCD `#5b9bc8` vs `#4891b3` (web rust `#b93611`); OCR `#b04f0f` vs `#ac4e0f` (web teal `#0a5962`); TSV bar black vs `#557fba`; TOP bar and button (web `#3a527a`); TEBT button `#6bd1e6` vs `#557fba`; TDP button `#f7a430` vs `#daa520` (web maroon `#7d161e`); TDLW bar off by 2 units (web rust) | iOS value (DEC-03) | Android | Not in the migration sheet, or the web color is far from both apps. | KNOWN |
| DSC-12 | Selected tab only: DP `#005f7e` vs `#4fa8d1`; TIVDB `#000000` vs `#807c7c`; TMN `#000000` vs `#6bd1e6`; OS `#15919d` vs `#00919e`; MC `#539cc4` vs `#4fa8d1`; TBH, TLBPT, TRDF (iOS black or `#9dd1f5` vs Android light blues) | iOS value (DEC-03) | Android | No secondary color in either sheet. | KNOWN |
| DSC-18 | 27 brand colors moved to the web color by DEC-02: TBH, TCE, TMI, TLBPT, TRDF, PSN, TPE, TSBS, TWDN (were open); OS button `#15919d` (iOS already); TCCDR, TETS, TJA, TSCS → `#32408f`; TLADN, TLS, TNH, TOD, TSEB, TMJ, TPM, TTH, TRR → `#b93611`; TMD, TMS → `#3a527a`; TGT → `#44687f`; NYDN → `#4492e0` | Web color (list in DECISIONS.md) | both (OS: Android) | Visually close to what ships (ΔE < 0.05); aligns apps with web themes. | KNOWN |
| DSC-13 | **TPD** Press Democrat: sheet says `#9e0b0f` / `#ffea00`; both apps use black bar and gray `#999999` | iOS value (DEC-03) | Android | Sheet row is marked WIP; only the iOS section header uses `#9e0b0f`. | KNOWN |
| DSC-14 | Legacy markets OS, SS, NYDN: the sheet's Primary (`#004e87`, `#000000`, `#ec2127`) appears in neither app | iOS value (DEC-03) | Android | Sheet column may mean something else for the legacy template. | KNOWN |
| DSC-15 | **🔴 ASAP · contrast.** Breaking-news red: iOS `#ff0000` (71) / `#d80000` (6), Android `#cf000e`. White on `#ff0000` = 4.0:1, fails WCAG AA | `#cf000e` (rgb 207, 0, 14) with white text, 5.74:1 AA (DEC-05) | iOS | Android already ships `#cf000e`. | KNOWN · PRIORITY · parked 2026-10-26 |
| DSC-19 | **🔴 ASAP · contrast.** iOS TIVDB breaking-news text is black (3.66:1 on `#cf000e`) | White `#ffffff` (`alerttext`) | iOS | Confirm Android banner text is white (not in the export). | KNOWN · PRIORITY · parked 2026-10-26 |
| DSC-16 | BS tab bar: iOS white with black unselected icons, Android black with white | iOS value (DEC-03) | Android | BS is decommissioned Nov 1 2026; may not need a fix. | KNOWN |
| DSC-17 | Bar text: TIVDB iOS `#cccccc` vs `#ffffff`; OS iOS `#333333` vs `#000000`; TDP unselected tab iOS `#999999` vs `#ffffff` | iOS value (DEC-03) | Android | | KNOWN |

## Components and controls

| ID | What differs | Should be | Fix on | Evidence | Status |
|----|--------------|-----------|--------|----------|--------|
| DSC-20 | Primary button: iOS radius 4 (legacy 5 + 1 pt border), Open Sans Bold 14; Android square corners, system font, 60 dp tall | One Core spec | both | Same component on both paywalls. DEC-07 (2026-10-26): kept per platform as tokens for now; height and label font are future changes (IMPROVEMENTS BTN-01, BTN-02). Spec: docs/components/BUTTON.md | KNOWN (kept per DEC-07) |
| DSC-21 | Subscription option: iOS radius 8, Open Sans Bold 16; Android square, system 16sp | One Core spec | both | | OPEN |
| DSC-22 | Article text size: iOS 6 steps (slider), Android 4 steps (list) | Same number of steps | ? | The control can differ per platform; the scale should not. | OPEN |
| DSC-23 | Your News checkbox: iOS uses 8 per-market image sets; Android tints one control | One tinted checkbox | iOS | | KNOWN |
| DSC-24 | Continue button: iOS uses pre-colored PNGs (10 copies); Android a tinted button with radius 9 | Core primary button | iOS | | KNOWN |

## Icons

| ID | What differs | Should be | Fix on | Evidence | Status |
|----|--------------|-----------|--------|----------|--------|
| DSC-30 | Saved in special sections: Android uses a star, iOS a bookmark | Bookmark (Core Saved) | Android | PLAT-09 | KNOWN |
| DSC-31 | Text size: iOS smaller/larger glyphs, Android one glyph | One Core glyph + iOS variant | — | PLAT-08 | KNOWN |

## Log

- **2026-10-26** — DEC-08: iOS is the default for unconfirmed mismatches, including close ones (SGVT, TDPS, TEBT now iOS). DSC-15 and DSC-19 parked: not raised with the Apps team yet.

- **2026-10-26** — DEC-07 button pilot: DSC-20 kept per platform as tokens; contrast failures listed as required changes in IMPROVEMENTS CLR-04.

- **2026-10-21** — DEC-05: one Core breaking-news red `#cf000e` with white text (5.74:1 AA). DSC-15 and DSC-19 flagged ASAP.

- **2026-10-21** — DEC-03: every remaining brand-color difference takes the iOS value (Android to fix). DEC-04: colors now ship as tokens (Swift + Kotlin); all values documented as hex and RGB in docs/BRAND-COLORS.md.

- **2026-10-21** — DEC-02 applied: 27 brand colors moved to the Cluster Audit web color (DSC-18). 28 brands still have an open color (16 bar/button, 12 selected tab only).

- **2026-10-21** — Started. Brand colors checked against the migration sheet: 47 of 77 markets fully resolved, 30 have at least one open role.

# Progress

One phase at a time. Each phase is reviewed before the next starts.

Legend: ✅ done · 🔄 in progress · ⏸ waiting on review/input · ⬜ not started

Item-level to-do list (every element and component from the iOS and Android style guides, with Figma / tokens / code status): **docs/BACKLOG.md**.

## Phase 0 — Structure & setup  ✅

| Step | Status | Notes |
|------|--------|-------|
| Read and inventory the iOS artifact | ✅ | 77 markets, 539 brand colors, 63 text styles, ~250 icons, 4 component families |
| Core DS Figma file connected (App Team / Assets) | ✅ | `MNG Apps Core Design System` |
| Local repo folder set up | ✅ | README, PROGRESS, docs/, data/, scripts/ |
| Improvements log started | ✅ | docs/IMPROVEMENTS.md |
| Missing-assets list started (icons first) | ✅ | docs/MISSING-ASSETS.md · contacts: Jess Navaro, Patrick Carr |
| Cover page | ✅ | Figma Cover page + file thumbnail |

## Phase 1 — Foundations (tokens)  🔄

| Step | Status | Notes |
|------|--------|-------|
| 1.1 Visualize all market palettes | ✅ | Figma page **Color · Market Palettes**: overview, 45 unique palettes with shipped vs suggested previews, all 77 markets, 59 unique hexes + merge candidates |
| 1.2 Pick merges and mode strategy | ⏸ later | Merges: keep shipped as-is for now. Modes: revisit later. Tab-label contrast (4.5:1): revisit later |
| 1.3 Build color variables (Primitives → Brand → System) | ⬜ | After 1.2 |
| 1.4 The other 117 themed colors per market | ⬜ | 62 are identical in every market → System collection |
| 1.5 Typography: text styles | ✅ DEC-09/10: tokens, code, Figma (iOS 56, Android 25) | Open Sans Light installed (assets/fonts). Android subhead font asked (MISSING-ASSETS 4.4) |
| 1.6 Spacing, radius, size, breakpoint variables | ✅ DEC-11/12: spacing, touch targets, breakpoints, component metrics | docs/SCALES-COMPARISON.md |
| 1.7 Icons page: system comparison grid | ✅ | Figma page **Icons · System Comparison**: 59 purposes × SF Symbols / Material Symbols / Font Awesome 5.15.1, gaps flagged. SF Symbols column filled from PNG export (scripts/export_sf_symbols.swift → assets/sf-symbols/) |
| 1.8 Icons: decide semantic icon list + build Icon component | ⬜ | After Apps team answers MISSING-ASSETS §1 |

## Phase 1A — Platform ownership (Core vs iOS vs Android)  ⏸ review

| Step | Status | Notes |
|------|--------|-------|
| Android source received | ✅ | MNG Android Style Guide artifact, android-tribpub @ 1cfb069a6 → data/source/android-markets.json |
| iOS + Android Figma files created | ✅ | MNG iOS Design System, MNG Android Design System (empty) |
| Icons: who uses each purpose | ⏸ | Figma Icons page → **04 · Platform ownership**: 32 Core, 2 Core + variant, 25 iOS only, 2 Android only |
| Colors: iOS vs Android per market | ⏸ | Figma Color page → **05 · iOS vs Android**: 7 Core roles, 2 aliases, 1 iOS-only, 2 Android-only; 43 markets aligned, 34 differ |
| Decisions PLAT-01 … PLAT-10 | ⏸ | docs/PLATFORM-OWNERSHIP.md |
| Palette cleanup by brand | ✅ | DEC-01 sheet + drift, DEC-02 Cluster Audit when close, DEC-03 iOS default: all 77 brands have all 7 Core roles. Final: iOS default confirmed by Karl (DEC-08, 2026-10-26) |
| Figma color variables | ✅ | Core file: Brand colors (624 vars, 78 markets) + Brand theme (20 modes); page Color · Brand Theme (DEC-06) |
| Design tokens | ✅ v1 | DEC-04: tokens/ (DTCG) → Style Dictionary → Swift (iOS repo), Kotlin + 77 flavor XML (Android repo); hex + RGB in docs/BRAND-COLORS.md | (Figma Color page **06 · Brand color source of truth**; MISSING-ASSETS 3.3) |
| Discrepancy tracker | ✅ | docs/DISCREPANCIES.md: DSC-01…31 |
| Architecture | ✅ | docs/ARCHITECTURE.md: registry, variables, wayfinding, rollout |
| Registry | ✅ | data/registry.json + docs/REGISTRY.md: 99 items (12 color roles, 61 icons, 20 components, 6 layout rules) |
| Components + layout: who owns what | ⏸ | New Figma page **Components · Platform Ownership**: 9 Core, 13 Core + variant, 2 iOS only, 2 Android only |
| Type comparison | ⬜ | |
| Pilot: button system end-to-end in all three files | ✅ reviewed 2026-10-26 | DEC-07. Tokens, docs/components/BUTTON.md, Swift + Android View code generated/written; Core Figma page **Components · Button** (01–04) + Button variable collection; iOS and Android files: page Components · Button with Button/Primary (instances of Core Button + platform overrides) and Button/Text link |

## Phase 2 — Core atoms  ⬜
## Phase 3 — iOS file & iOS atoms  ⬜
## Phase 4 — Molecules / organisms  ⬜
## Phase 5 — QA & publish  ⬜
## Phase 6 — Move platform-only items into the iOS and Android files  ⬜

## Next session (handoff 2026-10-26)

1. **Push.** Sessions without the repos attached can't push; Karl pushes (done for the 2026-10-26 work up to the backlog).
2. **Button pilot reviewed by Karl (2026-10-26).** Email to Jess and Patrick: button values only (MISSING-ASSETS 5.5). Kotlin package `com.mng.designsystem.tokens` confirmed (2026-10-29).
3. **Platform Figma files done** (libraries published and enabled 2026-10-26): iOS and Android each have page Components · Button. iOS text link color is a separate collection, Text link · iOS (20 modes matching Brand theme): set the same market in both. Tip: library imports and font loads hang when a file's tab is in the background; bring the file to the front.
4. **Ask the Apps team** (MISSING-ASSETS 5.5): iOS button height (pilot uses 44), Android label weight/size, iOS link font, pressed states. Code is not compiled yet (no Xcode or Android SDK here).
5. **Waiting:** clusters for TBAN, TBE, TB, TBCP, TBHS, TCHW, TDPS.
6. **Parked, pick up later** (Karl, 2026-10-26; not raised with the Apps team yet): DSC-15 iOS breaking-news red `#ff0000` → `#cf000e`; DSC-19 TIVDB black banner text on iOS, and confirm Android banner text is white.
7. **Next work after the pilot:** type, spacing and radius tokens; then the remaining components.

## Log

- **2026-10-16** — Phase 0 complete. Built Color · Market Palettes page in Figma. Started IMPROVEMENTS (15 items) and MISSING-ASSETS (icons first).
- **2026-10-16** — Decisions: merges on hold, modes later, tab-label contrast later. Added Cover page and Icons · System Comparison page. Apps team contacts recorded.
- **2026-10-16** — SF Symbols exported (46/46, macOS 15.5) and placed in the iOS column of the Icons page; export sheet kept in section 03 of that page.
- **2026-10-20** — Android export received. Added CLAUDE.md (project instructions). Built Core file sections: Icons 04 · Platform ownership, Color 05 · iOS vs Android. Wrote docs/PLATFORM-OWNERSHIP.md (PLAT-01 to PLAT-10).
- **2026-10-21** — Added docs/ARCHITECTURE.md, registry (data/registry.json, docs/REGISTRY.md) and Figma page Components · Platform Ownership. Palette cleanup paused until the Apps team explains the iOS/Android color differences (MISSING-ASSETS 3.3). "Rounding twins" renamed "near-identical hexes".
- **2026-10-21** — Checked brand colors against the migration sheet. Found the iOS drift pattern (2-decimal channels). PLAT-02 approved by rule. Started docs/DISCREPANCIES.md. Figma Color page section 06 added. Claude now pushes all commits.
- **2026-10-21** — DEC-02: 27 brand colors moved to Cluster Audit web colors where close; 15 kept (web too far); 9 still open. Added docs/DECISIONS.md.
- **2026-10-21** — DEC-03 (iOS default) and DEC-04 (design tokens). All brand colors decided; Swift and Kotlin generated into the platform repos.
- **2026-10-21** — DEC-05: breaking-news red `#cf000e` everywhere with white text (5.74:1 AA); new `alerttext` token; iOS fix flagged ASAP (DSC-15, DSC-19).
- **2026-10-21** — DEC-06: Figma Brand colors + Brand theme variables built in Core; Daily Herald added as provisional market (tokens now 78 markets).
- **2026-10-21** — Brand theme: swapped TNH and TSPPP (near-duplicates of OCR and TMN) for SGVT and OS.
- **2026-10-26** — Button pilot (DEC-07): keep shipped colors/radius/height as per-platform tokens; Core Button component, label font per platform. New: data/source/button-shipped.json, data/button-decisions.json, scripts/build_button_tokens.py, tokens/*/button.tokens.json, docs/components/BUTTON.md; IMPROVEMENTS CLR-04 now REQUIRED (15 action + 9 iOS link markets), BTN-01/02 FUTURE; MISSING-ASSETS 5.5. Figma Core: Button collection + page Components · Button. iOS repo: Tokens/MNGButtonTokens.swift, Components/Button/MNGButton.swift. Android repo: tokens/res/values/mng_button.xml, components/button/ (View-based). Figma iOS/Android: Button · iOS / Button · Android variables.
- **2026-10-26** — Core library published and enabled in the iOS and Android files. Built Button/Primary and Button/Text link in both platform files (mng_apps_ios_ds, mng_apps_android_ds).
- **2026-10-26** — Added docs/BACKLOG.md (scripts/build_backlog.py, status in data/backlog-status.json): 107 items with Figma, tokens and code status.
- **2026-10-26** — Karl reviewed the button pilot (DEC-07): approved. Drafted Apps team questions (MISSING-ASSETS 5.5, 3.3; DSC-15, DSC-19; Kotlin package).
- **2026-10-26** — DEC-08: iOS is the default for every unconfirmed brand-color mismatch, close ones included; DEC-03 final (MISSING-ASSETS 3.3 closed, PLAT-06/07 resolved). SGVT, TDPS, TEBT bar colors moved to iOS (tokens, Swift, Kotlin, flavor XML, Figma). DSC-15/19 parked. Platform code regenerated in mng_apps_ios_ds and mng_apps_android_ds.
- **2026-10-29** — Kotlin package `com.mng.designsystem.tokens` confirmed (DEC-04); placeholder notes removed in Core and mng_apps_android_ds.
- **2026-10-30** — Typography step 1: data/source/ios-type.json + android-type.json (from the style guides), scripts/compare_type.py → data/type-comparison.json, docs/TYPE-COMPARISON.md. 75 roles: 1 same, 1 close, 11 differ, 48 iOS only, 8 Android only, 6 unknown (MISSING-ASSETS 4.4). Main finding: iOS headlines/body in Spectral, Android in PT Serif. Figma review page waiting on the Desktop Bridge.
- **2026-10-30** — Figma Core: new page **Type · iOS vs Android** (01 summary, 02 the 19 roles both apps have drawn side by side in the shipped fonts, 03 the 56 one-app styles), from data/type-comparison.json. Waiting on Karl's step-2 decisions.
- **2026-10-30** — DEC-09: typography and components match production. Type tokens for all 63 iOS + 26 Android styles (scripts/build_type_tokens.py), docs/TYPE-STYLES.md, MNGTypeStyles.swift (mng_apps_ios_ds), MngTypeStyles.kt (mng_apps_android_ds). Open Sans Light/LightItalic/ExtraBold/ExtraBoldItalic added to assets/fonts for Figma. TYPE-03/04 FUTURE.
- **2026-10-30** — Karl: fonts stay per platform permanently (TYPE-03 rejected); TYPE-04 shared scale kept (renamed); TYPE-05 added (remove per-market font exceptions). Open Sans Light installed. Android Figma file: 25 text styles + page Type · Text styles (mng_apps_android_ds). iOS text styles waiting (font loading hangs while the iOS tab is in the background). Asked the Apps team for the Android article subhead font (`ArticleText.Subhead.Wapo`).
- **2026-11-03** — DEC-10: iOS legacy template acknowledged only (docs/LEGACY-TEMPLATE.md); removed from tokens and code (MNGTypeStyles.swift, MNGButtonTokens.swift, MNGButton.swift in mng_apps_ios_ds). Figma cleanup (iOS Button/Primary legacy variants, legacy variables, Core page notes) waits for the MNG files to be open.
- **2026-11-03** — Figma: legacy button variants/variables removed (iOS), legacy notes removed (Core Button and Type pages); duplicate iOS Button/Primary + Text link from the Oct 26 timeout deleted. iOS: 56 text styles + page Type · Text styles. DEC-11: docs/SCALES-COMPARISON.md, spacing/touch tokens (Core Spacing collection; Spacing · iOS / · Android), MNGScaleTokens.swift (mng_apps_ios_ds), mng_scale.xml (mng_apps_android_ds).
- **2026-11-03** — DEC-12: everything linked to tokens. Breakpoints and component metrics as platform tokens + Figma collections (Breakpoints · / Components · iOS and Android); Core Button collection has iOS/Android modes and the Core Button is fully bound; text links bound to the touch target. Regenerated MNGScaleTokens.swift (mng_apps_ios_ds) and mng_scale.xml (mng_apps_android_ds). Karl: "app chrome" is called **app shell** in this project from now on (docs keep their wording).
- **2026-11-03** — DEC-13 app shell: sizes wait on the Apps team (MISSING-ASSETS 5.6). Shell colors as tokens (scripts/build_shell_colors.py): Core navicon (= navtext), iOS section bar, Android section tabs + tab labels (follow Core roles except CT and 5 label markets). Figma: Core navicon (Brand colors + Brand theme); Shell colors / Shell theme collections in the iOS and Android files. Palettes regenerated in mng_apps_ios_ds and mng_apps_android_ds.
- **2026-11-03** — DEC-14 remaining buttons and controls: majority colors only, exceptions documented in docs/CONTROL-EXCEPTIONS.md (scripts/build_control_tokens.py → tokens/*/controls.tokens.json). Figma: Core Subscription option (iOS/Android modes); Android Switch + Checkbox (Components · Controls). iOS Switch + Text size slider pending (iOS plugin session hangs on library imports). MISSING-ASSETS 5.7 for the Apps team; Continue waits on Karl.
- **2026-11-04** — Karl: Continue kept as shipped per platform (component.ios/android.continue.* tokens; IMPROVEMENTS BTN-03). App shell exceptions no longer built: majority values only, 14 exceptions in docs/SHELL-EXCEPTIONS.md (IMPROVEMENTS CLR-08). Regenerated palettes (iOS MNGBrandColors; Android CT/DP/NYDN/TSAR flavors) and scale tokens. Figma updates wait for the bridge in the MNG files.
- **2026-11-04** — Figma: iOS Components · Controls (Switch, Text size slider, Continue image button; action bound via the existing Button binding since library imports hang in the iOS file). Android Continue (Components · Button › 02). iOS Shell colors: BS/DP/NYDN set to majority values. Still open (library imports hang unless the file is in front): Android Shell colors exceptions → aliases, Subscription option wrappers in both platform files.
- **2026-11-05** — Figma: Android Shell colors exceptions now alias the Core roles (10 values; DEC-14). Subscription option wrapped in both platform files in their own mode (iOS Components · Button › 02, Android › 03). Imports were stalling because the platform files had unaccepted Core library updates (note in CLAUDE.md).
- **2026-11-05** — Karl asked the Apps team MISSING-ASSETS 5.5 + 5.7 (button and control values) in #pd-mobile-public (reply to the 4.4 subhead thread).
- **2026-11-05** — Repo links point to the dfmedia org (CLAUDE.md, README.md; same change in mng_apps_ios_ds and mng_apps_android_ds). Pushed the 8 unpushed commits (DEC-11 to MISSING-ASSETS 5.5/5.7).

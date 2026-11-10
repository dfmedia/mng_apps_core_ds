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
| 1.4 The other themed colors per market | ⏸ step 1 review | docs/SYSTEM-COLORS.md + Core page **Color · System colors**: iOS 124 / Android 136 colors, 58 / 69 fixed in every market, 16 proposed pairs, market palettes (iOS 19, Android 29). Step 2 (tokens for every market) after review |
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
| Decisions PLAT-01 … PLAT-10 | ⏸ | docs/PLATFORM-OWNERSHIP.md. All closed (2026-11-10): 01, 08 approved and 09 rejected → DEC-17; 04 and 10 settled by DEC-14 |
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
- **2026-11-05** — DEC-15 (closes PLAT-05): iOS `header` and Android `statusbar` are aliases of Core navbar (scripts/build_tokens.py; MNGBrandColors.swift in mng_apps_ios_ds, MngBrandColors.kt + flavor XML in mng_apps_android_ds). 15 exceptions with suggested overrides in docs/SHELL-EXCEPTIONS.md, drawn majority vs override in Figma (iOS + Android: Components · App shell › 01; scripts/figma/build_role_exceptions.js). Android Figma: statusbar variables (78 + theme). iOS header variables wait: Core library import stalls in the iOS file again.
- **2026-11-05** — System colors step 1 (PROGRESS 1.4): scripts/compare_system_colors.py → data/system-color-comparison.json, docs/SYSTEM-COLORS.md; proposed pairs in data/system-color-pairs.json (MISSING-ASSETS 3.4). Figma Core: new page **Color · System colors** (01–06, scripts/figma_system_colors.py + scripts/figma/build_table_section.js). Waiting on Karl's review; goal for step 2: tokens for every market, shared palettes noted with their markets.
- **2026-11-05** — Figma iOS: `header` variables (78 aliases of Core navbar + Shell theme · iOS) now that the import works with the iOS file in front; Header band exceptions samples rebuilt on the live variables (mng_apps_ios_ds). Waiting on Karl: accept or reject the 15 suggested overrides (docs/SHELL-EXCEPTIONS.md).
- **2026-11-05** — DEC-15: Karl accepted all 15 header band / status bar overrides. data/shell-overrides.json → override tokens (scripts/build_tokens.py), MNGBrandPalette.headerOverride (mng_apps_ios_ds), MngBrandPalette.statusbarOverride + flavor XML (mng_apps_android_ds); Figma variables set to the shipped hex and the samples relinked (majority = Core navbar, override = variable). Android icon color asked of the Apps team (MISSING-ASSETS 5.6).
- **2026-11-05** — Apps team (Ameer M.) on Android status-bar icons: white on Android 14 and below (black override needed), white bar with dark icons on Android 15+ (= navbar); from code, device check pending. Recorded in MISSING-ASSETS 5.6, DEC-15, docs/SHELL-EXCEPTIONS.md. Modelling the 15+ behavior waits on Karl.
- **2026-11-06** — Karl: build both Android status bar versions (14 and below: dark override; 15+: navbar with dark icons) once the Apps team confirms on a device. MISSING-ASSETS 4.4/5.5/5.7 still unanswered (Jess will update the Android style guide).
- **2026-11-10** — Karl signed off DEC-11. DEC-16: system colors = majority tokens, every market's palette documented (not tokens); Android launcher icon background moved to docs/BRAND-COLORS.md as a market brand asset. Next: system colors step 2; alert topic rows need screenshots from the Apps team (MISSING-ASSETS 3.4). Figma Core page Color · System colors: launcher row and summary counts to update when the bridge is back.
- **2026-11-10** — DEC-16 step 2 (tokens + code): 11 approved pairs (alert topic rows ×4 and offline header = different designs, platform-only; MISSING-ASSETS 3.4 closed; DSC-32/33). scripts/build_system_tokens.py → tokens/*/system.tokens.json (Core 11, iOS 85, Android 103), docs/SYSTEM-TOKENS.md; sd-system-formats.mjs → MNGSystemColors.swift (mng_apps_ios_ds), MngSystemColors.kt + mng_system_colors.xml (mng_apps_android_ds). Figma variables next.
- **2026-11-10** — Figma: Core **System colors** collection (11 variables, iOS/Android modes); **System colors · iOS** (85; 8 alias the Core Brand theme) in mng_apps_ios_ds's file; **System colors · Android** (103; 19 alias Brand theme) in mng_apps_android_ds's file. Core page Color · System colors: 01, 02 rebuilt, 04 launcher row moved to brand assets, 06 note. MISSING-ASSETS 3.5 (Android settings colors) for the Apps team. Karl: publish the Core library so the new collection is available.
- **2026-11-10** — Apps team (Ameer M.) confirmed the Android status-bar behavior on device: Android 14 and below = white icons, so the black/#333333 overrides are needed; Android 15+ = white status bar with dark icons (= navbar) in DP, MC, NYDN, OS, SS, TSAR, VP. Updated MISSING-ASSETS 5.6, DEC-15, docs/SHELL-EXCEPTIONS.md, data/shell-overrides.json (note; corrected attribution from Jess to Ameer M.). The Android 15+ status bar version (Karl, 2026-11-06) is now unblocked.
- **2026-11-10** — DEC-15 Android 15+ status bar (Karl, 2026-11-06; confirmed on device): data/shell-overrides.json `statusbar_icons` → tokens `statusbar.android.<m>.icons` / `icons15` (scripts/build_tokens.py); docs/SHELL-EXCEPTIONS.md gets an Android 15+ column (scripts/build_shell_colors.py). mng_apps_android_ds: MngBrandColors.kt (`statusbarFor(sdkInt)`, `statusbarDarkIconsFor(sdkInt)`), flavor XML bool + values-v35 for DP, MC, NYDN, OS, SS, TSAR, VP. Figma Android: Components · App shell › 01 rebuilt as Android 14 and below vs 15+ (new emitter scripts/figma_role_exceptions.py). Open: 15+ icons in the other 70 markets inferred light (MISSING-ASSETS 5.6 follow-up for Ameer).
- **2026-11-10** — Figma Core page Color · System colors: **07 · iOS palette values** (I02–I19, 223 colors) and **08 · Android palette values** (A02–A29, 215 colors): each exception palette's shipped value next to the majority value, swatch + hex + RGB (scripts/figma_system_colors.py 7|8 from data/system-color-comparison.json; compact payload expanded in Figma, checked identical to the full rows).
- **2026-11-10** — PLAT- tidy (Karl): PLAT-04 and PLAT-10 marked settled by what's built (DEC-14); registry notes updated. Open for Karl: PLAT-01 (ownership buckets; this page lists 4, CLAUDE.md uses 5), PLAT-08 (text size icon), PLAT-09 (Android save star).
- **2026-11-10** — Compile check on every push (GitHub Actions): mng_apps_ios_ds type-checks Tokens/ + Components/ against the iOS 15 SDK (macOS); mng_apps_android_ds compiles the Kotlin and links the resources of all 78 flavors (compile-only build.gradle.kts). Generated token files passed first time. It found two bugs in hand-written button code, both fixed: iOS `MNGPrimaryButtonStyle` (private view named `Body`, renamed) and Android duplicate `@color/mng_button_primary_label` (state list renamed `mng_button_primary_label_states`). Both green (iOS 3f7477c, Android 7bc2fd2). BACKLOG code status now reads 'written, compile-checked, not in an app yet'.
- **2026-11-10** — DEC-17 (Karl): PLAT-01 approved (CLAUDE.md's five ownership buckets), PLAT-08 approved (one Core text-size icon + iOS variant), PLAT-09 rejected (Android star and iOS bookmark stay platform-specific, one icon name). Principle: one set of icons, or at least one set of icon names. DSC-30/31, icon map notes, registry updated. All PLAT- decisions closed. Drafted the Android 15+ status-bar icon follow-up for Ameer (MISSING-ASSETS 5.6).
- **2026-11-10** — LAY-01 not pursued (Karl: document what exists): IMPROVEMENTS LAY-01 now explains the two shipped iOS sets (FrontWidth 668/835/1113 for the page layout, PageItem 668/769/1025 for card widths); both already built as shipped (DEC-12). BACKLOG suggested order refreshed.
- **2026-11-10** — Icons: combined name list as shipped (DEC-17): scripts/build_icon_names.py → data/icon-names.json, docs/ICON-NAMES.md (61 purposes → 60 names, glyphs as each app ships them); Figma Core Icons · System Comparison › **05 · Icon names**. Names for Karl to review.
- **2026-11-10** — iOS Figma Components · App shell › 01 rebuilt (intro updated); Core navbar not linked yet: library import needs the iOS file in front. Builder now imports Core navbar/navtext when no local alias exists.

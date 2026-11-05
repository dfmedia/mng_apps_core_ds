# MNG Apps Core Design System

The design system for MNG's native news apps. One **Core** system (tokens, icons, platform-neutral atoms) that feeds two platform systems, **iOS** and **Android**. Project instructions: [CLAUDE.md](CLAUDE.md). Platform repos: [mng_apps_ios_ds](https://github.com/dfmedia/mng_apps_ios_ds), [mng_apps_android_ds](https://github.com/dfmedia/mng_apps_android_ds).

This project is **completely separate from the MNG Web Design System**. It does not use the web IcoMoon icon set, web tokens or web components.

## Figma

| File | Purpose | Status |
|------|---------|--------|
| MNG Apps Core Design System (`qgL4Pj306km9NbIBIAubFg`) | Tokens, icons, core atoms | In progress |
| MNG iOS Design System (`uNxwBNoP4ODDUFGByi73mZ`) | iOS-only atoms and patterns | Created, empty |
| MNG Android Design System (`FGUeuRYhGudxo0VQdToZT9`) | Android-only atoms and patterns | Created, empty |

## Source

- iOS: TroncKit @ `e30ad2585`, extracted into the MNG iOS Style Guide artifact. 77 market apps, light mode only.
- Android: android-tribpub @ `1cfb069a6` (2026-10-15), extracted into the MNG Android Style Guide artifact. 77 market apps (Gradle flavors), light mode on most screens.

## Repo layout

```
CLAUDE.md                 project instructions — read first
PROGRESS.md               phase tracker
docs/PLATFORM-OWNERSHIP.md  Core vs iOS vs Android findings and PLAT- decisions
docs/IMPROVEMENTS.md      proposed changes to the apps (shipped values stay as-is in the DS)
docs/MISSING-ASSETS.md    what we need from the Apps team
data/source/markets.json  iOS: every resolved color for all 77 markets (124 themed colors, Style.json palette, named colors, fonts)
data/source/android-markets.json  Android: every resolved color for all 77 markets (136 themed colors, flavor palettes, fonts)
data/source/ios-tokens.json  iOS tokens: 539 brand colors, 63 text styles, spacing, radius, size, breakpoints
data/palette-analysis.json   contrast checks, suggested fixes, 45 unique palettes
data/icon-comparison.json    59 icon purposes × SF Symbols / Material Symbols / Font Awesome 5.15.1
data/icon-platform-map.json  61 icon purposes → Core / iOS only / Android only
data/color-platform-comparison.json  brand roles iOS vs Android, per market
scripts/compare_platform_colors.py  regenerates color-platform-comparison.json
scripts/icon_platform_map.py  regenerates icon-platform-map.json
scripts/analyze_palettes.py  regenerates palette-analysis.json
scripts/export_sf_symbols.swift  (run on a Mac) renders the SF Symbols used on the Icons page → assets/sf-symbols/
```

Regenerate commands are in [CLAUDE.md](CLAUDE.md#repo-layout).

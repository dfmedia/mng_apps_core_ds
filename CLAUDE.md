# Project instructions — MNG Apps Design System

Read this file first in every session. **This is the only copy of the project instructions.** Karl edits it here (locally or on GitHub); the Claude project's own instructions only point to this file. If this file and a chat request disagree, ask.

## Start of every session

1. Pull all three repos (`mng_apps_core_ds`, `mng_apps_ios_ds`, `mng_apps_android_ds`) and re-read this file if it changed.
2. Read `PROGRESS.md` for the current phase and what is waiting on review. How the three libraries fit together: `docs/ARCHITECTURE.md`.
3. Check `docs/PLATFORM-OWNERSHIP.md` for open `PLAT-` decisions before moving anything between libraries.
4. End the session by updating `PROGRESS.md` (dated log line), committing and pushing.

To change these instructions, edit this file and push. No change in Claude is needed.

## Goal

Three Figma libraries for MNG's native news apps (77 market apps per platform, one codebase each):

```
MNG Apps Core Design System   ← everything both apps share
   ├── MNG iOS Design System      ← only what iOS can't share
   └── MNG Android Design System  ← only what Android can't share
```

**The less that lives in the platform files, the better.** Default every item to Core. An item goes to a platform file only when the other app has no such thing, or the platform convention forces it (SF Symbols vs Material Symbols glyphs, status bar, notification icon).

This project is **separate from the MNG Web Design System**. Don't use web tokens, the web IcoMoon set or web components here.

## Files and repos

Each library has one Figma file and one GitHub repo. This repo (Core) is the source of truth for the instructions, the shipped-code data and every iOS vs Android comparison. The platform repos hold only what is specific to their platform, and their CLAUDE.md points back here.

| Library | Figma key | GitHub | Local folder |
|---------|-----------|--------|--------------|
| MNG Apps Core Design System | `qgL4Pj306km9NbIBIAubFg` | [kuscholdMNG/mng_apps_core_ds](https://github.com/kuscholdMNG/mng_apps_core_ds) | `~/Github/mng_apps_core_ds` |
| MNG iOS Design System | `uNxwBNoP4ODDUFGByi73mZ` | [kuscholdMNG/mng_apps_ios_ds](https://github.com/kuscholdMNG/mng_apps_ios_ds) | `~/Github/mng_apps_ios_ds` |
| MNG Android Design System | `FGUeuRYhGudxo0VQdToZT9` | [kuscholdMNG/mng_apps_android_ds](https://github.com/kuscholdMNG/mng_apps_android_ds) | `~/Github/mng_apps_android_ds` |

Sync rule: when a session changes a repo, Claude commits with a clear message and pushes. (Karl asked Claude to do all pushing through the color work.) Start every session by pulling all three. A change that touches Core and a platform goes in both repos in the same session, and each PROGRESS.md log line names the other repo.

Use the figma-console Desktop Bridge. Pass `fileKey` on every call, or `figma_navigate` with `lock: true`, because other files (including the Web DS) are often open at the same time.

## Sources (shipped code, read-only)

| Platform | Code | Style guide (Claude artifact) | Data in this repo |
|----------|------|-------------------------------|-------------------|
| iOS | TroncKit @ `e30ad2585` | https://claude.ai/artifact/V364juyHFU3STfVZ6EgjMc | `data/source/markets.json`, `data/source/ios-tokens.json` |
| Android | android-tribpub @ `1cfb069a6` (dev, 2026-10-15) | https://claude.ai/artifact/5MyLP13QSt52WGRgXW35ZJ | `data/source/android-markets.json` |

Brand colors also come from the **migration sheet** "Tribpub-MNG App Migrations" (Google Sheet `1PGCnV0mSnOMOycNT-CSViYKyH82TrnwPSO4VrCl_HS4`, tab Production, Primary / Secondary color), copied to `data/source/migration-sheet-brand-colors.json`. It is the source of truth when it matches either app.

When the app team sends a new export, update `data/source/`, re-run the scripts and note the new commit here.

## Ownership buckets

Every token, icon and component gets exactly one:

| Bucket | Rule | Goes to |
|--------|------|---------|
| **Core** | Both apps have it. Values are the same or near-identical hexes (OKLab ΔE < 0.012: off by 1 in a channel, invisible). | Core |
| **Core, per-platform value** | Both apps have it, but values differ. Keep one Core variable; record the difference as a decision for Karl. Don't split it out yet. | Core (flagged) |
| **Core alias** | A role that equals another role almost everywhere (e.g. `buy` = `action`). | Core, as an alias |
| **iOS only** / **Android only** | The other app has no such thing. | Platform file (later) |

Thresholds: same < 0.012 ΔE · close < 0.05 · differs ≥ 0.05. Contrast targets: text 4.5:1, icons and large text 3:1.

## Rules

0. **Record every approved decision** in `docs/DECISIONS.md` (DEC- ID, rule, date, what changed). **Log every iOS/Android difference that should match** in `docs/DISCREPANCIES.md` (DSC- ID, right value, evidence, which app to fix).
1. **Shipped values are documented exactly as shipped**, failing ones included. Proposed changes go in `docs/IMPROVEMENTS.md` (iOS-era IDs) or `docs/PLATFORM-OWNERSHIP.md` (`PLAT-` IDs) and are shown beside the shipped value, never instead of it.
2. **One phase at a time.** Karl reviews each phase before the next starts. Track it in `PROGRESS.md` and add a dated line to its Log.
3. **Plan before work.** For anything beyond adding review pages or sections, post the plan and wait for an OK.
4. **Figma edits are additive.** Add new sections (`NN · Title`) beside existing ones and never overwrite or delete Karl's content. Re-running a build replaces only the section it created. Screenshot each section after building it.
5. **Tokens are the delivery format.** Colors (and later type, spacing, radius) live as DTCG tokens in `tokens/`; Swift and Kotlin are generated, never hand-written. Always document colors as hex and RGB.
6. **Data first, then Figma.** Every Figma table comes from a JSON in `data/` that a script in `scripts/` regenerates. Never type values by hand.
7. **Don't invent.** If the source doesn't say, write "unknown, ask Apps team" and add it to `docs/MISSING-ASSETS.md`.
8. **Moving items to the platform files** happens only after Karl approves the ownership page for that area.

## Figma page style (match the existing pages)

- Open Sans: titles Bold 32/44, body Regular 13–16, table text 11–13.
- Tables: white frame, 64 px padding; group rows `#1a1a1a` with white text; rows divided by a 1 px `#e6e6e6` bottom border.
- Ownership chips (always with a text label, never color alone): Core `#e6f4ea`/`#14532d` · Core + variant `#fff4d6`/`#6b4500` · iOS only `#e3eefc`/`#0b3d7a` · Android only `#efe7fb`/`#43217a` · Differs `#fde8e8`/`#8a1c1c`.

## Repo layout

```
CLAUDE.md                         this file (platform repos point here)
PROGRESS.md                       phase tracker + log (start here for status)
docs/ARCHITECTURE.md              how Core, iOS and Android fit together (registry, variables, wayfinding)
docs/PLATFORM-OWNERSHIP.md        Core vs iOS vs Android findings and PLAT- decisions
docs/DECISIONS.md                 approved decisions (DEC- IDs): rule, date, what changed
docs/DISCREPANCIES.md             iOS vs Android differences that should match (DSC- IDs), with the right value and which app to fix
docs/REGISTRY.md                  generated: every item and its owner (from data/registry.json)
docs/BACKLOG.md                   generated: what is left to build in Figma and export to GitHub (status in data/backlog-status.json)
docs/IMPROVEMENTS.md              proposed app changes (contrast, merges…)
docs/MISSING-ASSETS.md            what we need from the Apps team
docs/components/                  component specs (generated, e.g. BUTTON.md)
tokens/                           DTCG design tokens (generated; the source for Swift, Kotlin and Figma)
style-dictionary.config.mjs       builds Swift / Kotlin / Android XML from tokens/
docs/BRAND-COLORS.md              every brand color as hex and RGB (generated)
data/source/                      raw exports from each app (don't edit)
data/*.json                       generated analysis
scripts/                          regenerate data/*.json
```

Regenerate:

```
python3 scripts/analyze_palettes.py data/source/markets.json data/palette-analysis.json
python3 scripts/compare_platform_colors.py data/source/markets.json data/source/android-markets.json data/color-platform-comparison.json
python3 scripts/icon_platform_map.py data/icon-comparison.json data/icon-platform-map.json
python3 scripts/component_platform_map.py data/component-platform-map.json
python3 scripts/resolve_brand_colors.py data/source/markets.json data/source/android-markets.json data/source/migration-sheet-brand-colors.json data/brand-color-resolution.json
python3 scripts/apply_web_alignment.py data/brand-color-resolution.json data/source/cluster-audit-web-colors.json   # DEC-02, right after resolve
python3 scripts/apply_ios_default.py data/brand-color-resolution.json data/color-platform-comparison.json   # DEC-03
python3 scripts/apply_core_alert.py data/brand-color-resolution.json data/source/markets.json   # DEC-05 (fails if below WCAG AA)
python3 scripts/apply_new_markets.py data/brand-color-resolution.json data/source/new-markets.json   # provisional markets (TDH)
python3 scripts/build_tokens.py     # tokens/*.tokens.json + docs/BRAND-COLORS.md
python3 scripts/build_button_tokens.py   # button tokens, data/button-spec.json, docs/components/BUTTON.md, IMPROVEMENTS CLR-04 (DEC-07)
python3 scripts/select_theme_modes.py   # the 20 Figma Brand theme modes (DEC-06)
npm install && npm run build        # Style Dictionary → ../mng_apps_ios_ds/Tokens, ../mng_apps_android_ds/tokens
python3 scripts/compare_type.py     # typography step 1: data/type-comparison.json + docs/TYPE-COMPARISON.md
python3 scripts/build_registry.py   # run last; reads the two maps above
python3 scripts/build_backlog.py    # after the registry: docs/BACKLOG.md from data/backlog-status.json (edit that file to mark progress)
```

## People

- Karl: design system owner. Approves every phase.
- Apps team contacts: Jess Navaro, Patrick Carr.

## Working style

- Keep replies short. Lead with what changed and what needs a decision.
- Put long findings in `docs/`, not in chat.
- Say which commit and which file a number came from.

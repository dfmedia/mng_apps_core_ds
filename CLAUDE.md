# Project instructions — MNG Apps Design System

Read this file first in every session. **This is the only copy of the project instructions.** Karl edits it here (locally or on GitHub); the Claude project's own instructions only point to this file. If this file and a chat request disagree, ask.

## Start of every session

Karl can start a session with just "continue". Do these in order, without asking:

1. **Repos.** Attach the three dfmedia repos with push access (`add_repo`, `access: "push"`), clone each into `/home/claude/<repo>` one at a time, then `register_repo_root`. Re-read this file if it changed.
2. **Delete permission.** Ask once for delete permission on the three local folders (`device_request_delete_permission` on `~/Github/mng_apps_core_ds`, `_ios_ds`, `_android_ds`). Git deletes its own lock and temp files, and the permission resets every session. If a local pull already failed with "unable to unlink", get the permission, remove the leftover `.git/*.lock` and `.git/objects/**/tmp_obj_*`, check `git status` is clean, and pull again.
3. **Pull** all three, both the cloud clones and Karl's local folders (`device_bash`: `git pull --ff-only`).
4. **Read** the **Next session** handoff at the top of `PROGRESS.md` and the last ~10 log lines, the Summary of `docs/BACKLOG.md`, and `docs/MISSING-ASSETS.md` (look for new Apps team answers). How the libraries fit together: `docs/ARCHITECTURE.md`. Check `docs/PLATFORM-OWNERSHIP.md` for open `PLAT-` decisions before moving anything between libraries.
5. **Report** in a few lines: what changed since last time, what is unblocked, what you propose next. Then wait for an OK before building (rule 3).

**Where to work.** Edit, run scripts and commit in the cloud clones (`/home/claude/<repo>`), push, then `git pull --ff-only` in Karl's local folders so his copy stays current. Don't edit the local folders directly.

**Compile check.** Every push to mng_apps_ios_ds / mng_apps_android_ds runs GitHub Actions (about 2–3 minutes). Check it with `gh api "repos/dfmedia/<repo>/actions/runs?head_sha=<sha>" --jq '.workflow_runs[] | [.name,.status,.conclusion,.html_url] | @tsv'`; use Claude in Chrome only if the API is blocked. Fix a red run before anything else.

**End of session.** Add a dated log line to `PROGRESS.md` (and to the platform repo's when it changed), refresh the **Next session** handoff, commit, push, and pull into the local folders.

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
| MNG Apps Core Design System | `qgL4Pj306km9NbIBIAubFg` | [dfmedia/mng_apps_core_ds](https://github.com/dfmedia/mng_apps_core_ds) | `~/Github/mng_apps_core_ds` |
| MNG iOS Design System | `uNxwBNoP4ODDUFGByi73mZ` | [dfmedia/mng_apps_ios_ds](https://github.com/dfmedia/mng_apps_ios_ds) | `~/Github/mng_apps_ios_ds` |
| MNG Android Design System | `FGUeuRYhGudxo0VQdToZT9` | [dfmedia/mng_apps_android_ds](https://github.com/dfmedia/mng_apps_android_ds) | `~/Github/mng_apps_android_ds` |

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
8. **Match production (DEC-09).** Components and text styles are built exactly as they ship. Fonts stay per platform. Where no token exists for a value yet, use the raw production value; proposed changes go in IMPROVEMENTS.
9. **Moving items to the platform files** happens only after Karl approves the ownership page for that area.

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
docs/ICON-NAMES.md                generated: one icon name per purpose, with what each app ships (DEC-17)
docs/MISSING-ASSETS.md            what we need from the Apps team
docs/STYLE-GUIDE-INVENTORY.md     what the Apps team style guides contain vs what we have built (2026-11-10)
docs/GUIDE-EXTRAS.md              generated: style-guide items documented as shipped (ad slots, What's New button, widget, eEdition colors, images)
docs/components/                  component specs (generated, e.g. BUTTON.md, CHECKBOX-IOS.md)
docs/ORIENTATION.md               generated: phone / tablet / foldable orientation as shipped
docs/LEGACY-TEMPLATE.md           generated: iOS legacy-template values, acknowledged only (DEC-10)
tokens/                           DTCG design tokens (generated; the source for Swift, Kotlin and Figma)
style-dictionary.config.mjs       builds Swift / Kotlin / Android XML from tokens/
docs/BRAND-COLORS.md              every brand color as hex and RGB (generated)
data/source/                      raw exports from each app (don't edit)
data/*.json                       generated analysis
scripts/                          regenerate data/*.json
scripts/figma/                    Figma builders run through the Desktop Bridge (figma_execute), fed by data/*.json
```

Regenerate:

```
python3 scripts/analyze_palettes.py data/source/markets.json data/palette-analysis.json
python3 scripts/compare_platform_colors.py data/source/markets.json data/source/android-markets.json data/color-platform-comparison.json
python3 scripts/icon_platform_map.py data/icon-comparison.json data/icon-platform-map.json
python3 scripts/build_icon_names.py   # DEC-17: combined icon name list as shipped (data/icon-names.json, docs/ICON-NAMES.md); after icon_platform_map.py
python3 scripts/figma_icon_names.py    # prints JS for Core Icons · System Comparison › 05 · Icon list (combined: names, what ships, reference glyphs copied from 02)
python3 scripts/component_platform_map.py data/component-platform-map.json
python3 scripts/resolve_brand_colors.py data/source/markets.json data/source/android-markets.json data/source/migration-sheet-brand-colors.json data/brand-color-resolution.json
python3 scripts/apply_web_alignment.py data/brand-color-resolution.json data/source/cluster-audit-web-colors.json   # DEC-02, right after resolve
python3 scripts/apply_ios_default.py data/brand-color-resolution.json data/color-platform-comparison.json   # DEC-03
python3 scripts/apply_core_alert.py data/brand-color-resolution.json data/source/markets.json   # DEC-05 (fails if below WCAG AA)
python3 scripts/apply_new_markets.py data/brand-color-resolution.json data/source/new-markets.json   # provisional markets (TDH)
python3 scripts/build_tokens.py     # tokens/*.tokens.json + docs/BRAND-COLORS.md
python3 scripts/build_shell_colors.py   # DEC-13/15: app shell colors (tokens/*/shell.tokens.json, data/shell-colors.json incl. header/statusbar exceptions)
python3 scripts/figma_role_exceptions.py ios|android   # DEC-15 Figma samples (Components · App shell › 01) from data/shell-colors.json; prints JS for figma_execute
python3 scripts/build_control_tokens.py   # DEC-14: control colors, majority values (tokens/*/controls.tokens.json, docs/CONTROL-EXCEPTIONS.md)
python3 scripts/build_button_tokens.py   # button tokens, data/button-spec.json, docs/components/BUTTON.md, IMPROVEMENTS CLR-04 (DEC-07)
python3 scripts/select_theme_modes.py   # the 20 Figma Brand theme modes (DEC-06)
npm install && npm run build        # Style Dictionary → ../mng_apps_ios_ds/Tokens, ../mng_apps_android_ds/tokens
python3 scripts/compare_type.py     # typography step 1: data/type-comparison.json + docs/TYPE-COMPARISON.md
python3 scripts/build_type_tokens.py   # DEC-09: tokens/*/type.tokens.json, data/type-styles.json, docs/TYPE-STYLES.md (before npm run build)
python3 scripts/build_legacy_doc.py    # DEC-10: docs/LEGACY-TEMPLATE.md (run after build_type_tokens.py)
python3 scripts/build_font_exceptions.py   # per-market fonts as shipped: data/type-font-exceptions.json, docs/TYPE-FONT-EXCEPTIONS.md
python3 scripts/figma_font_exceptions.py 4|5   # prints JS for Core Type · iOS vs Android › 04 iOS / 05 Android per-market fonts
python3 scripts/build_ios_checkbox.py      # iOS checkbox as shipped (image sets): data/ios-checkbox.json, docs/components/CHECKBOX-IOS.md
python3 scripts/figma_ios_checkbox.py upload <file>|build   # iOS file Components · Controls › 02 · Checkbox: images one per call (length + hash checked), then the build
python3 scripts/build_orientation.py      # orientation as shipped: data/orientation.json, docs/ORIENTATION.md (from data/source/orientation.json)
python3 scripts/figma_orientation.py      # prints JS for Core Layout · iOS vs Android › 01 · Orientation
python3 scripts/build_guide_extras.py     # DEC-18: style-guide extras as shipped: data/guide-extras.json, docs/GUIDE-EXTRAS.md, tokens/android/guide-extras.tokens.json (before npm run build)
python3 scripts/figma_guide_extras.py vars|core-ads|android-ads <key>|android-widget|android-eedition|whats-new   # prints JS for the DEC-18 Figma sections
python3 scripts/compare_scales.py   # spacing/radius/size/breakpoints comparison: docs/SCALES-COMPARISON.md
python3 scripts/build_scale_tokens.py   # DEC-11: tokens/*/scale.tokens.json (before npm run build)
python3 scripts/compare_system_colors.py   # system colors step 1: data/system-color-comparison.json + docs/SYSTEM-COLORS.md (pairs: data/system-color-pairs.json)
python3 scripts/build_system_tokens.py     # DEC-16: tokens/*/system.tokens.json, data/system-tokens.json, docs/SYSTEM-TOKENS.md (before npm run build)
python3 scripts/build_registry.py   # run last; reads the two maps above
python3 scripts/build_backlog.py    # after the registry: docs/BACKLOG.md from data/backlog-status.json (edit that file to mark progress)
```

## People

- Karl: design system owner. Approves every phase.
- Apps team contacts: Jess Navaro, Patrick Carr, Ameer M. (Android).

## Vocabulary

- **App shell** = what the registry and older docs call "App chrome" (top bar, section tabs, bottom tab bar, breaking-news banner, section header band, status bar). Use "app shell" in conversation to avoid confusion with the Chrome browser; existing docs keep their wording.

## Working style

- Keep replies short. Lead with what changed and what needs a decision.
- Put long findings in `docs/`, not in chat.
- Say which commit and which file a number came from.

### Running Figma builds
- `figma_execute` can't read files: run the emitter (`python3 scripts/figma_*.py …`), then paste the printed JS. Several table sections for the same file can go in one call if each builder run is wrapped in its own scope.
- `figma_capture_screenshot` has no `fileKey`: lock the file first with `figma_navigate` (`lock: true`).
- Check `figma_list_open_files` before building; all three DS files must have the Desktop Bridge plugin open.

### Figma library imports stall (2026-11-05)
If `importVariableByKeyAsync` / `importComponentByKeyAsync` hang in a platform file while library listing works, the file has unaccepted Core library updates: ask Karl to accept them (Assets → Libraries → Update all). For a component the file has never used, Karl can drag one instance in from Assets; the build script then wraps that instance.
If the import still stalls after Karl accepts, retry once (2026-11-10: the Android ad slot import worked right after Karl accepted and published).

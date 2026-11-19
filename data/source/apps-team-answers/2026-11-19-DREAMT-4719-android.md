# Apps team answers — Android (DREAMT-4719), 2026-11-19

Source data: do not edit. Copied from Rajal Patel's two comments on [DREAMT-4719](https://digital1stmedia.atlassian.net/browse/DREAMT-4719): 276725 (2026-11-19 09:31 MT, "the 4 most important questions") and 276735 (10:13 MT, the rest). They answer docs/MISSING-ASSETS.md as numbered on 2026-11-19 (DEC-20: numbers kept). Code: android-tribpub (commit not stated; our export is `1cfb069a6`). Formatting converted from Jira to Markdown; wording unchanged. Comment 276735 repeats the 5.6 answer from 276725 word for word; it is kept once below. Rajal says the 5.3 screenshots will follow in a separate comment.

---

## Comment 276725 (09:31 MT)

Thank you @Karl Uschold. Here are the answers to your 4 most important questions. Will answer the others shortly.

- **5.5** Saratogian status bar: the answer is **no**. On Android 15+ it shows an off-white #F5F5F5 bar with white icons, which are barely visible.
  - **Shell sizes**:
    - Top bar: 56dp tall on phones, 64dp on tablets; title in Roboto Medium 16sp, all caps.
    - Section tabs: 48dp tall; labels in Open Sans SemiBold 12sp; 3dp indicator.
    - Bottom nav: 56dp tall; 24dp icons; labels in Roboto Regular 10sp.
    - Breaking-news banner: Open Sans Bold 14sp, white on #CF000E.
- **5.4:** No app-wide button style; plain Buttons get Material library defaults:
  - Main screens (MaterialComponents theme): Roboto Medium 14sp, ALL CAPS, letterSpacing 0.0893.
  - Settings / web view / paywall (Material3 theme): Roboto Medium 14sp, sentence case, line height 20sp.
  - Blocking paywall Subscribe: 60dp, no size/font set → Roboto Medium 14sp, all caps, white.
  - Subscription options buttons: Roboto Bold 16sp, white.
  - Pressed state: none designed. Material ripple on Material buttons, ?selectableItemBackground ripple on some views; the monthly subscription option has no pressed state. A few legacy selectors exist (e.g. What's New close: pressed #FF6859; update-app dialog button #076C9C → #6E8D9B pressed).
- **5.6:**
  - Alerts Enable ("CUSTOMIZE"): Roboto Medium 14sp all caps, 10dp padding (~40dp tall), full width, fill #FF6859 (same in every market), white text. "NO, THANKS" is transparent with black text. The Alerts-tab "Enable Alerts" is a system AlertDialog button.
  - What's New button ("EXPLORE THE FEATURES"): Open Sans Bold 14sp (18sp landscape, 25sp tablet), all caps, white. 15dp padding (~50dp tall), 6dp radius, fill whats_new_button_color (per market).
  - Segmented control (MaterialButtonToggleGroup): track #EEEEEE with 24dp radius. Selected segment @color/white (#FFFFFF; #F5F5F5 in tsar) with black text; unselected transparent with #696969 text; 17sp bold.
  - Loading indicators: section-front spinner #D5D5D5 (55dp); section-front top bar gradient #49B0D6→#35B5E4 (2dp); generic spinner #E0E6EC→#2A5381; paywall spinner #2A2A2A; web-view bar #1E88E5 on #E3F2FD; other ProgressBars use each market's MainStyle_Control_Activated.
- **3.3** Settings_Background: nobody sees #333333. The Settings theme paints the screen white in every market, so the 1.7:1 contrast problem never appears.
  - Why it never shows: every market sets that screen to white one way or another.
    - The ~70 markets that keep #333333: each one's own Settings theme sets both the window background and the default background of every view to white. The settings list and each row are painted white on top of the #333333 frame, and the window behind it is white too.
    - The other 7 (ct, dp, hc, mc, nydn, tod, vp): they set Settings_Background itself to white.
    - Overall, the design team can treat Settings_Background as **unused.**

## Comment 276735 (10:13 MT)

@Karl Uschold I added some more answers to your listed questions from the previous comment. For 5.3, I'll attach the screenshots in a separate comment.

**1.10:** Android already uses 10s, not 15s. AppPlaybackService SEEK_INCREMENT_MS = 10_000 with Media3 skip_back_10 / skip_forward_10 icons, hardcoded. Material Symbols' 10s icons work as they are.

**4.4:** Android top bar title = Roboto Medium 16sp, all caps (MC.TextAppearance.AppCompat.Widget.ActionBar.Title). Two screens (restaurants and the corekit settings) use the plain AppCompat title instead: Roboto Medium 20dp.

**4.5:** Neither loads; both fall back silently to the system font (Roboto Regular), no crash.

- NYDN OpenSansCondensed-Bold.ttff: Calligraphy catches the failed createFromAsset and leaves the default typeface. Affects the time/blurb line in notification/stream lists. Fix: rename to .ttf.
- MC OpenSans-Semibold.ttf: asset names are case-sensitive, so it would not load, but Article_Byline_Regular / Article_Dateline_Regular aren't referenced by any style. MC bylines/datelines actually use OpenSans-Bold.ttf (the *_Bold strings).

**5.1:** Toolbar 4dp on scroll (0 at rest). Settings, web and login toolbars 1dp. Section tabs 2dp. Cards 3dp (special-section cards 4dp). No design-system elevation scale.

**5.2:** No specs. Hardcoded only: footer ad slide 200ms; list item animator 300ms decelerate; section layout transition 300ms; slide_up/down use the system medium duration with accelerate; pulse 280ms scale 1.1; shimmer 1000–1200ms linear loop.

**5.6:** (same as in comment 276725)

**5.9:** Widget colors (no market overrides):

- widget_bg #FFFFFF / night #000000
- widget_text_main #000000 / night #FFFFFF
- widget_divider1 #000000 / night #FFFFFF
- widget_divider2 #B8B8B8 / night #B8B8B8
- Size: minWidth 300dp, minHeight 170dp, target 2x1 cells, not resizable, refreshes every 30 min.
- Layout: 16dp rounded card, 16dp padding. Date 12sp top-right. Logo 145x25dp. 2dp divider1. Lead row has a 66dp-wide thumbnail (7dp corners) and a bold 15sp headline (max 3 lines). 2px divider2 at 12dp. Second headline bold 16sp (max 2 lines).

# Questions for the Apps team

What the MNG Apps design system still needs from the Apps team (Jess Navaro, Patrick Carr, Ameer M.). Each question has a number. Please answer in the Jira ticket for this list, starting each answer with its number, for example "5.6: …". Partial answers help too.

We work from the shipped code (iOS TroncKit @ `e30ad2585`, Android android-tribpub @ `1cfb069a6`) and the two Apps team style guides. Everything here is something those don't tell us.

## Most needed

1. **5.6** App shell sizes, and the Saratogian status bar on Android 15+
2. **5.5** Button values
3. **5.7** Other buttons and controls
4. **5.8** iOS Your News checkbox
5. **4.4** Missing text styles
6. **4.5** Two Android font file names
7. **3.5** Android settings colors

Then the icon questions (section 1).

## 1. Icons

| # | Question | What we know |
|---|---|---|
| 1.1 | Can you send vector masters (SVG or PDF) for the icon images, or confirm none exist? | iOS: 213 of 218 images are PNG exports. Android: the style guide has 126 PNG and 12 SVG exports, not masters. Most useful first: nav bar, tab bar, general, player controls. |
| 1.2 | What should `ManageSubscriptionIcon` show? | The iOS image set has no image file. |
| 1.3 | Which icon was meant for the iOS Saved tab? | `CoreTabBarViewController.swift:140` uses `"saved"`, which isn't an SF Symbol, so nothing shows. |
| 1.4 | Which markets override tab icons, and can we have their vector files? | 9 markets ship their own Home tab icon; 2 override the Font Awesome tab icons. |
| 1.5 | Is there an intended design for these, or is it OK to use each platform's own symbols? | Text size small / large, Games tab, ±15 s skip, Filter, Follow / Unfollow topic. |
| 1.6 | Is it OK to replace each set of per-market recolored icons with one tinted icon? | `Saved-*`, `Checkmark-*`, `Uncheck-*`, `YourNews-*`, `Continue-*`, `TopicSelection-*` are the same glyph in different colors. |
| 1.8 | Is there a master vector for the For You / Your News tab icon? | No match in SF Symbols, Material Symbols or Font Awesome. |
| 1.9 | What does the iOS Digital tab open? | We need it to choose the icon. |
| 1.10 | What are the names of the six SF Symbols in tournament loading? | |
| 1.11 | Android: is 15 s skip required, or would 10 / 30 s work? | Material Symbols only has 5 / 10 / 30 s; 15 s needs a custom icon. |
| 1.12 | Can you send current official vectors for the brand marks? | Apple, Google, Facebook, X, Bluesky, Instagram, YouTube, Vimeo, Amazon, 1Password, Outbrain. |

## 2. Logos and artwork

| # | Question | What we know |
|---|---|---|
| 2.1 | Can you send vector masters for each market's app icon, main logo, lettermark, paywall logo and masthead? | 3–19 files per app, 77 apps. |
| 2.2 | What do markets without onboarding art show? | iOS has onboarding images only for BS, CT, DP, HC, MC, NYDN, OS, SS and VP. |

## 3. Color

| # | Question | What we know |
|---|---|---|
| 3.1 | Some iOS theme colors are left unset, so iOS uses its system default. Intended, or a missing value? | Unset in every market: `sectionListSectionSeparatorColor` (Android uses #f1f1f1 here) and `trackingConsentSwitchOnTintColor`. Unset in NYDN and OS only: `offlineViewSwitchTintColor` (every other market sets it). |
| 3.2 | Are there any plans for dark mode? | Both apps are light-only today. |
| 3.5 | Where is Android `Settings_Background` used? | #333333 in 70 of 77 markets, with black text on it (`Settings_Item`, `Settings_Category_Item`, `Settings_Summary_Item`): 1.7:1 contrast. |

## 4. Type

| # | Question | What we know |
|---|---|---|
| 4.1 | Which Open Sans Condensed files does NYDN bundle, and do they match the Google Fonts version? | Only NYDN uses it. |
| 4.2 | What is the intended text-size scale for article text? | Article text has 6 sizes (15 % steps) or follows the iOS text size setting; other screens are fixed. |
| 4.3 | Are Open Sans Light and ExtraBold used on iOS? If so, can you send the font files? | iOS bundles Light, Light Italic, ExtraBold and ExtraBold Italic; Figma's Open Sans doesn't have them. |
| 4.4 | What are the font and size for these text styles? | iOS: section tabs, settings rows and headers, search result headline. Android: top bar title, and the font for `ArticleText.Subhead.Wapo` (size 14sp). |
| 4.5 | Do these two Android font files load, or fall back to the system font? | NYDN `StreamModule_Font_Time_And_Blurb` → `OpenSansCondensed-Bold.ttff` (double f). MC `Article_Byline_Regular` and `Article_Dateline_Regular` → `OpenSans-Semibold.ttf` (the bundled file is `OpenSans-SemiBold.ttf`). |

## 5. Components

| # | Question | What we know |
|---|---|---|
| 5.2 | Are there shadow / elevation values? | None found in the code. |
| 5.3 | Are there animation specs? | None found in the code. |
| 5.4 | Can you send screenshots of key screens for a few markets? | Nav, section front, article, paywall, settings. We use them to check our work. |
| 5.5 | What are these button values? | iOS primary button height (we use 44 pt for now). Android button label weight and size (we use Roboto Medium 14sp). iOS paywall Log In link font (we use Open Sans Regular 14). Pressed state on both apps. |
| 5.6 | What are the production app shell sizes? And does Saratogian show a white status bar with dark icons on Android 15+ in production? | Sizes: heights, paddings and title / label text sizes for the top bar, section tabs, bottom tab bar and breaking-news banner (both apps), plus the iOS section header band. The style guides only have example values. Saratogian: the export's bar color is #F5F5F5, which by `EdgeToEdgeUtil.java:30` gives white icons. |
| 5.7 | What are the font, size and height of the remaining buttons, and the colors of two controls? | Buttons: iOS notification prompt Yes / No, Manage subscription / Delete account, savings label, social sign-in (Apple, Google, Facebook), Android Alerts Enable and What's New. Colors: segmented control and loading indicator, both apps. |
| 5.8 | iOS Your News checkbox: are the images centered at natural size, or scaled? Which markets use `Uncheck-Grey`? | The control is 30 × 30 pt; the images are 17 × 18 pt. |
| 5.9 | What ad slot sizes does iOS request? Is the iOS adhesion banner the same as the Android sticky footer? | Android: 320 × 50 phone / 728 × 90 tablet for the first slot and the sticky footer, 300 × 250 for the others. |
| 5.10 | Android home-screen widget: what are the night colors, and the layout and sizes? | `values-night` changes `widget_bg`, `widget_divider1`, `widget_divider2` and `widget_text_main`; the values aren't in the style guide. |

## 6. Platform

| # | Question | What we know |
|---|---|---|
| 6.2 | Is TroncKit `e30ad2585` still the current iOS commit? | |

## Answered and closed

| # | What | Outcome |
|---|---|---|
| 1.7 | Android icon set | Answered: the Android style guide carries 138 exported assets (126 PNG, 12 SVG), including the 77 market Home tab icons. Masters are still needed: see 1.1. |
| 3.3 | Confirm the iOS-default brand colors | Closed 2026-10-26 without asking: Karl confirmed iOS as the default (DEC-08). |
| 3.4 | iOS and Android system-color pairs | Closed 2026-11-10 without asking: 11 pairs approved by Karl; the rest are platform-only. |
| 5.1 | Missing button states | Closed 2026-11-10: Secondary and Loading are not designed; neither app ships them. |
| 5.6 (part) | Android status-bar icons | Answered by Ameer M. (2026-11-05, confirmed on device 2026-11-10): the main theme never sets `windowLightStatusBar`. Android 14 and below: white icons. Android 15+: `EdgeToEdgeUtil.java:30` gives dark icons only when `NavigationBar_Background` is exactly #FFFFFF (DP, MC, NYDN, OS, SS, VP), white icons otherwise. Saratogian is still open in 5.6. |
| 6.1 | Android source | Closed 2026-11-10: android-tribpub @ `1cfb069a6` export and the Android style guide. |

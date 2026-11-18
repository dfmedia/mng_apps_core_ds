# Questions for the Apps team

What the MNG Apps design system still needs from the Apps team (Jess Navaro, Patrick Carr, Ameer M.). Each question has a number. Please answer in the Jira ticket for the app the question is about, starting each answer with its number, for example "5.5: …". Questions about both apps can go in either ticket. Partial answers help too.

- iOS: [DREAMT-4718](https://digital1stmedia.atlassian.net/browse/DREAMT-4718)
- Android: [DREAMT-4719](https://digital1stmedia.atlassian.net/browse/DREAMT-4719)

We work from the shipped code (iOS TroncKit @ `f79fe3339` per your latest answers, our export is `e30ad2585`; Android android-tribpub @ `1cfb069a6`) and the two Apps team style guides. Everything here is something those don't tell us.

**Numbers don't change.** When a question is answered we remove it and leave a gap, so the numbers you have quoted stay the same.

**Thank you for the iOS answers.** Most iOS questions are now closed, and several below are down to their Android half. We are still reviewing your answer to 1.11: nothing more is needed on it for now. 1.3, 1.4, 1.8, 2.1, 4.1 and 6.1 have follow-up questions.

## Most needed

1. **5.5** Android app shell sizes, and the Saratogian status bar on Android 15+
2. **6.1** The iOS export at `f79fe3339`
3. **1.3 / 1.4 / 1.8** iOS tab bar: Saved icon, market tab icons, the e-edition tab and Patrick's newspaper icon (follow-ups)
4. **2.1** Logo files for every market
5. **5.4** Android button values
6. **5.6** Other Android buttons and controls
7. **4.4** Android top bar title style
8. **4.5** Two Android font file names
9. **3.3** Android settings colors

## 1. Icons

| # | Question | What we know |
|---|---|---|
| 1.1 | Android: can you send vector masters (SVG or PDF) for the icon images, or confirm none exist? | iOS: none exist (213 of 218 images are PNG exports; the only vectors are the 4 Author Profile SVGs). Android: the style guide has 126 PNG and 12 SVG exports, not masters. Most useful first: top bar, bottom navigation, general, player controls. |
| 1.3 | iOS Saved tab: which icon should it show, and is a fix planned? | Your answer: the tab calls `UIImage(systemName: "saved")`, which returns no image, so the tab shows no icon. Android shows a bookmark (`mc_tab_icon_saved`). Was the intent an SF Symbol such as `bookmark` / `bookmark.fill`, or a custom image? |
| 1.4 | Which markets override which tab-bar icons, what are the image set names, and can you send the files? | Your answer: 9 markets (CT, BS, DP, MC, NYDN, SS, VP, HC, OS) have their own Home icon and their own selected For You icon; Sections and Alerts use Font Awesome `bars` and `bell` everywhere. The earlier iOS style guide said 2 markets override the Font Awesome tab icons: which 2 markets and which icons, or is that out of date? Please send the 18 Home and For You files (PNG is fine). |
| 1.8 | iOS: what is the e-edition tab called and which icon does it use at `f79fe3339`, and is it in the export you're sending for 6.1? Could you also ask Patrick Carr for his newspaper icon (the vector source, and where it lives)? | Your answer: there's no Digital tab anymore; "Digital" was another name for the eNewspaper tab, and that code is commented out. Our `e30ad2585` export has two tab icons, `tab-enews` and `tab-newspaper`, and the e-edition was planned to move into the bottom navigation as "Newspaper". Patrick shared a newspaper icon as a PNG on Oct 21 (a newspaper with a folded edge, an image block and text lines): is that the one that ships, and is there a vector? Which markets show the tab, and does it open the native eNewspaper viewer? |
| 1.10 | Android: is 15 s skip required, or would 10 / 30 s work? | Material Symbols only has 5 / 10 / 30 s; 15 s needs a custom icon. |
| 1.11 | Can you send current official vectors for the brand marks? | Apple, Google, Facebook, X, Bluesky, Instagram, YouTube, Vimeo, Amazon, 1Password, Outbrain. |

## 2. Logos and artwork

| # | Question | What we know |
|---|---|---|
| 2.1 | Can you send every market's logo files: app icon, main logo, lettermark, paywall logo and masthead? Vectors where they exist, PNG otherwise. | iOS: 31 markets ship their main logo and lettermark as vectors, and PAC, SIT and TPD have vector logos too; please send those vector files. 3–19 files per app, 77 apps. |

## 3. Color

| # | Question | What we know |
|---|---|---|
| 3.3 | Where is Android `Settings_Background` used? | #333333 in 70 of 77 markets, with black text on it (`Settings_Item`, `Settings_Category_Item`, `Settings_Summary_Item`): 1.7:1 contrast. |

## 4. Type

| # | Question | What we know |
|---|---|---|
| 4.1 | Can you send the three Open Sans Condensed font files NYDN bundles (Bold, Light, Light Italic), or include them in the 6.1 export? | Your answer: NYDN bundles Bold, Light and Light Italic. We'll compare them with the Google Fonts version we use in Figma. |
| 4.4 | Android: what are the font and size of the top bar title? | iOS is answered; this is the last missing text style. |
| 4.5 | Do these two Android font files load, or fall back to the system font? | NYDN `StreamModule_Font_Time_And_Blurb` → `OpenSansCondensed-Bold.ttff` (double f). MC `Article_Byline_Regular` and `Article_Dateline_Regular` → `OpenSans-Semibold.ttf` (the bundled file is `OpenSans-SemiBold.ttf`). |

## 5. Components

| # | Question | What we know |
|---|---|---|
| 5.1 | Android: are there shadow / elevation values? | iOS sets each shadow where it's used, with no shared scale. None found in the Android code. |
| 5.2 | Android: are there animation specs? | iOS sets each duration where it's used, with no shared spec. None found in the Android code. |
| 5.3 | Android: can you send screenshots of key screens for a few markets? | Nav, section front, article, paywall, settings. We have the iOS ones (TDP, NYDN, VP), so the same markets would be ideal. We use them to check our work. |
| 5.4 | Android: what are the button label weight and size, and is there a pressed state? | Paywall Subscribe: 60 dp tall, square, white uppercase system font. We use Roboto Medium 14sp for now. |
| 5.5 | Android: what are the production app shell sizes? And does Saratogian show a white status bar with dark icons on Android 15+ in production? | Sizes: heights, paddings and title / label text sizes for the top bar, section tabs, bottom navigation and breaking-news banner. The style guide only has example values. iOS is answered. Saratogian: the export's bar color is #F5F5F5, which by `EdgeToEdgeUtil.java:30` gives white icons. |
| 5.6 | Android: what are the font, size and height of the Alerts Enable and What's New buttons, and the colors of the segmented control and loading indicator? | Segmented control: the For You / Saved / Alerts `MaterialButtonToggleGroup`. Loading: the full-screen progress dialog. iOS is answered. |
| 5.9 | Android home-screen widget: what are the night colors, and the layout and sizes? | `values-night` changes `widget_bg`, `widget_divider1`, `widget_divider2` and `widget_text_main`; the values aren't in the style guide. |

## 6. Platform

| # | Question | What we know |
|---|---|---|
| 6.1 | Can you send the iOS export at `f79fe3339`: the style guide's data files (market colors, tokens, type, assets) and the bundled font files, in the same format as before? | Your answer: `f79fe3339` is current, and the app shell (iOS 26 tab bar), Settings and Onboarding changed since `e30ad2585`, which is what our iOS data comes from. A ticket attachment or a shared folder both work. |

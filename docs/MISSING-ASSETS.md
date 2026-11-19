# Questions for the Apps team

What the MNG Apps design system still needs from the Apps team (Jess Navaro, Patrick Carr, Ameer M.). Each question has a number. Please answer in the Jira ticket for the app the question is about, starting each answer with its number, for example "5.5: …". Questions about both apps can go in either ticket. Partial answers help too.

- iOS: [DREAMT-4718](https://digital1stmedia.atlassian.net/browse/DREAMT-4718)
- Android: [DREAMT-4719](https://digital1stmedia.atlassian.net/browse/DREAMT-4719)

We work from the shipped code (iOS TroncKit @ `f79fe3339` per your latest answers, our export is `e30ad2585`; Android android-tribpub @ `1cfb069a6`) and the two Apps team style guides. Everything here is something those don't tell us.

**Numbers don't change.** When a question is answered we remove it and leave a gap, so the numbers you have quoted stay the same.

**Thank you for the iOS and Android answers.** Most questions are now closed. The rest are follow-ups: where an answer and the code (or the style guide) say different things, the question below says what each one says, so you can tell us which one ships. iOS: 1.3, 1.4, 1.8, 2.1, 4.1, 5.10 and 6.1. Android: 1.1, 3.4, 5.3 (screenshots to come), 5.4 and 5.6. Thank you for adding the answers to the Android style guide too.

## Most needed

1. **6.1** The iOS export at `f79fe3339`
2. **1.3 / 1.4 / 1.8** iOS tab bar: Saved icon, market tab icons, the NEWSPAPER tab and Patrick's newspaper icon (follow-ups)
3. **5.6** Android: Alerts Enable fill; account and savings label sizes (follow-up)
4. **5.4** Android: paywall button text case and subscription option weight (follow-up)
5. **3.4** Android: do some screens follow the phone's dark mode?
6. **2.1** Logo files for every market
7. **5.10** iOS meter paywall purchase button

## 1. Icons

| # | Question | What we know |
|---|---|---|
| 1.1 | Android: can you send vector masters (SVG or PDF) for the icon images, or confirm none exist? | iOS: none exist (213 of 218 images are PNG exports; the only vectors are the 4 Author Profile SVGs). Android: the style guide has 126 PNG and 12 SVG exports, not masters. Most useful first: top bar, bottom navigation, general, player controls. |
| 1.3 | iOS Saved tab: which icon should it show, and is a fix planned? | Your answer: the tab calls `UIImage(systemName: "saved")`, which returns no image, so the tab shows no icon. Android shows a bookmark (`mc_tab_icon_saved`). Was the intent an SF Symbol such as `bookmark` / `bookmark.fill`, or a custom image? |
| 1.4 | Which markets override which tab-bar icons, what are the image set names, and can you send the files? | Your answer: 9 markets (CT, BS, DP, MC, NYDN, SS, VP, HC, OS) have their own Home icon and their own selected For You icon; Sections and Alerts use Font Awesome `bars` and `bell` everywhere. (Android: only the Home tab icon is per market.) The earlier iOS style guide said 2 markets override the Font Awesome tab icons: which 2 markets and which icons, or is that out of date? Please send the 18 Home and For You files (PNG is fine). |
| 1.8 | iOS: is the NEWSPAPER tab in every market, which image set is its icon, and is there a vector? Could you ask Patrick Carr for his newspaper icon (the vector source, and where it lives)? | Your screenshots (TDP, NYDN, VP) show five tabs: NEWS · SECTIONS · GAMES · YOU · NEWSPAPER, with a filled newspaper icon that looks like the one Patrick shared as a PNG on Oct 21. You said "Digital" was another name for this tab and that code is commented out. Does the tab open the native eNewspaper viewer? |

## 2. Logos and artwork

| # | Question | What we know |
|---|---|---|
| 2.1 | Can you send every market's logo files: app icon, main logo, lettermark, paywall logo and masthead? Vectors where they exist, PNG otherwise. | iOS: 31 markets ship their main logo and lettermark as vectors, and PAC, SIT and TPD have vector logos too; please send those vector files. 3–19 files per app, 77 apps. |

## 3. Color

| # | Question | What we know |
|---|---|---|
| 3.4 | Android: on a phone set to dark mode, do Settings, web views, login / paywall or Your News topics look different? | The Android style guide says these screens use a DayNight theme with nothing forcing light, so theme defaults follow the device's dark setting. The iOS answer says all 77 apps are light mode only, and your 3.3 answer says Settings is painted white in every market. We want to know whether Android users ever see dark versions of these screens, and which parts change. |

## 4. Type

| # | Question | What we know |
|---|---|---|
| 4.1 | Can you send the three Open Sans Condensed font files NYDN bundles (Bold, Light, Light Italic), or include them in the 6.1 export? | Your answer: NYDN bundles Bold, Light and Light Italic. Android NYDN uses Google's legacy static Open Sans Condensed (Bold v1.11, Light v1.10, no Light Italic), per the Android style guide. Are the iOS files the same versions? We'll compare them with the Google Fonts version we use in Figma. |

## 5. Components

| # | Question | What we know |
|---|---|---|
| 5.3 | Android: can you send screenshots of key screens for a few markets? | Nav, section front, article, paywall, settings. We have the iOS ones (TDP, NYDN, VP), so the same markets would be ideal. We use them to check our work. |
| 5.4 | Android: (a) Which paywall buttons are sentence case and which are all caps? (b) Are all subscription option buttons Roboto Bold 16sp, or only Monthly? | (a) Your answer and the style guide: settings, web view and paywall use the Material3 theme (sentence case), but the blocking paywall Subscribe is all caps. (b) Your answer and the guide's text say the subscription options are Roboto Bold 16sp; the guide's Buttons table says "White 16sp; Monthly bold". |
| 5.6 | Android: (a) Which fill ships on the Alerts Enable "CUSTOMIZE" button? (b) What are the font, size and height of the account bottom-sheet buttons and the savings label? | (a) Your answer and the style guide: `Alerts_Enable_Button_Background` is #FF6859 in every market. The export at `1cfb069a6` (the guide's market data) has it per market: the market's action color in 58 of 77, #DAA520 in 15, #FF6859 only in OS and TSAR, #4FA8D1 in DP, #000000 in TPD. Is that color overridden somewhere (a drawable or style), so every market shows #FF6859? (b) Not covered yet: the account bottom-sheet buttons (radius 10, filled or outlined) and the savings label (white, 2dp stroke in the buy color, radius 15, text #004E87). Do they use the Material defaults from your 5.4 answer? The What's New fill, sizes, segmented control and loading colors are answered, thank you. |
| 5.10 | iOS meter paywall purchase button: is the label forced to uppercase or the text each market sets; is the height fixed at 45 pt or does it grow with the text; do BS, DP, HC, MC, OS, SS and VP draw it differently (radius, border); is the label always white? | Your answer: at least 45 pt (45 measured on TDP), radius 8, Open Sans Bold 14, `paywallPrimaryActionColor`. TDP's text "TRY ONE MONTH FREE" is uppercase; the default "Subscription Offers" isn't. We'll match our primary button to it once these are settled. |

## 6. Platform

| # | Question | What we know |
|---|---|---|
| 6.1 | Can you send the iOS export at `f79fe3339`: the style guide's data files (market colors, tokens, type, assets) and the bundled font files, in the same format as before? | Your answer: `f79fe3339` is current, and the app shell (iOS 26 tab bar), Settings and Onboarding changed since `e30ad2585`, which is what our iOS data comes from. A ticket attachment or a shared folder both work. |

# Questions for the Apps team

What the MNG Apps design system still needs from the Apps team (Jess Navaro, Patrick Carr, Ameer M.). Each question has a number. Please answer in the Jira ticket for the app the question is about, starting each answer with its number, for example "5.5: …". Questions about both apps can go in either ticket. Partial answers help too.

- iOS: [DREAMT-4718](https://digital1stmedia.atlassian.net/browse/DREAMT-4718)
- Android: [DREAMT-4719](https://digital1stmedia.atlassian.net/browse/DREAMT-4719)

We work from the shipped code (iOS TroncKit @ `f79fe3339`, from your export; Android android-tribpub @ `1cfb069a6`) and the two Apps team style guides. Everything here is something those don't tell us.

**Numbers don't change.** When a question is answered we remove it and leave a gap, so the numbers you have quoted stay the same.

**Thank you for the iOS export, the logos, fonts, tab icons and screenshots.** Every iOS-only question is now closed. Five questions are left: one for both apps (1.12) and four for Android (1.1, 3.4, 5.4, 5.6). Where an answer and the code (or the style guide) say different things, the question says what each one says, so you can tell us which one ships.

## Most needed

1. **5.6** Android: Alerts Enable fill; account and savings label sizes (follow-up)
2. **5.4** Android: paywall button text case and subscription option weight (follow-up)
3. **3.4** Android: do some screens follow the phone's dark mode?
4. **1.12** Both apps: is the Amazon sign-in icon used anywhere?
5. **1.1** Android: vector masters for the icon images

## 1. Icons

| # | Question | What we know |
|---|---|---|
| 1.1 | Android: can you send vector masters (SVG or PDF) for the icon images, or confirm none exist? | iOS: none exist (213 of 218 images are PNG exports; the only vectors are the 4 Author Profile SVGs). Android: the style guide has 126 PNG and 12 SVG exports, not masters. Most useful first: top bar, bottom navigation, general, player controls. |
| 1.12 | Is the Amazon sign-in icon used anywhere a reader can see it? | Both apps include it (iOS: the TroncKit default Amazon button; Android: `ic_amazon`), but login is the Auth0 web page on both apps, so the native Amazon button never shows. If it's unused, we'll leave it out of the design system. |

## 2. Logos and artwork

All answered, thank you.

## 3. Color

| # | Question | What we know |
|---|---|---|
| 3.4 | Android: on a phone set to dark mode, do Settings, web views, login / paywall or Your News topics look different? | The Android style guide says these screens use a DayNight theme with nothing forcing light, so theme defaults follow the device's dark setting. The iOS answer says all iOS apps are light mode only, and your 3.3 answer says Settings is painted white in every market. We want to know whether Android users ever see dark versions of these screens, and which parts change. |

## 4. Type

All answered, thank you.

## 5. Components

| # | Question | What we know |
|---|---|---|
| 5.4 | Android: (a) Which paywall buttons are sentence case and which are all caps? (b) Are all subscription option buttons Roboto Bold 16sp, or only Monthly? | (a) Your answer and the style guide: settings, web view and paywall use the Material3 theme (sentence case), but the blocking paywall Subscribe is all caps. (b) Your answer and the guide's text say the subscription options are Roboto Bold 16sp; the guide's Buttons table says "White 16sp; Monthly bold". |
| 5.6 | Android: (a) Which fill ships on the Alerts Enable "CUSTOMIZE" button? (b) What are the font, size and height of the account bottom-sheet buttons and the savings label? | (a) Your answer and the style guide: `Alerts_Enable_Button_Background` is #FF6859 in every market. The export at `1cfb069a6` (the guide's market data) has it per market: the market's action color in 58 of 77, #DAA520 in 15, #FF6859 only in OS and TSAR, #4FA8D1 in DP, #000000 in TPD. Is that color overridden somewhere (a drawable or style), so every market shows #FF6859? (b) Not covered yet: the account bottom-sheet buttons (radius 10, filled or outlined) and the savings label (white, 2dp stroke in the buy color, radius 15, text #004E87). Do they use the Material defaults from your 5.4 answer? The What's New fill, sizes, segmented control and loading colors are answered, thank you. |

## 6. Platform

All answered, thank you.

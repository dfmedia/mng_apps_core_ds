# iOS screenshots on DREAMT-4718 (5.3): what they show

Our notes from viewing the 17 attachments in Jira's preview (2026-11-19, Claude in Chrome). The images themselves are not in this repo: Jira's file host (api.media.atlassian.com) is blocked from this workspace. Builds: Debug, TroncKit `f79fe3339`, iPhone 17 simulator, iOS 27.0 (Apps team). Ads are Google test creatives; Settings shows a debug-only Paywall Meter State row.

Measurements are estimates from the 34 % preview (about 0.30 of the 3x image), good to about ±1 pt.

## Tab bar (iOS 26+ style)

- Same five tabs in TDP, NYDN and VP: **NEWS · SECTIONS · GAMES · YOU · NEWSPAPER**, uppercase labels, floating rounded bar; the selected tab sits on a lighter pill and takes the market color.
- NEWS icon: market Home icon (VP: its "P" lettermark; TDP: Font Awesome house, gold).
- SECTIONS: three bars. GAMES: puzzle piece (outline). YOU: person with a list. NEWSPAPER: a filled newspaper glyph with a folded left edge, an image block and text lines (looks like the icon Patrick shared on Oct 21; not confirmed).
- So the e-edition tab ships as **NEWSPAPER** in these three markets (MISSING-ASSETS 1.8).

## Paywall (TDP-6)

- Purchase button: TDP action gold fill, white bold uppercase label "TRY ONE MONTH FREE", about 44–45 pt tall, corner radius about 7–8 pt, full width with side insets. Matches the Apps team answer (at least 45 pt, radius 8), not our iOS spec (44 pt provisional, radius 4).
- Log In link: two centered lines, "Already a Subscriber? Log in to your Denver post account", **the whole text underlined** (the Apps team said only "Log In" is underlined in the default text; TDP's own text is underlined throughout).
- The label case question (forced uppercase or typed) is not settled: TDP's text is itself uppercase.

## Subscription options (TDP-5, NYDN-5)

- Option buttons: market fill (TDP gold, NYDN blue), white bold mixed-case labels ("Start your trial, then $14.99"), small corner radius; struck-through old price inside the yearly button.
- Savings pill ("70% savings"): white fill, market-color border and text, fully rounded, overlapping the yearly button's top-right corner.

## Settings (TDP-4, NYDN-4)

- Uppercase bold section headers (PREFERENCES, SUBSCRIPTIONS, SUBSCRIPTION TYPE, PERSONALIZED ALERTS, ABOUT) on a light gray band.
- "Use System Font" switch takes the market color when on (TDP gold, NYDN blue), so at least this switch is themed; 3.1 was about two other switches.
- Article Text Size slider with 6 stops and a PT Serif-style sample text.

## Onboarding (TDP-1, NYDN-1, VP-1)

- Hero image with market logo and "Maybe Later"; 6 topic chips (outlined, market color), "View all topics" link in market color, disabled gray "Continue ›" button.

## Problem

- **TDP-7-loading.png is the article screen**, not the loading indicator: same size to the byte as TDP-3-article.png (1,874,788 bytes) and the same picture. The loading indicator was not captured.

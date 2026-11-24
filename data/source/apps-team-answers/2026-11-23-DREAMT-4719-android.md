# Apps team answers — Android (DREAMT-4719), 2026-11-23

Source data: do not edit. Copied from Rajal Patel's comment 276938 on [DREAMT-4719](https://digital1stmedia.atlassian.net/browse/DREAMT-4719) (2026-11-23 12:15 MT), answering Karl's comment 276791 (2026-11-19). Questions as numbered in docs/MISSING-ASSETS.md on 2026-11-19 (DEC-20: numbers kept). Code: android-tribpub (commit not stated; our export is `1cfb069a6`). Formatting converted from Jira to Markdown; Rajal's quoted questions shortened to their number; answer wording unchanged. Rajal also updated the Android style guide (version `1795459789-4808`; its markets.json is byte-identical to data/source/android-markets.json).

---

- **5.6** (a) Alerts Enable "CUSTOMIZE" fill:
  - a) The export is right and the guide is wrong. The default in main is #FF6859, but 75 of the 77 markets set their own Alerts_Enable_Button_Background. Only OS and TSAR keep #FF6859. In 58 markets it is the same as the paywall Subscribe color (<m>-action); #DAA520 (gold) is the most common, in 17 markets
  - b) No. The two account bottom sheets (Manage subscription and Delete account) are built with the app context.
- **5.11** Paywall_LoginButton_Text isn't used anywhere in the code, so the TSAR / OS / SS values don't matter. The link is drawn in the color resource link, underlined (PaywallManagerImpl.java:165), on the white paywall screen (fragment_paywall_purchase.xml):
  - #56A1DD in 73 markets, including TDP, OS, SS and TSAR
  - NYDN #4591E0
  - DP and VP #004E87
  - MC #000000
- So the link is visible in OS, SS and TSAR. TDP and NYDN match the screenshots only because link happens to have the same values. The guide's "#000000" is right only for MC.
- **3.4** On a phone in dark mode, do Settings, web views, login / paywall or Your News topics look different? Only the web views, You News Topics, and Pop-Up Dialog in settings are different.
- **1.1** Vector masters (SVG or PDF) for the icon images, or confirm none exist. no
- **1.12** Is the Amazon sign-in icon (`ic_amazon`) shown anywhere? no

I did some changes in the architect regarding the answers above:

- Alerts Enable (5.6a): the "#ff6859 in every market" line is replaced with the real breakdown:
  - 58 markets use their Subscribe button color.
  - 15 use #daa520 (gold).
  - DP is #4fa8d1 and TPD is #000000.
  - Only OS and TSAR keep #ff6859.
- The Market colors notes and the Buttons note say the same.
  - Login link (5.11): the Buttons table gives the real link colors: #56a1dd in 73 markets, NYDN #4591e0, DP and VP #004e87, MC #000000. It's underlined and always on white. It also notes that Paywall_LoginButton_Text isn't used.
  - Account bottom sheets (5.6b): they use the phone's default button style, not Material. The row also has their fills, text colors and heights. Only Open Play Store has 10dp corners; the other buttons are 6dp. The radius-sheet-button and button-label token notes say this too.
  - Dark mode (3.4): the four things that can change: unstyled Settings dialogs, web views, the Auth0 login page, and the 7 markets whose Settings screen doesn't set a white background. Newsletters is added to the list of DayNight screens. The note still says this hasn't been checked on a device.
  - Icons (1.1, 1.12): ic_amazon moved from "Add" to "Remove", with the reason it's never shown. There's a new line saying the repo has no vector masters.

Passing it back to you so you can take a look.

---

## Our reading (2026-11-24)

- **5.6 (a)** 17 vs 15 for #DAA520: 17 counts every market whose fill is #DAA520; 15 leaves out the two whose action is also #DAA520 (they are in the 58). Our export agrees (17 at #DAA520).
- **5.6 (b)** values from the updated guide (project/5-controls.md, Buttons table): device default button style, Roboto Medium 14sp on stock Android (OEM fonts may differ), sentence case; Open Play Store fill `App_Primary`, text `Toolbar_Text_Primary`, radius 10; Cancel and Delete account outlined with a 1dp black stroke, radius 6 (`app:cornerRadius` ignored); Delete account's Cancel filled `cancel_btn_color` #014E85, white text; Delete account buttons 52dp, Manage subscription buttons at least 48dp.
- **Not answered:** the savings label's font, size and padding (the second half of 5.6 b). The updated guide still gives the savings label text as #004E87, against the VP screenshot.
- **3.4** the comment and the guide differ slightly (the comment names Your News topics; the guide names the Auth0 page and the Settings screen in CT, DP, HC, MC, NYDN, TOD, VP). Both are from code, not checked on a device.

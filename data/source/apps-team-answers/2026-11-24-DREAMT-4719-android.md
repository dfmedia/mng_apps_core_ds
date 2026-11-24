# Apps team answers — Android (DREAMT-4719), 2026-11-24

Source data: do not edit. Copied from Rajal Patel's comment 277025 on [DREAMT-4719](https://digital1stmedia.atlassian.net/browse/DREAMT-4719) (2026-11-24 11:31 MT), answering Karl's comment 277017 (MISSING-ASSETS 5.6, the savings label, the last open question). Code: android-tribpub (commit not stated; our export is `1cfb069a6`). Formatting converted from Jira to Markdown; wording unchanged. Rajal also updated the Android style guide (he calls it version 18; artifact version `1795544871-b15c`).

---

@Karl Uschold Here are the answers you requested. I also did a little change to the style guide.

*Text*
  • Roboto Bold, 14sp (Android default; the layout sets no font or size)
  • Content is set by the app as "<n>% savings" and the label is hidden when there's no saving
  • Same in every market (no market overrides the layout)

*Pill*
  • Size: wraps the text, padding 15dp left/right and 5dp top/bottom (about 29dp tall)
  • Shape: white fill, 2dp border in the market's Subscribe color (`<m>-buy`), 15dp corners (fully round ends)
  • Position: right-aligned 50dp from the edge, overlapping the top edge of the Yearly option, drawn above it

*Style-guide fix (done, version 18)*
The guide said the text was `#004e87` in every market. That was wrong: the text uses each market's `btn_blue` color, which matches the border in 72 of 77 markets.
Exceptions:
  • BS: text #779DCF, border #DAA520
  • DP: text #4FA8D1, border #005F7E
  • TDP: text #000000, border #DAA520
  • TPD: text #000000, border #999999
  • TSAR: text #000000, border #15919D

---

## Our reading (2026-11-24)

- Checked against data/source/android-markets.json: `btn_blue` equals the buy color (`Paywall_BuyButton_Background`) in 72 of 77 markets, and the five exceptions are exactly the ones above.
- "Roboto Bold 14sp (Android default)": the size and family are the system default; the bold comes from the layout's text style.
- Our screenshot estimate (Roboto Bold 15–16sp, about 114 × 29dp) was close on the pill and too large on the text.

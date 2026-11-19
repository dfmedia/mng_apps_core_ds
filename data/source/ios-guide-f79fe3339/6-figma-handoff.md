# Figma handoff

How this guide moves into Figma once someone has a Full seat on MNG's plan.

1. **Variables.** Import `assets/Data/markets.json`. Create one color collection per group of markets, or one collection with a mode per market. MNG's plan allows 20 modes per collection.
2. **Text styles.** Create one text style per entry under Typography. Open Sans, PT Serif and Spectral are Google Fonts, which Figma includes. Check how Open Sans Condensed (NYDN only) is available in Figma.
3. **Components.** Rebuild the components here (App chrome, Buttons, Subscription option, Controls) bound to those variables, laid out the way Karl's pages are.
4. **Icons.** Use Karl's vectors for every matched icon in **Icons**. Figma's MCP server can't place images, so the PNG assets here are for reference only.

Claude Code writes steps 1–3 through Figma's MCP server (`use_figma`). Step 4 is manual.

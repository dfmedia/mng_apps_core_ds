# iOS primary button: review (2026-11-18)

Findings only; nothing has been rebuilt. Karl asked to look into this before any change to the Button (DEC-07). Written by hand, not generated.

## The problem

Our iOS primary button spec (DEC-07 pilot, docs/components/BUTTON.md) was taken from the **paywall Log In / Register button** in the iOS style guide (TroncKit `e30ad2585`, data/source/button-shipped.json). The Apps team says that button is **never shown**: login is the Auth0 Universal Login page in every market (DREAMT-4718, 2026-11-18, TroncKit `f79fe3339`; data/source/apps-team-answers/). They also say iOS has **no single primary button**.

## Filled buttons iOS actually shows (Apps team, `f79fe3339`)

| Button | Height | Radius | Label | Fill |
|---|---|---|---|---|
| Meter paywall purchase button | at least 45 pt (45 measured on TDP) | 8 | Open Sans Bold 14; text set per market (default "Subscription Offers", TDP "TRY ONE MONTH FREE") | `paywallPrimaryActionColor` (= Core `action`) |
| Manage App Subscription (modal) | 44 pt | 8 | not stated | nav bar color (white on white in 7 markets, DSC-34) |
| Push prompt Yes | 40 pt | 5 | Open Sans Bold 14 | not stated |
| Newsletters login (Apple, Google) | at least 52 pt | 9 | Open Sans SemiBold 18, Dynamic Type | outlined (1 pt), not filled |
| Subscription option (earlier guide, `e30ad2585`) | not stated | 8 | Open Sans Bold 16 | `subscriptionTintColor` |

Pressed state on all of them: no custom state; the title fades and the fill stays the same (UIKit default).

## Our spec vs the closest shipped button (meter paywall purchase)

| | Our iOS spec (DEC-07) | Meter paywall purchase button | Same? |
|---|---|---|---|
| Fill | Brand theme `action` | `paywallPrimaryActionColor` = `action` | Yes |
| Label color | `#ffffff` | not stated (white on the old Log In button) | Probably; to confirm |
| Label font | Open Sans Bold 14 | Open Sans Bold 14 | Yes |
| Label case | Forced uppercase | Per-market text; default "Subscription Offers" is mixed case, TDP's is all caps | Unclear: forced or typed? |
| Radius | 4 pt (legacy markets 5 + 1 pt border) | 8 pt | **No** |
| Height | 44 pt, provisional | at least 45 pt | **Close, not the same** |
| Pressed | Native platform feedback | Title fades, fill unchanged | Yes (that is the native feedback) |
| Disabled | `#c1c8cb` / `#767676` (Android's, new on iOS) | not stated | Not shipped on iOS |

Text link (paywall "Log In"): our provisional Open Sans Regular 14 is confirmed as the default, but 6 markets use 11 (BS, DP, HC, MC, OS, SS) and 2 use 12 (NYDN, VP). Only the words "Log In" are underlined; our spec says iOS has no underline.

## What a re-base would change (not done)

- `button.ios.primary.radius` 4 → 8; the legacy 5 + 1 pt border note no longer applies unless the purchase button has its own legacy variant (unknown).
- `button.ios.primary.height` 44 provisional → 45 (or a 44 minimum, which the Apps team says fits all their buttons).
- iOS text link: font confirmed, per-market sizes added, "Log In" underlined.
- DSC-20 and IMPROVEMENTS BTN-01 / BTN-02 wording; the iOS Figma Button component and MNGButtonTokens.swift (regenerated).
- Unchanged: fill and CLR-04 (same `action` color), Android values.

## To settle first

1. Is the purchase button's label forced to uppercase, or is it whatever text the market sets?
2. Is the height fixed at 45 or content-driven ("at least 45")?
3. Do the legacy-template markets (BS, DP, HC, MC, OS, SS, VP) draw the purchase button differently?
4. Should "primary" mean the purchase button only, or the shared pattern of the purchase and Manage subscription buttons (radius 8, about 44 pt)?

The TDP paywall screenshot on DREAMT-4718 (TDP-6-paywall.png) would answer 1 and part of 2; we can't download it from this workspace yet.

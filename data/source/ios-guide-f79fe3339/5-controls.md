# Buttons, controls & touch targets

Values on this page were checked against TroncKit `f79fe3339` for DREAMT-4718.

## Login

Every market logs in through an Auth0 web view (`isAuth0` is true in all 78 configs). The native Log In / Register and Facebook / Google / Amazon buttons in TroncKit's Arc paywall code are never shown, so `radius-button`, `radius-google` and `size-social-icon` describe code that doesn't ship.

## Buttons

| Button | Size | Fill | Label | Shape |
| --- | --- | --- | --- | --- |
| Meter paywall purchase button ("TRY ONE MONTH FREE") | `size-button-purchase` (45; a minimum, but one line of fixed-size text never exceeds it) | `<m>-action` (`paywallViewPurchaseButtonColor` matches `paywallPrimaryActionColor` in every market) | `paywall-purchase`: white in every market, Open Sans Bold 14, always uppercase (`.uppercased()` on the localized text in all 78 markets) | `radius-purchase` (8), 0.7 pt border in the fill color, same in every market |
| Meter paywall Log In link | Minimum 50 | None | `paywall-login-link`: Open Sans Regular 14 (11 in BS, DP, HC, MC, OS, SS; 12 in NYDN, VP). "Already a Subscriber? Log in to your <market> account" (NYDN: "Log in to your New York Daily News account"), centered, the whole sentence underlined | None |
| Subscription option (monthly, yearly) | Fits content | `subscriptionTintColor` | White, Open Sans Bold 16 | `radius-subscription`, `space-subscription-inset` |
| Savings pill | `size-savings-pill` (110 × 30) | White, 2 pt `subscriptionTintColor` border | `savings-label`: "NN% savings", Open Sans Bold 13, `subscriptionTintColor` | `radius-savings` (13). Centered on the yearly option's top edge, inset `space-savings-inset-phone` (10) / `space-savings-inset-pad` (35) |
| Push prompt Yes | `size-button-push` (40) | `pushNotificationPromptYesButtonBackgroundColor` | `push-yes`: Open Sans Bold 14 | Radius 5 |
| Push prompt No | Same as Yes | None | `push-no`: Open Sans Regular 14, underlined (not in VP) | Radius 5; 1 pt border set to clear |
| Manage App Subscription (modal) | `size-button-modal` (44) | `navigationBarBackgroundColor` | White, system font | `radius-purchase` (8) |
| Cancel (same modal) | 44 | White, 1 pt black border | Black, system font | 8 |
| Newsletters: Continue with Apple / Google | `size-button-newsletters` (52, minimum) | System background, 1 pt outline in the system label color | `newsletters-button`: Open Sans SemiBold 18, Dynamic Type | `radius-newsletters` (9); icon `size-newsletters-icon` (22), gap 12 |

- **Manage App Subscription in 7 markets:** DP, MC, NYDN, OS, SS, TSAR and VP have a white nav bar, so this button is white text on a white fill.
- **Manage Subscription and Delete Account** in Settings are rows, not buttons. They use `settings-row`; Delete Account text is `destructive` red.
- **Primary height:** iOS has no single primary button height. The shipped values are 40, 44, 45 and 52. Design's 44 pt matches `size-touch-min` and the Manage Subscription buttons.

## States

- **Pressed:** none of the buttons above defines a pressed state. They're iOS system buttons, so the title fades while pressed and the fill stays the same. Newsletters buttons use the standard iOS button highlight. The only custom pressed colors are on the breaking-news dismiss button (`breakingNewsButtonColor`) and the action buttons in PostKit and push message views.
- **Disabled:** styled only on the tracking-consent Continue button.
- **Loading:** a full-screen overlay (`LoadingIndicatorManager`), except the Trinity audio button.
- **Secondary / Text variants:** none.

## Controls

| Control | Where | Colors |
| --- | --- | --- |
| Segmented control | For You / Saved / Alerts | `segment-selected` (white) on `segment-track` (#F2F2F7); system title font. Centered in a `size-segment-band` (50) band |
| Segmented control | eNewspaper editions | iOS default |
| Loading indicator | Full-screen overlay | Large iOS spinner in `progressHUDForegroundColor` on a white card, `radius-hud` (12). Spinner is #004E87 in 66 markets; #005F7E in DP and VP; BS #DAA520, HC #4FA8D1, MC #539CC4, NYDN #4591E0, OS #15919D, SS #761113, TDCD #5B9BC8, TDP #F7A430, TIVDB #E0E2E4 |
| Switch | Settings | `settingsSwitchTintColor` (nil = `ios-switch-on`) |
| Switch | Alert topics | `alertTopicCellSwitchTint` |
| Switch | Offline mode | `offlineViewSwitchTintColor`; unset in NYDN and OS, so `ios-switch-on` |
| Switch | Tracking consent | `trackingConsentSwitchOnTintColor`; unset in every market, so `ios-switch-on` |
| Slider | Article text size | `settingsSliderThumbTintColor`, `settingsSliderMinimumTrackTintColor`, `settingsSliderTickMarkTint` |
| Checkbox | Your News topics | 30 × 30 button; the 17 × 18 images sit centered at natural size, not scaled. BS, HC, MC, NYDN, OS, SS and VP use their own images, DP uses VP's, and every other market uses `Checked` / `Unchecked`. `Uncheck-Grey` isn't used anywhere |
| Radio button | — | Not used |

The section list separator (`sectionListSectionSeparatorColor`) is unset in every market, so it shows the iOS default separator color.

## Touch targets

- `size-touch-min` (44 pt) is set by hand only on the glass navigation button, the search field, the floating audio player, the Manage Subscription buttons and the Sign in with Apple row.
- Below 44 pt: Your News checkbox (30 × 30) and the push prompt buttons (40).

## Payments

- iOS has no Apple Pay, Google Pay or PayPal buttons. Subscriptions are StoreKit 2 in-app purchases.
- Karl's Payment Options badges (card brands, wallets) are web-only.

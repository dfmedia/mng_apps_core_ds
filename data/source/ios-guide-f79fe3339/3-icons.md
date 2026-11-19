# Icons

## What iOS uses

| Source | Count | Notes |
| --- | --- | --- |
| Font Awesome 5.15.1 (pod `FontAwesome.swift` 1.9.1) | 7 glyphs | `chevronUp`, `chevronDown` (all 78 markets); `search` (NYDN, SS, VP, OS); `home`, `bars`, `bookmark`, `bell` (TroncKit tab bar defaults; 9 markets replace `home` with their own PNG, see below) |
| TroncKit image assets | 218 images in 19 groups | 213 PNG, 4 SVG (Author Profile), 1 JPG. Shown under Assets. The `ManageSubscriptionIcon` image set has no image file, so the 100 pt logo area on the Manage Subscription modal is blank. `tab-digital` isn't referenced: the "DIGITAL" eNewspaper tab title is commented out, so iOS has no Digital tab. |
| SF Symbols | ~21 | `person.circle.fill`, `exclamationmark.triangle.fill`, `chevron.left`, `chevron.right`, `xmark`, `xmark.circle.fill`, `checkmark.circle.fill`, `envelope.fill`, `gamecontroller.fill`, `gobackward.15`, `goforward.15`, `arrow.clockwise`, `play.fill`, `pause.fill`, and six sport symbols in tournament loading at 72 pt: `soccerball.inverse`, `american.football.fill`, `baseball.fill`, `basketball.fill`, `hockey.puck.fill`, with `sportscourt.fill` as the fallback. `"saved"` at `CoreTabBarViewController.swift:140` is not a real SF Symbol, but that code is never called: Saved is a segment inside the YOU tab, not a tab of its own, so no tab shows the missing icon. |
| Per-market app catalogs | 3–19 per app | App icon, `Main logo`, `Lettermark`, paywall meter logo, masthead. 31 markets ship `Main logo` and `Lettermark` as vector files; PAC, SIT and TPD also have vector black / white logos. Logos live in Karl's separate Newspaper Logos file. |

iOS does not use the MNG IcoMoon icon font from Karl's web style guide.

### Asset groups

| Group | Count | Images |
| --- | --- | --- |
| General | 20 | AccountDeletionImage, AppleIcon, BTN_FollowTopic, BTN_UnFollowTopic, BannerCloseLight, Chevron - Down, Chevron - Up, CloseButton, FacebookIcon, FollowTopic, GoogleIcon, GreyCheckmark, Masthead, Minus-CT, Plus-CT, TwitterIcon, UnFollowTopic, icon_filter, textsizelarge, textsizesmall |
| Ads | 2 | ad-bigbox-offline-250, outbrainLogo |
| Alert | 2 | bell, exclamation-icon |
| Author Profile | 4 | AuthorContactBluesky, AuthorContactFacebook, AuthorContactInstagram, AuthorContactX |
| Checkmark-selected | 8 | Checked, Checkmark-BS, Checkmark-Hart, Checkmark-MC, Checkmark-NYDN, Checkmark-OS, Checkmark-SS, Checkmark-VP |
| ContinueBtn | 10 | Continue-BS, Continue-CT, Continue-Grey, Continue-Hart, Continue-MC, Continue-NYDN, Continue-OS, Continue-SS, Continue-TPD, Continue-VP |
| ENewspaper | 16 | black_expand-paper, black_fit-to-screen, black_left-arrow, black_menu, black_right-arrow, black_search, cover-placeholder, eNewspaper-overlay, expand-paper, fit-to-screen, left-arrow, menu, menu-line, overlay-close, right-arrow, search |
| Navigation Bar | 11 | Saved-Article, Unsaved-Article, nav-save-filled, nav-save-unfilled, nav-search, nav-search - black, nav-search - white, nav-settings, nav-settings - black, nav-settings - white, nav-share |
| Onboarding | 19 | BS, CT, DP, DP-logo-white, HC, HC-logo, MC, MC-logo-white, NYDN, NYDN-logo, OS, OS-logo, SS, SS-logo, VP, VP-logo-white, ct-logo, logo-bs-white, mng-top-image-view |
| Paywall | 2 | paywall-1password, paywall-logo |
| PostKit | 42 | button-downarrow, button-fastforward, button-miniplayer-close, button-miniplayer-close-dark, button-miniplayer-pause, button-miniplayer-pause-dark, button-miniplayer-play, button-miniplayer-play-dark, button-pause, button-pause-dark, button-pause-medium, button-pause-small, button-play, button-play-dark, button-play-medium, button-play-small, button-play-small-dark, button-rewind, embed-3d, embed-play, gif-play, instagram-logo, instagram-logo-footer, instagram-logo-video, player-error-image, player-offline-image, player-placeholder-compact, player-placeholder-regular, rating-star-empty, rating-star-full, rating-star-half, recirculationPlaceholder, tweet-favorite, tweet-logo, tweet-retweet, tweet-verified, twitter-logo, twp-slogan-dark, twp-slogan-light, video-fullscreen-close, vimeo-logo, youtube-logo |
| SaveIcon | 18 | Saved-Filled-BS, Saved-Filled-CT, Saved-Filled-DP, Saved-Filled-Hartford, Saved-Filled-MC, Saved-Filled-NYDN, Saved-Filled-Orlando, Saved-Filled-SS, Saved-Filled-VP, Saved-Unfilled-BS, Saved-Unfilled-CT, Saved-Unfilled-DP, Saved-Unfilled-Hartford, Saved-Unfilled-MC, Saved-Unfilled-NYDN, Saved-Unfilled-Orlando, Saved-Unfilled-SS, Saved-Unfilled-VP |
| Sections | 2 | chevron_down, chevron_up |
| Tab Bar | 19 | For You, For You , tab-alerts, tab-baltimoresun, tab-dailypress, tab-digital, tab-enews, tab-foryou, tab-games, tab-hart, tab-home, tab-morningcall, tab-newspaper, tab-nydn-active, tab-os, tab-saved, tab-sections, tab-sunsentinel, tab-viginia |
| Tab bar Your_news icons | 11 | YourNews-BS, YourNews-Black, YourNews-CT-Selected, YourNews-DP, YourNews-Hart, YourNews-MC, YourNews-NYDN, YourNews-OS, YourNews-SS, YourNews-VP, YourNews-White |
| Tab bar save icons | 11 | Saved - BS, Saved - Hart, Saved - MC, Saved - SS, Saved - White, Saved -Black, Saved -OS, Saved -VP, Saved CT - Selected, Saved- DP, Saved- NYDN |
| Topic Selection Button | 10 | ButtonWithCheckmark, TopicSelection-BS, TopicSelection-Grey, TopicSelection-Hart, TopicSelection-MC, TopicSelection-NYDN, TopicSelection-OS, TopicSelection-SS, TopicSelection-TPD, TopicSelection-VP |
| Uncheck | 9 | Uncheck-BS, Uncheck-Grey, Uncheck-Hart, Uncheck-MC, Uncheck-NYDN, Uncheck-OS, Uncheck-SS, Uncheck-VP, Unchecked |
| yournews | 2 | WhiteCheckmark, your_news_image |

## Source files and per-market icons

Checked against `f79fe3339` for DREAMT-4718.

- **Vector masters (1.1):** none in the repo. 213 of the 218 TroncKit images are PNG exports (1x / 2x / 3x), with no PDF or SVG master behind them. The only vectors are the 4 Author Profile SVGs.
- **Tab icons by market (1.4):**
  - **Home:** CT, BS, DP, MC, NYDN, SS, VP, HC and OS use their own PNG (`tab-home`, `tab-baltimoresun`, `tab-dailypress`, `tab-morningcall`, `tab-nydn-active`, `tab-sunsentinel`, `tab-viginia`, `tab-hart`, `tab-os`), selected and unselected (`Tronc+TabBar.swift:38`). Every other market draws Font Awesome `home`.
  - **For You:** unselected is `YourNews-White` in CT and HC and `YourNews-Black` everywhere else. Selected is `YourNews-CT-Selected` in CT and `YourNews-<market>` in the other 8 of those 9 markets (`ImageThemeable.swift:209`).
  - **Sections and Alerts:** Font Awesome `bars` and `bell` in every market. No market overrides them.
  - None of these have vector files.
- **Icons with no design behind them (1.5):** ±15 s skip uses SF Symbols `gobackward.15` / `goforward.15`. Text size (`textsizesmall` / `textsizelarge`), Games tab (`tab-games`), Filter (`icon_filter`) and Follow / Unfollow topic (`FollowTopic` / `UnFollowTopic`) are PNGs. iOS can switch any of them to SF Symbols.
- **Per-market recolored sets (1.6):** each set is one glyph saved as separate colored PNGs. On iOS, one template image tinted with the market color can replace each set.
- **Newspaper tab (1.8):** the fifth tab, titled "NEWSPAPER" ("Newspaper" in OS), in all 78 markets: 76 list it in their bundled config (`bottomNavTabs`), and TB and TBCP get it from the default tab list. The icon is `tab-enews` in every market, selected and unselected. `tab-newspaper` is only referenced by an unused property, so it never shows. The tab opens PageSuite's native reader (PSReader SDK) in `EnewsViewController`.
- **Tab icon helpers:** BS, DP, HC, MC, OS, SS and VP each carry their own copy of the Font Awesome tab icon helper, drawing at the same 26 × 23 pt. None of them changes which icon a tab uses.
- **For You master (1.7):** none. The icon exists only as the `YourNews-*` PNGs.
- **Brand marks (1.11):** the repo has no official brand vectors. Apple, Google, Facebook, X / Twitter, Instagram, YouTube, Vimeo, 1Password and Outbrain are all PNG. The only vector marks are the Author Profile SVGs (Bluesky, Facebook, Instagram, X). Current vectors would come from each brand's press kit.
- **Onboarding art (2.2):** BS, CT, DP, HC, MC, NYDN, OS, SS and VP show their own top image. Every other market shows the shared `mng-top-image-view` (`OnboardingViewController.swift:74`).

## Mapped to Karl's icon set

The matches below are by purpose, using the usage notes in Karl's file. Design should confirm each one.

| iOS use | iOS source today | Karl's icon (category) |
| --- | --- | --- |
| Search | FA `search`, `nav-search` PNG | `search` (User Interface) |
| Settings | `nav-settings` PNG | `cog` (Account Management) |
| Share | `nav-share` PNG | `ios-share` (Engagement) |
| Saved / unsaved article | FA `bookmark`, `Saved-*`, `nav-save-*` PNGs | `bookmark2` / `bookmark3` (Account Management) |
| Home tab | FA `home`, per-market `tab-*` PNGs | `home` (Decoration) |
| Sections tab | FA `bars`, `tab-sections` | `menu7` (User Interface) |
| Alerts | FA `bell`, `tab-alerts`, `bell` | `notification` (User Interface; on Karl's Change list) |
| Expand / collapse | FA `chevronUp` / `chevronDown`, `chevron_up` / `chevron_down` | `arrow-up` / `arrow-down` (User Interface) |
| Close | `CloseButton`, `overlay-close`, SF `xmark` | `close` (User Interface) |
| Play / pause | `button-play*`, `button-pause*`, SF `play.fill` / `pause.fill` | `play-arrow` / `pause2` (Multimedia) |
| Rewind / fast forward | `button-rewind`, `button-fastforward` | `backward2` / `next` (Multimedia) |
| Ratings | `rating-star-empty`, `rating-star-full`, `rating-star-half` | `star-empty` / `star-full` (Account Management); no half star |
| Checkmarks | `Checked`, `Unchecked`, `Checkmark-*`, `Uncheck-*` | `checkmark3`, `checkmark-circle`, `radio-unchecked` |
| Social login | `FacebookIcon`, `GoogleIcon`, `AppleIcon`, `TwitterIcon` | `facebook`, `google`, `appleinc`, `x-twitter` (Social Media / Brands) |
| Author links | `AuthorContactBluesky`, `AuthorContactFacebook`, `AuthorContactInstagram`, `AuthorContactX` | `bluesky`, `facebook`, `instagram`, `x-twitter` |
| Email | SF `envelope.fill` | `email` (Engagement) |
| eNewspaper | `tab-enews`, `tab-newspaper` | `newspaper` (Decoration) |

## Pending updates (Karl's format)

- **Add (source or make):** text size small / large, Games tab, ±15 s skip, the six sport symbols, Your News tab, filter (`icon_filter`), follow / unfollow topic. No match exists in Karl's set.
- **Change:** every row above with a match. Replace the iOS asset with Karl's vector.
- **Remove:** the per-market copies of one icon: `Saved-Filled-*` / `Saved-Unfilled-*` (9 markets), `Checkmark-*`, `Uncheck-*`, `YourNews-*`, `Continue-*` and `TopicSelection-*`. Also drop the dead `"saved"` SF Symbol reference and the unused `tab-newspaper` and `tab-digital` images.

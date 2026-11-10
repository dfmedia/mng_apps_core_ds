"""Component ownership: which components and layout rules belong in Core, iOS only or Android only.
Usage: python3 scripts/component_platform_map.py data/component-platform-map.json
Source: MNG iOS Style Guide (TroncKit @ e30ad2585) and MNG Android Style Guide (android-tribpub @ 1cfb069a6),
sections Buttons/Controls/Layout and components AppChrome/Buttons/Controls. Edit ROWS to update.
Owner: core | core+variant | ios | android   (see docs/ARCHITECTURE.md)
"""
import json, sys
from collections import Counter
# group, id, name, iOS today, Android today, owner, Core spec / note
ROWS = [
 ("App chrome", "nav-bar", "Top bar", "UINavigationBar · navbar fill, navtext title/buttons", "Toolbar · bar fill, bartext title/icons", "core+variant", "Same job and tokens; each platform draws its native bar."),
 ("App chrome", "section-tabs", "Section tabs", "sectionBar* colors", "Toolbar_Tabs_* colors", "core+variant", "Same job; native tab strip per platform."),
 ("App chrome", "tab-bar", "Bottom tab bar", "UITabBar · tabbar, tabactive, tabinactive; FA icons 26×23", "Bottom navigation · bar, navactive, bartext; 24dp icons", "core+variant", "Android always uses the nav bar color; iOS too except BS."),
 ("App chrome", "breaking-banner", "Breaking-news banner", "breakingNewsBanner* · alert fill", "Overlay · br_news_red #cf000e", "core", "One component, one Core alert color (PLAT-03)."),
 ("App chrome", "section-header", "Section header band", "Style.json cell-tertiary-header*", "—", "ios", "No band on Android. Equals navbar in 66/77 markets."),
 ("App chrome", "status-bar", "Status bar color", "System (takes nav bar)", "MainStyle_Primary_Dark", "android", "Equals navbar in 70/77 markets."),
 ("Buttons", "button-primary", "Primary button", "Paywall Log In / Register · action fill, white Open Sans Bold 14 caps, radius 4 (legacy 5 + 1pt border)", "Paywall Subscribe · action fill, white caps system font, 60dp tall, square", "core+variant", "One Core primary button. Differences to decide: radius (4 vs 0), height, font."),
 ("Buttons", "button-continue", "Continue button", "Continue-* PNGs (10 market copies); tracking-consent Continue has the only disabled state", "Your News Continue 152×54 radius 9; What's New Continue radius 6", "core", "Same job as Primary button; recommend it becomes Primary button, not its own component."),
 ("Buttons", "subscription-option", "Subscription option", "subscriptionTintColor, Open Sans Bold 16, radius 8, inset 16", "buy fill, white 16sp (Monthly bold), square, 14dp padding", "core+variant", "Fill = action on both (PLAT-04). Differences: radius, font."),
 ("Buttons", "button-text", "Text link button", "paywallLinkColor (Log In link)", "Paywall Log In link, system 16sp", "core", "Core text/link button."),
 ("Buttons", "permission-prompt", "Notification prompt buttons", "Push prompt Yes (filled) / No (text), radius 5", "Alerts enable button, square", "core+variant", "Same job; iOS has a Yes/No pair."),
 ("Buttons", "button-account", "Manage subscription / delete account", "Manage Subscription buttons, 44pt", "radius 10, filled or outlined (bottom sheets)", "core+variant", "Only place Android has an outlined (secondary) button."),
 ("Buttons", "button-whats-new", "What's New Continue button", "—", "whats_new_button_color fill (CT, NYDN, VP: drawable color), white caps Open Sans Bold, radius 6", "android", "Not in the iOS guide. As shipped: docs/GUIDE-EXTRAS.md."),
 ("Buttons", "savings-badge", "Savings label", "—", "White, 2dp stroke in buy color, radius 15", "android", "Not on iOS paywall."),
 ("Buttons", "social-signin", "Social sign-in buttons", "Apple (black, 44pt), Facebook, Google, Amazon (TroncKit defaults)", "Native buttons exist but are hidden; login is Auth0's web page", "ios", "Android shows them only on the Auth0 web page."),
 ("Buttons", "button-states", "Secondary, disabled, loading states", "Missing (one disabled Continue)", "Missing (Continue disabled #c1c8cb, text #767676)", "core", "Gap on both. Define once in Core (CTRL-02)."),
 ("Controls", "switch", "Switch", "UISwitch; 4 tint tokens, nil = iOS green", "SwitchCompat; accent on alert topics, Material default in Settings", "core+variant", "One Core on-color token (PLAT-10); native control per platform."),
 ("Controls", "checkbox", "Checkbox (Your News topics)", "30×30 images; 8 market image sets", "checkbox_tint: continue color checked, #757575 unchecked", "core", "One Core checkbox tinted by token; removes iOS image sets."),
 ("Controls", "text-size", "Text size setting", "6-step slider", "4-option list dialog with radio images", "core+variant", "Same job, different control. Core: the scale steps; platform: the control."),
 ("Controls", "segmented", "Segmented control", "UISegmentedControl (Your News, login/register, editions)", "MaterialButtonToggleGroup (For You / Saved / Alerts)", "core+variant", "Native control per platform; Core sets colors."),
 ("Controls", "loading", "Loading indicator", "Full-screen overlay (LoadingIndicatorManager)", "Full-screen progress dialog", "core", "Same pattern on both; no in-button spinner."),
 ("Layout", "grid", "Section-front grid", "12 columns (PageBuilder)", "12 columns (PageBuilder)", "core", "Identical."),
 ("Layout", "cell-spacing", "Cell spacing", "margin 16, padding 8", "padding 16, spacing 8", "core", "Same values, different names. Core: 16 / 8."),
 ("Layout", "breakpoints", "Breakpoints", "Window width 668 / 835 / 1113 pt (and 668 / 769 / 1025 in PageItem)", "Physical width 4.1 / 6.1 / 7.8 / 10.4 in", "core+variant", "Same job, different units. Core names the classes; platforms set thresholds (LAY-01)."),
 ("Layout", "article-margin", "Article side margin", "0.3125 × width − 160, min 16", "16 phone, 30 landscape, 75 tablet", "core+variant", "Both 16 on phones."),
 ("Layout", "touch-target", "Minimum touch target", "44 pt (not enforced)", "48 dp (not enforced)", "core+variant", "Core rule; platform value."),
 ("Layout", "orientation", "Orientation", "iPhone portrait, iPad all", "Phone portrait, tablet all", "core", "Identical."),
 ("Layout", "ad-slots", "Ad slots", "Sizes not in the guide; offline placeholder image, adhesion banner background", "320×50 phone / 728×90 tablet first slot and sticky footer, 300×250 others; hidden when the parent is narrower", "core+variant", "Colors Core (ad/background, ad/label); sizes per platform, iOS unknown (MISSING-ASSETS 5.9). docs/GUIDE-EXTRAS.md."),
 ("Other", "widget", "Home-screen widget", "—", "widget_* colors (day), values-night colors, per-market ic_logo + night logo", "android", "Day colors are System colors · Android tokens; night colors unknown (MISSING-ASSETS 5.10)."),
 ("Other", "eedition-colors", "eEdition (PageSuite) colors", "Own eNewspaper viewer (no PageSuite colors)", "Fixed SDK colors: tab container #ffffff, tab text #ffffff, inactive #999999, brand #0a1633", "android", "Same in every market. docs/GUIDE-EXTRAS.md."),
 ("Other", "images", "Non-icon images (logos, onboarding, placeholders)", "Onboarding art and logos, masthead, paywall logo, placeholders, topic button backgrounds (43 files)", "Per-market ic_logo + night logo, launcher, splash and notification icons (not in the guide)", "core+variant", "Per-market artwork, tracked not built. Vector masters: MISSING-ASSETS 2.1, 2.2."),
]
out = sys.argv[1]
items = [dict(zip(["group","id","name","ios_today","android_today","owner","note"], r)) for r in ROWS]
json.dump({"source": {"ios": "TroncKit @ e30ad2585", "android": "android-tribpub @ 1cfb069a6"},
           "summary": dict(Counter(i["owner"] for i in items)), "items": items}, open(out, "w"), indent=1)
print(dict(Counter(i["owner"] for i in items)), len(items))

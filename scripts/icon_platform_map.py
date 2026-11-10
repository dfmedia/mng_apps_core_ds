"""Icon ownership: which icon purposes belong in Core, iOS only or Android only.
Usage: python3 icon_platform_map.py data/icon-comparison.json data/icon-platform-map.json
Reads the 59 iOS purposes from icon-comparison.json and adds what Android ships
(android-tribpub @ 1cfb069a6, MNG Android Style Guide). Edit ANDROID / ANDROID_ONLY below to update.
Buckets: core            both apps use this purpose -> one semantic icon in Core, drawn natively per platform
         core-variant    both apps need it but the UI differs (one platform has extra glyphs)
         ios-only        only iOS uses it today
         android-only    only Android uses it today
"""
import json, sys
src, out = sys.argv[1], sys.argv[2]
rows = json.load(open(src))
# purpose -> (Android drawables in use, bucket, note)
ANDROID = {
 'Search': ('mc_ic_search (+8 market copies)', 'core', ''),
 'Settings': ('mc_ic_settings (+10 market copies)', 'core', ''),
 'Share': ('ic_share (+9 market copies)', 'core', 'Glyph differs by platform convention; one semantic name.'),
 'Save (not saved)': ('ic_bookmark_outline · ic_btn_unsave', 'core', ''),
 'Saved': ('ic_bookmark · ic_btn_save · mc_tab_icon_saved', 'core', 'Android special-section star (card_star_default) also means saved: kept as Android\'s glyph, same icon name (DEC-17, PLAT-09 rejected).'),
 'Home tab': ('mc_tab_icon_latestnews (77 market copies)', 'core', 'Both apps ship per-market Home icons; one Core glyph removes ~86 files.'),
 'Sections / menu': ('mc_tab_icon_sections', 'core', ''),
 'Alerts tab': ('mc_tab_icon_alerts · mc_alert_bell (69 market copies)', 'core', ''),
 'For You / Your News tab': ('mc_tab_icon_for_you', 'core', 'Gap on both: one custom Core vector.'),
 'eNewspaper tab': ('mc_tab_icon_newspaper · ic_newspaper', 'core', ''),
 'Games tab': ('mc_tab_icon_games · ic_games', 'core', ''),
 'Digital tab': (None, 'ios-only', 'Not on Android. Ask Apps team whether to retire.'),
 'Expand / show more': ('icon_uparrow', 'core', ''),
 'Collapse / show less': ('icon_downarrow', 'core', ''),
 'Back': ('web_view_navigation_back · ic_arrow_back_black_24dp (from PDFViewCtrlTools)', 'core', ''),
 'Forward / disclosure': ('web_view_navigation_forward · ic_arrow · liveblog_arrow · game_open_arrow', 'core', 'Android has 4 arrows for this; consolidate.'),
 'Close': ('ic_close_white_36dp · xbutton · ic_ad_close · close_player_button · ic_persistent_player_close', 'core', ''),
 'Close (circle)': ('ic_clear_search (search clear)', 'core', 'Confirm the Android glyph is a circled X.'),
 'Account': (None, 'ios-only', 'Android has no account icon; login is Auth0 web.'),
 'Warning': ('stat_notify_error (Android framework, notifications only)', 'core', 'Android uses it only in notifications.'),
 'Email': ('ic_email', 'core', ''),
 'Refresh': ('ic_wc_refresh', 'core', ''),
 'Filter': ('ic_filter (+27 market copies)', 'core', ''),
 'Text size smaller': ('ic_font_size · ic_textsize_change (one icon, opens a 4-step list)', 'core-variant', 'Core: one "text size" icon. iOS adds smaller/larger glyphs (DEC-17, PLAT-08).'),
 'Text size larger': ('(same single icon)', 'core-variant', 'See Text size smaller.'),
 'Follow topic': ('ic_follow_topic (file exists, not used)', 'ios-only', 'Android file is unreferenced.'),
 'Unfollow topic': ('ic_unfollow_topic (file exists, not used)', 'ios-only', 'Android file is unreferenced.'),
 'Checked': ('ic_check · ic_topic_selected · radio_button_on', 'core', ''),
 'Unchecked': ('radio_button_off', 'core', ''),
 'Continue': ('arrow_circle_right', 'core', ''),
 'Expand page': (None, 'ios-only', 'Android eEdition is the PageSuite SDK; its icons ship inside the SDK.'),
 'Fit to screen': (None, 'ios-only', 'PageSuite SDK on Android.'),
 'Previous page': (None, 'ios-only', 'PageSuite SDK on Android.'),
 'Next page': (None, 'ios-only', 'PageSuite SDK on Android.'),
 'Play': ('play_player_button · ic_persistent_player_play · ic_play_btn · btn_play_large', 'core', ''),
 'Pause': ('pause_player_button · ic_persistent_player_pause', 'core', ''),
 'Skip back 15 s': (None, 'ios-only', 'Android player has no skip controls.'),
 'Skip forward 15 s': (None, 'ios-only', 'Android player has no skip controls.'),
 'Rewind': (None, 'ios-only', ''),
 'Fast forward': (None, 'ios-only', ''),
 '3D embed': (None, 'ios-only', ''),
 'Tournament sport symbols (6)': (None, 'ios-only', 'Android World Cup tabs use text (Barlow Condensed), no icons.'),
 'Rating star (empty)': (None, 'ios-only', 'Android stars mean saved, not rating.'),
 'Rating star (half)': (None, 'ios-only', ''),
 'Rating star (full)': (None, 'ios-only', ''),
 'Like / favorite': (None, 'ios-only', 'iOS native tweet embeds only.'),
 'Repost': (None, 'ios-only', 'iOS native tweet embeds only.'),
 'Verified': (None, 'ios-only', 'iOS native tweet embeds only.'),
 'Apple': ('apple_button (file exists, not used)', 'ios-only', 'Sign in with Apple is iOS-only.'),
 'Google': ('google_button (only when Auth0 is off)', 'core', 'Dormant on Android.'),
 'Facebook': ('fb_button · ic_fb · author_contact_facebook', 'core', ''),
 'X (Twitter)': ('ic_twitter · author_contact_x', 'core', ''),
 'Bluesky': ('author_contact_bluesky', 'core', ''),
 'Instagram': ('author_contact_instagram', 'core', ''),
 'YouTube': (None, 'ios-only', ''),
 'Vimeo': (None, 'ios-only', ''),
 'Amazon (sign-in)': ('ic_amazon', 'core', ''),
 '1Password': (None, 'ios-only', 'iOS paywall password autofill.'),
 'Outbrain': (None, 'ios-only', 'Not in Android drawables; confirm Android Outbrain widget has no logo.'),
}
ANDROID_ONLY = [
 ('Navigation & UI', 'Notification small icon', 'per-market notification icons (monochrome)', 'android-only', 'Android requires a monochrome status-bar icon; no iOS equivalent.'),
 ('Ratings & social', 'Save star (special sections)', 'card_star_default · star_on_card_saved_state', 'android-only', 'Same meaning as Saved; kept as Android\'s glyph for now, one icon name (DEC-17, PLAT-09 rejected).'),
]
res = []
for g, purpose, ios_today, sf, mat, fa, rec in rows:
    a, b, note = ANDROID[purpose]
    res.append({'group': g, 'purpose': purpose, 'ios_today': ios_today, 'android_today': a, 'sf_symbol': sf,
                'material': mat[0] if mat else None, 'bucket': b, 'note': note, 'ios_recommendation': rec})
for g, p, a, b, n in ANDROID_ONLY:
    res.append({'group': g, 'purpose': p, 'ios_today': None, 'android_today': a, 'sf_symbol': None, 'material': None, 'bucket': b, 'note': n, 'ios_recommendation': None})
from collections import Counter
summary = Counter(r['bucket'] for r in res)
json.dump({'source': {'ios': 'TroncKit @ e30ad2585', 'android': 'android-tribpub @ 1cfb069a6'}, 'summary': dict(summary), 'purposes': res}, open(out, 'w'), indent=1)
print(dict(summary), len(res))

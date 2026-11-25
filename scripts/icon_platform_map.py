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
 'Saved': ('ic_bookmark · ic_btn_save · mc_tab_icon_saved', 'core', 'Android special-section star (card_star_default) also means saved: kept as Android\'s glyph, same icon name (DEC-17, PLAT-09 rejected). iOS has no Saved tab: Saved is a segment of the YOU tab (Apps team, 2026-11-19).'),
 'Home tab': ('mc_tab_icon_latestnews (77 market copies)', 'core', 'Both apps ship per-market Home icons; one Core glyph removes ~86 files. Android: only the Home tab icon is per market (Apps team, 2026-11-19).'),
 'Sections / menu': ('mc_tab_icon_sections', 'core', ''),
 'Alerts tab': ('mc_tab_icon_alerts · mc_alert_bell (69 market copies)', 'core', ''),
 'For You / Your News tab': ('mc_tab_icon_for_you', 'core', 'Gap on both: one custom Core vector.'),
 'eNewspaper tab': ('mc_tab_icon_newspaper · ic_newspaper', 'core', ''),
 'Games tab': ('mc_tab_icon_games · ic_games', 'core', ''),
 'Expand / show more': ('icon_uparrow', 'core', ''),
 'Collapse / show less': ('icon_downarrow', 'core', ''),
 'Back': ('web_view_navigation_back · ic_arrow_back_black_24dp (from PDFViewCtrlTools)', 'core', ''),
 'Forward / disclosure': ('web_view_navigation_forward · ic_arrow · liveblog_arrow · game_open_arrow', 'core', 'Android has 4 arrows for this; consolidate.'),
 'Close': ('ic_close_white_36dp · xbutton · ic_ad_close · close_player_button · ic_persistent_player_close', 'core', ''),
 'Close (circle)': ('ic_clear_search (search clear)', 'core', 'Confirm the Android glyph is a circled X.'),
 'Account': (None, 'ios-only', 'Android equivalent: none (login is the Auth0 web page; no account icon).'),
 'Warning': ('stat_notify_error (Android framework, notifications only)', 'core', 'Android uses it only in notifications.'),
 'Email': ('ic_email', 'core', ''),
 'Refresh': ('ic_wc_refresh', 'core', ''),
 'Filter': ('ic_filter (+27 market copies)', 'core', ''),
 'Text size smaller': (None, 'ios-only', 'iOS only (Karl, 2026-11-19, DEC-21). Android equivalent: one text-size icon (text-size, Android only).'),
 'Text size larger': (None, 'ios-only', 'iOS only (Karl, 2026-11-19, DEC-21). Android equivalent: one text-size icon (text-size, Android only).'),
 'Follow topic': ('ic_follow_topic (file exists, not used)', 'ios-only', 'Android equivalent: none shipped (file unused; topics are picked with Your News checkboxes).'),
 'Unfollow topic': ('ic_unfollow_topic (file exists, not used)', 'ios-only', 'Android equivalent: none shipped (file unused; topics are picked with Your News checkboxes).'),
 'Checked': ('ic_check · ic_topic_selected · radio_button_on', 'core', ''),
 'Unchecked': ('radio_button_off', 'core', ''),
 'Continue': ('arrow_circle_right', 'core', ''),
 'Expand page': (None, 'ios-only', 'Android equivalent: the PageSuite eEdition SDK draws its own controls (not our icons).'),
 'Fit to screen': (None, 'ios-only', 'Android equivalent: inside the PageSuite SDK (not our icons).'),
 'Previous page': (None, 'ios-only', 'Android equivalent: inside the PageSuite SDK (not our icons).'),
 'Next page': (None, 'ios-only', 'Android equivalent: inside the PageSuite SDK (not our icons).'),
 'Play': ('play_player_button · ic_persistent_player_play · ic_play_btn · btn_play_large', 'core', ''),
 'Pause': ('pause_player_button · ic_persistent_player_pause', 'core', ''),
 'Skip back 15 s': (None, 'ios-only', 'iOS only (Karl, 2026-11-19, DEC-21: the apps do different things, so one icon per platform). Android equivalent: skip-back-10 (Android only).'),
 'Skip forward 15 s': (None, 'ios-only', 'iOS only (Karl, 2026-11-19, DEC-21: the apps do different things, so one icon per platform). Android equivalent: skip-forward-10 (Android only).'),
 'Rewind': (None, 'ios-only', 'The PostKit player (Washington Post SDK in TroncKit) draws a counter-clockwise arrow with 15: same job as skip-back-15 (DEC-28). Android equivalent: skip-back-10.'),
 'Fast forward': (None, 'ios-only', 'The PostKit player draws a clockwise arrow with 15: same job as skip-forward-15 (DEC-28). Android equivalent: skip-forward-10.'),
 'Exit full screen': (None, 'ios-only', 'PostKit video player (DEC-28; was filed under Close). Android equivalent: none in the Android guide.'),
 'Player error': (None, 'ios-only', 'PostKit player error and offline states: one drawing for both (DEC-28). Android equivalent: none in the Android guide.'),
 'Coach-mark arrow': (None, 'ios-only', 'eNewspaper (DEC-28; was filed under Sections / menu). Where it shows is asked of the Apps team (MISSING-ASSETS 1.2). Android equivalent: the PageSuite SDK draws its own.'),
 '3D embed': (None, 'ios-only', 'Android equivalent: none in the Android guide.'),
 'Tournament sport symbols (6)': (None, 'ios-only', 'Android equivalent: none; World Cup tabs use text (Barlow Condensed).'),
 'Rating star (empty)': (None, 'ios-only', 'Android equivalent: none; its stars mean saved (special sections), not ratings.'),
 'Rating star (half)': (None, 'ios-only', 'Android equivalent: none (see Rating star (empty)).'),
 'Rating star (full)': (None, 'ios-only', 'Android equivalent: none (see Rating star (empty)).'),
 'Like / favorite': (None, 'ios-only', 'iOS native tweet embeds only. Android equivalent: none in the Android guide.'),
 'Repost': (None, 'ios-only', 'iOS native tweet embeds only. Android equivalent: none in the Android guide.'),
 'Verified': (None, 'ios-only', 'iOS native tweet embeds only. Android equivalent: none in the Android guide.'),
 'Apple': ('apple_button (file exists, not used)', 'ios-only', 'Sign in with Apple is iOS only. Android equivalent: none shipped (file unused).'),
 'Google': ('google_button (only when Auth0 is off)', 'core', 'Dormant on Android.'),
 'Facebook': ('fb_button · ic_fb · author_contact_facebook', 'core', ''),
 'X (Twitter)': ('ic_twitter · author_contact_x', 'core', ''),
 'Bluesky': ('author_contact_bluesky', 'core', ''),
 'Instagram': ('author_contact_instagram', 'core', ''),
 'YouTube': (None, 'ios-only', 'Android equivalent: none in the Android guide.'),
 'Vimeo': (None, 'ios-only', 'Android equivalent: none in the Android guide.'),
 'Amazon (sign-in)': ('ic_amazon', 'core', 'Neither app shows it: login is the Auth0 web page on both. Dropped (DROPPED below).'),
 '1Password': (None, 'ios-only', 'iOS paywall password autofill. Android equivalent: none in the Android guide.'),
 'Outbrain': (None, 'ios-only', 'Android equivalent: none in the Android drawables (whether the Outbrain widget shows a logo there is not in the guide).'),
}
ANDROID_ONLY = [
 ('Navigation & UI', 'Text size', 'ic_font_size · ic_textsize_change (one icon, opens a 4-step list)', 'android-only', 'Android only (Karl, 2026-11-19, DEC-21). iOS equivalent: text-size-smaller and text-size-larger (iOS only).'),
 ('Media', 'Skip back 10 s', 'Media3 skip_back_10 (AppPlaybackService SEEK_INCREMENT_MS 10_000)', 'android-only', 'Android only (Karl, 2026-11-19, DEC-21: the apps do different things, so one icon per platform). iOS equivalent: skip-back-15 (iOS only). Interval difference: DSC-35.'),
 ('Media', 'Skip forward 10 s', 'Media3 skip_forward_10', 'android-only', 'Android only (Karl, 2026-11-19, DEC-21: the apps do different things, so one icon per platform). iOS equivalent: skip-forward-15 (iOS only). Interval difference: DSC-35.'),
 ('Navigation & UI', 'Notification small icon', 'per-market notification icons (monochrome)', 'android-only', 'Android requires a monochrome status-bar icon. iOS equivalent: none needed (iOS notifications show the app icon).'),
 ('Ratings & social', 'Save star (special sections)', 'card_star_default · star_on_card_saved_state', 'android-only', 'Same meaning as Saved. iOS equivalent: the Saved bookmark (shared name saved, DEC-17, PLAT-09 rejected).'),
]
# Purposes left out of the design system: never shown in either app (they stay in icon-comparison.json as reference)
DROPPED = {'Amazon (sign-in)': 'Never shown on either app: iOS has no Amazon icon (only a text-only button on the native login screen, which never opens because Auth0 is on in all 78 markets); Android never shows ic_amazon (Apps team, DREAMT-4718 / 4719, 2026-11-23, MISSING-ASSETS 1.12).'}
res = []
for g, purpose, ios_today, sf, mat, fa, rec in rows:
    if purpose in DROPPED: continue
    a, b, note = ANDROID[purpose]
    res.append({'group': g, 'purpose': purpose, 'ios_today': ios_today, 'android_today': a, 'sf_symbol': sf,
                'material': mat[0] if mat else None, 'bucket': b, 'note': note, 'ios_recommendation': rec})
for g, p, a, b, n in ANDROID_ONLY:
    res.append({'group': g, 'purpose': p, 'ios_today': None, 'android_today': a, 'sf_symbol': None, 'material': None, 'bucket': b, 'note': n, 'ios_recommendation': None})
from collections import Counter
summary = Counter(r['bucket'] for r in res)
json.dump({'source': {'ios': 'TroncKit @ f79fe3339', 'android': 'android-tribpub @ 1cfb069a6'}, 'summary': dict(summary), 'purposes': res, 'dropped': [{'purpose': k, 'why': v} for k, v in DROPPED.items()]}, open(out, 'w'), indent=1)
print(dict(summary), len(res))

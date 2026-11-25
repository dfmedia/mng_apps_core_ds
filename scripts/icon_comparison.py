import json
# group, purpose, ios_today, sf, material(name, font M=Symbols Rounded / I=Material Icons filled), fa(name, unicode, style S/R/B)
R=[
("Navigation & UI","Search","FA search · nav-search (3 PNG) · ENewspaper search (2)","magnifyingglass",("search","M"),("search","f002","S")),
("Navigation & UI","Settings","nav-settings (3 PNG)","gearshape",("settings","M"),("cog","f013","S")),
("Navigation & UI","Share","nav-share PNG","square.and.arrow.up",("share","M"),("share-alt","f1e0","S")),
("Navigation & UI","Save (not saved)","FA bookmark · nav-save-unfilled · Unsaved-Article · Saved-Unfilled-* (9)","bookmark",("bookmark","M"),("bookmark","f02e","R")),
("Navigation & UI","Saved","nav-save-filled · Saved-Article · Saved-Filled-* (9) · Saved tab icons (11)","bookmark.fill",("bookmark","I"),("bookmark","f02e","S")),
("Navigation & UI","Home tab","FA home · tab-home · 9 market home icons","house",("home","M"),("home","f015","S")),
("Navigation & UI","Sections / menu","FA bars · tab-sections · eNewspaper menu","line.3.horizontal",("menu","M"),("bars","f0c9","S")),
("Navigation & UI","Alerts tab","FA bell · tab-alerts · Alert/bell","bell",("notifications","M"),("bell","f0f3","R")),
("Navigation & UI","For You / Your News tab","tab-foryou · For You · YourNews-* (11)",None,None,None),
("Navigation & UI","eNewspaper tab","tab-enews · tab-newspaper","newspaper",("newspaper","M"),("newspaper","f1ea","R")),
("Navigation & UI","Games tab","tab-games · SF gamecontroller.fill","gamecontroller.fill",("sports_esports","M"),("gamepad","f11b","S")),
("Navigation & UI","Expand / show more","FA chevronUp · Chevron - Up · chevron_up","chevron.up",("expand_less","M"),("chevron-up","f077","S")),
("Navigation & UI","Collapse / show less","FA chevronDown · Chevron - Down · chevron_down · button-downarrow","chevron.down",("expand_more","M"),("chevron-down","f078","S")),
("Navigation & UI","Back","SF chevron.left","chevron.left",("arrow_back","M"),("chevron-left","f053","S")),
("Navigation & UI","Forward / disclosure","SF chevron.right","chevron.right",("chevron_right","M"),("chevron-right","f054","S")),
("Navigation & UI","Close","CloseButton · overlay-close · BannerCloseLight · SF xmark","xmark",("close","M"),("times","f00d","S")),
("Navigation & UI","Close (circle)","SF xmark.circle.fill · button-miniplayer-close (2)","xmark.circle.fill",("cancel","M"),("times-circle","f057","S")),
("Navigation & UI","Account","SF person.circle.fill","person.circle.fill",("account_circle","M"),("user-circle","f2bd","S")),
("Navigation & UI","Warning","SF exclamationmark.triangle.fill · exclamation-icon","exclamationmark.triangle.fill",("warning","M"),("exclamation-triangle","f071","S")),
("Navigation & UI","Email","SF envelope.fill","envelope.fill",("mail","M"),("envelope","f0e0","S")),
("Navigation & UI","Refresh","SF arrow.clockwise","arrow.clockwise",("refresh","M"),("redo","f01e","S")),
("Navigation & UI","Filter","icon_filter","line.3.horizontal.decrease",("filter_list","M"),("filter","f0b0","S")),
("Navigation & UI","Text size smaller","textsizesmall","textformat.size.smaller",("text_decrease","M"),None),
("Navigation & UI","Text size larger","textsizelarge","textformat.size.larger",("text_increase","M"),None),
("Topics & selection","Follow topic","BTN_FollowTopic · FollowTopic · Plus-CT","plus.circle",("add_circle","M"),("plus-circle","f055","S")),
("Topics & selection","Unfollow topic","BTN_UnFollowTopic · UnFollowTopic · Minus-CT","minus.circle",("do_not_disturb_on","M"),("minus-circle","f056","S")),
("Topics & selection","Checked","Checked · Checkmark-* (7) · GreyCheckmark · WhiteCheckmark · ButtonWithCheckmark · TopicSelection-* (9)","checkmark.circle.fill",("check_circle","I"),("check-circle","f058","S")),
("Topics & selection","Unchecked","Unchecked · Uncheck-* (8)","circle",("radio_button_unchecked","M"),("circle","f111","R")),
("Topics & selection","Continue","Continue-* (10)","arrow.right.circle.fill",("arrow_circle_right","I"),("arrow-circle-right","f0a9","S")),
("eNewspaper","Expand page","expand-paper (2)","arrow.up.left.and.arrow.down.right",("open_in_full","M"),("expand","f065","S")),
("eNewspaper","Fit to screen","fit-to-screen (2)","arrow.down.right.and.arrow.up.left",("close_fullscreen","M"),("compress","f066","S")),
("eNewspaper","Previous page","left-arrow (2)","arrow.left",("arrow_back","M"),("arrow-left","f060","S")),
("eNewspaper","Next page","right-arrow (2)","arrow.right",("arrow_forward","M"),("arrow-right","f061","S")),
("Media","Play","button-play* (6) · embed-play · button-miniplayer-play (2) · SF play.fill","play.fill",("play_arrow","I"),("play","f04b","S")),
("Media","Pause","button-pause* (5) · button-miniplayer-pause (2) · SF pause.fill","pause.fill",("pause","I"),("pause","f04c","S")),
("Media","Skip back 15 s","SF gobackward.15","gobackward.15",None,None),
("Media","Skip forward 15 s","SF goforward.15","goforward.15",None,None),
("Media","Rewind","button-rewind","backward.fill",("fast_rewind","I"),("backward","f04a","S")),
("Media","Fast forward","button-fastforward","forward.fill",("fast_forward","I"),("forward","f04e","S")),
("Media","3D embed","embed-3d","cube",("view_in_ar","M"),("cube","f1b2","S")),
("Media","Tournament sport symbols (6)","SF soccerball.inverse · american.football.fill · baseball.fill · basketball.fill · hockey.puck.fill (fallback sportscourt.fill), 72 pt",None,None,None),
("Ratings & social","Rating star (empty)","rating-star-empty","star",("star","M"),("star","f005","R")),
("Ratings & social","Rating star (half)","rating-star-half","star.leadinghalf.filled",("star_half","I"),("star-half-alt","f5c0","S")),
("Ratings & social","Rating star (full)","rating-star-full","star.fill",("star","I"),("star","f005","S")),
("Ratings & social","Like / favorite","tweet-favorite","heart",("favorite","M"),("heart","f004","R")),
("Ratings & social","Repost","tweet-retweet","arrow.2.squarepath",("repeat","M"),("retweet","f079","S")),
("Ratings & social","Verified","tweet-verified","checkmark.seal.fill",("verified","I"),None),
("Brands","Apple","AppleIcon (Sign in with Apple)","apple.logo",None,("apple","f179","B")),
("Brands","Google","GoogleIcon",None,None,("google","f1a0","B")),
("Brands","Facebook","FacebookIcon · AuthorContactFacebook",None,None,("facebook","f09a","B")),
("Brands","X (Twitter)","TwitterIcon · AuthorContactX · tweet-logo · twitter-logo",None,None,("twitter (old bird)","f099","B")),
("Brands","Bluesky","AuthorContactBluesky",None,None,None),
("Brands","Instagram","AuthorContactInstagram · instagram-logo (3)",None,None,("instagram","f16d","B")),
("Brands","YouTube","youtube-logo",None,None,("youtube","f167","B")),
("Brands","Vimeo","vimeo-logo",None,None,("vimeo-v","f27d","B")),
("Brands","Amazon (sign-in)","TroncKit default button",None,None,("amazon","f270","B")),
("Brands","1Password","paywall-1password",None,None,None),
("Brands","Outbrain","outbrainLogo",None,None,None),
# DEC-28 (Karl, 2026-11-25): files that were filed under the wrong purpose get their own row
("Navigation & UI","Exit full screen","video-fullscreen-close (PostKit)","arrow.down.right.and.arrow.up.left",("close_fullscreen","M"),None),
("Media","Player error","player-error-image · player-offline-image (PostKit, same drawing)","exclamationmark.circle.fill",("error","M"),None),
("eNewspaper","Coach-mark arrow","menu-line",None,None,None),
]
def rec(r):
    g,p,ios,sf,m,fa=r
    if g=="Brands": return "Use official brand asset (custom Core vector)"
    if sf and m: return "Native on both platforms"
    if sf and not m: return "iOS native; Android needs custom vector"
    if not sf and not m: return "Custom vector needed — see Missing Assets"
    return "Android native; iOS needs custom vector"
rows=[[r[0],r[1],r[2],r[3],list(r[4]) if r[4] else None,list(r[5]) if r[5] else None,rec(r)] for r in R]
n=len(rows); sf=sum(1 for r in rows if r[3]); m=sum(1 for r in rows if r[4]); fa=sum(1 for r in rows if r[5])
print(json.dumps({'n':n,'sf':sf,'m':m,'fa':fa}))
json.dump(rows,open('data/icon-comparison.json','w'),separators=(',',':'))

"""Question bank: 20 privacy categories x 2 questions each.

Each answer option is (label, risk) where risk is 0 (best) .. 4 (worst).
Question weight (1-3) says how much that question matters inside its category.
Category weight says how much the category matters in the overall score.
"""
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass(frozen=True)
class Question:
    id: str
    category: str
    text: str
    options: Tuple[Tuple[str, int], ...]
    weight: int
    weakness: str          # shown when the answer is high-risk
    recommendation: str    # shown when the answer is not ideal

@dataclass(frozen=True)
class Category:
    key: str
    name: str
    weight: float          # relative importance in the overall score
    description: str
    awareness: str         # short security-awareness guidance
    checklist: str         # one-line checklist item

# ---- Reusable option scales -------------------------------------------------
VIS = (("Only me / nobody", 0), ("Close friends or small custom list", 1),
       ("Friends / connections only", 2), ("Friends of friends", 3), ("Public", 4))
SHARE = (("Never shared", 0), ("Shared with a small trusted list only", 1),
         ("Shared with friends only", 2), ("Shared with friends of friends", 3),
         ("Shared publicly", 4))
FREQ = (("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4))
YN_GOOD = (("Yes, always", 0), ("Mostly", 1), ("Sometimes", 2), ("Rarely", 3), ("Never / not sure", 4))

CATEGORIES: List[Category] = [
 Category("profile_visibility","Profile visibility",6,"Who can find and view your profile.",
  "A public profile gives strangers (and automated tools) a ready-made starting point for social engineering.",
  "Profile is limited to people I know"),
 Category("personal_info","Personal-information exposure",6,"Real name, photos, bio details on your profile.",
  "Small details (pet names, school, hobbies) are often reused in security questions and passwords.",
  "Profile shows minimal personal details"),
 Category("contact_info","Contact-information exposure",5,"Email and phone visibility.",
  "Visible contact details enable phishing, SMS scams, SIM-swap targeting and credential-stuffing.",
  "Email and phone are hidden from non-contacts"),
 Category("location","Location exposure",6,"Check-ins, geotags, live location, home city.",
  "Location patterns reveal where you live, work and when you are away from home.",
  "Location sharing is off or limited"),
 Category("work_edu","Workplace / education exposure",5,"Employer, role, school, graduation year.",
  "Employer details help attackers craft believable spear-phishing and impersonation (e.g., fake HR or IT).",
  "Work and school details are limited"),
 Category("birthday","Birthday exposure",4,"Full date of birth visibility.",
  "A full birth date is a common identity-verification data point and a frequent password component.",
  "Birth year is hidden; only day/month shown to friends at most"),
 Category("family","Family / relationship information",4,"Relatives, partner and relationship status.",
  "Family names and relationships help with 'trusted contact' scams and security-question guessing.",
  "Family links are private"),
 Category("post_visibility","Post visibility",6,"Default audience for new posts and stories.",
  "Public-by-default posting means every casual post is permanently searchable and screenshot-able.",
  "Default post audience is friends or narrower"),
 Category("friends_control","Friend / follower controls",5,"Who can send requests and see your friend list.",
  "Visible friend lists let attackers clone your identity and target your contacts.",
  "Friend list is hidden and requests are restricted"),
 Category("tagging","Tagging permissions",4,"Whether others can tag you without approval.",
  "Others can expose you through tags (location, events, photos) even if you post carefully.",
  "Tag review is turned on"),
 Category("third_party","Third-party application access",5,"Apps and games connected to your account.",
  "Forgotten connected apps can retain data access and are a common data-leak path.",
  "Connected apps reviewed in the last 6 months"),
 Category("authentication","Account authentication",6,"Password strength and recovery options.",
  "Weak or guessable passwords and recovery details are the most direct path to account takeover.",
  "Strong unique password and secure recovery options"),
 Category("mfa","MFA usage",7,"Multi-factor authentication.",
  "MFA blocks the majority of automated account-takeover attempts. App- or key-based MFA beats SMS.",
  "MFA enabled (authenticator app or security key preferred)"),
 Category("password_reuse","Password reuse awareness",6,"Reuse of passwords across sites; manager use.",
  "Reused passwords turn one breach elsewhere into a takeover of this account.",
  "Unique passwords stored in a password manager"),
 Category("login_alerts","Login alerts",3,"Alerts for new-device logins and session review.",
  "Alerts give you early warning; unreviewed old sessions can leave attackers logged in.",
  "Login alerts on; active sessions reviewed regularly"),
 Category("unknown_requests","Unknown connection requests",5,"Handling requests from people you do not know.",
  "Fake or cloned accounts use friend requests to gain trust and access to friends-only content.",
  "Unknown requests are declined / verified first"),
 Category("suspicious_links","Suspicious links / messages",6,"Clicking links, handling unexpected DMs.",
  "Phishing via direct messages (often from a hijacked friend account) is a leading attack vector.",
  "Unexpected links are verified before clicking"),
 Category("photo_metadata","Photo metadata awareness",3,"EXIF/GPS data in photos you upload.",
  "Photos can embed GPS coordinates and device info if the platform or your upload path does not strip them.",
  "Aware of EXIF; location tagging off in camera"),
 Category("historical_posts","Historical posts",4,"Old posts and old public content.",
  "Old posts can resurface in searches and contain outdated sensitive details.",
  "Old posts reviewed or limited to a narrower audience"),
 Category("social_engineering","Social-engineering exposure",6,"Oversharing and verification habits.",
  "Attackers combine small public facts into convincing pretexts. Verify identity through a second channel.",
  "Requests for money/codes are verified out-of-band"),
]

def _q(id_, cat, text, opts, w, weak, rec):
    return Question(id_, cat, text, tuple(opts), w, weak, rec)

QUESTIONS: List[Question] = [
 _q("pv1","profile_visibility","Who can find your profile through search engines or platform search?",VIS,3,
    "Your profile can be discovered by almost anyone.","Limit search-engine indexing and set profile discoverability to friends or connections."),
 _q("pv2","profile_visibility","Who can see your full profile (about, photos, friends)?",VIS,2,
    "Strangers can view detailed profile content.","Switch the profile audience to 'Friends'; review the 'View as public' preview."),
 _q("pi1","personal_info","How much real, identifying detail does your profile show (full real name, face photo, bio specifics)?",
    (("Pseudonym / minimal info",0),("Name only",1),("Name + photo",2),("Name, photo, hometown, interests",3),("Detailed bio incl. personal specifics",4)),3,
    "Your profile exposes many identifying details at once.","Trim the bio; remove specifics such as pet names, street, school nicknames."),
 _q("pi2","personal_info","Do you post details commonly used as security-question answers (pet name, mother's maiden name, first school)?",FREQ,2,
    "You post details that double as security-question answers.","Stop posting security-question facts and change those questions' answers to random values stored in a password manager."),
 _q("ci1","contact_info","Who can see your email address?",SHARE,3,
    "Your email address is visible to a wide audience.","Hide email from non-connections; use an alias email for social accounts."),
 _q("ci2","contact_info","Who can see your phone number?",SHARE,3,
    "Your phone number is visible to a wide audience.","Hide your number and disable 'find me by phone number'."),
 _q("lo1","location","How often do you tag your location or check in on posts?",FREQ,3,
    "You frequently reveal where you are.","Turn off default location tagging; post about places after you have left."),
 _q("lo2","location","Who can see your city, hometown or live location?",SHARE,2,
    "Your home area or live location is widely visible.","Remove exact city/hometown and disable live location sharing."),
 _q("we1","work_edu","Who can see your employer and job title?",SHARE,3,
    "Your employer and role are widely visible.","Limit employer details to connections; avoid listing internal team names or projects."),
 _q("we2","work_edu","Who can see your school/college, department and graduation year?",SHARE,2,
    "Education details are widely visible.","Limit education details; omit graduation year and student ID photos."),
 _q("bd1","birthday","Who can see your full date of birth (day, month, year)?",SHARE,3,
    "Your full birth date is widely visible.","Hide the birth year entirely; restrict day/month to 'Only me'."),
 _q("bd2","birthday","Do you post birthday messages/photos that reveal your age or full date publicly?",FREQ,1,
    "Birthday posts reveal your birth date repeatedly.","Avoid public birthday posts; restrict wishes to friends."),
 _q("fa1","family","Who can see your family members and relationships on your profile?",SHARE,2,
    "Family links are widely visible.","Remove or hide family links; restrict to 'Only me'."),
 _q("fa2","family","How often do you publicly post details about family (children's names/schools, relatives' travel)?",FREQ,3,
    "Family details are posted publicly, including potentially vulnerable members.","Avoid naming children, schools or travel plans; use close-friends lists."),
 _q("po1","post_visibility","What is your default audience for new posts?",VIS,3,
    "New posts default to a wide audience.","Set default audience to Friends or a custom list."),
 _q("po2","post_visibility","Who can see your stories / temporary posts and comments on public pages?",VIS,2,
    "Stories and comments are visible beyond trusted people.","Restrict stories to close friends; review where your comments appear."),
 _q("fr1","friends_control","Who can send you friend/follow requests?",
    (("Nobody / invitation only",0),("Friends of friends",2),("Anyone",4)),2,
    "Anyone can send you requests.","Restrict requests to friends of friends or invitation only."),
 _q("fr2","friends_control","Who can see your friend/follower list?",VIS,3,
    "Your connections list is widely visible.","Hide your friend/follower list from non-friends."),
 _q("tg1","tagging","Do you review tags before they appear on your profile?",
    (("Yes, always (tag review on)",0),("Mostly",1),("Sometimes",2),("No, tags appear automatically",4)),3,
    "Others can tag you without your approval.","Turn on tag review for posts and photos."),
 _q("tg2","tagging","Who can tag you or post on your timeline/wall?",VIS,2,
    "A broad audience can tag you or post to your profile.","Limit who can tag you / post on your profile to friends."),
 _q("tp1","third_party","How many third-party apps/games/logins are connected to your account?",
    (("None",0),("1-3",1),("4-7",2),("8-15",3),("More than 15 / I don't know",4)),3,
    "Many connected apps hold access to your account.","Open connected-apps settings and remove anything unused."),
 _q("tp2","third_party","When did you last review app permissions and data they can access?",
    (("Within 3 months",0),("Within 6 months",1),("Within a year",2),("More than a year ago",3),("Never",4)),2,
    "App permissions have not been reviewed recently.","Schedule a 6-monthly review of connected apps and permissions."),
 _q("au1","authentication","How strong is your password for this account?",
    (("Long passphrase / manager-generated (16+ chars)",0),("12-15 chars, random",1),("8-11 chars, mixed",2),("Short or with personal info",3),("Simple / guessable",4)),3,
    "Your password is weak or guessable.","Use a manager-generated password or a 4+ word passphrase of 16+ characters."),
 _q("au2","authentication","Are your recovery email/phone secure and up to date?",
    (("Yes, secured with MFA and current",0),("Current but not MFA-protected",2),("Outdated or shared",3),("Not set / not sure",4)),2,
    "Account recovery options are weak or outdated.","Update recovery contacts and secure the recovery email with MFA."),
 _q("mf1","mfa","Which MFA do you use on this account?",
    (("Security key / passkey",0),("Authenticator app",1),("SMS codes",2),("MFA available but off",4),("Don't know / none",4)),3,
    "MFA is not protecting your account.","Enable MFA now; prefer an authenticator app or passkey over SMS."),
 _q("mf2","mfa","Do you have MFA enabled on the email account linked to your social media?",
    (("Yes, strong MFA",0),("Yes, SMS",1),("No",4),("Not sure",4)),3,
    "Your linked email lacks MFA, which can unlock password resets.","Enable MFA on your primary email first; it is the master key to your accounts."),
 _q("pr1","password_reuse","How often do you reuse this password (or small variations) on other sites?",FREQ,3,
    "Password reuse makes breach-driven takeover likely.","Make every password unique; change reused ones starting with email and banking."),
 _q("pr2","password_reuse","Do you use a password manager?",
    (("Yes, for everything",0),("For most accounts",1),("A few accounts",2),("Browser autofill only",3),("No",4)),2,
    "No dedicated password manager in use.","Adopt a reputable password manager and set a strong master passphrase."),
 _q("la1","login_alerts","Are alerts for unrecognized logins enabled?",
    (("Yes, email + app notification",0),("Yes, one channel",1),("Not sure",3),("No",4)),2,
    "You would not be warned about suspicious logins.","Enable unrecognized-login alerts on at least two channels."),
 _q("la2","login_alerts","How often do you review active sessions/devices and log out unknown ones?",
    (("Monthly",0),("Every few months",1),("Yearly",2),("Rarely",3),("Never",4)),2,
    "Old or unknown sessions may remain logged in.","Review active sessions monthly and sign out anything unfamiliar."),
 _q("ur1","unknown_requests","How often do you accept requests from people you do not know?",FREQ,3,
    "You often accept unknown connections.","Only accept people you can verify; check mutual friends and account age."),
 _q("ur2","unknown_requests","Do you verify unknown or 'old friend, new account' requests through another channel?",YN_GOOD,2,
    "Cloned-account requests may not be verified.","Message the person on a known channel before accepting a 'new account' request."),
 _q("sl1","suspicious_links","How often do you click links in unexpected direct messages (even from friends)?",FREQ,3,
    "You often click unexpected links.","Treat unexpected links as suspicious; ask the sender via another channel."),
 _q("sl2","suspicious_links","Do you know how to report phishing/scam messages on your platform?",
    (("Yes, and I do it",0),("Yes",1),("Roughly",2),("No",3),("Never thought about it",4)),1,
    "You do not know how to report phishing.","Learn the platform's 'report' flow and block the sender after reporting."),
 _q("pm1","photo_metadata","Are you aware that photos can contain hidden GPS/device data (EXIF)?",
    (("Yes, and I strip or disable it",0),("Yes, and I sometimes check",1),("Heard of it",2),("No",3),("No, and location tagging is on in my camera",4)),2,
    "You may be leaking GPS data in photos.","Disable camera geotagging and use 'remove location' when sharing."),
 _q("pm2","photo_metadata","How often do you post photos of your home, workplace, vehicle plate, ID or tickets?",FREQ,3,
    "Photos may reveal sensitive places or documents.","Crop or blur plates, addresses, badges, boarding passes and tickets before posting."),
 _q("hp1","historical_posts","How old is the oldest post you have left visible to a wide audience?",
    (("Nothing public / all restricted",0),("Less than 1 year",1),("1-3 years",2),("3-7 years",3),("More than 7 years",4)),2,
    "Old public posts remain searchable.","Use 'limit past posts' and archive or delete old content."),
 _q("hp2","historical_posts","When did you last audit your old posts, photos and comments?",
    (("Within 6 months",0),("Within a year",1),("1-3 years ago",2),("More than 3 years ago",3),("Never",4)),2,
    "Your post history has not been audited.","Run a yearly audit of old posts, photos and comments."),
 _q("se1","social_engineering","Would you share a one-time code, or send money/gift cards, to a 'friend' who asked in chat?",
    (("Never without calling them",0),("Probably verify first",1),("Maybe if it sounded urgent",3),("Yes, I would help quickly",4)),3,
    "Urgency-based scams could succeed against you.","Adopt a rule: never share codes; verify money requests by voice call."),
 _q("se2","social_engineering","How often do you overshare (travel plans, routines, workplace details, achievements) publicly?",FREQ,2,
    "Public oversharing gives attackers material for pretexts.","Post travel/events after the fact and keep routine details private."),
]

CATEGORY_BY_KEY = {c.key: c for c in CATEGORIES}
QUESTION_BY_ID = {q.id: q for q in QUESTIONS}

def questions_for(category_key: str):
    return [q for q in QUESTIONS if q.category == category_key]

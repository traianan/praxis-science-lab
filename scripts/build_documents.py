"""Build the public English app documentation from reviewed source inventories."""
from pathlib import Path
from html import escape as e
import json
import re
import argparse

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://traianan.github.io/praxis-science-lab/'
EMAIL = 'traiananghel@gmail.com'
DATE = '2026-09-08'
APPS = json.loads((ROOT/'scripts/apps.json').read_text(encoding='utf-8'))
parser = argparse.ArgumentParser()
parser.add_argument('--app', choices=[a['slug'] for a in APPS], help='Rebuild only this app and the shared indexes.')
parser.add_argument('--home-only', action='store_true', help='Update only the homepage app cards.')
args = parser.parse_args()
home = (ROOT/'index.html').read_text(encoding='utf-8')
theme = re.search(r'<div class="theme-control".*?</div>', home, re.S).group()

def paragraphs(text):
    return ''.join(f'<p>{e(p)}</p>' for p in text.split('\n\n'))

def items(values):
    return '<ul>'+''.join(f'<li>{e(v)}</li>' for v in values)+'</ul>'

def page(route, title, subtitle, body):
    prefix = '../' * len(Path(route).parts) if route else './'
    parts = Path(route).parts
    navigation = ''
    back = f'<a class="back-link" href="{prefix}"><span aria-hidden="true">←</span> Back to home</a>'
    if len(parts) >= 2 and parts[0] == 'apps':
        app_prefix = '../' if len(parts) > 2 else './'
        back = (f'<a class="back-link" href="{app_prefix}"><span aria-hidden="true">←</span> Back to app</a>'
                if len(parts) > 2 else f'<a class="back-link" href="{prefix}#apps"><span aria-hidden="true">←</span> All apps</a>')
        links = []
        for section, label in [('privacy', 'Privacy policy'), ('support', 'Support &amp; testing'), ('publishing', 'Google Play materials')]:
            current = ' aria-current="page"' if len(parts) > 2 and parts[2] == section else ''
            links.append(f'<a href="{app_prefix}{section}/"{current}>{label}</a>')
        navigation = '<nav class="document-links" aria-label="App navigation">'+''.join(links)+'</nav>'
    output = ROOT/route/'index.html'
    output.parent.mkdir(parents=True, exist_ok=True)
    css_version = '20260911-clear-audio' if route.startswith('apps/clear-audio') else '20260908-nav'
    output.write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#1739d6"><meta name="description" content="{e(subtitle, quote=True)}">
<title>{e(title)} | Praxis Science Lab</title><link rel="canonical" href="{BASE}{route}/">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<script src="{prefix}assets/theme.js?v=20260907-icons"></script>
<link rel="stylesheet" href="{prefix}assets/site.css?v={css_version}">
<script src="{prefix}assets/copyright.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a><div class="page-shell">
<header class="site-header"><a class="brand" href="{prefix}" aria-label="Praxis Science Lab home"><img src="{prefix}assets/logo-mark.svg" width="48" height="48" alt=""><span class="wordmark">PRAXIS<span>SCIENCE LAB</span></span></a>
<nav aria-label="Main navigation"><a href="{prefix}#apps">Our apps</a><a href="{prefix}publishing/">Publishing kit</a><a href="mailto:{EMAIL}">Contact</a></nav>{theme}</header>
<main id="main" class="document">{back}<p class="eyebrow">PRAXIS SCIENCE LAB / ANDROID</p><h1>{e(title)}</h1><p class="document-lead">{e(subtitle)}</p>{navigation}{body}<div class="document-return">{back}</div></main>
<footer class="site-footer"><p>© <span id="copyright-years">2026</span> Praxis Science Lab</p><a href="{prefix}privacy/">Website privacy</a><a href="mailto:{EMAIL}">{EMAIL}</a></footer></div></body></html>''',encoding='utf-8')

contact = f'<p>Praxis Science Lab is the publishing brand used by Traian Anghel. For support or privacy questions, email <a href="mailto:{EMAIL}">{EMAIL}</a>. Include the app name and version. Do not send passwords, medical records, private recordings or other sensitive information.</p>'
support_privacy = '''<p>If you contact us, we receive your email address and the information you choose to send. We use it to answer your request and resolve the issue, not for advertising. Correspondence remains only as needed for that purpose and any applicable legal obligations; you can request deletion. Our email provider processes messages under its own terms. We do not sell support correspondence.</p>'''
external = f'<p>Opening this policy or other external links sends ordinary connection information to the website or browser provider. See our <a href="{BASE}privacy/">website privacy notice</a>. App-local data is not automatically included in those requests.</p>'
cards=[]
for a in APPS:
    slug=a['slug']; route=f'apps/{slug}'; url=BASE+route+'/'
    media=ROOT/route/'media'; media.mkdir(parents=True,exist_ok=True)
    cards.append(f'''<li><h3><a href="{route}/">{e(a['name'])} <span aria-hidden="true">↗</span></a></h3><p>{e(a['short'])}</p><span class="status">{e(a['status'])}</span></li>''')
    if args.home_only or (args.app and slug != args.app):
        continue
    intro = f'<p><span class="status">{e(a["status"])}</span> Not yet available on Google Play.</p>'
    if slug=='medical-terminology-flashcards':
        desc='<p>An educational terminology study project. Release preparation and the production learning content are still in progress.</p>'
    else: desc=paragraphs(a['description'])
    download = ''
    if a.get('download'):
        d = a['download']
        download = f'''<section class="app-download" aria-labelledby="download-title"><h2 id="download-title">Try {e(a['name'])}</h2><p>{e(d['label'])} · Android {e(d['android'])} or later · {e(d['size'])}</p><a class="button" href="{e(d['path'], quote=True)}" download>Download Android APK <span aria-hidden="true">↓</span></a><p class="download-note">A development build for testing. English is the default; Romanian and Spanish are available in More → App language. This is a direct download, not a Google Play release.</p><p><a href="support/#install">Installation and update help</a> · <a href="downloads/SHA256SUMS.txt">SHA-256 checksum</a></p></section>'''
    gallery = ''
    if a.get('screenshots'):
        gallery = '<h2>Inside the app</h2><p>Actual screenshots from version '+e(a['version'])+'.</p><div class="app-gallery">'+''.join(f'<figure><img src="media/{e(shot["file"], quote=True)}" alt="{e(shot["alt"], quote=True)}" width="{int(shot.get("width",320))}" height="{int(shot.get("height",640))}" loading="lazy"><figcaption>{e(shot["caption"])}</figcaption></figure>' for shot in a['screenshots'])+'</div>'
    if a.get('previews'):
        gallery += '<h2>Interface preview</h2><p>Rendered from the development app interface, version '+e(a['version'])+'. These previews are not Google Play screenshots.</p><div class="app-gallery">'+''.join(f'<figure><img src="media/{e(shot["file"], quote=True)}" alt="{e(shot["alt"], quote=True)}" width="{int(shot["width"])}" height="{int(shot["height"])}" loading="lazy"><figcaption>{e(shot["caption"])}</figcaption></figure>' for shot in a['previews'])+'</div>'
    page(route,a['name'],a['short'],intro+download+desc+gallery+f'<h2>Language</h2><p>{e(a["language"])}</p><h2>Using the app</h2><p>{e(a["safety"])}</p>'+contact)
    privacy=f'<p>Effective date: {a.get("policy_date", DATE)}. This notice describes Android version {e(a["version"])} and the configuration documented below.</p>'+contact
    privacy+=f'<h2>Information handled by the app</h2>{paragraphs(a["data"])}<h2>Permissions, services and sharing</h2>{paragraphs(a["permissions"])}<h2>Retention and deletion</h2>{paragraphs(a["retention"])}'
    privacy+='<h2>Security</h2><p>Private app files use Android application storage protections. No additional database-encryption guarantee is made. Keep your device protected and control access to files you export. There is no Praxis Science Lab account to delete for this app.</p>'
    privacy+='<h2>Support messages and external pages</h2>'+support_privacy+external
    privacy+='<h2>Your choices</h2><p>You can clear local data and use the contact above to ask about support correspondence or request access, correction or deletion where applicable. We may need information to identify the relevant request. You may also contact your local data protection authority. Local app information is processed to provide the functions you use; support correspondence is processed to respond to your request.</p>'
    if slug=='atomic-clock':privacy+='<p>Time providers: <a href="https://www.cloudflare.com/privacypolicy/">Cloudflare privacy</a>, <a href="https://developers.google.com/time">Google Public NTP</a>, and <a href="https://www.apple.com/legal/privacy/">Apple privacy</a>. NTP Pool contains independently operated servers; provider practices may differ.</p>'
    if slug=='medical-terminology-flashcards':privacy+='<p>Provider information: <a href="https://policies.google.com/privacy">Google privacy policy</a>. Any future activation of advertising will be documented before that release is distributed.</p>'
    if slug=='clear-audio':privacy+='<p>Provider information: <a href="https://policies.google.com/privacy">Google privacy policy</a>, <a href="https://developers.google.com/admob/android/next-gen/privacy/play-data-disclosure">Google Mobile Ads Next-Gen data disclosure</a> and <a href="https://developers.google.com/admob/android/privacy">Google UMP privacy options</a>. Privacy options are available from More when the provider requires them. Test ad identifiers do not mean that no connection or device information is processed.</p>'
    if slug=='spinora':privacy+='<p>Provider information: <a href="https://policies.google.com/privacy">Google privacy policy</a> and <a href="https://developers.google.com/admob/android/privacy/play-data-disclosure">Google Mobile Ads data disclosure</a>. Demo advertising does not generate revenue and does not guarantee that no network or device information is processed.</p>'
    privacy+='<h2>Changes</h2><p>We update this notice when app behavior or relevant practices change. The date and version above identify the policy you are reading.</p>'
    page(route+'/privacy',a['name']+' — Privacy Policy','How Praxis Science Lab handles information for this Android app.',privacy)
    support=contact+'<h2>Report a problem</h2><p>Tell us your Android version, device model, app version, what you did, what happened and what you expected. Remove personal information from attachments. Never post a tester email list or private feedback in a public repository.</p>'
    if a.get('download'):
        support+='<h2 id="install">Install or update the development APK</h2><ol><li>Open the app page on an Android 9 or newer device and download the APK.</li><li>Open the downloaded file and follow the Android installer prompts. It is distributed directly from this site, not through Google Play.</li><li>If ClarAudio or Clear Audio is already installed from our development builds, install the update over it to keep settings and profiles. If Android reports a signing conflict, contact support before uninstalling; uninstalling removes private app data.</li><li>Open Clear Audio. Use More → App language to choose English, Română or Español. USB debugging is not needed for local file playback.</li></ol><p>This development build uses Google test ad identifiers and includes advanced diagnostic tools. Do not grant DUMP or other diagnostic privileges for normal use. Keep source audio files backed up independently.</p>'
    support+='<h2>Testing checklist</h2>'+items(a['checks'])+'<h2>Data removal</h2>'+paragraphs(a['retention'])+f'<p><a href="{url}privacy/">Read the privacy policy</a></p>'
    support+='<h2>Joining a test</h2><p>Testing invitations and opt-in links will be supplied once a Google Play testing track is available. This page does not enroll you in a test. Report your experience honestly; no positive review is required.</p>'
    page(route+'/support',a['name']+' — Support','Help, data-removal information and a practical tester checklist.',support)
    # Plain-text store fields are deliberately separate from public product claims.
    listing=f"{a['title']}\n\nShort description\n{a['short']}\n\nFull description\n{a['description']}\n\nPublisher: Praxis Science Lab\nSupport: {EMAIL}\nWebsite: {url}\nPrivacy: {url}privacy/\nSuggested category: {a['category']}\n"
    (ROOT/route/'store-listing-en.txt').write_text(listing,encoding='utf-8')
    console='<table><tr><th>Field</th><th>Prepared value / action</th></tr>'
    for label,value in [('Title',a['title']),('Package',a['package']),('Reviewed version',a['version']),('Publisher','Praxis Science Lab'),('Support email',EMAIL),('Suggested category',a['category']),('App access','No login or restricted account access'),('Ads',a.get('ads_notice', 'Current development configuration disabled; recheck every active artifact' if slug=='medical-terminology-flashcards' else 'No advertising found in reviewed app dependencies')),('Target audience and IARC','Answer from the real intended audience and final content. No age rating has been assigned here.'),('Health declaration','Educational medical reference: review the applicable declaration and account rules' if slug=='medical-terminology-flashcards' else 'No health functionality in the reviewed scope; complete the form accurately')]:
        console+=f'<tr><td>{e(label)}</td><td>{e(value)}</td></tr>'
    console+='</table>'
    safety_note = 'Candidate: no off-device app data collection or sharing found in the reviewed implementation. Local-only processing is different from collection in the Play form. Verify the exact signed package, included SDKs and every active release before submitting.'
    if slug=='atomic-clock':safety_note='Not finalized: network time providers receive IP/request information. Determine the applicable data categories, purposes, retention and sharing treatment with provider evidence. Do not assume that processing is ephemeral or that all transfers are encrypted.'
    if slug=='medical-terminology-flashcards':safety_note='Not finalized: the current blank-ID configuration disables ad requests, but advertising libraries remain included. Verify startup and every active release. If ads are enabled, inventory SDK identifiers, approximate location, interactions and diagnostics and update policy/consent/store answers first.'
    if a.get('data_safety_note'):safety_note=a['data_safety_note']
    body='<p class="quiet-note">Preparation materials, not a submission or Google approval. Use these fields only for a verified release with the described functionality.</p><p><a href="../publishing-kit.zip" download>Download the English publishing kit (ZIP)</a></p>'+console
    body+=f'<h2>English listing</h2><p><a href="../store-listing-en.txt" download>Download store listing text</a></p><h3>Short description</h3><p>{e(a["short"])}</p><h3>Full description</h3>{paragraphs(a["description"])}'
    body+='<h2>Data safety worksheet</h2>'+paragraphs(safety_note)+paragraphs(a['data'])+paragraphs(a['permissions'])
    body+='<h2>Media</h2><p><a href="../media/app-icon.png">App icon — 512 × 512 PNG</a></p><p><a href="../media/feature-graphic.png">Feature graphic — 1024 × 500 PNG</a></p><p>Capture at least two authentic screenshots from the final app. Do not use simulated screens, synthetic medical fixtures or old-brand captures. Screenshot language must reflect the actual app; English captions do not imply an English-only interface.</p>'
    shots=sorted(media.glob('screenshot-*.png'))
    if shots:
        body+='<p>Actual Android test-build captures, prepared for listing review. Recheck against the final upload build.</p><ul>'+''.join(f'<li><a href="../media/{shot.name}">{e(shot.stem.replace("-"," ").title())}</a></li>' for shot in shots)+'</ul>'
    body+='<h2>Remaining release checks</h2>'+items(a['gaps'])+f'<p><a href="{BASE}publishing/">Shared Google Play preparation guide</a></p>'
    if not a.get('publishing_assets', True):
        body = re.sub(r'<p><a href="../publishing-kit.zip".*?</p>', '', body)
        body = re.sub(r'<p><a href="../media/app-icon.png".*?</p>', '', body)
        body = re.sub(r'<p><a href="../media/feature-graphic.png".*?</p>', '', body)
    page(route+'/publishing',a['name']+' — Publishing Materials','English listing, data inventory, graphics and release checks.',body)

start_marker='<!-- ANDROID_APPS_START -->'
end_marker='<!-- ANDROID_APPS_END -->'
if start_marker in home:
    start=home.index(start_marker)
    end=home.index(end_marker,start)+len(end_marker)
else:
    start=home.index('<article class="app-card">')
    end=home.index('\n      </section>',start)
grid=start_marker+'\n<ul class="projects-grid android-apps-grid">\n'+'\n'.join(cards)+'\n</ul>\n'+end_marker
home=home[:start]+grid+home[end:]
home=home.replace('Our first app.','Our Android apps.')
home=home.replace('Each app will have its own privacy policy, legal information and support resources here when it is released.','Find a dedicated privacy policy, support page and release-preparation materials for each Android app.')
home=home.replace('App-specific pages are coming with our releases.','<a href="publishing/">Open the Google Play publishing kit</a>')
home=home.replace('Have a question about a project or something to report? Our public GitHub support area is the place to start.',f'For app support or privacy questions, email <a href="mailto:{EMAIL}">{EMAIL}</a>.')
home=home.replace('assets/site.css?v=20260907-icons','assets/site.css?v=20260908-docs')
home=home.replace('assets/site.css?v=20260908-docs','assets/site.css?v=20260908-nav')
home=re.sub(r'assets/site\.css\?v=[^"\s]+','assets/site.css?v=20260911-compact-apps',home)
home=home.replace('<p>Curiosity, put into practice.</p>','<a href="privacy/">Website privacy</a>')
(ROOT/'index.html').write_text(home,encoding='utf-8')
if args.home_only:
    print(f'Updated compact homepage grid for {len(APPS)} Android apps.')
    raise SystemExit(0)

page('privacy','Website Privacy','Privacy information for the Praxis Science Lab documentation website.',f'<p>Effective date: {DATE}.</p>'+contact+'<h2>Site operation</h2><p>This static website uses GitHub Pages hosting. It has no application account, advertising, analytics script, contact form or tracking cookies added by Praxis Science Lab. It stores your selected color theme in browser local storage. You can remove it through browser site-data controls.</p><p>GitHub receives ordinary connection information when serving pages, including your IP address. See <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub privacy information</a>. GitHub controls hosting logs and their retention. External links and your email provider have separate privacy practices.</p><h2>Contact and deletion</h2>'+support_privacy+'<p>You can ask us to access, correct or delete correspondence through the contact above. App-specific privacy policies describe local app data separately. GitHub issues are public and require a GitHub account; do not use them for private information.</p><h2>Updates</h2><p>The effective date changes when this notice is revised.</p>')

guide='''<p>Reviewed on 8 September 2026. These materials prepare releases; they do not guarantee acceptance or replace the checks in the actual Play Console account.</p>
<h2>Release order</h2><p>Start with Scientific Calculator. Each other app has an independent release checklist. Account verification and access to production are separate steps; releasing one app does not automatically release the others.</p>
<h2>Account and testing</h2><p>Use the verified legal identity required by Google and Praxis Science Lab as the public publishing brand where permitted. A brand name does not itself establish a legal organization. Verify the public support email. For applicable new personal accounts, Google requires 12 testers continuously opted in for 14 days before applying for production access. Collect real engagement and feedback; do not manufacture test reports or reviews.</p>
<p>For the educational terminology app, review Google's Medical Reference and Education declaration and clarify the account-type requirement before choosing the account solely around this project. Educational intent does not make it a clinical device, but does not automatically remove Google's health-content declaration.</p>
<h2>Submission checks</h2><ul><li>Build a release AAB with a protected upload key, a stable package ID and an increasing version code. Never publish signing keys or tester addresses.</li><li>New mobile submissions currently require target API 36. Inspect the final bundle, not only source configuration. Validate 16 KB native-library compatibility and test on representative devices.</li><li>Complete App access, Ads, Data safety, Target audience, IARC content rating and the Health declaration from actual behavior and content. Do not choose adult-only audiences merely to avoid child-directed requirements.</li><li>Link the app-specific public HTML privacy policy in Play Console and within the app. Reconcile every active version and all SDK behavior with it.</li><li>Check crash handling, offline behavior, accessibility, permissions, background audio and exports where applicable. Run the Play pre-launch report and resolve findings.</li></ul>
<h2>Store assets</h2><p>Prepare a title up to 30 characters, short description up to 80 and full description up to 4,000. Use a distinct 512 × 512 app icon and a 1024 × 500 feature graphic. Supply at least two actual screenshots: JPEG or 24-bit PNG, dimensions 320–3840 pixels, longest side at most twice the shortest. Add other form-factor assets only for supported devices. Avoid rankings, endorsement claims, false availability or fabricated UI.</p>
<h2>Tester handoff</h2><p>Send invitations privately once the closed track is ready. Ask testers to install through the opt-in link, use the app over the test period and report device/version, steps, expected result and actual result. Keep a private record of issues and fixes. No tester list belongs on this public site.</p>
<h2>Account-only decisions</h2><p>The owner must complete identity verification and confirm countries, pricing, audience, ratings, production-access answers and any required declarations in Play Console. No account settings, legal attestations or store submission have been made by this website task.</p>
<h2>Official references</h2><ul>
<li><a href="https://support.google.com/googleplay/android-developer/answer/14151465?hl=en">Personal-account testing requirements</a></li>
<li><a href="https://support.google.com/googleplay/android-developer/answer/13634885?hl=en">Developer account types</a></li>
<li><a href="https://support.google.com/googleplay/android-developer/answer/10144311?hl=en">User Data and privacy policies</a></li>
<li><a href="https://support.google.com/googleplay/android-developer/answer/10787469?hl=en">Data safety definitions and exemptions</a></li>
<li><a href="https://support.google.com/googleplay/android-developer/answer/11926878?hl=en">Target API requirements</a></li>
<li><a href="https://developer.android.com/guide/practices/page-sizes">16 KB page-size compatibility</a></li>
<li><a href="https://support.google.com/googleplay/android-developer/answer/9866151?hl=en">Graphic and screenshot requirements</a></li>
<li><a href="https://support.google.com/googleplay/android-developer/answer/14738291?hl=en">Health apps declaration, including educational reference</a></li>
<li><a href="https://developers.google.com/admob/android/privacy/play-data-disclosure">Google advertising SDK data disclosure</a></li></ul>'''
guide+='<h2>App kits</h2><ul>'+''.join(f'<li><a href="../apps/{a["slug"]}/publishing/">{e(a["name"])}</a></li>' for a in APPS)+'</ul>'
page('publishing','Google Play Publishing Kit','Release preparation for Android apps published by Praxis Science Lab.',guide)
print(f'Built documentation for {len(APPS)} Android apps, plus website privacy and publishing guide.')


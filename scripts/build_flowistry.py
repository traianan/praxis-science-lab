"""Update only Flowistry pages and its catalog entry; preserve other public pages."""
from pathlib import Path
import json, re, sys, xml.etree.ElementTree as ET
from html import escape
from seo import enhance
from portfolio_cards import render_card
ROOT=Path(__file__).resolve().parents[1]
EMAIL='contact@praxissciencelab.app'
description='Sort colors, plan each pour and explore a calm offline puzzle game.'
app=dict(slug='flowistry', name='Flowistry', title='Flowistry', repo='FLOWISTRY-GATA', package='app.praxis.flowistry', version='0.1.0 (1)', policy_date='2026-10-16', language='English, Romanian and Spanish',status='In testing',category='Puzzle',short=description,publishing_assets=False,
description='Flowistry is an Android color-sorting puzzle in development. Pour matching colors between tubes and plan your moves. The development project includes a 240-level campaign, daily and weekly puzzles, Zen play and a puzzle editor. Mechanics, accessibility and store integrations are undergoing verification.\n\nCore puzzles work offline without a developer account. Android 8.0 or later is required. Google Play and Huawei AppGallery releases are being prepared; no public app download or store release is available from this page.',
data='Puzzle progress, attempts, preferences and editor drafts are stored on the device. No developer account or separate analytics service is required.',permissions='Network access supports optional store services; vibration supports feedback. Store-specific SDKs have their own privacy practices.',retention='Clear app storage to remove local progress and preferences. Earlier test builds may be included in Android system backup; privacy information explains version differences.',safety='A recreational puzzle game.',ads_notice='Commercial advertising and purchases are not activated. Store integrations are under development.',data_safety_note='Review the exact signed artifact before submitting store declarations.',checks=['Verify save/resume and all puzzle mechanics.','Verify store-specific consent, purchase and restoration flows.','Test accessibility and representative Android/Huawei devices.'])
apps_path=ROOT/'scripts/apps.json';apps=json.loads(apps_path.read_text(encoding='utf-8'))
apps=[a for a in apps if a['slug']!='flowistry']+[app]
apps_path.write_text(json.dumps(apps,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
media=ROOT/'apps/flowistry/media';media.mkdir(parents=True,exist_ok=True)
android=ET.parse(ROOT.parent/'FLOWISTRY-GATA/app/src/main/res/drawable/ic_launcher_foreground.xml').getroot()
ns='{http://schemas.android.com/apk/res/android}'
paths=[]
for p in android:
 attrs={'d':p.get(ns+'pathData'),'fill':p.get(ns+'fillColor','none'),'stroke':p.get(ns+'strokeColor','none'),'stroke-width':p.get(ns+'strokeWidth','0'),'fill-opacity':p.get(ns+'fillAlpha','1'),'stroke-opacity':p.get(ns+'strokeAlpha','1')}
 paths.append('<path '+' '.join(f'{k}="{v}"' for k,v in attrs.items())+'/>')
(media/'app-icon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108"><rect width="108" height="108" rx="24" fill="#0b1119"/>'+''.join(paths)+'</svg>',encoding='utf-8')
contact=f'<p>Published by <strong>PFA Praxis Science Lab</strong>, Brăila, Romania. For support or privacy questions: <a href="mailto:{EMAIL}">{EMAIL}</a>. <a href="../../../contact/">Business contact details</a>.</p>'
privacy='''<p>Effective date: 16 October 2026. This notice covers Flowistry development builds, package <code>app.praxis.flowistry</code> and the offline test package <code>app.praxis.flowistry.fosstest</code>. The game is in testing and is not publicly released.</p>
<h2>Information used by the game</h2><p>Puzzle attempts, move history, completed levels, local statistics, settings and editor drafts are stored in the app's private storage. Core gameplay works offline. Flowistry does not require a developer account, contacts, camera, microphone or precise location. There is no separate developer analytics or crash-reporting integration.</p>
<h2>Offline test and store builds</h2><p>The offline test edition has no Google or Huawei advertising or billing SDK. Store editions include provider-specific services. Commercial advertising and products are not activated during the current development stage. A simulated purchase in a test edition is not a payment or a transferable purchase.</p><p>If a test build enables advertising, its provider can process network information, IP address, device or advertising identifiers, interactions and diagnostics. Google builds use Google Mobile Ads and User Messaging Platform; Huawei builds use Huawei Ads and its consent tools. Test ads are not a promise of zero data processing. Applicable choices must be offered before advertising is requested; declining advertising must not prevent core play.</p><p>When configured, optional permanent Pro purchases are processed by Google Play Billing or Huawei IAP. The store handles account, payment and transaction information; we do not receive payment-card details. Local purchase records may be used to restore and verify access. Purchases do not automatically transfer between stores. No subscription is offered.</p>
<h2>Providers and links</h2><p>Provider practices depend on the installed edition and enabled services. See <a href="https://policies.google.com/privacy">Google privacy</a>, <a href="https://developers.google.com/admob/android/privacy/play-data-disclosure">Google advertising SDK disclosures</a> and <a href="https://consumer.huawei.com/en/privacy/privacy-statement-huawei/">Huawei privacy</a>. Opening this policy or a support link connects to the website or email provider, which has separate infrastructure practices.</p>
<h2>Retention, deletion and backup</h2><p>Local data remains until you clear Flowistry's storage or uninstall it. Puzzle codes shared through another app are handled by the recipient service and may remain there. Earlier evaluation builds allowed Android system backup and device transfer of local data; availability and retention depend on Android and the selected backup provider. Revised builds disable automatic backup so store entitlements are not trusted from a device backup. Clearing game data does not refund a purchase or delete records retained by an app store.</p>
<h2>Support and privacy requests</h2><p>If you contact us, we receive your email address and the information you choose to send, and use it to answer your request. Please do not send passwords, purchase tokens or private screenshots. Request access, correction or deletion of correspondence using the contact below. We cannot remotely retrieve or erase a puzzle stored only on your device. You may also contact your data protection authority; in Romania, <a href="https://www.dataprotection.ro/">ANSPDCP</a>.</p>
<h2>Children and changes</h2><p>No child-directed advertising configuration or public store audience has been launched. Audience and SDK settings will be reviewed before release. Do not submit personal information about children through support. This page will be updated if the enabled services or data practices change; check the effective date and your installed build.</p>'''+contact
support=f'<h2>Flowistry is in testing</h2><p>There is no public APK or store installation link. Google Play and Huawei AppGallery editions are being prepared. Android 8.0 or later is required.</p><h2>Report a problem</h2><p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> with Flowistry, your app version, device model, level or mode, and steps to reproduce the issue. Remove personal information from screenshots. Do not send purchase tokens, signing keys or passwords.</p><h2>Progress and purchases</h2><p>Progress is stored locally. Avoid clearing app storage while testing saved-game recovery. Test purchases do not charge money and do not establish ownership in another store. A commercial release will provide restoration through the store used for purchase.</p><p><a href="../privacy/">Read the privacy policy</a>.</p>'
publishing='<p>Preparation only. Flowistry is not approved or published in Google Play or Huawei AppGallery. No binary is available here.</p><h2>Release checks</h2><ul><li>Verify every game mode, save/resume, migration and accessibility.</li><li>Verify separate Google and Huawei artifacts and their store services.</li><li>Complete signing, consent, audience, content rating and privacy declarations for the exact artifact.</li><li>Supply genuine final-version screenshots and store-defined pricing.</li></ul><p>Package: <code>app.praxis.flowistry</code>. Development version: 0.1.0. Minimum Android: 8.0.</p><p><a href="../privacy/">Public privacy policy</a> · <a href="../support/">Support</a></p>'
overview=f'<p><span class="status">In testing</span> Not yet available on Google Play or Huawei AppGallery.</p><p><img src="media/app-icon.svg" width="108" height="108" alt="Flowistry droplet and braided ring icon"></p>'+''.join('<p>'+escape(p)+'</p>' for p in app['description'].split('\n\n'))+'<h2>Plan your next pour</h2><p>Start with color sorting, then discover locks, target tubes, hidden layers and directed routes. Undo and Restart are part of the core experience. English, Romanian and Spanish resources are included.</p><h2>Development status</h2><p>The game is undergoing gameplay, accessibility and distribution improvements. Features and release details may change during testing. Commercial purchases and advertising are not activated.</p>'
template=(ROOT/'apps/spinora/index.html').read_text(encoding='utf-8')
for section,title,subtitle,body in [('', 'Flowistry',description,overview),('privacy','Flowistry Privacy Policy','Privacy information for Flowistry development builds.',privacy),('support','Flowistry Support','Testing information and support for Flowistry.',support),('publishing','Flowistry Release Preparation','Preparation for Google Play and Huawei AppGallery.',publishing)]:
 depth=3 if section else 2;prefix='../'*depth; app_prefix='../' if section else './'
 html=template.replace('../../',prefix)
 html=re.sub(r'<title>.*?</title>',f'<title>{title} | Praxis Science Lab</title>',html)
 html=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{subtitle}">',html)
 links='<nav class="document-links" aria-label="App navigation">'+''.join(f'<a href="{app_prefix}{s}/">{label}</a>' for s,label in [('privacy','Privacy policy'),('support','Support &amp; testing'),('publishing','Release preparation')])+'</nav>'
 main=f'<main id="main" class="document"><a class="back-link" href="{prefix}apps/">← All apps</a><p class="eyebrow">PRAXIS SCIENCE LAB / ANDROID</p><h1>{title}</h1><p class="document-lead">{subtitle}</p>{links}{body}</main>'
 html=re.sub(r'<main\b.*?</main>',lambda m:main,html,flags=re.S)
 path=ROOT/'apps/flowistry'/section/'index.html';path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(enhance(path,html),encoding='utf-8')
cards_path=ROOT/'scripts/catalog_cards.json';cards=json.loads(cards_path.read_text(encoding='utf-8'))
card=render_card(app).replace('Everyday tools','Games')
cards['apps']=[c for c in cards['apps'] if 'apps/flowistry/' not in c]+[card]
cards_path.write_text(json.dumps(cards,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
catalog=ROOT/'apps/index.html';text=catalog.read_text(encoding='utf-8')
text=re.sub(r'<li\b[^>]*>(?:(?!</li>).)*href="../apps/flowistry/"(?:(?!</li>).)*</li>','',text,flags=re.S)
pos=text.index('</ul>',text.index('<ul class="projects-grid'))
text=text[:pos]+card.replace('apps/flowistry/','../apps/flowistry/')+text[pos:]
catalog.write_text(text,encoding='utf-8')
nsmap='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',nsmap)
tree=ET.parse(ROOT/'sitemap.xml');existing={x.text for x in tree.getroot().iter('{'+nsmap+'}loc')}
for section in ('','privacy/','support/'):
 url='https://praxissciencelab.app/apps/flowistry/'+section
 if url not in existing:ET.SubElement(ET.SubElement(tree.getroot(),'{'+nsmap+'}url'),'{'+nsmap+'}loc').text=url
ET.indent(tree);tree.write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
print('Flowistry pages, catalog, icon and sitemap updated. No APK published.')

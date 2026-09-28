"""Package public assets only. No application binaries, signing keys or tester data."""
from pathlib import Path
import json
import zipfile
import argparse
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--app', action='append', help='Package only the named app; repeat for several apps.')
args = parser.parse_args()
for a in json.loads((ROOT/'scripts/apps.json').read_text(encoding='utf-8')):
    if args.app and a['slug'] not in args.app: continue
    if not a.get('publishing_assets', True): continue
    folder=ROOT/'apps'/a['slug'];url=f'https://traianan.github.io/praxis-science-lab/apps/{a["slug"]}/'
    shots=sorted((folder/'media').glob('screenshot-*.png'))
    if a['slug']!='medical-terminology-flashcards':assert len(shots)>=2,a['slug']
    for shot in shots:
        with Image.open(shot) as im:
            assert im.mode=='RGB' and min(im.size)>=320 and max(im.size)<=3840 and max(im.size)<=2*min(im.size),shot
    with Image.open(folder/'media/app-icon.png') as im:assert im.size==(512,512)
    readme=f'''{a['name']} — Praxis Science Lab
English Google Play preparation kit. Reviewed version: {a['version']}.
Support: traiananghel@gmail.com
Privacy policy: {url}privacy/
Support and testing: {url}support/
Declarations and outstanding checks: {url}publishing/

The icon and feature graphic use their required pixel dimensions.
Screenshots: {len(shots)} genuine Android test-build captures, when available.
Screenshot version: {a.get('screenshots_version', a['version'])}. Captures may predate the current monetization update.
Revalidate all assets against the final signed upload artifact. No production medical content or fabricated screenshot is included.
This kit does not establish Google approval or completion of account verification, audience/rating forms or closed testing.

Remaining app-specific checks:
'''+''.join('- '+v+'\n' for v in a['gaps'])
    with zipfile.ZipFile(folder/'publishing-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('README.txt',readme)
        z.write(folder/'store-listing-en.txt','store-listing-en.txt')
        for p in sorted((folder/'media').iterdir()):
            if p.is_file():z.write(p,'media/'+p.name)
print('PASS: selected public asset ZIPs and screenshot format/dimension checks.')

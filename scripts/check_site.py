"""Static integrity checks for this small GitHub Pages site; no browser QA claim."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET
import json
import hashlib

ROOT=Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[];self.links=[];self.h1=0;self.lang=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if tag=='h1':self.h1+=1
        if 'id' in a:self.ids.append(a['id'])
        for key in ('href','src'):
            if key in a:self.links.append(a[key])
        if tag=='img':assert 'alt' in a, 'Image lacks alt attribute'
        assert tag not in {'iframe','form'}, 'Unexpected embedded page or form added'
        if tag=='script':
            src=urlsplit(a.get('src',''))
            assert not src.scheme and not src.netloc
            assert Path(src.path).name in {'copyright.js','theme.js'}, 'Unexpected script added'

pages={}
for file in [ROOT/'index.html', *sorted((ROOT/'apps').rglob('*.html')), ROOT/'privacy/index.html', ROOT/'publishing/index.html']:
    page=Page();page.feed(file.read_text(encoding='utf-8'));pages[file.resolve()]=page
    assert page.lang=='en' and page.h1==1, f'Language or main heading: {file}'
    assert len(page.ids)==len(set(page.ids)), f'Duplicate IDs: {file}'
for file,page in pages.items():
    for link in page.links:
        url=urlsplit(link)
        if url.scheme:
            assert url.scheme in {'https','mailto'}, f'Unexpected scheme: {link}'
            continue
        assert not url.netloc and not url.path.startswith('/'), f'Non-project-relative link: {link}'
        target=(file.parent/unquote(url.path)).resolve() if url.path else file
        assert target.is_relative_to(ROOT.resolve()), f'Asset outside site: {link}'
        if target.is_dir():target=target/'index.html'
        assert target.exists(), f'Missing local asset: {file}: {link}'
        if url.fragment:assert url.fragment in pages[target].ids, f'Broken anchor: {link}'
apps=json.loads((ROOT/'scripts/apps.json').read_text(encoding='utf-8'))
for app in apps:
    assert len(app['title'])<=30 and len(app['short'])<=80 and len(app['description'])<=4000
    if app.get('download'):
        folder=ROOT/'apps'/app['slug']; download=app['download']
        assert hashlib.sha256((folder/download['path']).read_bytes()).hexdigest().upper()==download['sha256']
        assert download['sha256'] in (folder/'downloads/SHA256SUMS.txt').read_text()
        from PIL import Image
        for shot in app.get('screenshots',[]):
            with Image.open(folder/'media'/shot['file']) as im: assert im.size==(320,640)
    if not app.get("publishing_assets", True): continue
    from PIL import Image
    with Image.open(ROOT/'apps'/app['slug']/'media/feature-graphic.png') as im:
        assert im.size==(1024,500) and im.mode=='RGB'
for path in (ROOT/'assets').glob('*.svg'):
    root=ET.parse(path).getroot();assert root.get('viewBox'), f'SVG lacks viewBox: {path}'
css=(ROOT/'assets/site.css').read_text()
assert 'focus-visible' in css and 'prefers-reduced-motion' in css and '@media' in css

def luminance(color):
    values=[int(color[i:i+2],16)/255 for i in (1,3,5)]
    linear=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in values]
    return sum(v*w for v,w in zip(linear,[.2126,.7152,.0722]))
for foreground,background in [('#15233b','#ffffff'),('#536076','#ffffff'),('#1739d6','#ffffff'),('#536076','#f3f6fb'),('#344769','#e8edf9'),('#f3f5fa','#000000'),('#b4bece','#111318'),('#a7baff','#000000'),('#d5dfff','#202b46'),('#bbc6d9','#111318')]:
    a,b=sorted([luminance(foreground),luminance(background)])
    ratio=(b+.05)/(a+.05)
    assert ratio>=4.5, f'Text contrast below 4.5: {foreground}/{background}'
    print(f'Contrast {foreground}/{background}: {ratio:.2f}:1')
assert (ROOT/'.nojekyll').exists()
print(f'PASS: {len(pages)} English pages, local links/anchors/assets, store field limits and available feature graphics, SVGs, responsive/focus/reduced-motion CSS and text contrast.')

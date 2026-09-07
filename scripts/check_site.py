"""Static integrity checks for this small GitHub Pages site; no browser QA claim."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

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
            assert a in ({'src':'assets/copyright.js','defer':None},{'src':'assets/theme.js'}), 'Unexpected script added'

page=Page();page.feed((ROOT/'index.html').read_text(encoding='utf-8'))
assert page.lang=='en' and page.h1==1
assert len(page.ids)==len(set(page.ids)), 'Duplicate IDs'
for link in page.links:
    url=urlsplit(link)
    if url.scheme:
        assert url.scheme=='https', f'Non-HTTPS link: {link}'
    elif url.path:
        assert not url.path.startswith('/'), 'Root-absolute path breaks the project Pages prefix'
        assert (ROOT/unquote(url.path)).exists(), f'Missing local asset: {link}'
    if not url.scheme and url.fragment:assert url.fragment in page.ids, f'Broken anchor: {link}'
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
print(f'PASS: English page, heading structure, {len(page.links)} links/assets, SVGs, responsive/focus/reduced-motion CSS and primary text contrast. Secondary pages are deferred.')

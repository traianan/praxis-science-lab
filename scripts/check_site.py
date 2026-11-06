"""Static integrity checks for this small GitHub Pages site; no browser QA claim."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET
import json
import hashlib
import re
from png_info import png_info
ROOT = Path(__file__).resolve().parents[1]

def require(condition, message):
    if not condition:
        raise ValueError(message)


class Page(HTMLParser):

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.h1 = 0
        self.lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.lang = a.get('lang')
        if tag == 'h1':
            self.h1 += 1
        if 'id' in a:
            self.ids.append(a['id'])
        for key in ('href', 'src'):
            if key in a:
                self.links.append(a[key])
        if tag == 'img':
            require('alt' in a, 'Image lacks alt attribute')
        require(tag not in {'iframe', 'form'}, 'Unexpected embedded page or form added')
        if tag == 'script':
            if a.get('type') == 'application/ld+json':
                require('src' not in a, 'Structured data must be local JSON')
                return
            src = urlsplit(a.get('src', ''))
            require((not src.scheme and not src.netloc) or (src.scheme == 'https' and src.netloc == 'praxissciencelab.app'), 'Unexpected external script')
            require(Path(src.path).name in {'copyright.js', 'theme.js', 'portfolio.js'}, 'Unexpected script added')
pages = {}
for file in [ROOT / 'index.html', ROOT / '404.html', *sorted((ROOT / 'apps').rglob('*.html')), ROOT / 'privacy/index.html', ROOT / 'publishing/index.html', *[ROOT / x / 'index.html' for x in ('contact', 'legal', 'terms', 'projects')]]:
    page = Page()
    page.feed(file.read_text(encoding='utf-8'))
    pages[file.resolve()] = page
    expected_lang = file.stem if file.parent.name in {'privacy', 'help'} and file.stem in {'ro', 'es'} else 'en'
    require(page.lang == expected_lang and page.h1 == 1, f'Language or main heading: {file}')
    require(len(page.ids) == len(set(page.ids)), f'Duplicate IDs: {file}')
for file, page in pages.items():
    for link in page.links:
        url = urlsplit(link)
        if url.scheme:
            require(url.scheme in {'https', 'mailto'}, f'Unexpected scheme: {link}')
            continue
        require(not url.netloc and (not url.path.startswith('/')), f'Non-project-relative link: {link}')
        target = (file.parent / unquote(url.path)).resolve() if url.path else file
        require(target.is_relative_to(ROOT.resolve()), f'Asset outside site: {link}')
        if target.is_dir():
            target = target / 'index.html'
        require(target.exists(), f'Missing local asset: {file}: {link}')
        if url.fragment:
            require(url.fragment in pages[target].ids, f'Broken anchor: {link}')
apps = json.loads((ROOT / 'scripts/apps.json').read_text(encoding='utf-8'))
for app in apps:
    require(len(app['title']) <= 30 and len(app['short']) <= 80 and (len(app['description']) <= 4000), 'Integrity check failed')
    for download in app.get('test_downloads', []):
        require(download['url'].startswith('https://github.com/traianan/praxis-science-lab/releases/download/'), 'Integrity check failed')
        require(download['url'].endswith('-QA-NOT-FOR-STORE.apk'), 'Integrity check failed')
        require(len(download['sha256']) == 64, 'Integrity check failed')
        checksums = (ROOT / 'apps' / app['slug'] / 'downloads/SHA256SUMS.txt').read_text()
        require(download['sha256'] + '  ' + download['url'].rsplit('/', 1)[1] in checksums, 'Integrity check failed')
    for preview in app.get('previews', []):
        require(png_info(ROOT / 'apps' / app['slug'] / 'media' / preview['file'])[0] == (preview['width'], preview['height']), 'Integrity check failed')
    if app.get('download'):
        folder = ROOT / 'apps' / app['slug']
        download = app['download']
        require(hashlib.sha256((folder / download['path']).read_bytes()).hexdigest().upper() == download['sha256'], 'Integrity check failed')
        require(download['sha256'] in (folder / 'downloads/SHA256SUMS.txt').read_text(), 'Integrity check failed')
        for shot in app.get('screenshots', []):
            require(png_info(folder / 'media' / shot['file'])[0] == (320, 640), 'Integrity check failed')
    if not app.get('publishing_assets', True):
        continue
    dimensions, colour = png_info(ROOT / 'apps' / app['slug'] / 'media/feature-graphic.png')
    require(dimensions == (1024, 500) and colour == 2, 'Integrity check failed')
for path in (ROOT / 'assets').glob('*.svg'):
    root = ET.parse(path).getroot()
    require(root.get('viewBox'), f'SVG lacks viewBox: {path}')
css = (ROOT / 'assets/site.css').read_text()
require('focus-visible' in css and 'prefers-reduced-motion' in css and ('@media' in css), 'Integrity check failed')

def luminance(color):
    values = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in values]
    return sum((v * w for v, w in zip(linear, [0.2126, 0.7152, 0.0722])))
# Check the actual theme tokens, including dark mode, rather than copied colour literals.
blocks = re.findall(r':root[^{}]*\{([^{}]+)\}', css)
base = dict(re.findall(r'(--[\w-]+):\s*(#[0-9a-fA-F]{6})(?:;|})', blocks[0]+'}'))
for index, block in enumerate(blocks):
    tokens = base | dict(re.findall(r'(--[\w-]+):\s*(#[0-9a-fA-F]{6})(?:;|})', block+'}'))
    for fg, bg in [('--ink','--paper'),('--muted','--paper'),('--muted','--wash'),('--accent','--paper'),('--accent','--wash'),('--status-ink','--status-bg')]:
        foreground, background = tokens[fg], tokens[bg]
        a, b = sorted([luminance(foreground), luminance(background)])
        ratio = (b + 0.05) / (a + 0.05)
        require(ratio >= 4.5, f'Text contrast below 4.5 in theme {index}: {fg}/{bg} ({ratio:.2f})')
print(f'PASS: contrast for {len(blocks)} CSS theme definitions (core text tokens).')
require((ROOT / '.nojekyll').exists(), 'Integrity check failed')
print(f'PASS: {len(pages)} pages, local links/anchors/assets, store field limits and available feature graphics, SVGs, responsive/focus/reduced-motion CSS and text contrast.')

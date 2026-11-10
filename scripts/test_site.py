"""Regression checks for metadata, catalog drift and public/private boundaries."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

import seo
from png_info import png_info

ROOT = Path(__file__).resolve().parents[1]


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (ROOT/"build").mkdir(exist_ok=True)

    def test_metadata_is_idempotent(self):
        for path in seo.public_pages():
            with self.subTest(page=path.relative_to(ROOT)):
                html = path.read_text(encoding='utf-8')
                once = seo.enhance(path, html)
                self.assertEqual(once, seo.enhance(path, once))

    def test_publishing_noindex_on_any_host(self):
        for path in seo.public_pages():
            if 'publishing' in path.relative_to(ROOT).parts:
                self.assertIn('<meta name="robots" content="noindex, follow">', path.read_text(encoding='utf-8'))

    def test_language_links_are_reciprocal(self):
        for path in seo.public_pages():
            if path.stem not in {'ro', 'es'}:
                continue
            html = path.read_text(encoding='utf-8')
            for code, name in [('en', 'index.html'), ('ro', 'ro.html'), ('es', 'es.html')]:
                sibling = path.parent / name
                if sibling.exists():
                    self.assertIn(f'hreflang="{code}" href="{seo.url_for(sibling)}"', html)
                    self.assertIn(f'href="{seo.url_for(path)}"', sibling.read_text(encoding='utf-8'))

    def test_catalog_matches_inventory_and_has_small_icons(self):
        apps = json.loads((ROOT/'scripts/apps.json').read_text(encoding='utf-8'))
        catalog = (ROOT/'apps/index.html').read_text(encoding='utf-8')
        self.assertEqual(len(apps), len(re.findall('class="portfolio-card"', catalog)))
        size = 0
        for app in apps:
            self.assertIn(f'href="../apps/{app["slug"]}/"', catalog)
        for image in re.findall(r'<img[^>]+src="([^"]+)"', catalog):
            size += (ROOT/'apps'/image.split('?')[0]).stat().st_size
        self.assertLess(size, 150_000)
        self.assertNotIn('<h3>', catalog)
        self.assertNotIn('"apps":', (ROOT/'scripts/catalog_cards.json').read_text())

    def test_png_rejects_invalid_header(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'build') as directory:
            path = Path(directory)/'invalid.png'
            path.write_bytes(b'not an image')
            with self.assertRaises(ValueError):
                png_info(path)

    def test_public_build_excludes_private_tree(self):
        # A separate fixture proves private files cannot enter the deployment artifact.
        with tempfile.TemporaryDirectory(dir=ROOT/'build') as directory:
            root = Path(directory)
            (root/'scripts').mkdir()
            (root/'scripts/build_public.cjs').write_bytes((ROOT/'scripts/build_public.cjs').read_bytes())
            for name in ['assets', 'apps', 'privacy', 'publishing', 'contact', 'legal', 'terms', 'projects', 'pfa-studio']:
                (root/name).mkdir()
            for name in ['index.html', '404.html', 'robots.txt', 'sitemap.xml', 'app-ads.txt', '.nojekyll']:
                (root/name).write_text('public')
            for name in ['pfa-studio/.env.local', 'apps/private.db', 'apps/.env', 'scripts/private.json']:
                (root/name).write_text('PRIVATE_FIXTURE')
            subprocess.run(['node', str(root/'scripts/build_public.cjs')], check=True, capture_output=True)
            output = root/'build/public'
            self.assertTrue((output/'404.html').exists())
            self.assertFalse((output/'pfa-studio').exists())
            self.assertFalse((output/'apps/private.db').exists())
            self.assertFalse((output/'apps/.env').exists())
            self.assertFalse((output/'scripts').exists())


if __name__ == '__main__':
    unittest.main()

"""Generate the legacy GitHub Pages artifact: redirects only, never site sources."""
from html import escape
from pathlib import Path
import shutil

from seo import BASE, ROOT, public_pages, url_for


def redirect_html(target):
    target = escape(target, quote=True)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Praxis Science Lab has moved</title>
<link rel="canonical" href="{target}">
<script src="/praxis-science-lab/redirect.js"></script>
<meta http-equiv="refresh" content="0;url={target}">
</head><body><h1>Praxis Science Lab has moved</h1>
<p>Continue to <a href="{target}">Praxis Science Lab</a>.</p>
</body></html>
'''


def build(output=None):
    output = Path(output) if output else ROOT/'build/pages-redirect'
    build_root = ROOT/'build'
    if build_root.is_symlink() or output.is_symlink():
        raise ValueError('Unsafe output link')
    resolved = output.resolve()
    if not resolved.is_relative_to(build_root.resolve()) or resolved == build_root.resolve():
        raise ValueError('Redirect output must be a subdirectory of build/')
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    count = 0
    for path in public_pages():
        target = output/path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(redirect_html(url_for(path)), encoding='utf-8')
        count += 1
    # Unknown legacy routes use the same fixed-origin JS mapping; no-JS fallback is home.
    (output/'404.html').write_text(redirect_html(BASE), encoding='utf-8')
    (output/'redirect.js').write_bytes((ROOT/'scripts/legacy_redirect.js').read_bytes())
    (output/'.nojekyll').touch()
    (output/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n', encoding='utf-8')
    print(f'Legacy Pages: {count} redirect pages plus path-preserving 404 fallback.')
    return output


if __name__ == '__main__':
    build()

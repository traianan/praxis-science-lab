from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
    'neon-radio': 'Sound & music', 'audiolab': 'Sound & music',
    'frequency-generator': 'Sound & music', 'clear-audio': 'Sound & music',
    'earmate': 'Sound & music', 'droplet': 'Sound & music',
    'prism-player': 'Sound & music', 'tempolab': 'Sound & music',
    'geostamp-camera': 'Photo & creativity', 'mosaic': 'Photo & creativity',
    'spinora': 'Everyday tools', 'atomic-clock': 'Everyday tools',
    'scientific-calculator': 'Science & learning',
    'medical-terminology-flashcards': 'Science & learning',
    'xlab-tools': 'Science & learning',
}
def render_card(app):
    e = escape
    slug = app['slug']
    group = GROUPS.get(slug, 'Everyday tools')
    icon = next((f'apps/{slug}/media/{name}' for name in ['app-icon.png', 'icon.png']
                 if (ROOT / f'apps/{slug}/media/{name}').exists()), None)
    visual = f'<img src="{icon}" alt="" width="56" height="56" loading="lazy">' if icon else f'<span class="app-monogram" aria-hidden="true">{e(app["name"][:2].upper())}</span>'
    return f'''<li class="portfolio-card" data-category="{e(group)}"><div class="card-top">{visual}<span class="card-category">{e(group)}</span></div><h3><a href="apps/{slug}/">{e(app['name'])} <span aria-hidden="true">↗</span></a></h3><p>{e(app['short'])}</p><span class="status">{e(app['status'])}</span></li>'''

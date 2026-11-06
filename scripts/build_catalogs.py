"""Build dedicated searchable catalogs and a curated homepage."""
from pathlib import Path
import json
import re
from html import escape
from portfolio_cards import render_card
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'scripts/catalog_cards.json'

def build():
    home=(ROOT/'index.html').read_text(encoding='utf-8')
    home=home.replace('<a href="publishing/">Open the Google Play publishing kit</a>', '<a href="apps/">Explore app information and support</a>')
    apps_block=re.search(r'<!-- ANDROID_APPS_START -->(.*?)<!-- ANDROID_APPS_END -->',home,re.S)
    app_cards=re.findall(r'<li\b.*?</li>',apps_block[1],re.S)
    projects=re.search(r'<section id="projects".*?</section>',home,re.S)[0]
    web_cards=re.findall(r'<li\b.*?</li>',projects,re.S)
    data=json.loads(SOURCE.read_text(encoding='utf-8')) if SOURCE.exists() else {}
    data['apps']=[render_card(app) for app in json.loads((ROOT/'scripts/apps.json').read_text(encoding='utf-8'))]
    if len(web_cards)>3:data['projects']=web_cards
    assert len(data.get('apps',[]))>4 and len(data.get('projects',[]))>3
    SOURCE.write_text(json.dumps({'projects': data['projects']},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    categories=['Science','Education','Science','Science','Utilities','Creativity','Science','Business']
    web=[]
    for i,card in enumerate(data['projects']):
        category=categories[i]
        card=card.replace('<li>',f'<li class="portfolio-card" data-category="{category}"><div class="card-top"><span class="app-monogram" aria-hidden="true">↗</span><span class="card-category">{category}</span></div>',1)
        web.append(card)
    for slug,title,description,cards in [('apps','Our apps','Explore Android apps for science, sound, creativity and everyday life.',data['apps']),('projects','Web projects','Explore interactive web projects for science, education, creativity and practical tasks.',web)]:
        cards=[card.replace('<h3>', '<h2>').replace('</h3>', '</h2>') for card in cards]
        cats=list(dict.fromkeys(re.search(r'data-category="([^"]+)"',c)[1] for c in cards))
        filters='<button type="button" data-filter="All" aria-pressed="true">All '+('apps' if slug=='apps' else 'projects')+'</button>'+''.join(f'<button type="button" data-filter="{c}" aria-pressed="false">{c}</button>' for c in cats)
        main=f'''<main id="main"><section class="section catalog" data-catalog-label="{'apps' if slug=='apps' else 'projects'}"><div class="section-heading"><div><p class="eyebrow">EXPLORE THE COLLECTION</p><h1>{title}</h1><p>{description}</p></div></div><div class="collection-tools" hidden><div class="filter-buttons" role="group" aria-label="Filter by category">{filters}</div><label class="app-search"><span class="sr-only">Search {title.lower()}</span><input type="search" placeholder="Search by name or description…" autocomplete="off"></label></div><p class="collection-count" aria-live="polite" hidden></p><ul class="projects-grid android-apps-grid">{''.join(cards)}</ul><p><a href="index.html">← Back to home</a></p></section></main>'''
        page=re.sub(r'<main\b.*?</main>',lambda m:main,home,flags=re.S)
        page=re.sub(r'<title>.*?</title>',f'<title>{title} | Praxis Science Lab</title>',page,flags=re.S)
        page=re.sub(r'<meta name="description" content="[^"]*"[^>]*>',f'<meta name="description" content="{description}">',page)
        page=re.sub(r'\s*<!-- SEO:START -->.*?<!-- SEO:END -->','',page,flags=re.S)
        def relative(m):
            value=m[2]
            if not re.match(r'(?:https?:|mailto:|data:|/)',value):value='../'+value
            return m[1]+value+m[3]
        page=re.sub(r'((?:href|src)=")([^"]+)(")',relative,page)
        page=page.replace('href="../#main"','href="#main"')
        path=ROOT/slug/'index.html';path.parent.mkdir(exist_ok=True);path.write_text(page,encoding='utf-8')
    featured=['tempolab','terralab','mosaic','wheel-mind-trivia']
    chosen=[next(c for c in data['apps'] if f'href="apps/{slug}/"' in c) for slug in featured]
    start=home.index('<div class="collection-tools"') if '<div class="collection-tools"' in home else -1
    if start>=0:
        end=home.index('<!-- ANDROID_APPS_START -->',start);home=home[:start]+home[end:]
    replacement='<!-- ANDROID_APPS_START -->\n<ul class="projects-grid android-apps-grid featured-apps">'+''.join(chosen)+'</ul>\n<!-- ANDROID_APPS_END -->'
    home=re.sub(r'<!-- ANDROID_APPS_START -->.*?<!-- ANDROID_APPS_END -->',lambda m:replacement,home,flags=re.S)
    home=re.sub(r'<!-- CATALOG_APPS_LINK -->.*?<!-- /CATALOG_APPS_LINK -->','',home,flags=re.S)
    home=home.replace('<!-- ANDROID_APPS_END -->','<!-- ANDROID_APPS_END --><!-- CATALOG_APPS_LINK --><p><a class="button" href="apps/">View all apps <span aria-hidden="true">→</span></a></p><!-- /CATALOG_APPS_LINK -->')
    short=re.sub(r'<ul class="projects-grid">.*?</ul>','<ul class="projects-grid">'+''.join(data['projects'][:3])+'</ul>',projects,flags=re.S)
    short=re.sub(r'<!-- CATALOG_WEB_LINK -->.*?<!-- /CATALOG_WEB_LINK -->','',short,flags=re.S)
    short=short.replace('</section>','<!-- CATALOG_WEB_LINK --><p><a class="button" href="projects/">View all web projects <span aria-hidden="true">→</span></a></p><!-- /CATALOG_WEB_LINK --></section>')
    home=re.sub(r'<section id="projects".*?</section>',lambda m:short,home,flags=re.S)
    home=home.replace('href="#apps">Find your next app','href="apps/">Find your next app').replace('href="#projects">Explore the web labs','href="projects/">Explore the web labs')
    home=home.replace('Explore the collection. Each project has its own story.','A selection from the lab. Discover the full collection in Our apps.')
    home=re.sub(r'<strong>\d+</strong><span>Android projects</span>',f'<strong>{len(data["apps"])}</strong><span>Android projects</span>',home)
    (ROOT/'index.html').write_text(home,encoding='utf-8')
    print(f'Catalogs: {len(data["apps"])} apps, {len(web)} web projects; Home: 4 apps and 3 web projects.')

if __name__=='__main__':
    build()
    from business_identity import build as identity
    identity()
    from seo import build as seo
    seo()

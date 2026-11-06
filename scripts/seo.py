"""Idempotent public-site metadata. PFA and private/local files are never scanned."""
from pathlib import Path
from html import escape, unescape
import json
import re
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://praxissciencelab.app/'

def public_pages():
    yield ROOT/'index.html'
    for section in ('apps','privacy','publishing','contact','legal','terms','projects'):
        for path in sorted((ROOT/section).rglob('*.html')):
            if 'developer-profile' not in path.parts: yield path

def url_for(path):
    route=path.relative_to(ROOT).as_posix()
    return BASE+(route[:-10] if route.endswith('index.html') else route)

def enhance(path, html):
    url=url_for(path)
    parts=path.relative_to(ROOT).parts
    apps={app['slug']:app for app in json.loads((ROOT/'scripts/apps.json').read_text(encoding='utf-8'))}
    app=apps.get(parts[1]) if len(parts)>2 and parts[0]=='apps' else None
    lang=re.search(r'<html\s+lang="([^"]+)"',html).group(1)
    if app and path.parent.name=='privacy':
        labels={'en':('Privacy Policy',f'How {app["name"]} handles data, permissions, retention and privacy requests.'),
                'ro':('Politica de confidențialitate',f'Cum gestionează {app["name"]} datele, permisiunile, păstrarea datelor și solicitările de confidențialitate.'),
                'es':('Política de privacidad',f'Cómo gestiona {app["name"]} los datos, permisos, conservación y solicitudes de privacidad.')}
        label,desc=labels.get(lang,labels['en'])
        html=re.sub(r'<title>.*?</title>',lambda m:f'<title>{escape(app["name"])} — {label} | Praxis Science Lab</title>',html,flags=re.S)
        html=re.sub(r'<meta name="description" content="[^"]*"\s*/?>',lambda m:f'<meta name="description" content="{escape(desc,quote=True)}">',html)
    elif app and path.parent.name in {'support','publishing'}:
        desc=(f'Support for {app["name"]}: troubleshooting, feedback and contact information.' if path.parent.name=='support' else f'Release preparation and publishing materials for {app["name"]}.')
        html=re.sub(r'<meta name="description" content="[^"]*"\s*/?>',lambda m:f'<meta name="description" content="{escape(desc,quote=True)}">',html)
    title=unescape(re.search(r'<title>(.*?)</title>',html,re.S).group(1))
    found=re.search(r'<meta\s+name="description"\s+content="([^"]*)"\s*/?>',html)
    description=unescape(found.group(1)) if found else title
    html=re.sub(r'\s*<!-- SEO:START -->.*?<!-- SEO:END -->\s*','',html,flags=re.S)
    html=re.sub(r'<link\s+rel="canonical"[^>]*>',f'<link rel="canonical" href="{escape(url,quote=True)}">',html)
    if 'rel="canonical"' not in html:html=html.replace('</head>',f'<link rel="canonical" href="{escape(url,quote=True)}">\n</head>')
    html=re.sub(r'\s*<meta\s+(?:property="og:[^"]+"|name="twitter:[^"]+")[^>]*>','',html)
    lang=re.search(r'<html\s+lang="([^"]+)"',html).group(1)
    meta=[('property','og:type','website'),('property','og:site_name','Praxis Science Lab'),
          ('property','og:title',title),('property','og:description',description),('property','og:url',url),
          ('property','og:image',BASE+'assets/logo.png'),('property','og:image:alt','Praxis Science Lab logo'),
          ('property','og:locale',{'en':'en_US','ro':'ro_RO','es':'es_ES'}.get(lang,'en_US')),
          ('name','twitter:card','summary'),('name','twitter:title',title),
          ('name','twitter:description',description),('name','twitter:image',BASE+'assets/logo.png')]
    tags=[f'<meta {attr}="{key}" content="{escape(value,quote=True)}">' for attr,key,value in meta]
    if 'publishing' in parts or path.name=='404.html':
        html=re.sub(r'<meta name="robots"[^>]*>','',html)
        tags.append('<meta name="robots" content="noindex, follow">')
    if app:
        graphic=next((ROOT/'apps'/app['slug']/'media'/name for name in ('feature-graphic.png','app-icon.png','icon.png') if (ROOT/'apps'/app['slug']/'media'/name).exists()),None)
        if graphic:
            social=BASE+graphic.relative_to(ROOT).as_posix()
            tags=[tag.replace(BASE+'assets/logo.png',social).replace('Praxis Science Lab logo',escape(app['name'],quote=True)).replace('content="summary"','content="summary_large_image"') for tag in tags]
        siblings=[(code,path.parent/filename) for code,filename in [('en','index.html'),('ro','ro.html'),('es','es.html')] if (path.parent/filename).exists()]
        if path.parent.name in {'privacy','help'} and len(siblings)>1:
            html=re.sub(r'<link[^>]*hreflang="[^"]*"[^>]*>','',html)
            tags.extend(f'<link rel="alternate" hreflang="{code}" href="{url_for(sibling)}">' for code,sibling in siblings)
            tags.append(f'<link rel="alternate" hreflang="x-default" href="{url_for(path.parent/"index.html")}">')
        graph=[]
        if parts==('apps',app['slug'],'index.html'):
            software={'@type':'SoftwareApplication','name':app['name'],'url':url,'operatingSystem':'Android','description':app['short'],'applicationCategory':app['category']}
            if graphic:software['image']=social
            graph.append(software)
        crumbs=[('Home',BASE),('Our apps',BASE+'apps/'),(app['name'],BASE+'apps/'+app['slug']+'/')]
        if len(parts)>3:crumbs.append((title,url))
        graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i,'name':label,'item':link} for i,(label,link) in enumerate(crumbs,1)]})
        tags.append('<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')+'</script>')
    if path==ROOT/'index.html':
        data={'@context':'https://schema.org','@graph':[
            {'@type':'Organization','@id':BASE+'#organization','name':'Praxis Science Lab','legalName':'PFA Praxis Science Lab','email':'contact@praxissciencelab.app','address':{'@type':'PostalAddress','streetAddress':'Str. Ion C. Brătianu, nr. 1','addressLocality':'Brăila','postalCode':'810067','addressCountry':'RO'},'url':BASE,'logo':BASE+'assets/logo.png','description':description},
            {'@type':'WebSite','@id':BASE+'#website','name':'Praxis Science Lab','url':BASE,'inLanguage':'en','publisher':{'@id':BASE+'#organization'}}]}
        tags.append('<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+'</script>')
    block='\n<!-- SEO:START -->\n'+'\n'.join(tags)+'\n<!-- SEO:END -->\n'
    return html.replace('</head>',block+'</head>')

def build():
    pages=list(public_pages())
    for path in pages:
        html=path.read_text(encoding='utf-8');updated=enhance(path,html)
        if updated!=html:path.write_text(updated,encoding='utf-8')
    ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9')
    root=ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset');count=0
    for path in pages:
        if 'publishing' in path.relative_to(ROOT).parts:continue
        node=ET.SubElement(root,'url');ET.SubElement(node,'loc').text=url_for(path);count+=1
    ET.indent(root)
    (ROOT/'sitemap.xml').write_bytes(ET.tostring(root,encoding='utf-8',xml_declaration=True))
    print(f'SEO: {len(pages)} public pages; {count} sitemap URLs; PFA excluded.')

if __name__=='__main__':build()

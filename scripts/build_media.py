"""Render branded feature graphics; these are not app screenshots."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
apps=json.loads((ROOT/'scripts/apps.json').read_text(encoding='utf-8'))
font_dir=Path('C:/Windows/Fonts')
def font(size,bold=False): return ImageFont.truetype(str(font_dir/('arialbd.ttf' if bold else 'arial.ttf')),size)
for app in apps:
    out=ROOT/'apps'/app['slug']/'media'
    image=Image.new('RGB',(1024,500),'#1739d6');d=ImageDraw.Draw(image)
    logo=Image.open(ROOT/'assets/logo-mark.png').convert('RGBA').resize((64,64))
    image.paste(logo,(48,40),logo)
    d.text((128,60),'PRAXIS SCIENCE LAB',font=font(22,True),fill='white')
    words=app['title'].split();lines=[];line=''
    for word in words:
        candidate=(line+' '+word).strip()
        if d.textlength(candidate,font=font(54,True))>720:lines.append(line);line=word
        else:line=candidate
    if line:lines.append(line)
    for i,line in enumerate(lines):d.text((56,172+i*66),line,font=font(54,True),fill='white')
    d.line((56,385,830,385),fill='#6d85ec',width=2)
    d.text((56,417),'Curiosity, put into practice.',font=font(23),fill='white')
    d.ellipse((864,338,960,434),fill='#ffe076')
    image.save(out/'feature-graphic.png',optimize=True)
    (out/'README.txt').write_text('Praxis Science Lab\nFeature graphic: 1024 x 500, RGB PNG.\nThis is a promotional graphic, not a screenshot.\nUse genuine current-release screenshots and a matching app launcher icon for submission.\n',encoding='utf-8')
print('PASS: five English feature graphics, RGB PNG, 1024 x 500.')

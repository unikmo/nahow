from pathlib import Path
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[1]
class Check(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.images=[];self.has_title=False;self.has_main=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='title':self.has_title=True
  if tag=='main':self.has_main=True
  if tag=='a' and a.get('href','').startswith('/'):self.links.append(a['href'])
  if tag=='img':self.images.append(a.get('src',''))
errors=[];pages=list(R.rglob('index.html'))
for page in pages:
 c=Check();c.feed(page.read_text())
 if not c.has_title or not c.has_main:errors.append(f'Invalid layout in {page}')
 for link in c.links:
  path=link.split('#')[0].split('?')[0];target=R/(path.strip('/'))/'index.html' if path!='/' else R/'index.html'
  if not target.exists():errors.append(f'Broken navigation: {page}: {link}')
 for src in c.images:
  if src.startswith('/') and not (R/src.strip('/')).exists():errors.append(f'Missing original image: {src}')
for f in ('robots.txt','sitemap.xml','assets/site.css','assets/site.js'):
 if not (R/f).exists():errors.append('Missing required asset: '+f)
if errors:
 print('\n'.join(errors));raise SystemExit(1)
print(f'PASS: {len(pages)} pages; internal navigation, images, SEO files and assets present')

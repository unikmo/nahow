"""Create small web copies of the original photographs. Originals in assets/images stay untouched."""
from pathlib import Path
import json
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
R=Path(__file__).resolve().parents[1]
SRC=R/'assets/images';OUT=R/'assets/web';OUT.mkdir(exist_ok=True)
HERO={'DSC_0857_Enwen-scaled.png'}
meta={}
for f in sorted(SRC.iterdir()):
 if f.suffix.lower() not in('.png','.jpg','.jpeg'):continue
 im=Image.open(f).convert('RGB')
 w=1600 if f.name in HERO else 960
 if im.width>w:im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
 o=OUT/(f.stem+'.webp');im.save(o,'WEBP',quality=74,method=6)
 meta[f.name]={'file':o.name,'w':im.width,'h':im.height,'bytes':o.stat().st_size}
json.dump(meta,open(OUT/'web-manifest.json','w'),indent=1)
# header logo: derived from the original logo, original kept in assets/brand
lg=Image.open(R/'assets/brand/NAHOW-eV-Logo_original.png').convert('RGBA')
bb=lg.getbbox();lg=lg.crop(bb);h=112;lg=lg.resize((round(lg.width*h/lg.height),h),Image.LANCZOS)
lg.save(R/'assets/brand/nahow-logo.png',optimize=True);print('logo',lg.size)
print(len(meta),'images,',sum(m['bytes'] for m in meta.values())//1024,'KB total')

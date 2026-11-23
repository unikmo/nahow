#!/usr/bin/env python3
"""Lossless copy of ORIGINAL image files from an exported WordPress uploads directory.
No resizing, transcoding, crop or metadata edits. Existing names preserved.
"""
from pathlib import Path
import argparse,hashlib,shutil,json,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('source',help='Folder containing original uploaded photographs');p.add_argument('--dest',default=str(Path(__file__).resolve().parents[1] / 'assets/images'));a=p.parse_args()
source=Path(a.source).resolve();dest=Path(a.dest).resolve();extensions={'.jpg','.jpeg','.png','.gif','.webp','.avif'}
if not source.is_dir():p.error('Source folder does not exist')
if source==dest or source in dest.parents:p.error('Source must be separate from destination')
manifest=[]
for item in sorted(source.rglob('*')):
 if not item.is_file() or item.suffix.lower() not in extensions:continue
 rel=item.relative_to(source);target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists() and hashlib.sha256(item.read_bytes()).digest()!=hashlib.sha256(target.read_bytes()).digest():
  print('CONFLICT: not overwriting',target,file=sys.stderr);continue
 if not target.exists():shutil.copy2(item,target)
 sha=hashlib.sha256(item.read_bytes()).hexdigest()
 if hashlib.sha256(target.read_bytes()).hexdigest()!=sha:raise RuntimeError('Copy verification failed: '+str(item))
 manifest.append({'path':str(rel),'sha256':sha,'bytes':item.stat().st_size})
(dest/'ORIGINALS-MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(f'Copied/verified {len(manifest)} original files without image manipulation. Run python tools/build.py next.')

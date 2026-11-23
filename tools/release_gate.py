#!/usr/bin/env python3
"""Fail closed: never claim production readiness unless originals and archive are migrated."""
from pathlib import Path
import json,sys
r=Path(__file__).resolve().parents[1]
conditions={
 'Original photographs imported': (r/'assets/images/ORIGINALS-MANIFEST.json').exists(),
 'Original photographs displayed': any('<img ' in p.read_text() for p in (r/'index.html',r/'einblicke/index.html')),
 'Report archive imported': (r/'assets/documents/ORIGINALS-MANIFEST.json').exists(),
 'HostEurope access verified': (r/'deployment/hosting-verified.txt').exists(),
 'Legal data reviewed': (r/'deployment/legal-reviewed.txt').exists(),
 'Rollback snapshot confirmed': (r/'deployment/rollback-verified.txt').exists(),
}
for k,v in conditions.items():print(('PASS' if v else 'BLOCKED')+' '+k)
sys.exit(0 if all(conditions.values()) else 1)

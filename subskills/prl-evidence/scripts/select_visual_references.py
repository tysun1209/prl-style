#!/usr/bin/env python3
"""Select figure examples from all 291 retained PRL sources; no PDF dependency."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def select(*, family=None, pattern=None, paper=None, version=None, query='', limit=5,
           include_holdout=False, verify_assets=False, root=ROOT):
    root=Path(root).resolve()
    if isinstance(limit,bool) or not isinstance(limit,int) or limit<1:
        raise ValueError('limit must be a positive integer')
    catalog=json.loads((root/'references/visual-corpus-sources.json').read_text())
    families={r['id'] for r in json.loads((root/'profiles/figure-families.json').read_text())['families']}
    if family and family not in families: raise ValueError('unknown family: '+family)
    if pattern and pattern not in catalog['counts']['pattern_counts']: raise ValueError('unknown pattern: '+pattern)
    if version and version not in catalog['counts']['versions']: raise ValueError('unknown source version: '+version)
    matches=[]
    for f in catalog['figures']:
        if f['held_out'] and not include_holdout: continue
        if family and family not in f['family_ids']: continue
        if pattern and pattern not in f['patterns']: continue
        if paper and paper.casefold() not in {f['paper_id'].casefold(),f['doi'].casefold()}: continue
        if version and version!=f['source_version']: continue
        if query and not all(w.casefold() in json.dumps(f,ensure_ascii=False).casefold() for w in query.split()): continue
        matches.append(dict(f))
    matches.sort(key=lambda f: (f['held_out'], f['source_version']!='publisher_pdf', f['id']))
    rows=matches[:limit]
    for row in rows:
        row['local_assets']={}
        if verify_assets:
            for key,rel in row['development_assets'].items():
                path=(root/rel).resolve()
                if not path.is_relative_to(root): raise ValueError('asset path escapes source root')
                if path.exists():
                    expected=row['pdf_sha256' if key=='pdf' else 'image_sha256']
                    if hashlib.sha256(path.read_bytes()).hexdigest()!=expected: raise ValueError('changed asset: '+row['id'])
                    row['local_assets'][key]=str(path)
    return dict(matches=len(matches),references=rows,scope=catalog['scope'],
                includes_holdout=include_holdout,source_assets_included=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['family','pattern','paper','version','query']:p.add_argument('--'+name)
    p.add_argument('--limit',type=int,default=5)
    p.add_argument('--include-holdout',action='store_true',help='Audit only; excluded from default calibration')
    p.add_argument('--verify-assets',action='store_true',help='Check optional local source hashes')
    a=p.parse_args();print(json.dumps(select(**vars(a)),ensure_ascii=False,indent=2))

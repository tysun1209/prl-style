#!/usr/bin/env python3
"""Find reviewed cross-field visual-development sources and composition patterns."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def select(*,family=None,pattern=None,field=None,query='',limit=5,root=ROOT):
    root=Path(root).resolve()
    if isinstance(limit,bool) or not isinstance(limit,int) or limit<1: raise ValueError('limit must be positive')
    catalog=json.loads((root/'references/crossfield-sources.json').read_text())
    patterns=json.loads((root/'profiles/crossfield-visual-patterns.json').read_text())['patterns']
    if pattern and pattern not in {p['id'] for p in patterns}: raise ValueError('unknown pattern: '+pattern)
    rows=catalog['sources']
    if field and field not in {r['field'] for r in rows}: raise ValueError('unknown field: '+field)
    if family and family not in {r['id'] for r in json.loads((root/'profiles/figure-families.json').read_text())['families']}: raise ValueError('unknown family: '+family)
    selected=[]
    for row in rows:
        if row['review_status']!='accepted' or row['split']!='crossfield_visual_development': continue
        if family and family not in row['family_ids']: continue
        if pattern and pattern not in row['patterns']: continue
        if field and field!=row['field']: continue
        if query and not all(w.casefold() in json.dumps(row,ensure_ascii=False).casefold() for w in query.split()): continue
        selected.append(dict(row))
    count=len(selected); selected=selected[:limit]
    for row in selected:
        local={}
        for kind,rel in row['development_assets'].items():
            path=(root/rel).resolve()
            if not path.is_relative_to(root): raise ValueError('asset path escapes root')
            if path.exists():
                expected=row['pdf_sha256' if kind=='pdf' else 'image_sha256']
                if hashlib.sha256(path.read_bytes()).hexdigest()!=expected: raise ValueError('source asset changed: '+row['id'])
                local[kind]=str(path)
        row['local_assets']=local
    return dict(matches=count,references=selected,patterns=[p for p in patterns if not pattern or p['id']==pattern],
                evidence_scope=catalog['scope'],assets_included=False,
                notice='Local source assets are reported only when present and hash verified. Public packages provide DOI/page locators; these development references do not constitute held-out validation.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['family','pattern','field','query']:p.add_argument('--'+name)
    p.add_argument('--limit',type=int,default=5);a=p.parse_args()
    print(json.dumps(select(family=a.family,pattern=a.pattern,field=a.field,query=a.query or '',limit=a.limit),ensure_ascii=False,indent=2))

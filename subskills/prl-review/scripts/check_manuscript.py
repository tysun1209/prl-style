#!/usr/bin/env python3
"""Estimate APS core equivalent length from an explicit, audited inventory."""
import argparse
import json
import math
import re
from pathlib import Path
from corpus_lib import write_json

RULES=Path(__file__).resolve().parents[1]/'profiles/official-rules.json'


def count_words(text):
    # Deliberately plain text only. A TeX parser cannot safely be approximated by deleting commands.
    if not isinstance(text,str):raise ValueError('text must be a string')
    if re.search(r'\\[A-Za-z]|\$|[\u3400-\u9fff]',text):raise ValueError('unsupported markup or non-English text; supply audited English prose inventory')
    return len(re.findall(r"[A-Za-z0-9]+(?:[’'−.-][A-Za-z0-9]+)*",text))


def check(doc):
    errors=[];warnings=[];components={'prose':0,'equations':0,'figures':0,'tables':0}
    rules={r['id']:r for r in json.loads(RULES.read_text())['rules']}
    def error(code,where):errors.append({'code':code,'where':where})
    if not isinstance(doc,dict):return {'passed':False,'errors':[{'code':'document_not_object'}],'ready_to_submit':False}
    if doc.get('inventory_complete') is not True:error('inventory_not_attested','inventory_complete')
    for key in ['body','captions','notes']:
        if key not in doc:error('missing_prose',key);continue
        try:components['prose']+=count_words(doc[key])
        except ValueError as e:error('unparsed_text',key+': '+str(e))
    known={}; all_ids=set()
    for key in ['equations','figures','tables']:
        rows=doc.get(key)
        if not isinstance(rows,list):error('missing_inventory',key);rows=[]
        known[key]=set()
        for i,item in enumerate(rows):
            loc=f'{key}[{i}]'
            try:
                if not isinstance(item,dict):raise ValueError('item must be an object')
                ident=item.get('id')
                if not isinstance(ident,str) or not ident:raise ValueError('missing id')
                if ident in all_ids:raise ValueError('duplicate id')
                all_ids.add(ident);known[key].add(ident)
                col=item['columns']
                if type(col) is not int or col not in [1,2]:raise ValueError('only explicit 1 or 2 columns supported; other spans need manual accounting')
                if key=='figures':
                    w,h=item['width_mm'],item['height_mm']
                    if any(type(v) not in [int,float] or not math.isfinite(v) or v<=0 for v in [w,h]):raise ValueError('positive finite dimensions required')
                    v=rules['APS-LENGTH-FIGURE']['value'];prefix='single' if col==1 else 'double'
                    components[key]+=v[prefix+'_numerator']*h/w+v[prefix+'_offset']
                else:
                    n=item['rows']
                    if type(n) is not int or n<1:raise ValueError('positive integer row count required')
                    if key=='equations':components[key]+=n*rules['APS-LENGTH-MATH']['value']['single_column' if col==1 else 'double_column']
                    else:
                        v=rules['APS-LENGTH-TABLE']['value'];prefix='single' if col==1 else 'double'
                        components[key]+=v[prefix+'_base']+n*v[prefix+'_per_row']
            except (KeyError,ValueError,TypeError) as e:error('invalid_inventory',loc+': '+str(e))
    citations=doc.get('citation_ids')
    if not isinstance(citations,list) or any(not isinstance(x,str) for x in citations):error('missing_citation_inventory','citation_ids');citations=[]
    if len(citations)!=len(set(citations)):error('duplicate_citation','citation_ids')
    known['citations']=set(citations)
    refs=doc.get('references_used')
    if not isinstance(refs,dict):error('missing_reference_inventory','references_used');refs={}
    for key in ['figures','tables','equations','citations']:
        vals=refs.get(key)
        if not isinstance(vals,list):error('missing_reference_type',key);continue
        for ident in vals:
            if not isinstance(ident,str) or ident not in known[key]:error('unresolved_reference',key+':'+str(ident))
    abstract=doc.get('abstract')
    if not isinstance(abstract,str):error('missing_abstract','abstract');abstract=''
    chars=len(abstract);confirm=[]
    if chars>rules['PRL-ABSTRACT']['value']:
        confirm.append({'code':'abstract_limit_conflict','characters':chars,'source':rules['PRL-ABSTRACT']['source_url'],'action':'Verify current PRL-specific applicability; preserve the scientific boundary in any shortened candidate.'})
    if '\n\n' in abstract.strip() or re.search(r'\\cite|\[\d+\]|\\\[|\$\$',abstract):error('abstract_structure','abstract')
    end=doc.get('end_matter_pages')
    if end is None:warnings.append({'code':'end_matter_layout_unverified'})
    elif type(end) not in [int,float] or not math.isfinite(end) or end<0:error('invalid_end_matter','end_matter_pages')
    elif end>rules['PRL-END']['value']:error('end_matter_over_limit','end_matter_pages')
    total=sum(components.values())
    if total>rules['PRL-CORE']['value']:error('core_over_limit',str(total))
    return {'passed':not errors,'errors':errors,'warnings':warnings,'requires_confirmation':confirm,
      'components':components,'core_equivalent_words_estimate':round(total,2) if not any(e['code'] in ['invalid_inventory','unparsed_text','missing_prose','missing_inventory','inventory_not_attested'] for e in errors) else None,
      'abstract_characters_including_spaces':chars,'excluded':['title','abstract','authors','affiliations','references','acknowledgments','author byline footnotes','separately inventoried End Matter'],
      'ready_to_submit':False,'semantic_review_required':True,
      'limits':['Estimate from supplied plain-text and geometry inventory; not a complete TeX/PDF parser.','Reference IDs are inventory checks; compare with actual prose, bibliography and rendered pages.','An inventory attestation cannot establish completeness; inspect manuscript.'],
      'rule_source':'https://journals.aps.org/authors/length-guide'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();r=check(json.loads(a.manifest.read_text()))
    if a.output:write_json(a.output,r)
    print(json.dumps(r,indent=2));raise SystemExit(1 if not r['passed'] else 2 if r['requires_confirmation'] else 0)

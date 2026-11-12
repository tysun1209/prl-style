#!/usr/bin/env python3
"""Check evidence-ledger structure and references, never scientific truth."""
import argparse
import json
from pathlib import Path
from corpus_lib import write_json


def validate(ledger, artifacts=None):
    errors=[]; open_issues=[]
    def fail(code,where): errors.append({'code':code,'where':where})
    if not isinstance(ledger,dict):return {'passed':False,'errors':[{'code':'ledger_not_object'}],'semantic_review_required':True}
    indexes={}
    for key in ['evidence','claims','figures','citations']:
        rows=ledger.get(key)
        if not isinstance(rows,list):fail('missing_list',key);rows=[]
        index={}
        for i,row in enumerate(rows):
            if not isinstance(row,dict) or not isinstance(row.get('id'),str) or not row['id'].strip():fail('missing_id',f'{key}[{i}]');continue
            if row['id'] in index:fail('duplicate_id',row['id'])
            index[row['id']]=row
        indexes[key]=index
    if not indexes['claims']:fail('no_claims','claims')
    for eid,e in indexes['evidence'].items():
        for field in ['source','locator','description','kind']:
            if not isinstance(e.get(field),str) or not e[field].strip():fail('missing_evidence_field',eid+':'+field)
        if e.get('kind') not in ['author_supplied','computed','published_verified','synthetic_demo']:fail('unknown_evidence_kind',eid)
    for cid,c in indexes['claims'].items():
        for field in ['text','scope','strength','uncertainty']:
            if not isinstance(c.get(field),str) or not c[field].strip():fail('missing_claim_field',cid+':'+field)
        if c.get('status') not in ['supported','open']:fail('unknown_claim_status',cid)
        if c.get('status')=='open':open_issues.append({'id':cid,'reason':c.get('open_issue','Unresolved evidence')})
        for field,target in [('evidence_ids','evidence'),('figure_ids','figures'),('citation_ids','citations')]:
            ids=c.get(field)
            if not isinstance(ids,list):fail('missing_reference_list',cid+':'+field);continue
            if field=='evidence_ids' and not ids and c.get('status')=='supported':fail('supported_without_evidence',cid)
            for ident in ids:
                if not isinstance(ident,str) or ident not in indexes[target]:fail('unknown_'+target,cid+':'+str(ident))
        facts=c.get('protected_facts')
        if not isinstance(facts,list):fail('missing_protected_facts',cid);continue
        seen=set()
        for fact in facts:
            if not isinstance(fact,dict):fail('malformed_fact',cid);continue
            for field in ['id','meaning','value','unit']:
                if field not in fact or not isinstance(fact[field],str) or not fact[field].strip():fail('missing_fact_field',cid+':'+field)
            fid=fact.get('id')
            if isinstance(fid,str):
                if fid in seen:fail('duplicate_fact',cid+':'+fid)
                seen.add(fid)
    for cid,c in indexes['citations'].items():
        if c.get('verification')!='verified' or not c.get('source'):fail('unverified_citation',cid)
    from quantity_audit import audit
    quantities=audit(ledger,artifacts)
    errors.extend(quantities['errors'])
    if ledger.get('schema_version') == 3:
        from assertive_writing import validate_contracts
        errors.extend(validate_contracts(ledger.get('claims'), ledger.get('evidence')))
    return {'passed':not errors,'errors':errors,'quantity_audit':quantities,'open_issues':open_issues,'counts':{k:len(v) for k,v in indexes.items()},
        'semantic_review_required':True,'scientific_validity':'not_certified','ready_to_submit':False,
        'limits':['A source string or a verified flag does not establish evidence quality. Inspect the actual source and its support for each claim.']}


if __name__=='__main__':
    from quantity_audit import load_artifacts
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('ledger',type=Path);p.add_argument('--output',type=Path)
    p.add_argument('--figure-report',action='append',default=[],metavar='ID=PATH',help='Export report with actual labels and hash-verified images (PNG by default; legacy PDF reports supported)')
    p.add_argument('--text',action='append',default=[],metavar='ID=PATH',help='Actual caption/manuscript file; locator is text')
    a=p.parse_args()
    try:
        artifacts,provenance=load_artifacts(a.figure_report,a.text)
        r=validate(json.loads(a.ledger.read_text()),artifacts)
        r['audited_artifacts']=provenance
    except (OSError,ValueError) as exc:
        r={'passed':False,'errors':[{'code':'artifact_load_error','detail':str(exc)}],'semantic_review_required':True}
    if a.output:write_json(a.output,r)
    print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(0 if r['passed'] else 1)

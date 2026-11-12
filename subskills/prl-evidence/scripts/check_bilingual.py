#!/usr/bin/env python3
"""Check explicit protected bilingual spans; semantic equivalence needs review."""
import argparse
from collections import Counter
from decimal import Decimal,InvalidOperation
import json
import re
import unicodedata
from pathlib import Path
from corpus_lib import write_json

NUMBER_WORDS=dict(zip('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split(),map(str,range(21))))
UNITS={'percent':[r'%',r'\bpercent\b',r'百分之'], 'count':[], 'dimensionless':[],
       'GHz':[r'(?<![A-Za-z])GHz(?![A-Za-z])',r'吉赫兹'], 'K':[r'(?<![A-Za-z])K(?![A-Za-z])',r'开尔文'],
       's':[r'(?<![A-Za-z])s(?![A-Za-z])',r'\bseconds?\b',r'秒'], 'mm':[r'(?<![A-Za-z])mm(?![A-Za-z])',r'毫米']}


def normalize(text):
    text=unicodedata.normalize('NFKC',text).replace('−','-').replace('–','-').replace('﹣','-')
    text=re.sub(r'([+\-]?\d+(?:\.\d+)?)\s*[×x]\s*10\s*\^?\s*([+\-]?\d+)',r'\1e\2',text)
    text=re.sub(r'\b('+ '|'.join(NUMBER_WORDS)+r')\b',lambda m:NUMBER_WORDS[m[0].lower()],text,flags=re.I)
    return re.sub(r'\s+',' ',text).strip()


def numbers(text):
    return [Decimal(x) for x in re.findall(r'(?<![A-Za-z0-9_.])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?(?![\d.])',normalize(text))]


def reference_tokens(text):
    text=normalize(text)
    figs=re.findall(r'(?:Fig(?:ure)?\.?\s*|图\s*)(\d+(?:\([a-z]\))?)',text,flags=re.I)
    cites=re.findall(r'\[\[cite:([^\]]+)\]\]',text)
    return {'figures':Counter(x.lower() for x in figs),'citations':Counter(cites)}


def check(doc,known_claim_ids=None):
    errors=[];warnings=[]
    def error(code,where):errors.append({'code':code,'where':where})
    if not isinstance(doc,dict):return {'passed':False,'errors':[{'code':'document_not_object'}],'semantic_equivalence':'unverified'}
    segments=doc.get('segments')
    if not isinstance(segments,list) or not segments:error('missing_segments','segments');segments=[]
    ids=set()
    for i,s in enumerate(segments):
        loc=f'segments[{i}]'
        if not isinstance(s,dict):error('invalid_segment',loc);continue
        if not isinstance(s.get('id'),str) or not s['id']:error('missing_segment_id',loc)
        elif s['id'] in ids:error('duplicate_segment_id',s['id'])
        else:ids.add(s['id'])
        if any(not isinstance(s.get(lang),str) or not s[lang].strip() for lang in ['en','zh']):error('missing_language',loc);continue
        claims=s.get('claim_ids')
        if not isinstance(claims,list) or not claims or any(not isinstance(c,str) for c in claims):error('missing_claim_mapping',loc)
        elif known_claim_ids is not None:
            for cid in claims:
                if cid not in known_claim_ids:error('unknown_claim',loc+':'+cid)
        else:warnings.append({'code':'claim_ids_not_checked_against_ledger','where':loc})
        texts={lang:normalize(s[lang]) for lang in ['en','zh']}
        if reference_tokens(s['en'])!=reference_tokens(s['zh']):error('reference_mismatch',loc)
        facts=s.get('protected_facts')
        if not isinstance(facts,list):error('missing_facts',loc);facts=[]
        fact_ids=set()
        for f in facts:
            if not isinstance(f,dict):error('invalid_fact',loc);continue
            fid=f.get('id');floc=loc+':'+str(fid)
            if not isinstance(fid,str) or not fid:error('missing_fact_id',floc)
            elif fid in fact_ids:error('duplicate_fact',floc)
            else:fact_ids.add(fid)
            try:
                values=f['values']
                if not isinstance(values,list) or not values:raise ValueError('nonempty numeric values list required')
                expected=[Decimal(str(v)) for v in values]
                if any(not v.is_finite() for v in expected):raise ValueError('finite numbers required')
                unit=f['unit']
                if unit not in UNITS:raise ValueError('unit unsupported; extend explicit aliases or review manually')
                for lang in ['en','zh']:
                    anchor=f['anchors'][lang]
                    if not isinstance(anchor,str) or not anchor:raise ValueError('nonempty anchor required')
                    anchor=normalize(anchor)
                    if anchor not in texts[lang]:error('protected_anchor_missing',floc+':'+lang)
                    # Order preserves intervals and mean/uncertainty pairs; do not use sets.
                    if numbers(anchor)!=expected:error('protected_number_mismatch',floc+':'+lang)
                    if UNITS[unit] and not any(re.search(p,anchor) for p in UNITS[unit]):error('protected_unit_missing',floc+':'+lang)
            except (KeyError,TypeError,ValueError,InvalidOperation) as e:error('invalid_fact',floc+':'+str(e))
        terms=s.get('term_checks',[])
        if not isinstance(terms,list):error('invalid_terms',loc);terms=[]
        for term in terms:
            try:
                for lang in ['en','zh']:
                    phrase=term[lang]
                    if not isinstance(phrase,str) or not phrase:raise ValueError('empty term')
                    if normalize(phrase) not in texts[lang]:error('term_missing',loc+':'+lang+':'+phrase)
                    for forbidden in term.get('forbidden_'+lang,[]):
                        if normalize(forbidden) in texts[lang]:error('forbidden_term',loc+':'+lang+':'+forbidden)
            except (KeyError,TypeError,ValueError) as e:error('invalid_terms',loc+':'+str(e))
        # Anchors help detect omissions. Their presence never proves semantic identity.
        for constraint in s.get('meaning_anchors',[]):
            try:
                for lang in ['en','zh']:
                    phrase=constraint[lang]
                    if not isinstance(phrase,str) or not phrase:raise ValueError('empty anchor')
                    if normalize(phrase) not in texts[lang]:error('meaning_anchor_missing',loc+':'+constraint['id']+':'+lang)
            except (KeyError,TypeError,ValueError) as e:error('invalid_meaning_anchor',loc+':'+str(e))
    return {'passed':not errors,'errors':errors,'warnings':warnings,'segments_checked':len(segments),
      'semantic_equivalence':'unverified; agent or expert comparison required','ready_to_submit':False,
      'required_semantic_review':['negation and its scope','baseline and comparison direction','causal versus associational statement','regime and exclusions','uncertainty and statistical meaning','unlisted numerical facts and references','native-language argument flow'],
      'limits':['Protected spans are supplied by the reviewer and may be incomplete.','Exact anchors can produce conservative false alarms after valid paraphrasing; re-inspect before updating them.','No implicit unit conversion; use identical declared normalized units or explicitly review the conversion.','Reference parser covers simple Fig./Figure/图 references and [[cite:ID]] tokens; compound ranges and native bibliography markup need manual review.']}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('pair',type=Path);p.add_argument('--ledger',type=Path);p.add_argument('--output',type=Path)
    p.add_argument('--figure-report',action='append',default=[],metavar='ID=PATH',help='Bind actual export labels and hash-verified images (PNG by default; legacy PDF reports supported)')
    p.add_argument('--text',action='append',default=[],metavar='ID=PATH',help='Bind actual caption/manuscript text for the ledger quantity audit')
    a=p.parse_args(argv)
    if (a.figure_report or a.text) and not a.ledger:p.error('artifact bindings require --ledger')
    known=None;vr=None;provenance={}
    try:
        if a.ledger:
            from validate_claims import validate
            from quantity_audit import load_artifacts
            ledger=json.loads(a.ledger.read_text());artifacts,provenance=load_artifacts(a.figure_report,a.text);vr=validate(ledger,artifacts)
            if vr['passed']:known={c['id'] for c in ledger['claims']}
        r=vr if vr is not None and not vr['passed'] else check(json.loads(a.pair.read_text()),known)
        if vr is not None and vr['passed']:r['ledger_validation']=vr
        if a.ledger:r['audited_artifacts']=provenance
    except (OSError,ValueError) as exc:
        r={'passed':False,'errors':[{'code':'artifact_or_input_load_error','detail':str(exc)}],'semantic_equivalence':'unverified'}
    if a.output:write_json(a.output,r)
    print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if r['passed'] else 1


if __name__=='__main__':raise SystemExit(main())

"""Local writing audit: declared evidence contracts plus nonoverlapping lexical spans.

A passing result covers the supplied contract, not arbitrary semantic equivalence.
Rewriting is performed by the skill's agent, never by blind string substitution.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import unicodedata
from collections import Counter
from decimal import Decimal
from pathlib import Path
from typing import Any

# Only editorial padding and compound hedges enter the reduction denominator.
PADDING = {
    'en': (r'\bit is important to note(?: that)?\b', r'\bit should be noted(?: that)?\b',
           r'\bit is worth noting(?: that)?\b', r'\b(?:may|might|could) (?:possibly|potentially)\b',
           r'\bperhaps possibly\b', r'\bin some sense\b', r'\bto some extent\b',
           r'\bit can be (?:clearly )?seen that\b'),
    'zh': (r'值得注意的是', r'需要指出的是', r'可以(?:明显地)?看出', r'在一定程度上', r'或许可能'),
}
MODALS = {'en': (r'\b(?:may|might|could|perhaps|possibly|potentially)\b', r'\b(?:appears|seems) to\b'),
          'zh': (r'可能会|可能|或许|似乎|看起来|潜在地',)}
INTERPRETATIONS = {'en': (r'\b(?:is|are) consistent with\b', r'\bsuggest(?:s|ed)?\b', r'\bindicat(?:e|es|ed)\b'),
                   'zh': (r'与[^。；]*?一致', r'提示',)}
VERB_FAMILIES = {
    'show': ['show','shows','showed','shown','表明','显示'],
    'find': ['find','finds','found','发现'],
    'measure': ['measure','measures','measured','测得','测量'],
    'calculate': ['calculate','calculates','calculated','计算得到'],
    'derive': ['derive','derives','derived','推导出','推导'],
    'prove': ['prove','proves','proved','proven','证明'],
    'establish': ['establish','establishes','established','建立','证实'],
    'demonstrate': ['demonstrate','demonstrates','demonstrated'],
}
RISK_PATTERNS = {'en': (r'\buniversal(?:ly)?\b',r'\bfor all\b',r'\barbitrary\b',r'\bexact\b',
                        r'\bstatistically significant\b', r'\bcaus(?:e|es|ed)\b', r'\bfirst observation\b'),
                 'zh': (r'普适|普遍适用|所有范围|任意',r'精确|严格',r'统计显著',r'导致',r'首次')}
LEVELS = {'observation','numerical','derivation','mechanism_test','nondiscriminating','unknown'}
CLAIM_TYPES = {'observation','numerical','theory','comparison','mechanism','interpretation','unknown'}
NUMBER_RE = re.compile(r'(?<![A-Za-z0-9_.])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?(?![\d.])')
UNITS = {'percent': r'(?:%|percent\b)', 'count': '', 'dimensionless': '',
         's': r'(?:s\b|seconds?\b|秒)', 'mm': r'(?:mm\b|毫米)',
         'GHz': r'(?:GHz\b|吉赫兹)', 'K': r'(?:K\b|开尔文)'}


def normalize(text: str) -> str:
    text = unicodedata.normalize('NFKC', text).replace('−','-')
    # En dash between numeric endpoints is a separator, not a negative sign.
    text = re.sub(r'(?<=\d)[–—](?=[+\-]?\d)', ' to ', text)
    return re.sub(r'\s+', ' ', text).strip()


def spans(text: str, patterns, excluded=()) -> list[dict]:
    matches = [m for p in patterns for m in re.finditer(p, text, re.I)]
    result = []
    occupied = [(x['start'],x['end']) for x in excluded]
    for m in sorted(matches, key=lambda m: (m.start(), -(m.end()-m.start()))):
        if any(m.start() < end and m.end() > start for start,end in occupied):
            continue
        occupied.append(m.span())
        result.append({'text':m.group(), 'start':m.start(), 'end':m.end()})
    return result


def split_sentences(text: str, language: str) -> list[str]:
    if language == 'zh':
        return [p.strip() for p in re.split(r'(?<=[。！？；])', text) if p.strip()]
    safe = re.sub(r'\b(?:Fig|Figs|Eq|Eqs|Dr|Prof|vs)\.', lambda m:m.group().replace('.', '\uE000'), text)
    safe = re.sub(r'\b(?:e\.g\.|i\.e\.|et al\.)',lambda m:m.group().replace('.', '\uE000'),safe)
    safe = re.sub(r'(?<=\d)\.(?=\d)', '\uE000', safe)
    return [p.replace('\uE000','.').strip() for p in re.split(r'(?<=[.!?])\s+',safe) if p.strip()]


def extract_numbers(text: str) -> list[Decimal]:
    return [Decimal(m.group()) for m in NUMBER_RE.finditer(normalize(text))]


def phrase_present(text: str, phrase: str) -> bool:
    phrase = normalize(phrase)
    if not phrase:
        return False
    left = r'(?<![A-Za-z0-9_])' if phrase[0].isascii() and phrase[0].isalnum() else ''
    right = r'(?![A-Za-z0-9_])' if phrase[-1].isascii() and phrase[-1].isalnum() else ''
    return bool(re.search(left + re.escape(phrase) + right, normalize(text), re.I))


def verb_forms(text: str) -> list[str]:
    return sorted({v for forms in VERB_FAMILIES.values() for v in forms if phrase_present(text,v)})


def verb_root(verb: str) -> str:
    return next((root for root,forms in VERB_FAMILIES.items() if verb in forms), verb)


def analyze_text(text: str, language: str) -> dict[str, Any]:
    if language not in PADDING:
        raise ValueError('language must be en or zh')
    padding = spans(text,PADDING[language])
    return {'language':language, 'sentence_count':len(split_sentences(text,language)),
            'redundant_hedges':len(padding), 'hedge_spans':padding,
            'modal_candidates':spans(text,MODALS[language],padding),
            'qualified_interpretations':len(spans(text,INTERPRETATIONS[language])),
            'qualified_spans':spans(text,INTERPRETATIONS[language]),
            'strong_verbs':verb_forms(text), 'risk_candidates':spans(text,RISK_PATTERNS[language]),
            'numbers':[str(v) for v in extract_numbers(text)],'character_count':len(text)}


def reference_tokens(text):
    text = normalize(text)
    return {'figures':Counter(re.findall(r'(?:Fig(?:ure)?\.?\s*|图\s*)(\d+(?:\([a-z]\))?)',text,re.I)),
            'citations':Counter(re.findall(r'\[\[cite:([^\]]+)\]\]|\\cite(?:t|p)?\{([^}]+)\}',text))}


def forms_for(item, language):
    if isinstance(item,str):
        return [item]
    if not isinstance(item,dict):
        return []
    values = item.get('forms',[])
    if isinstance(values,dict):
        values=values.get(language,[])
    return values if isinstance(values,list) and all(isinstance(x,str) and x.strip() for x in values) else []


def contains_fact(text, fact):
    """Require exact numerical values and their unit, with no substring matching."""
    try:
        values = [Decimal(str(x)) for x in fact.get('values',[fact.get('value')])]
        if not values or not all(v.is_finite() for v in values):
            return False
    except Exception:
        return False
    text=normalize(text)
    matches=list(NUMBER_RE.finditer(text))
    expected=Counter(values)
    actual=Counter(Decimal(m.group()) for m in matches)
    if expected-actual:
        return False
    unit = fact.get('unit','')
    if unit in ('count','dimensionless'):
        return True
    pattern=UNITS.get(unit, re.escape(unit)+r'(?![A-Za-z])')
    if not unit:
        return False
    for i in range(len(matches)-len(values)+1):
        group=matches[i:i+len(values)]
        if [Decimal(m.group()) for m in group] != values:
            continue
        if re.match(r'\s*'+pattern,text[group[-1].end():],re.I):
            return True
        if unit=='percent' and text[max(0,group[0].start()-3):group[0].start()]=='百分之':
            return True
    return False


def validate_contracts(claims, evidence):
    """Validate v3 extension independently from the v1 physical-quantity ledger."""
    errors=[]
    def fail(code,detail): errors.append({'code':code,'detail':detail})
    if not isinstance(claims,list) or not claims:
        return [{'code':'missing_claims','detail':'Provide at least one claim for evidence-bound audit.'}]
    if not isinstance(evidence,list) or any(not isinstance(e,dict) for e in evidence):
        return [{'code':'missing_evidence','detail':'evidence must be a list of source records'}]
    evidence_by_id={}
    for e in evidence:
        eid=e.get('id')
        if not isinstance(eid,str) or not eid or eid in evidence_by_id:
            fail('invalid_evidence','Evidence IDs must be nonempty and unique.'); continue
        evidence_by_id[eid]=e
        if not all(isinstance(e.get(k),str) and e[k].strip() for k in ('source','locator','description','kind')):
            fail('invalid_evidence',eid)
    ids=set()
    for c in claims:
        if not isinstance(c,dict):
            fail('invalid_claim','claim must be an object'); continue
        cid=c.get('id')
        if not isinstance(cid,str) or not cid or cid in ids:
            fail('invalid_claim','Claim IDs must be nonempty and unique.'); continue
        ids.add(cid)
        for field in ('supporting_artifacts','hedge_reason','audit_status'):
            if field not in c: fail('invalid_claim_field',f'{cid}:{field}')
        if 'required_boundary' not in c and 'required_boundaries' not in c:
            fail('invalid_claim_field',f'{cid}:required_boundary')
        if not isinstance(c.get('hedge_reason'),str): fail('invalid_claim_field',f'{cid}:hedge_reason')
        if c.get('audit_status') not in ('pending','contract_passed','needs_evidence','failed'):
            fail('invalid_claim_field',f'{cid}:audit_status')
        if c.get('claim_type') not in CLAIM_TYPES or c.get('evidence_level') not in LEVELS:
            fail('invalid_claim_level',cid)
        for key in ('allowed_verbs','forbidden_strengthening'):
            values=c.get(key)
            if not isinstance(values,list) or any(not isinstance(x,str) or not x.strip() for x in values):
                fail('invalid_claim_field',f'{cid}:{key}')
        values=c.get('allowed_strengthening',[])
        if not isinstance(values,list) or any(not isinstance(x,str) or not x.strip() for x in values):
            fail('invalid_claim_field',f'{cid}:allowed_strengthening')
        facts=c.get('protected_facts')
        if not isinstance(facts,list) or any(not isinstance(f,dict) for f in facts):
            fail('invalid_claim_field',f'{cid}:protected_facts')
        boundary=c.get('required_boundary',c.get('required_boundaries',[]))
        if isinstance(boundary,str): boundary=[boundary]
        for field,values in (('required_boundary',boundary),('protected_terms',c.get('protected_terms',[]))):
            if not isinstance(values,list) or any(not isinstance(x,(str,dict)) for x in values):
                fail('invalid_claim_field',f'{cid}:{field}')
        evidence_ids=c.get('evidence_ids',[])
        if not isinstance(evidence_ids,list) or any(not isinstance(x,str) for x in evidence_ids):
            fail('missing_evidence',cid); continue
        if c.get('status')=='supported' and not evidence_ids:
            fail('missing_evidence',cid)
        for eid in evidence_ids:
            if eid not in evidence_by_id: fail('missing_evidence',f'{cid}:{eid}')
        artifacts=c.get('supporting_artifacts',evidence_ids)
        if not isinstance(artifacts,list) or any(not isinstance(x,str) or x not in evidence_ids for x in artifacts):
            fail('invalid_supporting_artifacts',cid)
        if c.get('status') not in ('supported','open'): fail('invalid_claim_status',cid)
        if c.get('causal_status') not in ('not_tested','association','supported','not_applicable'):
            fail('invalid_causal_status',cid)
        if not isinstance(c.get('aggregation_level'),str) or not c['aggregation_level']:
            fail('missing_aggregation_level',cid)
    return errors


def _audit_segment(segment, claims, language):
    errors=[]; unresolved=[]
    def fail(code,detail): errors.append({'code':code,'detail':detail,'segment_id':segment['id']})
    original=segment['original']; revised=segment['revised']
    before=analyze_text(original,language); after=analyze_text(revised,language)
    old_numbers=Counter(extract_numbers(original)); new_numbers=Counter(extract_numbers(revised))
    if old_numbers-new_numbers: fail('protected_fact_changed', 'Removed or changed numbers: '+str(dict(old_numbers-new_numbers)))
    if new_numbers-old_numbers: fail('new_number','Added numbers: '+str(dict(new_numbers-old_numbers)))
    if reference_tokens(original)!=reference_tokens(revised): fail('reference_mismatch','Figure/citation references changed.')
    allowed=set(); permissions=set(); evidence_ids=set(); conditions=[]; facts=[]
    for c in claims:
        cid=c['id']; evidence_ids.update(c.get('evidence_ids',[]))
        if c.get('status')!='supported' or c.get('evidence_level')=='unknown':
            unresolved.append({'claim_id':cid,'issue':c.get('open_issue','Claim evidence is unresolved.')})
        allowed.update(str(v) for v in c.get('allowed_verbs',[]))
        permissions.update(c.get('allowed_strengthening',[]))
        for fact in c.get('protected_facts',[]):
            valid=isinstance(fact,dict) and contains_fact(revised,fact)
            facts.append({'claim_id':cid,'fact_id':fact.get('id') if isinstance(fact,dict) else None,'passed':valid})
            if not valid: fail('protected_fact_changed',f'{cid}: {fact}')
        boundary=c.get('required_boundary',c.get('required_boundaries',[]))
        if isinstance(boundary,str): boundary=[boundary]
        if not isinstance(boundary,list):
            fail('invalid_boundary',cid); boundary=[]
        for kind,items in (('boundary',boundary),('meaning',c.get('protected_terms',[]))):
            if not isinstance(items,list):
                fail('invalid_constraint',cid); continue
            for item in items:
                forms=forms_for(item,language)
                valid=bool(forms) and any(phrase_present(revised,f) for f in forms)
                conditions.append({'claim_id':cid,'kind':kind,'forms':forms,'passed':valid})
                if not valid: fail('boundary_removed' if kind=='boundary' else 'meaning_constraint_missing', f'{cid}:{forms}')
        for forbidden in c.get('forbidden_strengthening',[]):
            if isinstance(forbidden,str) and phrase_present(revised,forbidden):
                fail('unsupported_strengthening',f'{cid}: prohibited expression {forbidden}')
    # Each changed proposition is audited against only its explicitly mapped claims.
    added=set(after['strong_verbs'])-set(before['strong_verbs'])
    for verb in added:
        if verb not in allowed: fail('unsupported_strengthening',f'New verb {verb!r} lacks a mapped permission.')
    for verb in after['strong_verbs']:
        root=verb_root(verb)
        if root in ('derive','prove') and not any(c.get('evidence_level')=='derivation' for c in claims):
            fail('unsupported_strengthening',f'{verb} requires a derivation for this claim.')
        if root in ('establish','demonstrate') and verb not in allowed:
            fail('unsupported_strengthening',f'{verb} requires an explicit claim-specific permission.')
    for risk in after['risk_candidates']:
        expression=risk['text']
        if not any(phrase_present(expression,p) or phrase_present(p,expression) for p in permissions):
            # Negated/qualified statements are candidates for review, never a ban
            # on e.g. "no statistically significant difference" or exact theories.
            protected=any(phrase_present(f,expression) for c in claims
                          for item in c.get('protected_terms',[]) for f in forms_for(item,language))
            if protected:
                continue
            if not phrase_present(original,expression):
                fail('unsupported_strengthening',f'New scope/causal/statistical expression: {expression}')
            else:
                unresolved.append({'issue':f'Existing assertion requires a scope/evidence contract: {expression}'})
    neg = r'\b(?:no|not|never|neither|without)\b' if language=='en' else r'未|不|无|没有'
    if bool(re.search(neg,original,re.I)) != bool(re.search(neg,revised,re.I)):
        has_negation_contract=any(t.get('category')=='negation' for c in claims for t in c.get('protected_terms',[]) if isinstance(t,dict))
        if not has_negation_contract:
            unresolved.append({'issue':'Negation changed; provide a meaning constraint for the affected claim.'})
    if before['modal_candidates'] and not after['modal_candidates']:
        if any(c.get('evidence_level') in ('nondiscriminating','unknown') for c in claims):
            fail('unsupported_strengthening','Interpretation lost its evidence-dependent qualification.')
    return {'id':segment['id'],'claim_ids':segment['claim_ids'],'evidence_ids':sorted(evidence_ids),
            'original':original,'revised':revised,'original_sentences':split_sentences(original,language),
            'revised_sentences':split_sentences(revised,language),'before':before,'after':after,
            'verb_changes':{'added':sorted(added),'removed':sorted(set(before['strong_verbs'])-set(after['strong_verbs']))},
            'facts':facts,'constraints':conditions,'errors':errors,'unresolved':unresolved}


def audit_document(document: Any) -> dict:
    report={'schema_version':'prl-assertive-audit-v3','passed':False,'errors':[],'warnings':[],
            'segments':[],'unresolved':[],'semantic_equivalence':'not_established_by_lexical_audit'}
    def invalid(code,detail):
        report['errors'].append({'code':code,'detail':detail}); return report
    if not isinstance(document,dict): return invalid('invalid_document','Input must be an object.')
    language=document.get('language','en'); mode=document.get('mode','assertive_calibrated')
    if language not in ('en','zh'): return invalid('unsupported_language',str(language))
    if mode not in ('assertive_calibrated','legacy_v2'): return invalid('unsupported_mode',str(mode))
    claims=document.get('claims'); evidence=document.get('evidence',[])
    report['errors']=validate_contracts(claims,evidence)
    if report['errors']: return report
    by_id={c['id']:c for c in claims}
    segments=document.get('segments')
    if segments is None:
        if len(claims)!=1: return invalid('ambiguous_mapping','Multiple claims require explicit segments.')
        segments=[{'id':'S1','claim_ids':[claims[0]['id']],'original':document.get('original'),'revised':document.get('revised')}]
    if not isinstance(segments,list) or not segments: return invalid('missing_segments','No edit segments supplied.')
    seen=set()
    for s in segments:
        if not isinstance(s,dict): return invalid('invalid_segment','Segment must be an object.')
        sid=s.get('id'); ids=s.get('claim_ids')
        if not isinstance(sid,str) or not sid or sid in seen: return invalid('invalid_segment_id',str(sid))
        seen.add(sid)
        if not isinstance(ids,list) or not ids or any(not isinstance(i,str) or i not in by_id for i in ids):
            return invalid('unknown_claim',sid)
        if len(ids) != 1:
            return invalid('ambiguous_mapping', f'{sid}: split the edit into atomic claim segments; shared permissions cannot be assigned to individual assertions.')
        if not all(isinstance(s.get(k),str) and s[k].strip() for k in ('original','revised')):
            return invalid('missing_text',sid)
        row=_audit_segment(s,[by_id[i] for i in ids],language)
        report['segments'].append(row); report['errors'].extend(row['errors']); report['unresolved'].extend(row['unresolved'])
    before=sum(s['before']['redundant_hedges'] for s in report['segments'])
    after=sum(s['after']['redundant_hedges'] for s in report['segments'])
    reduction=(before-after)/before if before else None
    eligible=before>0
    if after>before: report['warnings'].append({'code':'editorial_padding_increased','detail':'Inspect added padding.'})
    # The agreed percentage is a batch diagnostic. Small passages often need to
    # remove one whole redundant phrase; do not retain fluff to hit a quota.
    target='not_eligible' if not eligible else ('within_target' if .2<=reduction<=.35 else 'outside_target')
    report['metrics']={'original_redundant_hedges':before,'revised_redundant_hedges':after,
        'hedge_reduction_fraction':round(reduction,6) if reduction is not None else None,
        'hedge_target_status':target,'eligible_for_hedge_target':eligible,
        'boundary_status':'failed' if any(e['code']=='boundary_removed' for e in report['errors']) else 'passed',
        'protected_fact_status':'failed' if any(e['code'] in ('protected_fact_changed','new_number') for e in report['errors']) else 'passed'}
    report.update(language=language, section=document.get('section','unspecified'), policy=mode,
        mechanical_passed=not report['errors'], passed=not report['errors'] and not report['unresolved'],
        audit_status='failed' if report['errors'] else ('needs_evidence' if report['unresolved'] else 'contract_passed'),
        input_sha256=hashlib.sha256(json.dumps(document,ensure_ascii=False,sort_keys=True).encode()).hexdigest())
    return report


def load_document(path: Path, ledger: Path | None=None) -> dict:
    document=json.loads(Path(path).read_text(encoding='utf-8'))
    if ledger is not None:
        data=json.loads(Path(ledger).read_text(encoding='utf-8'))
        if not isinstance(document,dict) or not isinstance(data,dict): raise ValueError('Input and ledger must be objects.')
        if 'claims' in document and document['claims'] != data.get('claims'):
            raise ValueError('Embedded claims conflict with the explicit ledger.')
        if 'evidence' in document and document['evidence'] != data.get('evidence'):
            raise ValueError('Embedded evidence conflicts with the explicit ledger.')
        document=copy.deepcopy(document)
        document['claims']=data.get('claims',[]); document['evidence']=data.get('evidence',[])
    return document

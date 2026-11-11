#!/usr/bin/env python3
"""Audit declared claim contracts for English/Chinese edits; save detail on request."""
import argparse
import json
from pathlib import Path
from assertive_writing import audit_document, load_document


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--ledger',type=Path)
    p.add_argument('--language',choices=['en','zh'])
    p.add_argument('--section')
    p.add_argument('--mode',choices=['assertive_calibrated','legacy_v2'])
    p.add_argument('--audit','--output',dest='audit',type=Path,help='Write the optional detailed JSON audit.')
    a=p.parse_args()
    try:
        doc=load_document(a.input,a.ledger)
        if not isinstance(doc,dict): raise ValueError('Input must be a JSON object.')
        for key in ('language','section','mode'):
            if getattr(a,key) is not None: doc[key]=getattr(a,key)
        report=audit_document(doc)
    except (OSError,ValueError,TypeError) as exc:
        report={'passed':False,'errors':[{'code':'input_error','detail':str(exc)}]}
    if a.audit:
        a.audit.parent.mkdir(parents=True,exist_ok=True)
        a.audit.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'passed':report['passed'],'audit_status':report.get('audit_status','invalid_input'),
                      'errors':report['errors'][:3],'unresolved':report.get('unresolved',[])[:3],
                      'audit':str(a.audit) if a.audit else None},ensure_ascii=False))
    return 0 if report['passed'] else 1


if __name__=='__main__': raise SystemExit(main())

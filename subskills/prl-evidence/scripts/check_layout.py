#!/usr/bin/env python3
"""Measure real manuscript PDFs and TeX diagnostics; never certify prose or layout."""
import argparse
from pathlib import Path
import re
import fitz
from corpus_lib import sha256,write_json


def font_record(doc,font):
    key=font[0];record={'name':font[3],'type':font[2]}
    if font[2]=='Type3' and key:
        # Type3 embeds glyph drawing programs, not an extractable FontFile.
        kind,value=doc.xref_get_key(key,'CharProcs')
        if kind=='xref':value=doc.xref_object(int(value.split()[0]))
        refs=[int(x) for x in re.findall(r'(\d+)\s+0\s+R',value)] if kind in ['xref','dict'] else []
        embedded=bool(refs) and all(doc.xref_is_stream(x) and bool(doc.xref_stream(x)) for x in refs)
        return record|{'embedded':embedded,'embedding_basis':'Type3 CharProcs glyph streams','glyph_programs':len(refs)}
    return record|{'embedded':bool(doc.extract_font(key)[3]) if key else False,'embedding_basis':'extractable font program'}


def inspect_layout(pdf,log=None):
    pdf=Path(pdf);errors=[];warnings=[];pages=[];fonts={}
    with fitz.open(pdf) as doc:
        if not len(doc):errors.append('empty PDF')
        for number,page in enumerate(doc,1):
            sizes=[];spans=0
            for font in page.get_fonts(full=True):
                key=font[0]
                fonts[key]=font_record(doc,font)
            for block in page.get_text('dict')['blocks']:
                if block['type']!=0:continue
                for line in block['lines']:
                    for span in line['spans']:
                        if not span['text'].strip():continue
                        spans+=1;sizes.append(span['size'])
                        if '\ufffd' in span['text']:errors.append(f'page {number}: replacement glyph in extracted text')
                        if '\x00' in span['text']:warnings.append({'code':'nul_in_extracted_text','page':number,'note':'Possible missing glyph or character mapping; inspect visible text and compilation diagnostics.'})
                        box=fitz.Rect(span['bbox']);bounds=page.rect+(-.5,-.5,.5,.5)
                        if not bounds.contains(box):warnings.append({'code':'font_bbox_outside_page','page':number,'text':span['text'],'bbox':list(box),'note':'Font metrics can exceed visible ink; inspect the actual page before declaring clipping.'})
            pages.append({'page':number,'width_mm':page.rect.width*25.4/72,'height_mm':page.rect.height*25.4/72,'text_spans':spans,'min_text_size_pt':min(sizes) if sizes else None,'max_text_size_pt':max(sizes) if sizes else None})
    if not fonts:warnings.append({'code':'no_text_fonts','note':'May be rasterized or outlined; text legibility and extraction require inspection.'})
    for font in fonts.values():
        if not font['embedded']:errors.append('unembedded font: '+font['name'])
    log_record={'status':'not_supplied','compilation_verified':False}
    if log is not None:
        log=Path(log);content=log.read_text(errors='replace');diagnostics=[]
        for line in content.splitlines():
            if re.search(r'undefined (references|citations)|(?:Reference|Citation).*undefined|Missing character:|^! |Fatal error',line,re.I):
                diagnostics.append(line);errors.append('TeX diagnostic: '+line)
            elif re.search(r'(Overfull|Underfull) \\[hv]box|Rerun to get cross-references right',line):
                warnings.append({'code':'tex_layout_warning','text':line})
        log_record={'status':'inspected','path':str(log),'sha256':sha256(log),'diagnostics':diagnostics,'compilation_verified':False,'note':'A log does not prove it belongs to this PDF; retain source, command, exit status and hashes in a separate compile record.'}
    return {'passed':not errors,'scope':'PDF/log mechanical inspection only','pdf':str(pdf),'pdf_sha256':sha256(pdf),'errors':errors,'warnings':warnings,'pages':pages,'fonts':list(fonts.values()),'log':log_record,'visual_review':'required','limitations':['Font sizes are reported after placement; readability depends on actual glyphs and context.','No scientific, semantic, reference-support, float-order or complete clipping certification.','No claim of TeX compilation without a separately recorded successful command.']}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('pdf',type=Path);p.add_argument('--log',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    report=inspect_layout(a.pdf,a.log)
    if a.output:write_json(a.output,report)
    import json
    print(json.dumps(report,indent=2,ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)

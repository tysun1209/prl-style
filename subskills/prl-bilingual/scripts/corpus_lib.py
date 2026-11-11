"""Corpus provenance and conservative selection. No network or writes on import."""
from __future__ import annotations

import calendar
import hashlib
import html
import json
import re
from datetime import date
from pathlib import Path

import pymupdf as fitz


def load_jsonl(path):
    path = Path(path)
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []


def write_json(path, data):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + '\n')
    temp.replace(path)


def write_jsonl(path, rows):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(''.join(json.dumps(r, ensure_ascii=False, sort_keys=True)+'\n' for r in rows))
    temp.replace(path)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def clean_text(text):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', text))).strip()


def classify_title(title):
    title = clean_text(title)
    if re.search(r'(^reply\b|\breply\s*:?$)', title, re.I): return 'Reply'
    for kind in ['Comment', 'Erratum', 'Editorial', 'Publisher Correction', 'Retraction', 'Addendum', 'Obituary', 'In Memoriam', 'Essay']:
        if re.match(r'^'+kind+r'\b', title, re.I): return kind
    return 'Letter_candidate'


def date_interval(item):
    parts = (item.get('published', {}).get('date-parts') or [[]])[0]
    if not parts: return None
    try:
        y = int(parts[0]); m = int(parts[1]) if len(parts)>1 else None
        if len(parts)>2:
            d = date(y,m,int(parts[2])); return d,d,'day'
        if m: return date(y,m,1), date(y,m,calendar.monthrange(y,m)[1]), 'month'
        return date(y,1,1),date(y,12,31),'year'
    except (TypeError, ValueError): return None


def select_articles(items, start_date, end_date, limit=None):
    start, end = date.fromisoformat(start_date), date.fromisoformat(end_date)
    if start>end: raise ValueError('start_date is after end_date')
    if limit is not None and limit<0: raise ValueError('negative limit')
    found = {}
    for item in items:
        doi = item.get('DOI', '').strip().lower()
        title_raw = (item.get('title') or [''])[0]
        interval = date_interval(item)
        journals = item.get('container-title', [])
        if not doi or item.get('type')!='journal-article' or classify_title(title_raw)!='Letter_candidate': continue
        if journals and not any(clean_text(j).lower()=='physical review letters' for j in journals): continue
        if interval is None or interval[0]<start or interval[1]>end: continue
        lo, hi, precision = interval
        found.setdefault(doi, {
            'article_id':doi, 'doi':doi, 'title':clean_text(title_raw), 'title_raw':title_raw,
            'year':lo.year, 'published_date':lo.isoformat() if precision=='day' else None,
            'date_interval':[lo.isoformat(),hi.isoformat()], 'date_precision':precision,
            'volume':item.get('volume'), 'issue':item.get('issue'), 'article_number':item.get('article-number'),
            'article_type':'Letter_candidate', 'article_type_evidence':'Crossref journal + title exclusion; requires PDF review',
            'source_url':f'https://doi.org/{doi}', 'discovery_source':'Crossref',
            'authors':[clean_text(' '.join([a.get('given',''),a.get('family','')])) for a in item.get('author',[])],
        })
    rows = sorted(found.values(), key=lambda r:(r['date_interval'][0],r['doi']))
    return rows if limit is None else rows[:limit]


def safe_relative(path, root):
    return str(Path(path).resolve().relative_to(Path(root).resolve()))


def resolve_asset(root, value):
    p = Path(value)
    if p.is_absolute(): raise ValueError('absolute corpus asset path')
    path = Path(root)/p
    safe_relative(path, root)
    return path


def locate_figure(page, figure_number):
    """Return a geometry-based candidate, never a claim of reviewed correctness."""
    blocks = page.get_text('blocks')
    caption_blocks = []
    for b in blocks:
        if b[6] != 0: continue
        m = re.match(r'^(?:FIG\.?|Figure)\s*(\d+)\s*[.:]', clean_text(b[4]), re.I)
        if m: caption_blocks.append((int(m.group(1)),b))
    matched = [b for number,b in caption_blocks if number==figure_number]
    if not matched: return None, ['caption_not_found']
    caption = matched[0]; cap = fitz.Rect(caption[:4]); mid=page.rect.width/2
    if cap.x0<mid-30 and cap.x1>mid+30:
        left,right=40,page.rect.width-40
    elif cap.x0<mid: left,right=40,mid-3
    else: left,right=mid+3,page.rect.width-40
    floor=42.0
    for b in blocks:
        rect=fitz.Rect(b[:4]); text=clean_text(b[4]) if b[6]==0 else ''
        if rect.y1>=cap.y0-1 or rect.x0>=right or rect.x1<=left: continue
        # Body paragraphs and preceding captions bound the region above this caption.
        if len(text)>130 and len(b[4].splitlines())>=3:
            floor=max(floor,rect.y1+1)
    region=fitz.Rect(left,floor,right,cap.y0-1)
    geometry=[]
    for info in page.get_image_info():
        r=fitz.Rect(info['bbox'])
        if r.width>25 and r.height>15 and r.intersects(region) and r.y1<=cap.y0+1:
            geometry.append(r & region)
    for drawing in page.get_drawings():
        r=fitz.Rect(drawing['rect'])
        # Ignore full-page rules and link underlines; include thin plot paths.
        if r.y0<42 or r.y1>cap.y0+1 or not r.intersects(region): continue
        if r.width>page.rect.width*.8 and r.height<2: continue
        if max(r.width,r.height)<3: continue
        r=fitz.Rect(r.x0-.2,r.y0-.2,r.x1+.2,r.y1+.2) & region
        if not r.is_empty: geometry.append(r)
    if not geometry: return None,['no_graphics_geometry']
    box=fitz.Rect(geometry[0])
    for r in geometry[1:]: box |= r
    # Include nearby axis/panel text, without adjoining body or the caption.
    for b in blocks:
        if b[6]!=0: continue
        r=fitz.Rect(b[:4]); text=clean_text(b[4])
        if r.y0>=cap.y0-1 or r.y1<floor or r.x1<left or r.x0>right: continue
        if len(text)>130 and len(b[4].splitlines())>=3: continue
        nearby=fitz.Rect(box.x0-22,box.y0-16,box.x1+22,min(cap.y0-1,box.y1+22))
        if r.intersects(nearby): box |= (r & region)
    box=fitz.Rect(max(left,box.x0-2),max(floor,box.y0-2),min(right,box.x1+2),min(cap.y0-1,box.y1+2))
    warnings=[]
    if box.height<30 or box.width<50: warnings.append('small_geometry_candidate')
    if cap.y0-box.y1>35: warnings.append('large_caption_gap')
    return [round(v,3) for v in box], warnings


def validate_records(root, articles, figures):
    errors=[]; warnings=[]; ids=[a['article_id'] for a in articles]
    if len(ids)!=len(set(ids)): errors.append('duplicate article IDs')
    fids=[f['figure_id'] for f in figures]
    if len(fids)!=len(set(fids)): errors.append('duplicate figure IDs')
    for f in figures:
        fid=f['figure_id']
        if f['article_id'] not in ids: errors.append(fid+': orphan article')
        try:
            asset=resolve_asset(root,f['image_path'])
            if not asset.exists(): errors.append(fid+': missing asset')
            elif f.get('image_sha256') and sha256(asset)!=f['image_sha256']: errors.append(fid+': image hash mismatch')
        except (ValueError,KeyError): errors.append(fid+': invalid relative asset path')
        if f.get('review_status')=='accepted' and f.get('annotation_status')!='reviewed': errors.append(fid+': accepted without annotation review')
        if f.get('review_status')!='accepted': warnings.append(fid+': excluded from style statistics pending review')
    return {'passed':not errors,'errors':errors,'warnings':warnings,'counts':{'articles':len(articles),'figures':len(figures),'accepted_figures':sum(f.get('review_status')=='accepted' for f in figures)}}

#!/usr/bin/env python3
"""Measure figure geometry; explicitly separate mechanical and perceptual checks."""
import argparse
import json
from pathlib import Path
import numpy as np
import pymupdf as fitz
from matplotlib.text import Text
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties,findfont
from corpus_lib import write_json


def cap_height_mm(prop):
    fp=FontProperties(fname=findfont(prop),size=prop.get_size_in_points())
    return TextPath((0,0),'H',prop=fp).get_extents().height*25.4/72


def inspect_artists(fig):
    fig.canvas.draw();renderer=fig.canvas.get_renderer();errors=[];warnings=[];heights=[]
    width,height=fig.get_size_inches()*fig.dpi
    for text in fig.findobj(match=Text):
        if not text.get_visible() or not text.get_text().strip():continue
        # Tick Text objects outside active axis limits are not drawn by Matplotlib.
        if text.axes is not None and text in [tick.label1 for axis in [text.axes.xaxis,text.axes.yaxis] for tick in axis.get_major_ticks()]:
            pass
        bb=text.get_window_extent(renderer)
        # Ignore tick labels Matplotlib has positioned beyond the axes limits.
        is_tick=False;outside_tick=False
        for ax in fig.axes:
            for axis in [ax.xaxis,ax.yaxis]+([ax.zaxis] if hasattr(ax,'zaxis') else []):
                lo,hi=sorted(axis.get_view_interval())
                for tick in axis.get_major_ticks()+axis.get_minor_ticks():
                    if text in [tick.label1,tick.label2]:
                        is_tick=True;outside_tick=tick.get_loc()<lo-1e-10 or tick.get_loc()>hi+1e-10
        if outside_tick:continue
        if min(bb.x0,bb.y0)<-1 or bb.x1>width+1 or bb.y1>height+1:
            errors.append({'code':'text_outside_figure','text':text.get_text(),'bbox_px':[round(v,2) for v in bb.extents]})
        mm=float(cap_height_mm(text.get_fontproperties()));heights.append(mm)
        if mm<1.98:errors.append({'code':'small_lettering','text':text.get_text(),'capital_height_mm':round(mm,3)})
        if '$' in text.get_text():warnings.append({'code':'math_glyph_review','text':text.get_text(),'reason':'base-font capital measurement does not certify scripts or individual math glyphs'})
    for line in fig.findobj(match=Line2D):
        if not line.get_visible():continue
        if line.get_linestyle() not in ['None','none','',None] and line.get_linewidth()<.5:
            errors.append({'code':'thin_line','width_pt':line.get_linewidth()})
        marker=line.get_marker()
        if marker in ['|','_'] and line.get_markeredgewidth()<.5:
            errors.append({'code':'thin_errorbar_cap','width_pt':line.get_markeredgewidth()})
        # Tick markers (integer IDs) and annotation strokes are not data points.
        if isinstance(marker,str) and marker not in ['None','none','', ' ', '|','_'] and line.get_markersize()*25.4/72<.99:
            errors.append({'code':'small_data_marker','diameter_mm':line.get_markersize()*25.4/72})
    # Matplotlib stores error-bar stems (and many contours) in collections, not Line2D.
    for collection in fig.findobj(match=LineCollection):
        if not collection.get_visible() or not len(collection.get_segments()):continue
        for width_pt in collection.get_linewidths():
            if width_pt<.5:errors.append({'code':'thin_line_collection','width_pt':float(width_pt)})
    return {'errors':errors,'warnings':warnings,'base_capital_height_min_mm':min(heights) if heights else None,
      'limits':['Does not prove semantic correctness, label-data separation or color-vision accessibility.','Scatter area, rasters, custom transforms and math scripts require separate visual inspection.']}


def inspect_pdf(path):
    with fitz.open(path) as doc:
        if len(doc)!=1:raise ValueError('expected a single-page figure PDF')
        page=doc[0];fonts=[]
        for font in page.get_fonts(full=True):
            xref=font[0]
            content=doc.extract_font(xref)[3] if xref else b''
            fonts.append({'name':font[3],'type':font[2],'embedded':bool(content)})
        widths=[float(d['width']) for d in page.get_drawings() if d.get('type') in ['s','fs'] and d.get('width',0)>0]
        return {'width_mm':page.rect.width*25.4/72,'height_mm':page.rect.height*25.4/72,
           'fonts':fonts,'fonts_embedded':all(f['embedded'] for f in fonts),'vector_stroke_min_pt':min(widths) if widths else None,
           'embedded_rasters':len(page.get_images()),'text_spans':sum(len(l['spans']) for b in page.get_text('dict')['blocks'] if b['type']==0 for l in b['lines']),
           'compliance_status':'measurements_only; scene/caption/scientific review still required'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('pdf',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();r=inspect_pdf(a.pdf)
    if a.output:write_json(a.output,r)
    print(json.dumps(r,indent=2))

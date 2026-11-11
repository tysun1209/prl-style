#!/usr/bin/env python3
"""Reproducible local style and fixed-size scientific figure exports."""
from contextlib import contextmanager
import csv
import json
import platform
import warnings
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler
import numpy as np
from PIL import Image
from corpus_lib import write_json,sha256
from typography import resolve_font,check_figure_fonts

ROOT=Path(__file__).resolve().parents[1]
DEFAULTS=json.loads((ROOT/'profiles/figure-defaults.json').read_text())

@contextmanager
def figure_context(profile=None, width_mm=None):
    profile=profile or DEFAULTS['default_font_profile']
    if profile not in DEFAULTS['font_profiles']:raise ValueError('profile must be times, sans or serif')
    font=DEFAULTS['font_profiles'][profile]
    resolve_font(font['family'])
    families=[font['family']]
    if font.get('cjk_family') and resolve_font(font['cjk_family'],required=False):
        families.append(font['cjk_family'])
    with mpl.rc_context(fname=ROOT/'assets/styles/prl.mplstyle'):
        mpl.rcParams.update({'font.family':families,'mathtext.fontset':font['mathtext'],
            'axes.prop_cycle':cycler(color=DEFAULTS['colors'])})
        yield


def new_figure(width_mm=85,height_mm=65,nrows=1,ncols=1,**kwargs):
    if not np.isfinite([width_mm,height_mm]).all() or min(width_mm,height_mm)<=0:raise ValueError('positive finite dimensions required')
    return plt.subplots(nrows,ncols,figsize=(width_mm/25.4,height_mm/25.4),layout='constrained',**kwargs)


def read_xy_csv(path):
    with Path(path).open(newline='') as stream:
        reader=csv.DictReader(stream)
        if not reader.fieldnames or not {'x','y'}<=set(reader.fieldnames):raise ValueError('CSV requires x and y columns')
        has_err='yerr' in reader.fieldnames
        rows=[]
        for i,row in enumerate(reader,2):
            try:
                values=[float(row[k]) for k in ['x','y']+(['yerr'] if has_err else [])]
            except (ValueError,TypeError,KeyError) as exc:raise ValueError(f'invalid numeric data at CSV line {i}') from exc
            if not np.isfinite(values).all():raise ValueError(f'non-finite data at CSV line {i}; no rows were removed')
            if has_err and values[2]<0:raise ValueError('uncertainty must be nonnegative')
            rows.append(values)
    if not rows:raise ValueError('empty data')
    return np.asarray(rows,dtype=float)


def export_figure(fig,output_stem,provenance,*,grayscale=False):
    """Export PDF, PNG and inspection JSON; grayscale preview requires explicit opt-in."""
    from inspect_figure import inspect_artists,inspect_pdf
    from quantity_audit import collect_labels
    font_paths=check_figure_fonts(fig)
    stem=Path(output_stem);stem.parent.mkdir(parents=True,exist_ok=True)
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter('always')
        # Equal-aspect axes with a colorbar can need several layout passes.
        # Inspect the settled geometry, rather than the first transient draw.
        previous=None
        for _ in range(8):
            fig.canvas.draw()
            positions=np.array([ax.get_position().bounds for ax in fig.axes])
            if previous is not None and np.allclose(positions,previous,rtol=0,atol=1e-6):
                break
            previous=positions
        artist_report=inspect_artists(fig)
        fig.savefig(stem.with_suffix('.pdf'),bbox_inches=None,metadata={'Creator':'prl-style','CreationDate':None,'ModDate':None})
        fig.savefig(stem.with_suffix('.png'),dpi=600,bbox_inches=None)
    if grayscale:
        with Image.open(stem.with_suffix('.png')) as im:
            im.convert('L').save(stem.with_name(stem.name+'-gray').with_suffix('.png'))
    pdf_report=inspect_pdf(stem.with_suffix('.pdf'))
    if pdf_report['vector_stroke_min_pt'] is not None and pdf_report['vector_stroke_min_pt']<.499:
        artist_report['warnings'].append({'code':'thin_pdf_stroke_requires_review','width_pt':pdf_report['vector_stroke_min_pt'],'reason':'PDF stroke has no semantic role; inspect whether it is a curve, error bar, decorative detail, or transform artifact.'})
    messages=[str(w.message) for w in captured]
    glyph_errors=[m for m in messages if 'Glyph' in m and 'missing' in m]
    report={'passed':not artist_report['errors'] and not glyph_errors and pdf_report['fonts_embedded'],
      'artist_inspection':artist_report,'pdf_inspection':pdf_report,'render_warnings':messages,
      'labels':collect_labels(fig),'label_inventory_scope':'visible axis/title/legend/annotation text, including inset axes; tick values excluded',
      'provenance':provenance,'python':platform.python_version(),'matplotlib':mpl.__version__,
      'numpy':np.__version__,'pdf_sha256':sha256(stem.with_suffix('.pdf')),
      'requested_font_files':font_paths,
      'font_defaults_sha256':sha256(ROOT/'profiles/figure-defaults.json'),
      'style_sha256':sha256(ROOT/'assets/styles/prl.mplstyle'),
      'semantic_review':'required: meaningful comparison, axes, uncertainty definition and caption'+('; grayscale interpretation for the requested preview' if grayscale else ''),
      'visual_review_status':'pending'}
    write_json(stem.with_suffix('.json'),report)
    return report

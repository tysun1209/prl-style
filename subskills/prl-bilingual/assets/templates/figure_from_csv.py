#!/usr/bin/env python3
"""Plot an existing x,y[,yerr] CSV with explicit labels and no data transformation."""
import argparse
import sys
from pathlib import Path

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('csv',type=Path);p.add_argument('--output',required=True,type=Path)
p.add_argument('--xlabel',required=True);p.add_argument('--ylabel',required=True)
p.add_argument('--uncertainty-description');p.add_argument('--width-mm',type=float,default=85);p.add_argument('--height-mm',type=float,default=65)
p.add_argument('--font',choices=['times','sans','serif'],default='times',help='Default: Times New Roman for Latin/digits and SimSun for Chinese')
p.add_argument('--palette',default=None,help='Categorical palette ID from the PRL color library')
p.add_argument('--grayscale',action='store_true',help='Also export a grayscale PNG preview when explicitly requested')
p.add_argument('--formats',nargs='+',help='Image formats: png (default), pdf, eps, svg, jpg, tiff')
p.add_argument('--dpi',type=float,help='Raster resolution; default 600 dpi')
p.add_argument('--skill-root',type=Path,default=Path(__file__).resolve().parents[2])
a=p.parse_args();sys.path.insert(0,str(a.skill_root/'scripts'))
import matplotlib
matplotlib.use('Agg')
from prl_figure import figure_context,new_figure,read_xy_csv,export_figure
from corpus_lib import sha256
values=read_xy_csv(a.csv)
if values.shape[1]==3 and not a.uncertainty_description:p.error('yerr needs --uncertainty-description stating what the bars represent')
family='uncertainty_bars' if values.shape[1]==3 else 'scatter'
with figure_context(a.font,palette_id=a.palette,family=family,objects=['samples']) as palette_info:
    fig,ax=new_figure(a.width_mm,a.height_mm)
    if values.shape[1]==3:ax.errorbar(values[:,0],values[:,1],yerr=values[:,2],fmt='o',capsize=2,elinewidth=.65)
    else:ax.plot(values[:,0],values[:,1],'o',ms=4)
    ax.set(xlabel=a.xlabel,ylabel=a.ylabel)
    r=export_figure(fig,a.output,{'input_path':str(a.csv),'input_sha256':sha256(a.csv),'rows':len(values),'data_transformations':[], 'uncertainty':a.uncertainty_description,'palette':palette_info},grayscale=a.grayscale,formats=a.formats,dpi=a.dpi)
print('mechanical inspection:',r['passed'],'; scientific and visual review still required')
raise SystemExit(0 if r['passed'] else 1)

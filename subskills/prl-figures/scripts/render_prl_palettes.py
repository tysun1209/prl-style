#!/usr/bin/env python3
"""Render the source-linked swatchbook and original synthetic usage examples."""
from pathlib import Path
import argparse
from contextlib import ExitStack
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
from matplotlib.colors import BoundaryNorm, Normalize, TwoSlopeNorm
import numpy as np

from prl_palette import load_catalog, colormap, categorical
from prl_figure import figure_context, new_figure, export_figure, resolve_export_options, SUPPORTED_FORMATS
from corpus_lib import write_json, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'reports/prl-colors-2025-2026'


def atlas_pages(rows, per_page=12):
    """Keep full pages, balancing the tail to avoid a nearly empty last page."""
    pages = [rows[i:i+per_page] for i in range(0, len(rows), per_page)]
    if len(pages) > 1 and len(pages[-1]) < per_page // 2:
        tail_count = min(3, len(pages))
        tail = [row for page in pages[-tail_count:] for row in page]
        size, extra = divmod(len(tail), tail_count)
        balanced, offset = [], 0
        for i in range(tail_count):
            count = size + (i < extra)
            balanced.append(tail[offset:offset+count])
            offset += count
        pages[-tail_count:] = balanced
    return pages


def render_atlas(out=OUT, *, formats=None, dpi=None):
    formats,dpi=resolve_export_options(formats,dpi)
    out=Path(out)
    catalog = load_catalog()
    rows = catalog['palettes']
    pages = atlas_pages(rows)
    years = [s['published_date'][:4] for p in rows for s in p['sources']]
    period = f'{min(years)}–{max(years)}'
    out.mkdir(parents=True,exist_ok=True)
    with figure_context(), ExitStack() as stack:
        pdf=stack.enter_context(PdfPages(out/'palette-atlas.pdf',metadata={'Title':f'PRL {period}: {len(rows)} source-backed color palettes'})) if 'pdf' in formats else None
        for number, page in enumerate(pages, 1):
            fig,axes = plt.subplots(4,3,figsize=(11.7,8.3))
            fig.subplots_adjust(left=.045,right=.985,bottom=.04,top=.91,hspace=.42,wspace=.18)
            fig.suptitle(f'PRL {period} | Color atlas | {len(rows)} palettes | {number}/{len(pages)}',fontsize=18,x=.045,ha='left')
            for ax,p in zip(axes.flat,page):
                ax.set_axis_off();ax.set_xlim(0,1);ax.set_ylim(0,1)
                ax.text(0,.94,f"{p['id']}   {p['kind']}",fontsize=12,weight='bold')
                if p['kind']=='categorical':
                    for i,c in enumerate(p['colors']):
                        ax.add_patch(Rectangle((i/len(p['colors']),.43),1/len(p['colors']),.36,facecolor=c,edgecolor='none'))
                    text = '  '.join(p['colors'][:4])+'\n'+'  '.join(p['colors'][4:])
                else:
                    ax.imshow(np.linspace(0,1,512)[None,:],extent=(0,1,.43,.79),cmap=colormap(p['id']),aspect='auto',interpolation='nearest')
                    text = f"{p['colors'][0]}  ->  {p['colors'][-1]} | {p['interpolation']}"
                ax.text(0,.31,text,fontsize=8,va='top',linespacing=1.3)
                s=p['sources'][0]
                ax.text(0,.04,f"{s['doi']} | Fig. {s['figure_number']}",fontsize=8,url=s['source_url'])
            for ax in list(axes.flat)[len(page):]: ax.set_axis_off()
            if pdf is not None:pdf.savefig(fig,dpi=dpi)
            for fmt in formats:
                if fmt!='pdf':fig.savefig(out/f"atlas-{number:02d}.{fmt}",format=fmt,dpi=dpi,bbox_inches=None)
            plt.close(fig)
    report = {'catalog_sha256': sha256(ROOT/'profiles/prl-color-palettes.json'),
              'palettes': len(rows), 'formats': formats, 'dpi': dpi,
              'pages': [{'page': i, 'palette_ids': [p['id'] for p in page]}
                        for i, page in enumerate(pages, 1)],
              'pdf_pages': len(pages) if 'pdf' in formats else 0}
    if pdf is not None:
        report['pdf_sha256'] = sha256(out/'palette-atlas.pdf')
    write_json(out/'atlas-manifest.json', report)
    return report


def render(out=OUT,*,formats=None,dpi=None):
    formats,dpi=resolve_export_options(formats,dpi)
    out=Path(out)
    atlas = render_atlas(out, formats=formats, dpi=dpi)
    rows = load_catalog()['palettes']
    selected = {p['name_zh']:p for p in rows}
    names=['玫红—钢蓝—芥黄','蓝—浅蓝—绿—橙—紫五相','深紫—蓝绿—黄强度',
           '深蓝—白—深红功','紫—中性浅色—浅绿十阶','亮蓝—紫—玫红输入']
    ps=[selected[n] for n in names]
    x=np.linspace(0,1,150);xx,yy=np.meshgrid(x,x)
    with figure_context():
        fig,axs=new_figure(width_mm=185,height_mm=128,nrows=2,ncols=3)
        ax=axs[0,0]
        for i,c in enumerate(categorical(ps[0]['id'])):
            y=np.exp(-((x-.25-.2*i)/.17)**2)*(1-.12*i)
            ax.plot(x,y,color=c,label=str(i+1),marker=['o','s','^'][i],markevery=20,ms=3.5)
            ax.fill_between(x,y-.045,y+.045,color=c,alpha=.18,linewidth=0)
        ax.legend(fontsize=9,loc='upper center',ncol=3,handlelength=1,
            handletextpad=.3,columnspacing=.8,borderpad=.2)
        ax.set(xlabel='x',ylabel='Response',ylim=(-.08,1.25))
        from matplotlib.colors import ListedColormap
        phase=np.minimum(4,(xx*3+yy*2).astype(int))
        axs[0,1].imshow(phase,origin='lower',extent=(0,1,0,1),aspect='auto',
            cmap=ListedColormap(categorical(ps[1]['id'])),norm=BoundaryNorm(np.arange(6)-.5,5))
        axs[0,1].contour(xx,yy,phase,levels=np.arange(4)+.5,colors='black',linewidths=.55)
        axs[0,1].set(xlabel='Control A',ylabel='Control B')
        z=np.exp(-((xx-.55)**2+(yy-.4)**2)/.055)
        im=axs[0,2].imshow(z,origin='lower',extent=(0,1,0,1),aspect='auto',cmap=colormap(ps[2]['id']),vmin=0,vmax=1)
        fig.colorbar(im,ax=axs[0,2],pad=.03,label='Intensity',ticks=[0,.5,1]);axs[0,2].set(xlabel='x',ylabel='y')
        signed=np.sin(2*np.pi*xx)*np.cos(2*np.pi*yy)
        im=axs[1,0].imshow(signed,origin='lower',extent=(0,1,0,1),aspect='auto',cmap=colormap(ps[3]['id']),norm=TwoSlopeNorm(vcenter=0,vmin=-1,vmax=1))
        fig.colorbar(im,ax=axs[1,0],pad=.03,label='Signed field',ticks=[-1,0,1]);axs[1,0].set(xlabel='x',ylabel='y')
        cmap=colormap(ps[4]['id']);edges=ps[4]['bin_edges_normalized']
        im=axs[1,1].imshow(xx*yy,origin='lower',extent=(0,1,0,1),aspect='auto',cmap=cmap,norm=BoundaryNorm(edges,cmap.N))
        fig.colorbar(im,ax=axs[1,1],pad=.03,label='Probability',ticks=[0,.5,1]);axs[1,1].set(xlabel='x',ylabel='y')
        cmap=colormap(ps[5]['id'])
        for s in np.linspace(0,1,9): axs[1,2].plot(x,np.exp(-((x-.25-.4*s)/.16)**2),color=cmap(s))
        fig.colorbar(plt.cm.ScalarMappable(norm=Normalize(0,1),cmap=cmap),ax=axs[1,2],pad=.03,label='s',ticks=[0,.5,1])
        axs[1,2].set(xlabel='x',ylabel='Response')
        for i,ax in enumerate(axs.flat):ax.set_title(f'({chr(97+i)})',loc='left')
        report=export_figure(fig,out/'usage-examples',{'data_kind':'synthetic_demonstration',
             'palette_ids':[p['id'] for p in ps], 'purpose':'Exercise color selection and mapping; not scientific evidence'},formats=formats,dpi=dpi)
        plt.close(fig)
    (out/'usage-examples-caption.md').write_text('配色调用示例，全部数据为合成演示。(a) 三组曲线与同色误差带；(b) 五类相区及黑色边界；(c) 正值强度场；(d) 以零为中心的有符号场；(e) 十级概率分箱；(f) 按连续参数着色的曲线族。配色来源见图册及 JSON；这些示例不表示论文原始研究结果。\n',encoding='utf-8')
    write_json(out/'render-manifest.json',{'catalog_sha256':sha256(ROOT/'profiles/prl-color-palettes.json'),
        'formats':formats,'dpi':dpi,'pdf_pages':atlas['pdf_pages'],'example_report_passed':report['passed'],
        'example_palette_ids':[p['id'] for p in ps], 'data_kind':'synthetic_demonstration'})
    print(json.dumps({'pages':len(atlas['pages']),'example_passed':report['passed']}))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=OUT)
    parser.add_argument('--formats',nargs='+',choices=SUPPORTED_FORMATS,help='Image formats; default: png only; pdf adds the atlas PDF')
    parser.add_argument('--dpi',type=float,help='Raster resolution; default: 600')
    parser.add_argument('--atlas-only',action='store_true',help='Render the complete color atlas without regenerating usage examples')
    args=parser.parse_args()
    if args.atlas_only:
        print(json.dumps(render_atlas(args.output,formats=args.formats,dpi=args.dpi)))
    else:
        render(args.output,formats=args.formats,dpi=args.dpi)

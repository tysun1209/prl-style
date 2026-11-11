#!/usr/bin/env python3
"""Generate original, explicitly synthetic regression/demo figures in seven roles."""
import argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,FancyArrowPatch
from prl_figure import default_colormap,figure_context,new_figure,export_figure,DEFAULTS
from corpus_lib import write_json


def render_gallery(out):
    out.mkdir(parents=True,exist_ok=True);reports=[];colors=DEFAULTS['colors']
    def finish(fig,name,caption,role):
        report=export_figure(fig,out/name,{'data_kind':'synthetic_demonstration','seed':20261015,'role':role,'caption':caption,'scientific_claim':'None; original layout example, not a research result.'})
        (out/(name+'.caption.txt')).write_text('SYNTHETIC DEMONSTRATION. '+caption+'\n')
        reports.append({'name':name,'passed':report['passed'],'errors':report['artist_inspection']['errors']});plt.close(fig)
    with figure_context():
        x=np.linspace(0,5,13)
        fig,ax=new_figure(85,67)
        for k in range(2):
            y=np.exp(-x/(1+k*.7));err=.025+0*x
            ax.errorbar(x,y,yerr=err,fmt=['o','s'][k],ms=4,color=colors[k],capsize=2,elinewidth=.65,label=['Series A','Series B'][k])
            xx=np.linspace(0,5,200);ax.plot(xx,np.exp(-xx/(1+k*.7)),['-','--'][k],color=colors[k])
        ax.set(xlabel='Time (s)',ylabel='Response (a.u.)');ax.legend(loc='upper right',handlelength=1.4)
        finish(fig,'01-trend','Points show two synthetic series; bars indicate fixed illustrative deviations of 0.025 a.u.; solid and dashed curves are the generating functions.','trend_uncertainty')
        fig,axes=new_figure(178,70,ncols=2)
        for n,color,marker,ms in zip([20,40,80],colors,DEFAULTS['markers'],[6,4.5,3]):
            xx=np.geomspace(.1,10,16); yy=n**.3*xx**.6
            axes[0].loglog(xx,yy,marker=marker,color=color,label=f'Size {n}')
            axes[1].loglog(xx,yy/n**.3,marker=marker,color=color,ls='none',mfc='none',ms=ms)
        axes[0].set(xlabel='Control (a.u.)',ylabel='Response (a.u.)');axes[0].legend()
        axes[1].set(xlabel='Control (a.u.)',ylabel='Scaled response (a.u.)')
        for ax,label in zip(axes,['(a)','(b)']):ax.text(.04,.96,label,va='top',transform=ax.transAxes)
        finish(fig,'02-scaling','(a) Three explicitly generated power-law series. (b) The same values divided by the known generating size factor. This example demonstrates layout only and is not evidence of a scaling law.','scaling')
        fig,ax=new_figure(85,72)
        x=np.linspace(-2,2,101);X,Y=np.meshgrid(x,x);Z=np.tanh(X-.5*Y)
        im=ax.pcolormesh(X,Y,Z,cmap=default_colormap('diverging'),vmin=-1,vmax=1,rasterized=True,shading='auto')
        ax.plot(.5*x,x,'k--',lw=1);ax.text(-1.6,1.2,'A',color='white',weight='bold');ax.text(1,-1.5,'B',color='white',weight='bold')
        ax.set(xlabel='Control 1 (a.u.)',ylabel='Control 2 (a.u.)');cb=fig.colorbar(im,ax=ax);cb.set_label('Order (a.u.)')
        finish(fig,'03-phase-map','Illustrative signed field with a fixed zero-centered scale. The dashed line denotes its analytic zero contour; A and B identify sides independently of color.','phase_map')
        fig,ax=new_figure(85,67)
        x=np.linspace(-3,3,300)
        ax.plot(x,np.exp(-x*x/2)/np.sqrt(2*np.pi),color=colors[0],label='Reference')
        ax.plot(x,np.exp(-abs(x))/2,color=colors[1],ls='--',label='Comparison')
        ax.set(xlabel='Position (a.u.)',ylabel='Density (a.u.)');ax.legend()
        finish(fig,'04-distribution','Two analytical demonstration densities, distinguished by both line style and color. Neither curve is a fit to measured data.','distribution')
        fig,axes=new_figure(178,78,ncols=2)
        x=np.linspace(-2,2,70);X,Y=np.meshgrid(x,x);Z=np.exp(-((X-.6)**2+(Y+.2)**2))
        im=axes[0].imshow(Z,extent=(-2,2,-2,2),origin='lower',cmap=default_colormap('sequential'),vmin=0,vmax=1)
        t=np.linspace(0,5,180);axes[1].plot(np.cos(t)*np.exp(-t/4),np.sin(t)*np.exp(-t/4),color=colors[0]);axes[1].plot([1],[0],'o',color=colors[0]);axes[1].plot([np.cos(5)*np.exp(-1.25)],[np.sin(5)*np.exp(-1.25)],'s',color=colors[1])
        axes[1].set_aspect('equal');axes[1].set(xlim=(-2,2),ylim=(-2,2))
        for ax,label in zip(axes,['(a)','(b)']):ax.set(xlabel='x (mm)',ylabel='y (mm)');ax.text(.03,.97,label,transform=ax.transAxes,va='top',color='white' if ax is axes[0] else 'black')
        fig.colorbar(im,ax=axes[0],label='Intensity (a.u.)',shrink=.8)
        finish(fig,'05-spatial-trajectory','(a) Synthetic spatial field with a fixed intensity scale. (b) Independent demonstration trajectory; circle and square mark its start and end. Coordinates use a common spatial scale.','spatial_trajectory')
        fig,axes=new_figure(178,119,nrows=2,ncols=2)
        x=np.linspace(0,4,12)
        for i,ax in enumerate(axes.flat):
            for j in range(2):ax.plot(x,(1+.2*i)*np.exp(-x/(1+j*.8)),marker=['o','s'][j],ms=4,ls=['-','--'][j],color=colors[j],label=['A','B'][j])
            ax.set(xlabel='Time (s)',ylabel='Response (a.u.)');ax.text(.05,.09,f'({chr(97+i)})',transform=ax.transAxes,va='bottom')
        axes[0,1].legend()
        finish(fig,'06-multipanel','Panels (a)–(d) compare the same two synthetic series at four illustrative amplitudes. Color, markers and line styles retain their meaning across panels.','multipanel')
    with figure_context():
        fig,ax=new_figure(85,45);ax.set(xlim=(0,3),ylim=(.15,1.85));ax.axis('off')
        for xy,name,color in [((.5,1),'A',colors[0]),((2.5,1),'B',colors[1])]:
            ax.add_patch(Circle(xy,.28,facecolor='white',edgecolor=color,lw=1.2));ax.text(*xy,name,ha='center',va='center',fontsize=12)
        ax.add_patch(FancyArrowPatch((.85,1.1),(2.15,1.1),arrowstyle='->',mutation_scale=12,lw=1.1,color='black'))
        ax.add_patch(FancyArrowPatch((2.15,.9),(.85,.9),arrowstyle='->',mutation_scale=12,lw=1.1,linestyle='--',color='black'))
        ax.text(1.5,1.4,'Forward',ha='center');ax.text(1.5,.5,'Reverse',ha='center')
        finish(fig,'07-schematic','Original two-state schematic. Solid and dashed arrows identify opposite transitions; no transition rates or physical equivalence are asserted.','schematic')
    write_json(out/'gallery-report.json',{'passed':all(r['passed'] for r in reports),'figures':reports,'visual_review':'pending'})
    return reports


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=Path('reports/gallery'));a=p.parse_args();r=render_gallery(a.output)
    for item in r:print(item)
    raise SystemExit(0 if all(x['passed'] for x in r) else 1)

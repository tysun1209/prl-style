"""Comparison and scaling recipes; no fitted scientific result is asserted."""
import numpy as np
from .common import Example,single,labels,panel,C
from prl_figure import new_figure

NAMES={'line_comparison','scatter','uncertainty_bars','uncertainty_band','residuals','parity','parameter_sweep','log_scaling','finite_size_collapse'}

def build(name,rng):
    x=np.linspace(0,4,16);reference=np.exp(-x);observed=reference+.035*np.sin(3*x)
    if name=='residuals':
        fig,axs=new_figure(110,105,nrows=2)
        axs[0].plot(x,reference,label='Reference',color=C[0]);axs[0].plot(x,observed,'s',label='Samples',color=C[1],ms=4)
        axs[0].legend();labels(axs[0]);panel(axs[0],'(a)')
        difference=observed-reference;axs[1].axhline(0,color='0.5',lw=.6);axs[1].plot(x,difference,'o-',ms=4,color=C[1]);labels(axs[1],y='Sample − reference (a.u.)');panel(axs[1],'(b)')
        return Example(fig,'(a) Constructed samples and an analytic reference. (b) Sample minus reference; this discrepancy was imposed, not inferred from an independent experiment.',dict(x=x,observed=observed,reference=reference,residual=difference),['residual = observed - reference'])
    if name=='finite_size_collapse':
        fig,axs=new_figure(178,76,ncols=2);sizes=np.array([16.,32.,64.]);base=np.geomspace(.15,6,25);raw=[]
        for i,n in enumerate(sizes):
            y=n**.25*np.exp(-base);raw.append(y);xx=base*n**.5
            axs[0].plot(xx,y,marker=['o','s','^'][i],ms=4,label=f'N = {n:g}',color=C[i]);axs[1].plot(xx/n**.5,y/n**.25,marker=['o','s','^'][i],ms=[6,4.8,3.6][i],mfc='none',ls=['-','--',':'][i],color=C[i])
        axs[0].legend();labels(axs[0],x='Control (a.u.)');labels(axs[1],x='Scaled control',y='Scaled response')
        for ax,l in zip(axs,['(a)','(b)']):panel(ax,l)
        return Example(fig,'(a) Curves constructed with known size factors. (b) Control divided by N to power 0.5 and response divided by N to power 0.25. Collapse is imposed by construction and is not evidence for a fitted exponent or universality.',dict(sizes=sizes,scaled_x=base,raw_x=sizes[:,None]**.5*base,raw_y=np.array(raw)),['known generating scale factors; no optimization'])
    fig,ax=single()
    if name=='line_comparison':
        ax.plot(x,reference,'o-',ms=4,label='A',color=C[0]);ax.plot(x,np.exp(-x/1.6),'s--',ms=4,label='B',color=C[1]);ax.legend();labels(ax)
        return Example(fig,'Two analytic response curves sampled at the same control values. Lines join the specified samples; no fit or measurement is implied.',dict(x=x,a=reference,b=np.exp(-x/1.6)))
    if name=='scatter':
        a=rng.normal(size=90);b=.6*a+rng.normal(scale=.5,size=90);ax.scatter(a,b,s=22,c=C[0],alpha=.8,edgecolors='none');labels(ax,'Observable A (a.u.)','Observable B (a.u.)')
        return Example(fig,'Ninety constructed paired samples. Association is built into the generator and does not demonstrate a causal mechanism.',dict(x=a,y=b))
    if name=='uncertainty_bars':
        lower=.03+.01*x;upper=.05+.01*x;ax.errorbar(x,observed,yerr=np.stack([lower,upper]),fmt='o',ms=4,capsize=2,elinewidth=.7,color=C[0]);labels(ax)
        return Example(fig,'Constructed samples with asymmetric illustrative extents. Bars are neither estimated standard deviations nor confidence intervals.',dict(x=x,y=observed,yerr_lower=lower,yerr_upper=upper))
    if name=='uncertainty_band':
        lo=reference-.04;hi=reference+.04;ax.fill_between(x,lo,hi,color=C[0],alpha=.2,label='Given range');ax.plot(x,reference,color=C[0],label='Central curve');ax.legend();labels(ax)
        return Example(fig,'Analytic curve with an imposed pointwise range of ±0.04 a.u. The shaded range has no assigned statistical coverage.',dict(x=x,y=reference,lower=lo,upper=hi))
    if name=='parity':
        a=np.linspace(.1,1,30);b=a+rng.normal(0,.035,len(a));ax.scatter(a,b,s=22,color=C[0]);ax.plot([0,1.1],[0,1.1],'--',color='0.35',label='Identity');ax.set(xlim=(0,1.1),ylim=(0,1.1));ax.set_aspect('equal');ax.legend();labels(ax,'Given value (a.u.)','Constructed prediction (a.u.)')
        return Example(fig,'Given values and constructed predictions. Dashed line is exact identity, not a fitted regression.',dict(observed=a,predicted=b))
    if name=='parameter_sweep':
        from matplotlib.colors import Normalize
        from matplotlib.cm import ScalarMappable
        params=np.linspace(.7,1.7,6);cmap=__import__('matplotlib').colormaps['viridis'];norm=Normalize(params.min(),params.max())
        for p in params:ax.plot(x,np.exp(-x/p),color=cmap(norm(p)))
        fig.colorbar(ScalarMappable(norm=norm,cmap=cmap),ax=ax,label='Decay scale (a.u.)');labels(ax)
        return Example(fig,'Analytic responses for six ordered decay scales. Color encodes a continuous parameter, not six unordered phases.',dict(x=x,parameters=params,y=np.exp(-x[None,:]/params[:,None])))
    if name=='log_scaling':
        xx=np.geomspace(.1,10,20);yy=xx**1.4;ax.loglog(xx,yy,'o',ms=4,color=C[0],label='Samples');ax.loglog(xx,xx**1.4,'--',color=C[1],label='Generating power');labels(ax);ax.legend()
        return Example(fig,'Samples of a specified power with exponent 1.4. The straight log-log appearance is imposed and does not establish a power law in measured data.',dict(x=xx,y=yy))
    raise ValueError(name)

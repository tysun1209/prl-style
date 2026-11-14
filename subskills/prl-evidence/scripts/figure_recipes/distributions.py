"""Distribution summaries with explicit normalization and estimator choices."""
import numpy as np
from .common import Example,single,labels,panel
from prl_figure import default_colormap,new_figure
NAMES={'histogram','ecdf','box_violin','joint_density','survival','polar'}

def build(name,rng,*,colors):
    C=colors
    samples=rng.normal(size=400)
    if name=='box_violin':
        fig,axs=new_figure(178,78,ncols=2);groups=[rng.normal(i*.35, .65, size=80) for i in range(3)]
        boxes=axs[0].boxplot(groups,whis=1.5,patch_artist=True,flierprops={'marker':'o','markersize':3.2},boxprops={'linewidth':.8},medianprops={'linewidth':1,'color':'0.15'},whiskerprops={'linewidth':.8},capprops={'linewidth':.8})
        violins=axs[1].violinplot(groups,showmeans=False,showmedians=True,bw_method=.3)
        for patch,body,color in zip(boxes['boxes'],violins['bodies'],C):
            patch.set(facecolor=color,edgecolor='0.25')
            body.set(facecolor=color,edgecolor='0.25',alpha=1,linewidth=.8)
        for key in ['cmedians','cbars','cmins','cmaxes']:violins[key].set_color('0.25')
        for ax,l in zip(axs,['(a)','(b)']):ax.set_xticks([1,2,3],['A','B','C']);labels(ax,'Group','Value (a.u.)');panel(ax,l)
        return Example(fig,'Three constructed groups, 80 samples each. (a) Median, quartiles, and whiskers reaching the most extreme samples within 1.5 IQR; points beyond are retained. (b) Gaussian-kernel violin estimates with bandwidth factor 0.3; horizontal central marks show medians, and vertical lines with end caps span each full sample minimum–maximum range.',dict(samples=np.array(groups)),['quartiles; 1.5 IQR whisker rule','Gaussian kernel with bandwidth factor 0.3; full sample min–max extent'])
    if name=='polar':
        fig,ax=new_figure(100,90,subplot_kw={'projection':'polar'});theta=np.linspace(0,2*np.pi,181);radius=1+.4*np.cos(2*theta);ax.plot(theta,radius,color=C[0]);ax.set_theta_zero_location('E');ax.set_theta_direction(1);ax.set_yticks([.5,1,1.5]);ax.set_title('Response (a.u.)',pad=18)
        return Example(fig,'Analytic angular response. Angle increases counterclockwise from the right; radius encodes response, not enclosed probability.',dict(theta_rad=theta,radius=radius))
    fig,ax=single(height=76)
    if name=='histogram':
        edges=np.linspace(min(-3.5,np.floor(samples.min())),max(3.5,np.ceil(samples.max())),15);counts,_,_=ax.hist(samples,bins=edges,density=False,color=C[0],edgecolor='white',linewidth=.6);labels(ax,'Value (a.u.)','Samples per bin')
        return Example(fig,'Four hundred synthetic normal samples binned with explicit edges covering all observations. Vertical values are counts; no samples are omitted.',dict(samples=samples,edges=edges,counts=counts),['14 bins covering the full sample range; no smoothing'])
    if name in ['ecdf','survival']:
        xx=np.unique(samples);cdf=np.searchsorted(np.sort(samples),xx,side='right')/len(samples);yy=cdf if name=='ecdf' else 1-cdf
        ax.step(xx,yy,where='post',color=C[0]);ax.set_ylim(0,1.03);labels(ax,'Value (a.u.)','Fraction ≤ value' if name=='ecdf' else 'Fraction > value')
        return Example(fig,'Empirical '+('cumulative distribution' if name=='ecdf' else 'strict upper-tail fraction')+' of 400 uncensored synthetic samples. Repeated values use their full multiplicity; no parametric distribution is fitted.',dict(samples=samples,x=xx,fraction=yy),['empirical rank with right-inclusive cumulative counts'])
    if name=='joint_density':
        a=rng.normal(size=1500);b=.5*a+rng.normal(size=1500)*.7;h= ax.hist2d(a,b,bins=24,cmap=default_colormap('sequential'));fig.colorbar(h[3],ax=ax,label='Samples per bin');labels(ax,'Observable A (a.u.)','Observable B (a.u.)')
        return Example(fig,'Two-dimensional counts for 1500 synthetic paired samples on 24 bins per coordinate. Color represents counts per rectangular bin, not a probability density.',dict(x=a,y=b,counts=h[0],xedges=h[1],yedges=h[2]),['24 rectangular bins per coordinate; no smoothing'])
    raise ValueError(name)

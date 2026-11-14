"""Spectra, structures and layouts with explicit scientific roles."""
import numpy as np
from matplotlib.patches import Circle,FancyArrowPatch
from .common import Example,single,labels,panel
from prl_figure import new_figure
NAMES={'spectrum','dispersion','energy_levels','network','schematic','inset_zoom','multipanel','wide_narrow'}

def build(name,rng,*,colors):
    C=colors
    if name in ['multipanel','wide_narrow']:
        if name=='multipanel':fig,axes=new_figure(178,130,nrows=2,ncols=2);axs=list(axes.flat)
        else:
            import matplotlib.pyplot as plt
            fig=plt.figure(figsize=(178/25.4,128/25.4),layout='constrained');grid=fig.add_gridspec(2,2);axs=[fig.add_subplot(grid[0,:]),fig.add_subplot(grid[1,0]),fig.add_subplot(grid[1,1])]
        x=np.linspace(0,4,20)
        for i,ax in enumerate(axs):
            for j in range(2):ax.plot(x,np.exp(-x/(1+j*.5))*(1+.2*i),marker=['o','s'][j],ms=4,ls=['-','--'][j],color=C[j],label=['A','B'][j])
            labels(ax,'Time (s)','Response (a.u.)');panel(ax,f'({chr(97+i)})')
        axs[0].legend()
        return Example(fig,'Constructed comparisons with consistent series encodings. Each panel retains its own readable numerical axes'+('; the upper full-width axis is not supplied by either narrower lower panel.' if name=='wide_narrow' else '.'),dict(time=x,amplitudes=1+.2*np.arange(len(axs))))
    fig,ax=single(width=110 if name in ['inset_zoom','energy_levels'] else 85,height=78)
    if name=='spectrum':
        x=np.linspace(0,8,400);y=1/(1+((x-2)/.25)**2)+.55/(1+((x-5)/.4)**2);ax.plot(x,y,color=C[0]);labels(ax,'Frequency (a.u.)','Response (a.u.)')
        return Example(fig,'Sum of two specified Lorentzian profiles with centers 2 and 5 a.u. Widths are generator parameters, not measured instrumental resolution or inferred lifetimes.',dict(frequency=x,response=y))
    if name=='dispersion':
        k=np.linspace(-1,1,200);a=np.sqrt(k*k+.12**2)
        ax.plot(k,a,color=C[0]);ax.plot(k,-a,'--',color=C[1]);ax.axhline(0,color='0.5',lw=.6);labels(ax,'Wave vector (a.u.)','Energy (a.u.)')
        return Example(fig,'Two analytic branches along a declared one-dimensional wave-vector coordinate. Zero is the chosen energy reference; the gap is imposed and no topological conclusion is asserted.',dict(k=k,upper=a,lower=-a))
    if name=='energy_levels':
        levels=np.array([0.,1.,1.8]);ax.set(xlim=(0,3),ylim=(-.25,2.2));ax.set_xticks([]);ax.set_ylabel('Energy (a.u.)')
        for i,e in enumerate(levels):ax.hlines(e,.6,2.3,color=C[i],lw=1);ax.text(2.4,e,f'{i}',va='center')
        ax.add_patch(FancyArrowPatch((1,0),(1,1),arrowstyle='->',mutation_scale=13,lw=1,color=C[0]));ax.add_patch(FancyArrowPatch((1.8,1),(1.8,1.8),arrowstyle='->',mutation_scale=13,lw=1,color=C[1]))
        return Example(fig,'Three assigned levels with two indicated transitions. Arrow widths carry no rate or strength information, and no selection rule is inferred.',dict(energies=levels,transitions=np.array([[0,1],[1,2]])))
    if name=='network':
        theta=np.arange(8)*2*np.pi/8;pos=np.column_stack([np.cos(theta),np.sin(theta)]);edges=np.array([(i,(i+1)%8) for i in range(8)]+[(0,4),(1,5)])
        for a,b in edges:ax.plot(pos[[a,b],0],pos[[a,b],1],color='0.55',lw=.8,zorder=1)
        ax.scatter(pos[:,0],pos[:,1],s=85,color=C[0],zorder=2)
        for i,(x,y) in enumerate(pos):ax.text(x*1.22,y*1.22,str(i+1),ha='center',va='center')
        ax.set(xlim=(-1.5,1.5),ylim=(-1.5,1.5));ax.set_aspect('equal');ax.axis('off')
        return Example(fig,'An undirected unweighted eight-node graph. Circular node placement is a layout choice and does not encode physical distance.',dict(positions=pos,edges=edges))
    if name=='schematic':
        ax.set(xlim=(0,3),ylim=(0,2));ax.axis('off')
        for x,l,c in [(.5,'A',C[0]),(2.5,'B',C[1])]:ax.add_patch(Circle((x,1),.3,fc='white',ec=c,lw=1.2));ax.text(x,1,l,ha='center',va='center')
        ax.add_patch(FancyArrowPatch((.9,1.1),(2.1,1.1),arrowstyle='->',mutation_scale=13,lw=1));ax.add_patch(FancyArrowPatch((2.1,.9),(.9,.9),arrowstyle='->',mutation_scale=13,lw=1,linestyle='--'));ax.text(1.5,1.5,'Forward',ha='center');ax.text(1.5,.5,'Reverse',ha='center')
        return Example(fig,'Original conceptual two-state diagram. Solid and dashed arrows denote forward and reverse relations; no rate, scale or experimentally established mechanism is encoded.',dict(state_positions=np.array([[.5,1],[2.5,1]])))
    if name=='inset_zoom':
        x=np.linspace(0,6,240);base=np.exp(-x);other=base+.025*np.exp(-(x-3)**2/.15)
        ax.plot(x,base,color=C[0],label='A');ax.plot(x,other,'--',color=C[1],label='B');labels(ax,'Time (s)','Response (a.u.)');ax.legend(loc='upper right')
        inset=ax.inset_axes([.48,.38,.48,.32]);inset.plot(x,base,color=C[0]);inset.plot(x,other,'--',color=C[1]);inset.set(xlim=(2.6,3.4),ylim=(.025,.085));inset.set_xticks([2.6,3.4]);inset.set_yticks([.03,.08]);ax.indicate_inset_zoom(inset,edgecolor='0.5',linewidth=.7)
        return Example(fig,'Full analytic curves and an inset of the same axes over 2.6–3.4 s and 0.025–0.085 a.u. The small difference is prescribed; no statistical significance is claimed.',dict(time=x,a=base,b=other,inset_bounds=np.array([2.6,3.4,.025,.085])))
    raise ValueError(name)

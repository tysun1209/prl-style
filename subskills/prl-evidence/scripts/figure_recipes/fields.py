"""Maps, fields and trajectories with explicit coordinates and encodings."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap,BoundaryNorm
from .common import Example,single,labels,C
from prl_figure import default_colormap
NAMES={'phase_discrete','phase_continuous','heatmap','contours','correlation_matrix','image_scalebar','vector_field','streamlines','space_time','trajectory','phase_portrait','surface_3d','raster_events'}

def build(name,rng):
    x=np.linspace(-2,2,51);X,Y=np.meshgrid(x,x);Z=np.sin(X)*np.cos(Y)
    if name=='surface_3d':
        fig=plt.figure(figsize=(140/25.4,105/25.4),layout='constrained');ax=fig.add_subplot(projection='3d');ax.plot_surface(X,Y,Z,cmap=default_colormap('sequential'),linewidth=0,rasterized=True);ax.set(xlabel='x (a.u.)',ylabel='y (a.u.)',zlabel='Field (a.u.)');ax.view_init(elev=28,azim=-55)
        return Example(fig,'Perspective of a prescribed scalar field. Height and color encode the same field; inspect a map or alternate view if occlusion hides a decisive feature.',dict(x=x,y=x,field=Z))
    fig,ax=single(width=100 if name in ['vector_field','streamlines','correlation_matrix'] else 85,height=80)
    if name in ['phase_discrete','phase_continuous','heatmap']:
        if name=='phase_discrete':
            z=np.where(X<-.5,0,np.where(Y>X,1,2));cmap=ListedColormap(C[:3]);im=ax.pcolormesh(X,Y,z,cmap=cmap,norm=BoundaryNorm([-.5,.5,1.5,2.5],3),shading='nearest',rasterized=True);cb=fig.colorbar(im,ax=ax,ticks=[0,1,2]);cb.ax.set_yticklabels(['A','B','C']);cb.set_label('Assigned class');caption='Three classes assigned by explicit coordinate inequalities on a fixed grid. These labels illustrate categorical display, not a measured phase boundary.'
        else:
            z=np.tanh(X-.4*Y) if name=='phase_continuous' else Z;im=ax.pcolormesh(X,Y,z,cmap=default_colormap('diverging'),vmin=-1,vmax=1,shading='nearest',rasterized=True);fig.colorbar(im,ax=ax,label='Diagnostic (a.u.)' if name=='phase_continuous' else 'Field (a.u.)');caption='Prescribed continuous '+('diagnostic' if name=='phase_continuous' else 'scalar field')+' with zero-centered normalization. A color transition alone is not evidence of a phase transition.'
        labels(ax,'Control 1 (a.u.)','Control 2 (a.u.)');return Example(fig,caption,dict(x=x,y=x,values=z))
    if name=='contours':
        levels=np.array([-.8,-.4,0,.4,.8]);cs=ax.contour(X,Y,Z,levels=levels,colors=C[0],linewidths=.8);ax.clabel(cs,inline=True,fontsize=9.5,manual=[(-1.3,.55),(-.5,.55),(0,.8),(.5,-.55),(1.3,-.55)]);labels(ax,'x (a.u.)','y (a.u.)');ax.set_aspect('equal')
        return Example(fig,'Labeled contours of a prescribed scalar field at −0.8, −0.4, 0, 0.4 and 0.8 a.u. The contours interpolate a grid, not additional measurements.',dict(x=x,y=x,field=Z,levels=levels),['Matplotlib contour interpolation on the stated grid'])
    if name=='correlation_matrix':
        values=rng.normal(size=(150,4));values[:,1]=.6*values[:,0]+.8*values[:,1];matrix=np.corrcoef(values,rowvar=False);im=ax.imshow(matrix,vmin=-1,vmax=1,cmap=default_colormap('diverging'));fig.colorbar(im,ax=ax,label='Pearson correlation');ax.set_xticks(range(4),list('ABCD'));ax.set_yticks(range(4),list('ABCD'));labels(ax,'Variable','Variable')
        return Example(fig,'Pearson correlations of four synthetic variables across 150 samples. Colors describe estimates, not significance tests or causal relations.',dict(samples=values,correlation=matrix),['Pearson sample correlation'])
    if name=='image_scalebar':
        half_pixel=(x[1]-x[0])/2
        z=np.exp(-((X-.5)**2+(Y+.3)**2));ax.imshow(z,extent=(x[0]-half_pixel,x[-1]+half_pixel,x[0]-half_pixel,x[-1]+half_pixel),origin='lower',cmap=default_colormap('sequential'),vmin=0,vmax=1);ax.plot([-1.65,-.65],[-1.55,-1.55],color='white',lw=2,solid_capstyle='butt');ax.text(-1.15,-1.35,'1 mm',color='white',ha='center');labels(ax,'x (mm)','y (mm)');caption='Synthetic image with assigned spatial calibration. Saved coordinates locate pixel centers, with outer edges half a pixel beyond. White bar spans exactly 1 mm in the declared coordinates; no experimental microscopy or measured calibration is implied.'
        return Example(fig,caption,dict(x_mm=x,y_mm=x,intensity=z,scale_bar_mm=np.array([1.])))
    if name in ['vector_field','streamlines']:
        xx=np.linspace(-2,2,13);xxg,yyg=np.meshgrid(xx,xx);u=-yyg;v=xxg
        if name=='vector_field':
            q=ax.quiver(xxg,yyg,u,v,angles='xy',scale_units='xy',scale=7,color=C[0]);ax.set(xlim=(-2.35,2.35),ylim=(-2.35,2.75));ax.quiverkey(q,.68,.93,1,'1 a.u.',labelpos='E',coordinates='axes')
        else:ax.streamplot(xx,xx,u,v,color=np.hypot(u,v),cmap=default_colormap('sequential'),density=.8,linewidth=.8,arrowsize=.9)
        ax.set_aspect('equal');labels(ax,'x (a.u.)','y (a.u.)')
        caption='Prescribed rotation field. '+('Arrows use a scale of 7 vector units per coordinate unit; the reference arrow denotes magnitude 1.' if name=='vector_field' else 'Streamlines are interpolated from the instantaneous field, not particle trajectories; color shows vector magnitude in arbitrary units.')
        if name=='streamlines':
            from matplotlib.cm import ScalarMappable
            from matplotlib.colors import Normalize
            fig.colorbar(ScalarMappable(norm=Normalize(np.hypot(u,v).min(),np.hypot(u,v).max()),cmap=default_colormap('sequential')),ax=ax,label='Magnitude (a.u.)')
        return Example(fig,caption,dict(x=xx,y=xx,u=u,v=v))
    if name=='space_time':
        time=np.linspace(0,4,61);pos=np.linspace(-2,2,51);z=np.sin(2*pos[:,None]-3*time[None,:]);im=ax.pcolormesh(time,pos,z,cmap=default_colormap('diverging'),vmin=-1,vmax=1,shading='nearest',rasterized=True);fig.colorbar(im,ax=ax,label='Field (a.u.)');labels(ax,'Time (s)','Position (mm)')
        return Example(fig,'Prescribed traveling field on a regular time–position grid. Color normalization is fixed; propagation is a property of the generator.',dict(time_s=time,position_mm=pos,field=z))
    if name in ['trajectory','phase_portrait']:
        time=np.linspace(0,10,250);a=np.cos(time)*np.exp(-time/7);b=np.sin(time)*np.exp(-time/7);ax.plot(a,b,color=C[0]);ax.plot(a[0],b[0],'o',ms=5,color=C[1],label='Start');ax.plot(a[-1],b[-1],'s',ms=5,color=C[2],label='End');ax.set_aspect('equal');ax.legend();labels(ax,'x (mm)' if name=='trajectory' else 'State 1 (a.u.)','y (mm)' if name=='trajectory' else 'State 2 (a.u.)')
        return Example(fig,'One constructed '+('spatial path' if name=='trajectory' else 'state-space orbit')+' with time-ordered samples and marked endpoints. No ensemble or general stability claim follows from this example.',dict(time=time,x=a,y=b))
    if name=='raster_events':
        events=[np.sort(rng.uniform(0,5,size=8+i)) for i in range(6)];ax.eventplot(events,colors=C[0],linewidths=.8,linelengths=.6);labels(ax,'Time (s)','Realization');ax.set_yticks(range(6),range(1,7));ax.set_xlim(0,5)
        return Example(fig,'Synthetic events in six independent illustrative realizations over a common 5 s window. Rows identify realizations, and event counts differ by construction.',dict(**{f'events_{i+1}':e for i,e in enumerate(events)}))
    raise ValueError(name)

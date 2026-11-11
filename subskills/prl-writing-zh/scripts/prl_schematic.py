"""Editable scientific-diagram primitives in final-size millimetres.

This helper validates declared topology and simple geometry, not scientific
truth. Use arbitrary Matplotlib primitives for the physical model itself.
"""
from dataclasses import dataclass
import math

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
from matplotlib.path import Path
import numpy as np


def canvas(width_mm=178, height_mm=70):
    if not np.isfinite([width_mm,height_mm]).all() or min(width_mm,height_mm)<=0:
        raise ValueError('Canvas dimensions must be positive and finite')
    return plt.figure(figsize=(width_mm/25.4,height_mm/25.4),layout=None)


def panel(fig, bounds_mm, tag=None):
    """Add an axis-free panel; coordinates and bounds are in physical mm."""
    x,y,w,h=map(float,bounds_mm)
    fw,fh=fig.get_size_inches()*25.4
    if not np.isfinite([x,y,w,h]).all() or min(x,y)<0 or min(w,h)<=0 or x+w>fw+.001 or y+h>fh+.001:
        raise ValueError('Panel must fit inside the canvas')
    ax=fig.add_axes([x/fw,y/fh,w/fw,h/fh],xlim=(0,w),ylim=(0,h),aspect='equal')
    ax.set_axis_off()
    if tag:ax.text(1,h-1,tag,ha='left',va='top',fontsize=10.5)
    return ax


@dataclass
class Node:
    id: str
    xy: tuple
    size: tuple
    patch: object
    text: object

    def port(self, side):
        if side not in {'N','E','S','W'}:raise ValueError('Port must be N, E, S or W')
        dx,dy={'N':(0,.5),'E':(.5,0),'S':(0,-.5),'W':(-.5,0)}[side]
        return self.xy[0]+dx*self.size[0],self.xy[1]+dy*self.size[1]

    def bounds(self, inset=0):
        x,y=self.xy;w,h=self.size
        return x-w/2+inset,y-h/2+inset,x+w/2-inset,y+h/2-inset


def _crosses_box(a,b,box):
    """Liang–Barsky clipping, used for straight routed segments."""
    x0,y0,x1,y1=box;dx=b[0]-a[0];dy=b[1]-a[1];lo,hi=0.,1.
    for p,q in [(-dx,a[0]-x0),(dx,x1-a[0]),(-dy,a[1]-y0),(dy,y1-a[1])]:
        if abs(p)<1e-12:
            if q<0:return False
        elif p<0:lo=max(lo,q/p)
        else:hi=min(hi,q/p)
        if lo>hi:return False
    return True


class Diagram:
    def __init__(self, ax):
        self.ax=ax;self.nodes={};self.relations=[]

    def node(self, ident, label, xy, size=(24,12), *, color='black', fill='white', shape='box'):
        if not ident or ident in self.nodes:raise ValueError('Node IDs must be nonempty and unique')
        if len(xy)!=2 or len(size)!=2 or not np.isfinite([*xy,*size]).all() or min(size)<=0:
            raise ValueError('Node geometry must be finite with positive size')
        x,y=xy;w,h=size
        if shape=='circle':
            if not math.isclose(w,h):raise ValueError('Circle width and height must agree')
            patch=Circle((x,y),w/2,facecolor=fill,edgecolor=color,lw=1.)
        elif shape=='box':patch=Rectangle((x-w/2,y-h/2),w,h,facecolor=fill,edgecolor=color,lw=1.)
        else:raise ValueError('Node shape must be box or circle')
        self.ax.add_patch(patch)
        text=self.ax.text(x,y,label,ha='center',va='center',fontsize=10,color='black')
        self.nodes[ident]=Node(ident,tuple(xy),tuple(size),patch,text)
        return self.nodes[ident]

    def arrow(self, start, end, *, meaning, via=(), label=None, label_xy=None,
              color='black', linestyle='-', arrowstyle='-|>'):
        if not isinstance(meaning,str) or not meaning.strip():raise ValueError('Declare what each arrow means')
        points=[tuple(start),*[tuple(p) for p in via],tuple(end)]
        if any(len(p)!=2 for p in points) or not np.isfinite(points).all():raise ValueError('Arrow coordinates must be finite pairs')
        if any(np.linalg.norm(np.subtract(a,b))<1e-8 for a,b in zip(points,points[1:])):
            raise ValueError('Arrow segments must have nonzero length')
        path=Path(points,[Path.MOVETO]+[Path.LINETO]*(len(points)-1))
        patch=FancyArrowPatch(path=path,arrowstyle=arrowstyle,mutation_scale=9,lw=1.1,
                              color=color,linestyle=linestyle,capstyle='round',joinstyle='round',zorder=2)
        self.ax.add_patch(patch)
        if label:
            if label_xy is None:
                lengths=np.linalg.norm(np.diff(points,axis=0),axis=1);distance=lengths.sum()/2
                for a,b,length in zip(points,points[1:],lengths):
                    if distance<=length:
                        label_xy=np.asarray(a)+(np.asarray(b)-a)*distance/length;break
                    distance-=length
            self.ax.text(*label_xy,label,ha='center',va='center',fontsize=10,
                         bbox=dict(facecolor='white',edgecolor='none',pad=1.2),zorder=3)
        row=dict(meaning=meaning,points=points,color=color,linestyle=linestyle,label=label)
        self.relations.append(row)
        return row

    def edge(self, source, target, *, meaning, ports=('E','W'), **kwargs):
        if source not in self.nodes or target not in self.nodes:raise ValueError('Unknown source or target node')
        row=self.arrow(self.nodes[source].port(ports[0]),self.nodes[target].port(ports[1]),meaning=meaning,**kwargs)
        row.update(source=source,target=target,ports=list(ports))
        return row

    def inspect(self):
        self.ax.figure.canvas.draw();renderer=self.ax.figure.canvas.get_renderer();errors=[]
        for name,node in self.nodes.items():
            text=node.text.get_window_extent(renderer)
            # Rectangle test is conservative for circular nodes; visual review
            # additionally checks the actual circular boundary.
            bounds=self.ax.transData.transform([[*node.bounds()[:2]],[*node.bounds()[2:]]])
            if text.x0<bounds[0,0]+1 or text.y0<bounds[0,1]+1 or text.x1>bounds[1,0]-1 or text.y1>bounds[1,1]-1:
                errors.append(dict(code='node_label_overflow',node=name))
            if not self.ax.bbox.contains(*bounds[0]) or not self.ax.bbox.contains(*bounds[1]):
                errors.append(dict(code='node_outside_panel',node=name))
        for i,relation in enumerate(self.relations):
            for point in relation['points']:
                if not self.ax.bbox.contains(*self.ax.transData.transform(point)):
                    errors.append(dict(code='arrow_outside_panel',relation=i))
            for name,node in self.nodes.items():
                if name in (relation.get('source'),relation.get('target')):continue
                if any(_crosses_box(a,b,node.bounds(.3)) for a,b in zip(relation['points'],relation['points'][1:])):
                    errors.append(dict(code='arrow_crosses_unrelated_node',relation=i,node=name))
        texts=[t for t in self.ax.texts if t.get_visible() and t.get_text()]
        for i,a in enumerate(texts):
            for b in texts[i+1:]:
                if a.get_window_extent(renderer).overlaps(b.get_window_extent(renderer)):
                    errors.append(dict(code='label_overlap',labels=[a.get_text(),b.get_text()]))
        return dict(passed=not errors,errors=errors,nodes=[dict(id=n.id,xy=n.xy,size=n.size,label=n.text.get_text()) for n in self.nodes.values()],
                    relations=self.relations,limitations=['Declared topology is not scientific validation.','Custom shapes, arrow/text overlap, arrow crossings and curved decorations need visual inspection.'])

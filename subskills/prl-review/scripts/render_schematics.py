#!/usr/bin/env python3
"""Render original scientific Fig. 1 examples; adapt functions to supplied science."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Rectangle, ConnectionPatch
import numpy as np

from prl_figure import figure_context, export_figure, resolve_export_options
from prl_layout import style_ticks
from prl_schematic import canvas, panel, Diagram

EXAMPLES=('particle-model','apparatus','feedback','pipeline','protocol','hybrid')


def particle_model(colors):
    fig=canvas(178,70)
    left=Diagram(panel(fig,(4,4,81,62),'(a)'))
    right=Diagram(panel(fig,(93,4,81,62),'(b)'))
    positions=np.array([[18,22],[35,36],[54,25],[67,39],[22,40],[42,20]])
    angles=np.array([.4,2.2,np.arctan2(12,20),3.3,-1.0,1.1])
    for y in [11,48]:left.ax.plot([12,74],[y,y],color='0.35',lw=1.1)
    for i,((x,y),angle) in enumerate(zip(positions,angles)):
        c=colors[1] if i==2 else colors[0]
        left.ax.add_patch(Circle((x,y),2.3,facecolor=c,edgecolor=c,lw=.8))
        direction=np.array([np.cos(angle),np.sin(angle)])
        left.arrow(np.array([x,y])+direction*3,np.array([x,y])+direction*8,
                   meaning='prescribed propulsion direction of illustrative particle '+str(i+1),color=c)
    left.ax.text(42,54,'Active particles',ha='center',va='center',fontsize=10)
    left.arrow((8,11),(8,48),meaning='wall separation',arrowstyle='<->',label='H',label_xy=(8,29))
    right.ax.add_patch(Circle((36,28),9,facecolor=colors[1],alpha=.25,edgecolor='none'))
    right.ax.add_patch(Circle((36,28),9,fill=False,edgecolor=colors[1],lw=1.))
    right.arrow((36,28),(62,28),meaning='local horizontal reference direction',color='0.45',arrowstyle='->')
    right.arrow((36,28),(56,40),meaning='propulsion direction',color=colors[1])
    angle=np.degrees(np.arctan2(12,20))
    right.ax.add_patch(Arc((36,28),28,28,theta1=0,theta2=angle,lw=.8,color='0.3'))
    right.ax.text(52,32,r'$\theta$',fontsize=10,ha='center')
    right.ax.text(59,42,'v',fontsize=10,ha='center')
    right.arrow((36,28),(45,28),meaning='particle radius',color='0.2',arrowstyle='->')
    right.ax.text(40,23,'R',ha='center',fontsize=10)
    right.ax.text(43,54,'Local geometry',ha='center',va='center',fontsize=10)
    return fig,[left,right],dict(positions=positions.tolist(),angles_rad=angles.tolist()),(
        'Illustrative active particles confined between two parallel walls. '
        '(a) Short arrows indicate prescribed propulsion directions; H denotes the wall separation. '
        '(b) Enlarged definition of particle radius R and orientation angle theta relative to the horizontal direction. '
        'Colors and propulsion direction preserve the highlighted particle identity between panels. '
        'The positions are constructed for this demonstration; panel (b) enlarges the isolated particle definition and omits the walls.')


def apparatus(colors):
    fig=canvas(178,74)
    a=Diagram(panel(fig,(4,4,90,66),'(a)'))
    b=Diagram(panel(fig,(99,4,75,66),'(b)'))
    a.node('light','Light source',(17,34),(30,14),color=colors[0])
    # A chamber is a physical object, not another processing node.
    a.ax.add_patch(Rectangle((44,22),18,24,facecolor='0.96',edgecolor='0.3',lw=1.))
    a.ax.text(53,51,'Chamber',ha='center',fontsize=10)
    positions=[(50,28),(54,34),(50,40)]
    for x,y in positions:
        a.ax.add_patch(Circle((x,y),1.3,facecolor=colors[1],edgecolor=colors[1],lw=.8))
    a.arrow((32,34),(44,34),meaning='illumination direction',color=colors[0])
    a.arrow((62,34),(69,34),meaning='transmitted light reaches detector',color=colors[0])
    a.ax.add_patch(Rectangle((70,24),6,20,facecolor='0.93',edgecolor='0.3',lw=1.))
    a.ax.text(73,34,'D',ha='center',va='center',fontsize=10)
    for x in [14,50]:b.ax.plot([x,x],[10,58],lw=1.1,color='0.3')
    b.ax.text(36,63,'Sample detail',ha='center',fontsize=10)
    for x,y in positions:
        b.ax.add_patch(Circle((14+2*(x-44),10+2*(y-22)),2.6,facecolor=colors[1],edgecolor=colors[1],lw=.8))
    b.arrow((14,4),(50,4),meaning='chamber-width definition',arrowstyle='<->',label='W',label_xy=(32,4))
    # A pair of gray guide lines refers to a changed scale, not to a force or beam.
    for start,end in [((62,46),(14,58)),((62,22),(14,10))]:
        fig.add_artist(ConnectionPatch(start,end,'data','data',axesA=a.ax,axesB=b.ax,
                                      color='0.65',lw=.8,ls='--',clip_on=False))
    return fig,[a,b],dict(elements=['source','particle chamber','transmission detector'],particle_positions=positions,detail_scale=2,
                        meaning='illustrative transmission geometry; no actual device dimensions'),(
        'Illustrative transmission setup. (a) Light passes through a particle-containing chamber to detector D. '
        '(b) A uniformly enlarged sample detail defines the chamber width W and preserves particle positions. Colored arrows show light propagation; '
        'gray dashed guide lines indicate the detail view. Particle positions and device geometry are illustrative, '
        'and no numerical dimensions or measurement performance are implied.')


def pipeline(colors):
    fig=canvas(178,76);d=Diagram(panel(fig,(4,4,170,68)))
    for name,label,xy,size,c in [
        ('train','Training data',(23,48),(38,14),colors[0]),
        ('fit','Fit model',(78,48),(32,14),colors[0]),
        ('predict','Predict',(133,48),(32,14),colors[0]),
        ('test','Test inputs',(78,17),(32,14),colors[1]),
        ('truth','Test targets',(23,17),(38,14),colors[1]),
        ('compare','Compare',(133,17),(32,14),colors[1])]:
        d.node(name,label,xy,size,color=c)
    d.edge('train','fit',meaning='use only training data to estimate the model',color=colors[0])
    d.edge('fit','predict',meaning='use the fitted model for prediction',color=colors[0])
    d.edge('test','predict',meaning='supply held-out inputs without refitting',ports=('N','S'),
           via=[(78,33),(133,33)],color=colors[1],linestyle='--')
    d.edge('predict','compare',meaning='compare predictions against held-out targets',ports=('E','E'),
           via=[(161,48),(161,17)],color=colors[0])
    d.edge('truth','compare',meaning='supply held-out target values only to evaluation',ports=('S','S'),
           via=[(23,3),(133,3)],color=colors[1])
    return fig,[d],dict(training_uses=['Training data'],evaluation_uses=['Test inputs','Test targets']),(
        'Illustrative model-evaluation workflow. Training data determine the fitted model. '
        'Held-out inputs enter prediction through the dashed route; held-out target values enter only the comparison. '
        'No arrow from the comparison or test targets returns to fitting. The diagram specifies data flow, not a measured performance result.')


def feedback(colors):
    fig=canvas(178,75);d=Diagram(panel(fig,(5,5,168,65)))
    d.node('policy','Controller',(35,34),(42,21),color=colors[0])
    d.node('environment','Environment',(131,34),(42,21),color=colors[1])
    d.edge('policy','environment',meaning='controller applies an action to the environment',
           color=colors[0],label='Action',label_xy=(83,38))
    d.edge('environment','policy',meaning='environment supplies the next observation',ports=('N','N'),
           via=[(131,56),(35,56)],label='Observation',color='0.25')
    d.edge('environment','policy',meaning='environment supplies a reward to the controller',ports=('S','S'),
           via=[(131,11),(35,11)],label='Reward',color=colors[1],linestyle='--')
    return fig,[d],dict(protocol='Illustrative controller-environment interaction; no actor/critic architecture assumed.'),(
        'Illustrative closed-loop control. The controller sends an action to the environment; '
        'the environment returns an observation and a reward on distinct directed paths. '
        'The dashed path denotes reward, not uncertainty or an unobserved physical force. '
        'The controller architecture and update rule are not specified by this conceptual diagram.')


def protocol(colors):
    fig=canvas(178,68);d=Diagram(panel(fig,(4,4,170,60)))
    # A repeated two-particle state keeps object identities across operations.
    centers=[22,85,148];states=[(0,0),(0,np.pi/3),(np.pi/3,np.pi/3)]
    labels=['Initial state','Rotate B','Rotate A']
    for k,(cx,angles) in enumerate(zip(centers,states)):
        d.ax.text(cx,53,f'({chr(97+k)})',ha='center',va='center',fontsize=10.5)
        for j,angle in enumerate(angles):
            x=cx+(-7 if j==0 else 7);y=32;c=colors[j]
            d.ax.add_patch(Circle((x,y),4.2,facecolor=c,edgecolor=c,lw=.8,alpha=.2))
            d.ax.add_patch(Circle((x,y),4.2,fill=False,edgecolor=c,lw=.9))
            d.arrow((x,y),(x+8*np.cos(angle),y+8*np.sin(angle)),meaning=f'orientation of particle {"AB"[j]} in state {k}',color=c)
            d.ax.text(x,21,'AB'[j],ha='center',fontsize=10,color=c)
        d.ax.text(cx,9,labels[k],ha='center',va='center',fontsize=10)
    d.arrow((39,33),(65,33),meaning='apply rotation to particle B',label='B',label_xy=(52,40),color='0.2')
    d.arrow((102,33),(128,33),meaning='apply rotation to particle A',label='A',label_xy=(115,40),color='0.2')
    return fig,[d],dict(states_rad=states,operations=['rotate B by pi/3','rotate A by pi/3']),(
        'Illustrative two-step orientation protocol. (a) Both particles initially point to the right. '
        '(b) B rotates counterclockwise by 60 degrees while A retains its orientation. '
        '(c) A undergoes the same rotation while B remains fixed. Colored arrows indicate particle orientation; '
        'black interstage arrows indicate the order of operations. This is a prescribed sequence, not a simulated trajectory.')


def hybrid(colors):
    fig=canvas(178,78);d=Diagram(panel(fig,(4,7,73,64),'(a)'))
    # Physical two-state geometry on the left; an explicitly synthetic result on the right.
    d.node('A','A',(15,35),(13,13),shape='circle',color=colors[0])
    d.node('B','B',(57,35),(13,13),shape='circle',color=colors[1])
    d.edge('A','B',meaning='transition A to B at the supplied illustrative rate',ports=('N','N'),
           via=[(15,51),(57,51)],color=colors[0],label='k',label_xy=(36,51))
    d.ax.text(36,13,'Irreversible transition',ha='center',fontsize=10)
    # Dedicated physical box for a quantitative panel. Axis labels remain outside axes.
    ax=fig.add_axes([101/178,17/78,71/178,49/78])
    t=np.linspace(0,4,81);a=np.exp(-t);b=1-a
    ax.plot(t,a,color=colors[0],label='A',lw=1.2)
    ax.plot(t,b,color=colors[1],ls='--',label='B',lw=1.2)
    ax.set(xlim=(0,4),ylim=(0,1),xlabel='Time (1/k)',ylabel='Population')
    ax.set_xticks([0,1,2,3,4]);ax.set_yticks([0,.5,1]);style_ticks(ax)
    ax.legend(loc='center right',frameon=False)
    ax.text(.04,.95,'(b)',transform=ax.transAxes,ha='left',va='top',fontsize=10.5)
    return fig,[d],dict(time=t.tolist(),population_A=a.tolist(),population_B=b.tolist(),rate=1,
                        initial_populations=[1,0],data_origin='analytic demonstration'),(
        'Original schematic-plus-data demonstration. (a) Irreversible A-to-B transition with rate k. '
        '(b) Analytic populations for an initially pure A state, plotted against time in units of 1/k. '
        'A decays exponentially and B is its complement, so their sum remains one. '
        'The curves are constructed from this stated model and are not experimental or simulation measurements.')


def render(output, examples=EXAMPLES, *, formats=None, dpi=None, palette_id=None):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    formats,dpi=resolve_export_options(formats,dpi);rows=[]
    builders={'particle-model':particle_model,'apparatus':apparatus,'feedback':feedback,'pipeline':pipeline,'protocol':protocol,'hybrid':hybrid}
    for name in examples:
        if name not in builders:raise ValueError('Unknown example '+name)
        with figure_context(palette_id=palette_id) as palette:
            fig,diagrams,data,caption=builders[name](palette['colors'])
            checks=[d.inspect() for d in diagrams]
            c0,c1=palette['colors'][:2]
            mappings={
                'particle-model':{'ordinary particles and their propulsion':c0,'highlighted particle and its propulsion in both panels':c1},
                'apparatus':{'illumination and transmission':c0,'particles':c1,'detail guides':'0.65'},
                'feedback':{'controller and action':c0,'environment and reward':c1,'observation':'0.25'},
                'pipeline':{'training, model and prediction':c0,'held-out inputs, targets and comparison':c1},
                'protocol':{'particle A across all stages':c0,'particle B across all stages':c1},
                'hybrid':{'state A and population A':c0,'state B and population B':c1}}
            provenance=dict(kind='original illustrative schematic',example=name,palette=palette,
                            color_mapping=mappings[name],
                            schematic_checks=checks,source_data=data)
            try:
                report=export_figure(fig,output/name,provenance,formats=formats,dpi=dpi)
            finally:plt.close(fig)
            (output/(name+'-caption.txt')).write_text(caption+'\n')
            rows.append(dict(example=name,passed=report['passed'] and all(x['passed'] for x in checks),
                             artifacts=report['artifacts'],report=name+'.json',caption=name+'-caption.txt'))
    result=dict(passed=all(r['passed'] for r in rows),formats=formats,dpi=dpi,examples=rows,
                visual_review='Required on exported artifacts; not established by this runtime check.')
    (output/'schematics-report.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--all',action='store_true');group.add_argument('--example',choices=EXAMPLES)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--formats',nargs='+');parser.add_argument('--dpi',type=float)
    parser.add_argument('--palette',help='Categorical palette ID; default from figure profile')
    args=parser.parse_args()
    result=render(args.output,EXAMPLES if args.all else [args.example],formats=args.formats,dpi=args.dpi,palette_id=args.palette)
    print(json.dumps(result,indent=2));return 0 if result['passed'] else 1


if __name__=='__main__':raise SystemExit(main())

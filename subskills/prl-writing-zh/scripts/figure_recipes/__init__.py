"""Deterministic original examples for the registered scientific figure families."""
import numpy as np
from prl_figure import palette_context, choose_colors
from palette_selection import family_rule
from . import comparisons,distributions,fields,structures
MODULES=(comparisons,distributions,fields,structures)
# These identities describe the actual demo artists, not all possible datasets.
OBJECTS={
    'line_comparison':['A','B'], 'scatter':['samples'], 'uncertainty_bars':['samples'],
    'uncertainty_band':['mean and uncertainty'], 'residuals':['reference','samples and residual'],
    'parity':['samples'], 'log_scaling':['samples','generating relation'],
    'finite_size_collapse':['N=16','N=32','N=64'], 'histogram':['samples'],
    'ecdf':['samples'], 'survival':['samples'], 'box_violin':['A','B','C'],
    'polar':['angular response'], 'phase_discrete':['A','B','C'], 'contours':['isolines'],
    'vector_field':['vectors'], 'trajectory':['path','start','end'],
    'phase_portrait':['orbit','start','end'], 'raster_events':['events'],
    'multipanel':['A','B'], 'wide_narrow':['A','B'], 'spectrum':['spectrum'],
    'dispersion':['upper branch','lower branch'], 'energy_levels':['level 1','level 2','level 3'],
    'network':['nodes'], 'schematic':['state A','state B'], 'inset_zoom':['A','B']}

def build(family,seed=20261016):
    for module in MODULES:
        if family in module.NAMES:
            with palette_context(family) as plans:
                colors=[]
                if family in OBJECTS:
                    mark=family_rule(family)['mark']
                    if mark not in {'line','point','fill'}:mark='line'
                    if family=='schematic':mark='line'  # This legacy example uses unfilled circles.
                    colors=choose_colors(family, role='categorical', mark=mark,
                                         objects=OBJECTS[family])['colors']
                example=module.build(family,np.random.default_rng(seed),colors=colors)
                example.palettes=plans
                example.figure._prl_palette_plans=plans
                return example
    raise ValueError('unknown figure family: '+family)

def implemented():return set().union(*(m.NAMES for m in MODULES))

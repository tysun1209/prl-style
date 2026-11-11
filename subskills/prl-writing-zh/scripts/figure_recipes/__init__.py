"""Deterministic original examples for the registered scientific figure families."""
import numpy as np
from . import comparisons,distributions,fields,structures
MODULES=(comparisons,distributions,fields,structures)

def build(family,seed=20261016):
    for module in MODULES:
        if family in module.NAMES:return module.build(family,np.random.default_rng(seed))
    raise ValueError('unknown figure family: '+family)

def implemented():return set().union(*(m.NAMES for m in MODULES))

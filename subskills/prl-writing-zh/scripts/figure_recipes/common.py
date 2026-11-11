"""Original demonstrations only; adapt data and scientific definitions explicitly."""
from dataclasses import dataclass,field
import numpy as np
from prl_figure import new_figure,DEFAULTS
C=DEFAULTS['colors']

@dataclass
class Example:
    figure: object
    caption: str
    data: dict=field(default_factory=dict)
    transformations: list=field(default_factory=list)

def single(width=85,height=70):return new_figure(width,height)
def labels(ax,x='Control (a.u.)',y='Response (a.u.)'):ax.set(xlabel=x,ylabel=y)
def panel(ax,label):ax.text(.02,1.02,label,transform=ax.transAxes,va='bottom',weight='bold')

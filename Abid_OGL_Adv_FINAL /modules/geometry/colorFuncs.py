"""
Author: Liz Matthews
"""

from ..utils.vector import vec, lerp
import numpy as np
import random

COLORS = [vec(1,0,0), vec(1,1,0), vec(0,1,0), vec(0,1,1), vec(0,0,1), vec(1,0,1)]
WRAP_COLORS = list(COLORS) + [COLORS[0]]

def randomColor(u, v, uMaxIndex, vMaxIndex):
    return vec(random.random(), random.random(), random.random())

def rainbowGradient(u, v, uMaxIndex, vMaxIndex,
                    orientation="u", wrap=False):
    if wrap:
        colors = WRAP_COLORS
    else:
        colors = COLORS
    
    if orientation == "u":
        percent = u / uMaxIndex
    else:
        percent = v / vMaxIndex
    
    percent *= len(colors)-1
    start = int(np.floor(percent))
    end = start + 1
    remainder = percent - start
    return lerp(colors[start], colors[end], remainder)
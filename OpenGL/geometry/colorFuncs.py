"""
Author: Liz Matthews
"""

from ..utils.vector import vec, lerp
import numpy as np
import random

def randomColor(u, v, uMaxIndex, vMaxIndex):
    return vec(random.random(), random.random(), random.random())
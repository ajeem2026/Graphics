"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

import numpy as np
from math import sqrt
from .definitions import EPSILON

def magnitude(vector):    
    """Give the magnitude of a vector."""
    return np.linalg.norm(vector)

def normalize(vector):
    """Normalize a numpy array."""
    mag = magnitude(vector)
    if mag == 0.0:
        return vec(1,0,0)
    return vector / mag

def lerp(a, b, percent):
    """Linearly interpolate between a and b given a percent."""
    return (1.0 - percent)*a + percent*b

def smerp(a, b, percent):
    """Smooth interpolation."""
    percent = min(1.0, max(0.0, percent))
    x = (2*percent) - 1
    y = (3/4)*x-(1/4)*(x**3)+(1/2)
    smoothPercent = 3*percent**2 - 2*percent**3
    return a + y*(b-a)

def vec(x, y=None, z=None):
    """Make a numpy vector of x, y, z."""
    if not(y is None) and not(z is None):
        return np.array((x,y,z), dtype=np.float32)
    else:
        return np.array(x, dtype=np.float32)

def posDot(v,w):
    dot = np.dot(v,w)
    return max(0.0, dot)


if __name__ == '__main__':
    print(getConeAbout(vec(0,1,0), np.pi / 4, 2))


#Addition from lighting slide codebase
#=============================

def rot3D(vector, xAngle, yAngle, zAngle):
    return rotZ(rotY(rotX(vector,
                          xAngle),
                     yAngle),
                zAngle)
def rot3DInv(vector, xAngle, yAngle, zAngle):
    return rotX(rotY(rotZ(vector,
                          -zAngle),
                     -yAngle),
                -xAngle)

def rotX(vector, theta):
    x,y,z = vector
    return vec(x,
               y*np.cos(theta) - z*np.sin(theta),
               y*np.sin(theta) + z*np.cos(theta))

def rotY(vector, theta):
    x,y,z = vector
    return vec(x*np.cos(theta) - z*np.sin(theta),
               y,
               x*np.sin(theta) + z*np.cos(theta))

def rotZ(vector, theta):
    x,y,z = vector
    return vec(x*np.cos(theta) - y*np.sin(theta),
               x*np.sin(theta) + y*np.cos(theta),
               z)


def reflected(vector, normal):
    """Reflect vector about normal."""
    return vector - 2 * np.dot(vector, normalize(normal)) * normalize(normal)



def calcNormal(P0, P1, P2):
    v1 = vec(*P1) - vec(*P0)
    v2 = vec(*P2) - vec(*P0)
    normal = np.cross(v1,v2)
    normal = normalize(normal)
    return normal


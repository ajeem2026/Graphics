"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from ..oGL.attribute import Attribute
from ..oGL.uniform import Uniform
from ..utils.vector import vec
from ..utils.matrix import Matrix

import numpy as np
from OpenGL.GL import *

class Object3D(object):        
    """As described in Developing Graphics Frameworks
       with Python and OpenGL by Lee Stemkoski and
       Michael Pascal.
       
       Edits include change to use absolute transformation
       values instead of accumulative values."""
       
    def __init__(self):
        self.parent   = None
        self.children = []
        self.rotation = vec(0,0,0)
        self.position = vec(0,0,0)
        self.scale    = vec(1,1,1)
    
    def update(self, deltaTime=0):
        """Stub method so that all objects can be called
           to update even if they do not need to update."""
        pass
        
    def add(self, child):
        self.children.append(child)
        child.parent = self
    
    def remove(self, child):
        self.children.remove(child)
        child.parent = None
    
    def getDescendantList(self):
        """Depth-first traversal to obtain a list of descendants."""
        descendants = []
        nodesToProcess = [self]
        while len( nodesToProcess ) > 0:
            node = nodesToProcess.pop(0)
            descendants.append(node)
            nodesToProcess = node.children + nodesToProcess
            
        return descendants
    
    ## Absolute transformation calculation ##
    def getWorldMatrix(self):
        """Obtain the final transformation matrix based on all
           transforms in parent chain."""
           
        t = Matrix.makeIdentity()
        t = Matrix.scaleAsymmetric(t, *self.scale, False)
        t = Matrix.rotate(t, *self.rotation, False)
        t = Matrix.translate(t, *self.position, False)
        
        if self.parent == None:
            return t
        else:
            return self.parent.getWorldMatrix() @ t
    
    ## Mutator methods to adjust absolute values for translations ##
        
    def setPosition(self, position):
        self.position = vec(*position)
            
    def setRotateX(self, angle, localCoord=True):
        self.rotation[0] = angle
        
    def setRotateY(self, angle, localCoord=True):
        self.rotation[1] = angle
        
    def setRotateZ(self, angle, localCoord=True):
        self.rotation[2] = angle
    
    def setRotate(self, angleX, angleY, angleZ, localCoord=True):
        self.rotation = vec(angleX, angleY, angleZ)
        
    def setScale(self, s, localCoord=True):        
        self.scale = vec(s,s,s)
        
    def setScaleAsymmetric(self, sx, sy, sz, localCoord=True):
        self.scale = vec(sx, sy, sz)
        
    
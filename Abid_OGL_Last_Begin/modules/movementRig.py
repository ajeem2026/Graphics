"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

from .objects import Moving
from .objects import Object3D
from .utils.vector import vec, magnitude, normalize
from .utils.matrix import Matrix
from .utils.definitions import EPSILON

from pygame.locals import *
import numpy as np

class MovementRig(Moving, Object3D):
    """A first-person perspective movement rig.
       WASD to move, ZX to ascend/descend, mouse
       movement to look around.
       
       WASD/ZX are oriented around the current look
       direction."""
       
    def __init__(self,
                 speed=2,
                 rotSpeed=np.radians(20)):
        
        super().__init__(speed, rotSpeed)
        Object3D.__init__(self)
        
        # Initialize attached Object3D
        self.lookAttachment = Object3D()
        self.children = [self.lookAttachment]
        self.lookAttachment.parent = self
        
        # Keep track of keys
        self.movement = { }
        for k in [K_w, K_a, K_s, K_d, K_q, K_e, K_z, K_x]:
            self.movement[k] = False
            
        self.velocityMap = {
            K_w : vec( 0, 0,-1),
            K_s : vec( 0, 0, 1),            
            K_a : vec(-1, 0, 0),            
            K_d : vec( 1, 0, 0),
            K_z : vec( 0,-1, 0),
            K_x : vec( 0, 1, 0)
        }
        
    # Override functions from Object3D class        
    def add(self, child):
        self.lookAttachment.add(child)
        
    def remove(self, child):
        self.lookAttachment.remove(child)
        
    def update(self, deltaTime):
        self.velocity = np.zeros((3))
        for key in [K_w, K_a, K_s, K_d, K_z, K_x]:
            if self.movement[key]:
                self.velocity += self.velocityMap[key]
        
        if magnitude(self.velocity) > EPSILON:
                
            rotX = Matrix.makeRotationX(self.rotation[0])
            rotY = Matrix.makeRotationY(self.rotation[1])
            
            newVel = list(self.velocity)
            
            # Add homogeneous fourth coordinate
            newVel.append(1)
            
            # Multiply by matrices
            newVel = rotX @ newVel
            newVel = rotY @ newVel
            
            # Remove homogeneous coordinate
            self.velocity = vec(newVel[0:3])
        
        super().update(deltaTime)
        
        
    def handleOtherInput(self, event, deltaTime):
        if event.type in [KEYDOWN, KEYUP]:
            if event.key in self.movement.keys():
                self.movement[event.key] = event.type == KEYDOWN
                
        if event.type == MOUSEMOTION:
            turnAmt = self.rotationalSpeed
            self.rotation[0] += turnAmt * -event.rel[1] * deltaTime
            self.rotation[1] += turnAmt * -event.rel[0] * deltaTime
            
            
            
            
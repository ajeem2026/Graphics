"""
Author: Liz Matthews, Geoff Matthews
"""
from ..utils.vector import vec
import numpy as np

class Camera(object):
    """Camera object for raytracing.
    Initialization camera pointing
    at an arbitrary plane focus. Can get position
    and obtain a ray based on a percentage along
    the x and y of the focus plane."""

    def set(self,
            focus = vec(0,0,0),
            fwd = vec(0,0,-1),
            up = vec(0,1,0),
            fov = 90.0,
            distance = 2.5,
            aspect = 4/3):
        """Sets up the camera given the parameters.
           Calculates position, ul, ur, ll, and lr."""
        
        self.position = vec(0,0,0)
        self.ul = vec(0,0,0)
        self.ur = vec(0,0,0)
        self.ll = vec(0,0,0)
        self.lr = vec(0,0,0)

 #Given all of these, set up orthonomrla frame 
    def __init__(self,
                 focus = vec(0,0,0),
                 fwd = vec(0,0,-1),
                 up = vec(0,1,0),
                 fov = 45.0,
                 distance = 2.5,
                 aspect = 4/3):
        
        #This is the most part where we setup our frame 
        #Initilization calls self.set to change camera's aspect ratio middle of program 
        #fwd: forward, fov: field of view, and aspect ratio
        
        #1. Calculate frame using vector multiplation 
        #2. Plane size based on our parameters
        #Other stuff on slide 
        self.set(focus, fwd, up, fov, distance, aspect)

#If the camera and line is in the same direction then your direction is just fwd 

#Just change this to get orthonormal projection (not required for the prog assignment but
# will be an exam question)
    def getRay(self, xPercent, yPercent):
        """Returns a ray based on a percentage for the x and y coordinate."""
        pass

    def getPosition(self):
        """Getter method for position."""
        return self.position
    
    def getDistanceToFocus(self, point):
        """Getter method for distance from the given point to the center of focus."""
        focus = (self.ul + self.ur + self.ll + self.lr) / 4
        return np.linalg.norm(point - focus)

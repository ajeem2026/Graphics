"""
Author: Liz Matthews, Geoff Matthews
"""
import numpy as np
from .camera import Camera
from ..utils.vector import vec

#Smallest T> front of everyone else 
# Have ability to have multiple lights 
class Scene(object):
    """A class to contain all items in a scene.
       Contains a camera.
       Contains a list of lights.
       Contains a list of objects."""
    def __init__(self,
                 focus = vec(0,0.2,0),
                 direction = vec(0,0,-1),
                 up = vec(0,1,0),
                 fov = 45.0,
                 distance = 2.5,
                 aspect = 4/3):
        #Lights and objects are lists 
        self.lights = []
        self.objects = []
        self.camera = Camera(focus, direction, up, fov, distance, aspect)
        
        #Prof: Set up lights, spheres,  and planes here
    
    
    #List comprehension in nearestObject (just creates a list of and goes through it)
    #Can change list comprehension to NOT include negative ones or filter out negative ones
    #after you calcualte your distances
    
    #We need to know what object we collided with to know which object to calcualte with our
    #surface normal 
    def nearestObject(self, ray):
        """Returns the nearest collision object and the distance to the object."""
        distances = [o.intersect(ray) for o in self.objects]        
        nearestObj = None
        minDistance = np.inf
        
        return nearestObj, minDistance

#Optionally here if you want to exclude nearest shadow 
    def shadowed(self, obj, ray):
        """Returns the nearest collision object and the distance to the object,
           excluding obj."""
           #If it is NOT the object we want to exclude
        distances = [o.intersect(ray) for o in self.objects if not o is obj]
        minDistance = np.inf
        
        return minDistance
        
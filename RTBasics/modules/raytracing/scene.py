"""
Author: Abid Jeem, Liz Matthews, Geoff Matthews
"""
import numpy as np
from .camera import Camera
from .objects import Sphere, Plane
from .lights import *
from .materials import *
from ..utils.vector import vec
from ..utils.definitions import EPSILON

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
        #Prof: Set up lights, spheres,  and planes here

        self.lights = [PointLight(np.array([1,3,0]), np.array([1,1,1]))]
        self.objects = [
            #position, ambient, diffuse, specular, shininess, specCoefficient and radius
            Sphere(np.array([0,1,-3]), Material((0.2,0.2,0.4), (0.2,0.2,1), (0.8,0.8,1), 5, 0.1), 0.7),
            #position, ambient, diffuse, specular, shininess, specCoefficient and radius
            Sphere(np.array([-1,-0.2,-4]), Material((0.2,0.4,0.2), (0.2,1,0.2), (0.8,1,0.8), 100, 1.0), 0.7),
            #position, ambient, diffuse, specular, shininess, specCoefficient and radius
            Sphere(np.array([1,0,-2.3]), Material((0.4,0.2,0.2), (1,0.2,0.2), (1,0.8,0.8), 100, 1.0), 0.7),
            Plane(np.array([0,-1,0]), np.array([0,1,0]), Material((0.3,0.3,0.3), (0.7,0.7,0.7), (1,1,1), 5, 0.1))
        ]
        
        #alreadt setup 
        self.camera = Camera(focus, direction, up, fov, distance, aspect)
        
    
    
    #List comprehension in nearestObject (just creates a list of and goes through it)
    #Can change list comprehension to NOT include negative ones or filter out negative ones
    #after you calcualte your distances
    
    #We need to know what object we collided with to know which object to calcualte with our
    #surface normal 
    def nearestObject(self, ray):
       #""" Returns the nearest collision object and the distance to the object."""
       # distances = [o.intersect(ray) for o in self.objects]        
       # nearestObj = None
       # minDistance = np.inf
        
       # return nearestObj, minDistance 
        
        nearestObj = None
        minDistance = np.inf
        
        for obj in self.objects:
            t = obj.intersect(ray)
            if t is not None and t > EPSILON and t < minDistance:
                minDistance = t
                nearestObj = obj
                
        return nearestObj, minDistance

#Optionally here if you want to exclude nearest shadow 
    def shadowed(self, other, ray):
        """Returns the nearest collision object and the distance to the object,
           excluding obj."""
           #If it is NOT the object we want to exclude
        nearestObj = None
        minDistance = np.inf
        
        for obj in self.objects:
            if other is obj:
                continue
            t = obj.intersect(ray)
            if t is not None and t > EPSILON and t < minDistance:
                minDistance = t
                nearestObj = obj
                
        return minDistance
        
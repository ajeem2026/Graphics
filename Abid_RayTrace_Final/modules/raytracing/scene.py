"""
Author: Abid Jeem, Liz Matthews, Geoff Matthews
"""
import numpy as np
from .camera import Camera
from .objects import *
from .lights import *
from .materials import *
from ..utils.vector import vec
from ..utils.noise import NoisePatterns
from ..utils.definitions import EPSILON

# Smallest T> front of everyone else 
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
        
        #Let's get some noise 
        noise_patterns = NoisePatterns.getInstance()
        
        #For each new 3D Noise material
        wood_material = Material3D(
            ambient_noise=noise_patterns.wood3D,
            diffuse_noise=noise_patterns.wood3D,
            specular_noise=noise_patterns.wood3D,
            shine=50, specCoeff=0.5
        )

        marble_material = Material3D(
            ambient_noise=noise_patterns.marble3D,
            diffuse_noise=noise_patterns.marble3D,
            specular_noise=noise_patterns.marble3D,
            shine=100, specCoeff=1.0
        )

        clouds_material = Material3D(
            ambient_noise=noise_patterns.clouds3D,
            diffuse_noise=noise_patterns.clouds3D,
            specular_noise=noise_patterns.clouds3D,
            shine=50, specCoeff=0.3
        )
        
        floor = Material2D(
            "images/floor.jpg",
            tile=True,        
            scaleU=0.5,       
            scaleV=0.5,       
            ambient=(0.2,0.2,0.2),
            diffuse=(0.8,0.8,0.8),
            specular=(1,1,1),
            shine=50,
            specCoeff=1.0
        )
        
        ball8 = Material2D(
            "images/ball8.png",
            tile=True,       
            scaleU=2,       
            scaleV=1,      
            ambient=(0.7, 0.7, 0.7),
            diffuse=(0.8,0.8,0.8),
            specular=(1,1,1),
            shine=50,
            specCoeff=1.0
        )
        
        #perfect mirror with no refraction
        mirror= Material(
            ambient=(0,0,0),
            diffuse=(0,0,0),
            specular=(1,1,1),
            shine=100,
            specCoeff=1.0,
            reflection_factor=1.0,   
            trans=0.0,        
            refractive_index=1.0
        )
        
        glass= Material(
            ambient=(0.1,0.1,0.1),
            diffuse=(0.2,0.2,0.2),
            specular=(1,1,1),
            shine=100,
            specCoeff=1.0,
            reflection_factor=0.2,  
            trans=0.8,        
            refractive_index=1.52   
        )
        
        
        
        self.lights = [PointLight(np.array([1,3,0]), np.array([1,1,1]))]
        
        #DirectionLight(np.array([-1, -1, -1]), np.array([0.8, 0.8, 0.8]))
        
        self.objects = [
            #position, ambient, diffuse, specular, shininess, specCoefficient and radius
            #Sphere(np.array([1,-0.2,-2]), Material((0.2,0.2,0.4), (0.6,0.6,0.6), (1,1,1), 300, 1.0), 0.4),
            #position, ambient, diffuse, specular, shininess, specCoefficient and radius
            SphereTextured3D(np.array([-0.25, 0.25, -1]),0.25, marble_material),
           
            #center, fwd, up, length, material: ambient, diffuse, specular,shine, specCoeff
            #Cube(np.array([2, 0.5, -3]), np.array([1, 1, -1]), np.array([0, 1, 0]), 0.5, Material((0.3,0.3,0), (1.0,1.0,1.0), (1.0,1.0,1.0), 50, 1.0)),
            CubeTextured3D(np.array([2, 0.5, -3]), np.array([1, 1, -1]), np.array([0, 1, 0]), 0.5,wood_material),
            
            #center, multiple radii, rotation, material: ambient, diffuse, specular,shine, specCoeff
            #Ellipsoid(np.array([-1.25, -0.2, -1]), np.array([0.2, 0.2, 0.5]), np.array([40, 55, 25]), Material((0.4, 0.1, 0.4), (0.8, 0.2, 0.8), (1, 1, 1), 75, 0.8)),
            EllipsoidTextured3D(np.array([1, 2, -5]),np.array([1, 1, 1]), np.array([30, 45, 15]), clouds_material),
            
            #Final ray tracing additions
            SphereTextured2D(np.array([-2, 1.5, -3]),0.75, ball8, np.radians(65)),     
            PlaneTextured2D(np.array([0, -1, 0]),np.array([0, 1, 0]), floor),
         
            Sphere(np.array([1,-0.2,-2]),mirror,0.5),
            Sphere(np.array([-1.25, -0.2, -1]),glass,0.5)
        ]
        
        
        #alreadt setup 
        self.camera = Camera(focus, direction, up, fov, distance, aspect)
                        #==============================     Scene setup ends here    ==================================
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
# Updated shadowed function to accomodate both point and directional light
    def shadowed(self, other, ray,light):
        """Returns the nearest collision object and the distance to the object,
           excluding obj."""
           #If it is NOT the object we want to exclude
        minDistance = np.inf
        
        for obj in self.objects:
            if other is obj:
                continue
            
            t = obj.intersect(ray)
            
            if t is not None and t > EPSILON:
                if isinstance(light, PointLight):
                #point light
                    if t < light.getDistance(ray.position):
                        return True  
            elif isinstance(light, DirectionLight):
                return True 
                
        return False
        
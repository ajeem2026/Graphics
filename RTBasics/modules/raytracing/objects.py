"""
Author: Abid Jeem, Liz Matthews, Geoff Matthews
"""
from abc import ABC, abstractmethod
import numpy as np
from ..utils.vector import *


class Object3D(ABC):
    """Abstract base class for all objects in the raytraced scene.
       Has a position, material.
       Has getter methods for all material properties.
       Has abstract methods intersect and getNormal."""

    def __init__(self, pos, material):

        # Each object has a its own position and material its made of
#All attributes are stored in a numpy array
        self.position = np.array(pos)
        self.material = material

    def getAmbient(self, intersection=None):
        """Getter method for the material's ambient color.
           Intersection parameter is unused for Ray Tracing Basics."""

        return self.material.getAmbient()

    def getDiffuse(self, intersection=None):
        """Getter method for the material's diffuse color.
           Intersection parameter is unused for Ray Tracing Basics."""

        return self.material.getDiffuse()

    def getSpecular(self, intersection=None):
        """Getter method for the material's specular color.
           Intersection parameter is unused for Ray Tracing Basics."""

        return self.material.getSpecular()

    def getShine(self):
        """Getter method for the material's shininess factor."""

        return self.material.getShine()

    def getSpecularCoefficient(self, intersection=None):
        """Getter method for the material's specular coefficient.
           Intersection parameter is unused for Ray Tracing Basics."""

        return self.material.getSpecularCoefficient()

    @abstractmethod
    def intersect(self, ray):
        """Find the intersection for the given object. Must override."""
        pass

    @abstractmethod
    def getNormal(self, intersection):
        """Find the normal for the given object. Must override."""
        pass
class Sphere(Object3D):
    "Initalizing and overrding abstract class methods for Sphere."
    def __init__(self, pos, material,radius):
        super().__init__(vec(pos), material)
        self.radius=radius
    
    def intersect(self, ray):
        """Plane Intersection calculation"""

        # let radius be r
        r = self.radius

        # Let the ray advance along the direction of v which is to be
        # parametrized by 't'
        v = ray.direction

        # p is the vector to be parametrized by 't'
        p = ray.position - self.position

        # a = <v,v>
        a = np.dot(v, v)
        # b= 2<p,v>
        b = 2*np.dot(p, v)
        # c= <p,p> -r^2
        c = np.dot(p, p) - r*r

        # Discriminant from quadratic equaiton
        discriminant = b*b-4*a*c

        # No roots case == no intersection
        if discriminant < 0:
            return None

        # Solving the quadratic formula to get our values of t'

        t1 = (-b-np.sqrt(discriminant))/(2*a)
        t2 = (-b+np.sqrt(discriminant))/(2*a)

        # We only care about positive values of t that aligns with viewport collisions
        if t1 > 0:
            return t1
        elif t2 > 0:
            return t2
        # We DONT care about negative values of t which means obj is behind camera
        return None
    
    def getNormal(self,intersection):
        #Normalization
        return normalize(intersection-self.position)
    
class Plane(Object3D):
    "Initalizing and overrding abstract class methods for Plane."
    
    def __init__(self,pos,normal,material):
        super().__init__(pos,material)
        self.normal= normalize(vec(normal))

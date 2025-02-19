"""
Authors: Abid Jeem, Liz Matthews, Geoff Matthews
"""
import numpy as np
from ..utils.vector import vec

class Material(object):
    """A class to contain all properties of a material.
       Contains ambient, diffuse, specular colors.
       Contains shininess property.
       Contains specular coefficient."""
    def __init__(self, ambient, diffuse, specular,
                 shine=100, specCoeff=1.0):
        self.ambient = vec(*ambient)
        self.diffuse = vec(*diffuse)
        self.specular = vec(*specular)
        self.shine = shine
        self.specCoeff = specCoeff

#You can change these to get normal? But prof leaves this calcualtions to the rayTracer (glorified struct)
    def getAmbient(self):
        """Getter method for ambient color."""
        return vec(*self.ambient)

    def getDiffuse(self):
        """Getter method for diffuse color."""
        return vec(*self.diffuse)

    def getSpecular(self):
        """Getter method for specular color."""
        return vec(*self.specular)

    def getShine(self):
        """Getter method for shininess factor."""
        return self.shine

    def getSpecularCoefficient(self):
        """Getter method for specular coefficient."""
        return self.specCoeff
    
    
    
class Material3D(Material):
    
    def __init__(self, ambient_noise, diffuse_noise, specular_noise,
                 shine=100, specCoeff=1.0):
        
        super().__init__((0, 0, 0), (0, 0, 0), (0, 0, 0), shine, specCoeff)
        self.ambient_noise=ambient_noise
        self.diffuse_noise=diffuse_noise
        self.specular_noise=specular_noise
        
        
        """
        
        How do we calculate ambient, diffuse, and specular given one noise color value?
        Multiply!
        Ambient is multiplying by a value less than 1
        Specular is multiplying by a value greater than one
        Be careful! Clip the color to a cap of 1.0 for rgb otherwise you get weird things

        """
        
    def getAmbient(self, x, y, z):
        noise_value = self.ambient_noise(x, y, z)
        #Ambient is multiplying by a value less than 1
        return vec(*np.clip(noise_value * np.array([0.5, 0.5, 0.5]), 0, 1))

    def getDiffuse(self, x, y, z):
        noise_value = self.diffuse_noise(x, y, z)
        #Diffuse is multiplying by a value less than 1
        return vec(*np.clip(noise_value * np.array([0.8, 0.8, 0.8]), 0, 1))

    def getSpecular(self, x, y, z):
        noise_value = self.specular_noise(x, y, z)
        #Specular is multiplying by a value greater than one
        return vec(*np.clip(noise_value * np.array([2, 2, 2]), 0, 1))
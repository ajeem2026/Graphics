"""
Authors: Abid Jeem, Liz Matthews, Geoff Matthews
"""
import numpy as np
import pygame as pygame
from ..utils.vector import vec

class Material(object):
    """A class to contain all properties of a material.
       Contains ambient, diffuse, specular colors.
       Contains shininess property.
       Contains specular coefficient."""
    def __init__(self, ambient, diffuse, specular,
                 shine=100, specCoeff=1.0, reflection_factor=0.0,
                 trans=0.0,
                 refractive_index=1.0):
        self.ambient = vec(*ambient)
        self.diffuse = vec(*diffuse)
        self.specular = vec(*specular)
        self.shine = shine
        self.specCoeff = specCoeff
        
        #for recursive ray tracing (reflection+refraction)
        self.reflection_factor= reflection_factor
        self.trans= trans
        self.refractive_index=refractive_index


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
    
# ---------------------------Using 2D image to color a surface-------------------------------------

class Material2D(Material):

    def __init__(self, imageName, tile=True, scaleU=1.0, scaleV=1.0,
                 ambient=(0.2, 0.2, 0.2),
                 diffuse=(0.8, 0.8, 0.8),
                 specular=(1.0, 1.0, 1.0),
                 shine=50,
                 specCoeff=1.0):
        
        super().__init__(ambient, diffuse, specular, shine, specCoeff)
        self.tile=tile
        self.scaleU=scaleU
        self.scaleV=scaleV

        #loading images
        #pygame can load images onto surfaces
        self.image=pygame.image.load(imageName)
        self.width,self.height=self.image.get_size()

    def get_U_V(self, u, v):
        #Calculating u and v on the surface depends on the shape
        #planes are the easiest 

        u_scaled=u*self.scaleU
        v_scaled=v*self.scaleV
        
        if self.tile:
            #modulo wrap around
            u_mod=u_scaled%1
            v_mod=v_scaled%1
        else:
            #clamp in numpy array mode 
            u_mod=max(0,min(1,u_scaled))
            v_mod=max(0,min(1,v_scaled))
            
        #pixel color lookup calculations

        #multiply pixel width by u
        px=int(u_mod*(self.width-1))
        #multiply pixel height by v
        py=int(v_mod*(self.height-1))

        #0,0 in top left of image
        #will be in 255 mode
        #pixel's color contains RGB and alpha 
        color_255_mode=self.image.get_at((px, py))  
        # Convert it to a numpy array in 1.0 mode (throw away the alpha to convert it to RGB)
        color=np.array(color_255_mode[:3])/255.0
        return color

    #the values of u and v from 0 to 1 means one full image per unit vector ( both can be scaled independently )
    #the useMath approach for ambient, diffuse and specular values
    def getAmbient(self, u, v):
        return vec(*(super().getAmbient() * self.get_U_V(u, v)))

    def getDiffuse(self, u, v):
        return vec(*(super().getDiffuse() * self.get_U_V(u, v)))

    def getSpecular(self, u, v):
        return vec(*(super().getSpecular() * self.get_U_V(u, v)))

    
# Here we add 3D material with their own noise --------------------------------
class Material3D(Material):
    
    def __init__(self, ambient_noise, diffuse_noise, specular_noise,
                 shine=100, specCoeff=1.0):
        
        super().__init__((0, 0, 0), (0, 0, 0), (0, 0, 0), shine, specCoeff)
        self.ambient_noise=ambient_noise
        self.diffuse_noise=diffuse_noise
        self.specular_noise=specular_noise
        
        
        """
        Algorithm from slide:
        
        How do we calculate ambient, diffuse, and specular given one noise color value?
        Multiply!
        Ambient is multiplying by a value less than 1
        Specular is multiplying by a value greater than one
        Be careful! Clip the color to a cap of 1.0 for rgb otherwise you get weird things

        """
    #I made arbitray choices with the numbers below
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
    
    
#For reflective material with reflection factor, refraction index
#and transparency


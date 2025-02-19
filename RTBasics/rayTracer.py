"""
Author: Abid Jeem, Liz Matthews, Geoff Matthews
"""

# Prof recommedation: Keep calculation in RayTracer (not in the other classes)

# Its going to seem overengineered now
import numpy as np
import pygame
from modules.raytracing.ray import Ray

from render import ProgressiveRenderer, ShowTypes

from modules.raytracing.scene import Scene
from modules.utils.vector import *
from modules.raytracing.lights import *

class RayTracer(ProgressiveRenderer):
    def __init__(self, width=800, height=600, show=ShowTypes.PerColumn):
        super().__init__(width, height, show=show)
        self.fog = vec(0.7, 0.9, 1.0)
        self.scene = Scene(aspect=width/height, fov=45)

    # eventually to be used recursively
    def getColorR(self, ray):
        # Start with zero color
        #color = np.zeros((3))

        # Find any objects it collides with and calculate color
        nearest_object, minimum_distance= self.scene.nearestObject(ray)
        
        #No collision: just fog
        if nearest_object is None:
            # Return fog if doesn't hit anything
             return self.fog
        collision= ray.getPositionAt(minimum_distance)
        #Normal at collision point
        n= nearest_object.getNormal(collision)
        
        #Implementing general color algorithm
        
        #Start with ambient color 
        
        color = nearest_object.getAmbient(collision)
        
        #For each light...
        for light in self.scene.lights: 
            l= normalize(light.getVectorToLight(collision))
            l_prime= light.getVectorToLight(collision)
            
        # If the light is not shadowed by another object
           # if self.scene.shadowed(nearest_object, Ray(light.position,-l),light) < light.getDistance(collision):
                #continue
        
            if isinstance(light, PointLight):
                shadow_ray = Ray(collision, l)
                if self.scene.shadowed(nearest_object, shadow_ray, light):
                    continue 

            elif isinstance(light, DirectionLight):
                shadow_ray = Ray(collision, -light.direction)  
                if self.scene.shadowed(nearest_object, shadow_ray, light):
                    continue  
        
    # Multiply the diffuse color, minus the current color, by the diffuse cosine value, and add to the current color
            diffuse_cosine= np.dot(n, l)
            if diffuse_cosine > 0:
                color += (diffuse_cosine)*(nearest_object.getDiffuse(collision)-color)
    # Multiply the specular color, minus the current color, by the specular value, multiply by the specular coefficient, and add to the current color
        #Reflection vector, r = l - (l- (n * l) n )
        
            #r= l -(l - (np.dot(n,l)*n))
            r= normalize(l-ray.direction)
            e=normalize(n)
            specular_angle= np.dot(r,e)
            
            if specular_angle > 0:
                s_color= nearest_object.getSpecular(collision)
                s_coefficient= nearest_object.getSpecularCoefficient()
                s_value=nearest_object.getShine()
                
                # color+= ((specular_angle ** s_value) * s_color *s_coefficient)-color
                
                color += (s_color-color)*(specular_angle**s_value)*s_coefficient
        
        
        return color

# Calculates x% and y% along the pixel
    def getColor(self, x, y):
        # Calculate the percentages for x and y
        xPercent = x/self.width
        yPercent = y/self.height

        # Get the ray from the camera
        cameraRay = self.scene.camera.getRay(xPercent, yPercent)

        # Get the color based on the ray
        color = self.getColorR(cameraRay)

        # Fixing any NaNs in numpy, clipping to 0, 1.
        # Prevents crashing
        color = np.nan_to_num(np.clip(color, 0, 1), 0)

        return color


# Calls the 'main' function when this script is executed
if __name__ == '__main__':
    RayTracer.main("Ray Tracer Basics")
    pygame.quit()

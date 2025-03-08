"""
Author: Abid Jeem, Liz Matthews, Geoff Matthews
"""

# Prof recommedation: Keep calculation in RayTracer (not in the other classes)

# Its going to seem overengineered now
import numpy as np
import pygame
from modules.raytracing.ray import Ray
from modules.utils.definitions import *
from render import ProgressiveRenderer, ShowTypes

from modules.raytracing.scene import Scene
from modules.utils.vector import *
from modules.raytracing.lights import *


class RayTracer(ProgressiveRenderer):
    def __init__(self, width=800, height=600, show=ShowTypes.PerColumn):
        super().__init__(width, height, show=show)
        self.fog = vec(0.7, 0.9, 1.0)
        self.scene = Scene(aspect=width/height, fov=45)

# ================================================================
    # eventually to be used recursively (feb,2025)
    # now we're going ot make it recursive (march,2025)
    def getColorR(self, ray, depth=5):
        # Start with zero color
        # color = np.zeros((3))

        # base case for recursion
        if depth <= 0:
            return self.fog

        # Find any objects it collides with and calculate color
        nearest_object, minimum_distance = self.scene.nearestObject(ray)

        # No collision: just fog
        if nearest_object is None:
            # Return fog if doesn't hit anything
            return self.fog
        collision = ray.getPositionAt(minimum_distance)
        # Normal at collision point
        n = nearest_object.getNormal(collision)

        # Implementing general color algorithm

        # Start with ambient color

        color = nearest_object.getAmbient(collision)

        # For each light...
        for light in self.scene.lights:
            l = normalize(light.getVectorToLight(collision))

        # If the light is not shadowed by another object
           # if self.scene.shadowed(nearest_object, Ray(light.position,-l),light) < light.getDistance(collision):
            # continue

            if isinstance(light, PointLight):
                shadow_ray = Ray(collision, l)
                if self.scene.shadowed(nearest_object, shadow_ray, light):
                    continue

            elif isinstance(light, DirectionLight):
                shadow_ray = Ray(collision, -light.direction)
                if self.scene.shadowed(nearest_object, shadow_ray, light):
                    continue

    # Multiply the diffuse color, minus the current color, by the diffuse cosine value, and add to the current color
            diffuse_cosine = np.dot(n, l)
            if diffuse_cosine > 0:
                color += (diffuse_cosine) * \
                    (nearest_object.getDiffuse(collision)-color)
    # Multiply the specular color, minus the current color, by the specular value, multiply by the specular coefficient, and add to the current color
        # Reflection vector, r = l - (l- (n * l) n )

            # r= l -(l - (np.dot(n,l)*n))
            r = normalize(l-ray.direction)
            e = normalize(n)
            specular_angle = np.dot(r, e)

            if specular_angle > 0:
                s_color = nearest_object.getSpecular(collision)
                s_coefficient = nearest_object.getSpecularCoefficient()
                s_value = nearest_object.getShine()

                # color+= ((specular_angle ** s_value) * s_color *s_coefficient)-color

                color += (s_color-color) * \
                    (specular_angle**s_value)*s_coefficient

        rf = nearest_object.material.reflection_factor
        t = nearest_object.material.trans
        eta_obj = nearest_object.material.refractive_index
        eta_air = 1.0

        # =====recursive REFLECTION=====
        # calculate only if the object has a reflection factor
        if rf > 0 or t > 0:
            v = ray.direction
            reflect_ray = Ray(collision+n*0.0001,
                              normalize(v-2*np.dot(v, n)*n))
            reflect_color = self.getColorR(reflect_ray, depth-1)
            color = lerp(color, reflect_color, rf)
        # =====recursive REFLECTION=====

        # ==== refraction ===
        trans_color = vec(0, 0, 0)
        freshnel = 0.0

        # snell's law
        if t > 0:
            # enter case
            if np.dot(ray.direction, n) < 0:
                eta_in = eta_air
                eta_out = eta_obj
                new_n = n
            # exit case
            else:
                eta_in = eta_obj
                eta_out = eta_air
                new_n = -n

            cos_i = -np.dot(new_n, ray.direction)
            eta_ratio = eta_in/eta_out
            sin_t2 = eta_ratio**2*(1-cos_i**2)

            if sin_t2 > 1.0:
                # TIR
                trans_color = reflect_color

            else:
                cos_t = np.sqrt(1-sin_t2)
                ut = normalize(eta_ratio*ray.direction +
                               (eta_ratio*cos_i-cos_t)*new_n)

                refract_ray = Ray(collision-new_n*0.0001, ut)
                trans_color = self.getColorR(refract_ray, depth-1)

            # freshnel equation w/ shlick
            cos_theta = posDot(new_n, -ray.direction)
            r_theta = ((eta_in-eta_out)/(eta_in+eta_out))**2
            freshnel = r_theta+(1-r_theta)*(1-cos_theta)**5

            # Trying a double lerp approach
            # 1st lerp: reflection_refraction weighted by freshnel

            # reflection: fershnel
            # refraction: 1- freshnel
            reflection_refraction = lerp(
                reflect_color, trans_color, 1-freshnel)

            # blend original color with reflection_refraction by (rf+t)

            # original; 1-(rf+t)
            # reflection_refraction: (rf+t)
            color = lerp(color, reflection_refraction, rf+t)

            return color

        # color=lerp(color,reflect_color,rf)
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

"""
Author: Abid Jeem, Liz Matthews, Geoff Matthews
"""
from abc import ABC, abstractmethod
import numpy as np
from ..utils.vector import *
from typing import override


class Object3D(ABC):
    """Abstract base class for all objects in the raytraced scene.
       Has a position, material.
       Has getter methods for all material properties.
       Has abstract methods intersect and getNormal.

       This version has: Sphere, Plane, Cube, Ellipsoid and their textured versions. """

    def __init__(self, pos, material):

        # Each object has a its own position and material its made of
        # All attributes are stored in a numpy array
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

    def __init__(self, pos, material, radius):
        super().__init__(vec(pos), material)
        self.radius = radius

    def intersect(self, ray):
        """Sphere Intersection calculation"""

        # let radius be r
        r = self.radius

        # Let the ray advance along the direction of v which is to be
        # parametrized by 't'
        v = ray.direction

        # p is the vector to be parametrized by 't'
        p = ray.position - self.position

        # a = <v,v>
        a = 1
        # b= 2<p,v>
        b = 2 * (p.dot(v))
        # c= <p,p> -r^2
        c = p.dot(p) - r*r

        # Discriminant from quadratic equaiton
        discriminant = b*b-4*a*c
        # No roots case == no intersection
        if discriminant < 0:
            return np.inf

        # Solving the quadratic formula to get our values of t'

        t1 = (-b-np.sqrt(discriminant))/(2*a)
        t2 = (-b+np.sqrt(discriminant))/(2*a)

        # We only care about positive values of t that aligns with viewport collisions

        if t1 > 0 and t2 > 0:
            # return closest intersection
            return min(t1, t2)
        elif t1 > 0:
            return t1
        elif t2 > 0:
            return t2
        # We DONT care about negative values of t which means obj is behind camera
        return np.inf

    def getNormal(self, intersection):
        # Normalization
        return normalize(intersection-self.position)


class Plane(Object3D):
    "Initalizing and overrding abstract class methods for Plane."

    def __init__(self, pos, normal, material):
        super().__init__(pos, material)
        self.normal = normalize(vec(normal))

    def intersect(self, ray):
        """Plane Intersection calculation"""
        # Formula to be implemented
        # t = (q-p)*n/ v*n

        # Let the ray advance along the direction of v which is to be
        # parametrized by 't'
        n = self.normal
        v = ray.direction
        denominator = np.dot(v, n)

        # DEno can't be zero

        if abs(denominator) > 1e-11:  # avoiding floating point error
            t = np.dot(self.position-ray.position, n)/denominator

            if t > 0:
                return t
            else:
                return None

        return None

    def getNormal(self, intersection):

        # Consistnet for the entire surface of the plane
        return self.normal
    
    #Final ray tracing addition 
    
    def uvCoordinates(self, intersection):
        fwd = np.array([1, 0, 0])
        if abs(np.dot(fwd, self.normal)) > 0.9:
            #something else if parallel
            fwd = np.array([0, 0, 1]) 

        uAxis = normalize(fwd - (np.dot(fwd, self.normal)*self.normal))
        vAxis = normalize(np.cross(self.normal, uAxis))

        p = intersection - self.position
        u = np.dot(p, uAxis)
        v = np.dot(p, vAxis)
        return (u, v)

# ----------------------------------------------------------------
                                                    # TO DO: Create a cube

class Cube(Object3D):

    # 1.A cube is just a six sided square
    # 2.We will create a cube with six planes ( 3pairs of  parallel planes)
    # 3.For intersection: compute the 'enter' and 'exit' for each plane

    def __init__(self, center, fwd, up, length, material):
        super().__init__(center, material)

        # center, f vector and u vector
        # half the length for addition from center
        half = length/2

        # orthonormal basis for the cube
        # fwd normalized
        f = normalize(fwd)
        # right= f x up
        r = normalize(np.cross(f, up))
        # up= r x f
        u = normalize(np.cross(r, f))

        # each face is a plane: the "front" plane is at +f, "back" plane is at -f
        # center +/- half in each direction => plane positions

        # plane constructor signature (pos, normal, material)
        # each plane's position = center + direction*(half), normal is +/- direction

        frontPos = center + f*half
        backPos = center - f*half
        rightPos = center + r*half
        leftPos = center - r*half
        topPos = center + u*half
        bottomPos = center - u*half

        # create the planes
        # sotre planes in a list to loop over for intersection checks
        self.planes = [

            # Three pairs of parallel planes

            # Left and right planes
            Plane(rightPos, r, material),
            Plane(leftPos, -r, material),

            # Top and bottom planes
            Plane(topPos, u, material),
            Plane(bottomPos, -u, material),

            # Front and back planes
            Plane(frontPos, f, material),
            Plane(backPos, -f, material)
        ]

        # Last Intersection Call => LIC
        # store the plane that actually "won" the intersection in _LIC
        self._LIC = None

    def intersect(self, ray):

        # All light rays begin and end at infinity
        maxEnter = -np.inf
        minExit = np.inf

        # These are the intersection planes

        # Intersections entering the shape
        planeEnter = None
        # Intersections are exiting the shape
        planeExit = None

# How can we tell when we enter or exit a plane?
        # for each plane --> compute t=plane.intersect(ray).
        # the plane's normal vs. the ray direction => enter or exit check


# ================================================================

# CHECKING ALL PLANES

        for pl in self.planes:
            t = pl.intersect(ray)

         # None if parallel => no intersection
            if t is None:
                # If v dot n > 0 or t < 0 then the plane is behind the ray
                # Return t regardless of its sign for the cube
                # The cube will then check all values of t for all of its planes

                return np.inf

            else:
                # Plane intersection case
                # is it eneter or exit?
                # We need each all exit/enters
                # only return SMALLEST POSITIVE value for t
                v_dot_n = np.dot(ray.direction, pl.normal)

                if v_dot_n < 0:
                    # ray hitting 'front' of that plane => an ENTER
                    if t > maxEnter:
                        maxEnter = t
                        # putting entered plane on to the list
                        planeEnter = pl
                else:
                    # EXIT CASE
                    if t < minExit:
                        minExit = t
                        planeExit = pl

            # if maxEnter > minExit, no intersection:
            if maxEnter > minExit:
                return np.inf

            # ALL PLANES CHECKED#
    # ================================================================

        # Only valid intersectios maxEnter >0 && maxEnter < minExit

        if maxEnter >= 0:
            self._LIC = planeEnter
            return maxEnter

        elif minExit > 0:
            # ray starts inside cube
            self._LIC = planeExit
            return minExit
        else:
            return np.inf

# Code given in class
    def getNormal(self, intersection):
        if self._LIC is not None:
            return self._LIC.getNormal(intersection)
        return super().getNormal(intersection)

    def getDiffuse(self, intersection=None):
        if self._LIC is not None:
            return self._LIC.getDiffuse(intersection)
        return super().getDiffuse(intersection)

    # Overriding other accessors as well

    def getAmbient(self, intersection=None):
        if self._LIC is not None:
            return self._LIC.getAmbient(intersection)
        return super().getAmbient(intersection)

    def getSpecular(self, intersection=None):
        if self._LIC is not None:
            return self._LIC.getSpecular(intersection)
        return super().getSpecular(intersection)

    def getSpecularCoefficient(self, intersection=None):
        if self._LIC is not None:
            return self._LIC.getSpecularCoefficient(intersection)
        return super().getSpecularCoefficient(intersection)

    def getShine(self):
        if self._LIC is not None:
            return self._LIC.getShine()
        return super().getShine()


# ----------------------------------------------------------------
                                                # TO DO: Create an ellipsoid

def rotZ(point, theta):
    x, y, z = point
    return np.array([x*np.cos(theta) - y * np.sin(theta), x*np.sin(theta) + y * np.cos(theta), z])


def rotY(point, theta):
    x, y, z = point
    return np.array([y * np.cos(theta) - z * np.sin(theta), y, x*np.sin(theta) + z * np.cos(theta)])


def rotX(point, theta):
    x, y, z = point
    return np.array([x, y * np.cos(theta) - z * np.sin(theta), y*np.sin(theta) + z * np.cos(theta)])


def rotPoint(point, angles):
    xAngle, yAngle, zAngle = angles
    return rotZ(rotY(rotX(point, xAngle), yAngle), zAngle)


def inverse_point(point, angles):
    xAngle, yAngle, zAngle = angles
    return rotX(rotY(rotZ(point, -zAngle), -yAngle), -xAngle)


class Ellipsoid (Object3D):

    def __init__(self, center, radius, rotation, material):
        super().__init__(center, material)

        self.radius = np.array(radius)
        self.rotation = np.radians(rotation)

    def intersect(self, ray):

        # Now we follow the algorithm

        # 1. Transform the ray point to object space

        # 1.1 Rotate the ray point by the INVERSE+ ROTATION of the object
        p = inverse_point(ray.position - self.position, self.rotation)

        # 1.2 Rotate the ray vector by the inverse rotation of the object
        v = inverse_point(ray.direction, self.rotation)

        # Find t and use to find original ray

        # Using simplified formula

        s = 1 / self.radius

        v_s = v*s
        p_s = p*s

        A = np.dot(v_s, v_s)
        B = 2*np.dot(v_s, p_s)
        C = np.dot(p_s, p_s)-1

        roots = np.roots([A, B, C])

        # Filter non real roots

        roots = roots[np.isreal(roots)].real

        # Only keep positive rotos
        roots = roots[roots > 0]

        if len(roots) > 0:
            return np.min(roots)

        else:
            None

    def getNormal(self, intersection):

        # 1. Translate and rotate the ray to find hit point using pre algorithm

        hit_point = inverse_point(intersection-self.position, self.rotation)

        # 2. COmpute gradient to find normal at the hit point

        s = 1/self.radius

        hit_normal = normalize(2 * (hit_point * s**2))

        # 3. Rotate this normal using the original rotation (NOT THE INVERSE)

        return normalize(rotPoint(hit_normal, self.rotation))

# ----------------------------------------------------------------

                                            #Part-3:  TODO: Textured3D (repetitive code)
    # Create a *Textured3D class for all objects (SphereTextured3D, PlaneTextured3D, etc) which uses the intersection given to getDiffuse,
    # getAmbient, getSpecular, extracts the x, y, z components, and passes it on to the Material3D.

class Textured3D(Object3D):
    def __init__(self, pos, material3D):
        super().__init__(pos, material3D)

    def getAmbient(self, intersection):
        if intersection is None:
            return super().getAmbient()
        x, y, z = intersection
        return self.material.getAmbient(x, y, z)

    def getDiffuse(self, intersection):
        if intersection is None:
            return super().getDiffuse()
        x, y, z = intersection
        return self.material.getDiffuse(x, y, z)

    def getSpecular(self, intersection):
        if intersection is None:
            return super().getSpecular()
        x, y, z = intersection
        return self.material.getSpecular(x, y, z)
    
#---------------------------for 2d texture class-------------------------------------
#This class will be used if i want to extend my 2d texture to objects beyond spheres and planes
class Textured2D(Object3D):
    def __init__(self, pos, material2D):
        super().__init__(pos, material2D)

#we'll override the uv calculation based on the object
    @override
    def uvCoordinates(self, intersection):
        pass
    
    def getAmbient(self, intersection):
        if intersection is None:
            return super().getAmbient()  
        u,v =self.uvCoordinates(intersection)
        return self.material.getAmbient(u,v)

    def getDiffuse(self, intersection):
        if intersection is None:
            return super().getDiffuse()
        u,v=self.uvCoordinates(intersection)
        return self.material.getDiffuse(u,v)

    def getSpecular(self, intersection):
        if intersection is None:
            return super().getSpecular()
        u,v=self.uvCoordinates(intersection)
        return self.material.getSpecular(u,v)


#---------------------------for 2d texture class-------------------------------------

class SphereTextured3D(Sphere, Textured3D):
    def __init__(self, center, radius, material3D):
        Sphere.__init__(self, center, material3D, radius)
        Textured3D.__init__(self, center, material3D)

    def getAmbient(self, intersection):
        return super().getAmbient(intersection)

    def getDiffuse(self, intersection):
        return super().getDiffuse(intersection)

    def getSpecular(self, intersection):
        return super().getSpecular(intersection)
    
# ---------------------------2d texture for spheres-------------------------------------

class SphereTextured2D(Sphere, Textured2D):
    
    def __init__(self, pos, radius, material2D, rotation_angle=0.0):
        Sphere.__init__(self, pos, material2D, radius)
        Textured2D.__init__(self, pos, material2D)
        self.rotation_angle = rotation_angle

#uv calculation based on algorithm from slides 
    def uvCoordinates(self, intersection):
        #calculate d as the vector to the intersection from the center (translating to object space )
        d=intersection-self.position
        
        #d w/ unit length
        #d= normalized [x,y,z]
        d=normalize(d)
        
        #so dx= d[0], dy=d[1] and dz=d[2] 
        #azimuthal angle
        theta=np.arctan2(d[2],d[0])  
        #polar angle
        phi=np.arccos(d[1]) 
        
        #i added this to rotate the sphere to show numbers on the billiard ball
        theta+= self.rotation_angle

       #final calc from slides
       #add 0,5 to u in order to avoid negative angles
       #reverse the sign when computing u to fix the horizontal flip
        u=0.5-(theta)/(2*np.pi)
        v=phi/np.pi 
        return (u, v)

# ---------------------------final ray tracin addition-------------------------------------

class PlaneTextured3D(Plane, Textured3D):
    def __init__(self, pos, normal, material3D):
        Plane.__init__(self, pos, normal, material3D)
        Textured3D.__init__(self, pos, material3D)

    def getAmbient(self, intersection):
        return super().getAmbient(intersection)

    def getDiffuse(self, intersection):
        return super().getDiffuse(intersection)

    def getSpecular(self, intersection):
        return super().getSpecular(intersection)

#--------------------------------for 2d textured planes--------------------------------
class PlaneTextured2D(Plane, Textured2D):
    def __init__(self, pos, normal, material2D):
        Plane.__init__(self, pos, normal, material2D)
        Textured2D.__init__(self, pos, material2D)

    def uvCoordinates(self, intersection):
    #plane uv calculations from slides
        fwd = np.array([1,0,0])
        if abs(np.dot(fwd, self.normal)) > 0.9:
            fwd = np.array([0,0,1])

        u = normalize(fwd - np.dot(fwd,self.normal)*self.normal)
        v = normalize(np.cross(self.normal,u))
        p = intersection - self.position
        coordU = np.dot(p,u)
        coordV = np.dot(p,v)
        return (coordU, coordV)  

    
#----------------------------------------------------------------

class CubeTextured3D(Cube, Textured3D):
    def __init__(self, center, fwd, up, length, material3D):
        Cube.__init__(self, center, fwd, up, length, material3D)
        Textured3D.__init__(self, center, material3D)

    def getAmbient(self, intersection):
        x, y, z = intersection
        return self.material.getAmbient(x, y, z)

    def getDiffuse(self, intersection):
        x, y, z = intersection
        return self.material.getDiffuse(x, y, z)

    def getSpecular(self, intersection):
        x, y, z = intersection
        return self.material.getSpecular(x, y, z)


class EllipsoidTextured3D(Ellipsoid, Textured3D):
    def __init__(self, center, radius, rotation, material3D):
        Ellipsoid.__init__(self, center, radius, rotation, material3D)
        Textured3D.__init__(self, center, material3D)

    def getAmbient(self, intersection):
        x, y, z = intersection
        return self.material.getAmbient(x, y, z)

    def getDiffuse(self, intersection):
        x, y, z = intersection
        return self.material.getDiffuse(x, y, z)

    def getSpecular(self, intersection):
        x, y, z = intersection
        return self.material.getSpecular(x, y, z)

# for extra credit ========================================

class Disk(Plane):
    def __init__(self, pos, normal, radius, thickness, material):
        super().__init__(pos, normal, material)
        self.radius = radius
        self.thickness = thickness  # New attribute for thickness

    def intersect(self, ray):
        t = super().intersect(ray)
        if t is None:
            return None
        
        intersection = ray.position + t * ray.direction
        distance_to_center = np.linalg.norm(intersection - self.position)
        
        # Ensure the intersection is within the disk's radius
        if distance_to_center <= self.radius:
            return t  
        return None

    
#============================================
class PlaneBumpMapped(PlaneTextured2D):
    def __init__(self, pos, normal, bumpMaterial2D):
        super().__init__(pos, normal, bumpMaterial2D)
    
    def getNormal(self, intersection):
        # Get the base normal from the plane
        baseNormal = super().getNormal(intersection)
        
        # Calculate UV coordinates
        u, v = self.uvCoordinates(intersection)
        
        # We need to calculate tangent and bitangent vectors
        # These are perpendicular to the normal and to each other
        tangent = self._calculateTangent()
        bitangent = np.cross(baseNormal, tangent)
        
        # For bump mapping, we need to sample the height map at slightly offset positions
        # to compute an approximation of the gradient
        epsilon = 0.00001
        h = self.material.getBumpValue(u, v)
        h_du = self.material.getBumpValue(u + epsilon, v)
        h_dv = self.material.getBumpValue(u, v + epsilon)
        
        # Calculate the partial derivatives of the height field
        du = (h_du - h) / epsilon
        dv = (h_dv - h) / epsilon
        
        # Scale by bump strength
        du *= self.material.bumpStrength
        dv *= self.material.bumpStrength
        
        # Perturb the normal using the tangent space
        perturbedNormal = baseNormal - du * tangent - dv * bitangent
        
        # Normalize the result
        return normalize(perturbedNormal)
    
    def _calculateTangent(self):
        # Calculate a tangent vector perpendicular to the normal
        # This is arbitrary but consistent for a given normal
        if abs(np.dot(np.array([1, 0, 0]), self.normal)) > 0.9:
            # If normal is close to x-axis, use z-axis for reference
            tangent = np.cross(self.normal, np.array([0, 0, 1]))
        else:
            # Otherwise use x-axis
            tangent = np.cross(self.normal, np.array([1, 0, 0]))
        
        return normalize(tangent)
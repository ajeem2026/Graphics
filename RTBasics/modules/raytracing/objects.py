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
    
    
#----------------------------------------------------------------

    # TODO: Textured3D
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


"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from . import AbstractGeometry, PolygonGeometry
from ..utils.matrix import Matrix
from ..utils.vector import *
from .colorFuncs import *
import math
import numpy as np


class AbstractParametric(AbstractGeometry):
    """Abstract parametric class for parametric geometry.
       Expects a surface function which defines the surface
       of the shape. *Start, *End, and *Resolution define
       how much of the shape is created and at what level
       of detail."""

    def __init__(self, uStart, uEnd, uResolution,
                 vStart, vEnd, vResolution,
                 surfaceFunction,
                 colorFunction=None):
        super().__init__()

        # Generate set of points based on the function
        deltaU = (uEnd - uStart) / uResolution
        deltaV = (vEnd - vStart) / vResolution
        positions = []
        vertexNormal = []
        uvList = []
        uvData = []

        for uIndex in range(uResolution+1):
            vArray = []
            rowNormals = []
            rowUVs = []

            for vIndex in range(vResolution+1):
                u = uStart + uIndex * deltaU
                v = vStart + vIndex * deltaV

                vArray.append(surfaceFunction(u, v))

                # for normal: cross product of tangent vectors
                p0 = surfaceFunction(u, v)
                p1 = surfaceFunction(u+0.001, v)
                p2 = surfaceFunction(u, v+0.001)
                normal = calcNormal(p0, p1, p2)
                rowNormals.append(normal)

                uvCoord = [uIndex/uResolution, vIndex/vResolution]
                rowUVs.append(uvCoord)
            uvList.append(rowUVs)

            positions.append(vArray)
            vertexNormal.append(rowUVs)

        # Store vertex data
        positionData = []
        colorData = []
        vertexNormalData = []
        faceNormalData = []

        # Default vertex colors
        C1, C2, C3 = [1, 0, 0], [0, 1, 0], [0, 0, 1]
        C4, C5, C6 = [0, 1, 1], [1, 0, 1], [1, 1, 0]

        # Group vertex data into triangles
        for xIndex in range(uResolution):
            for yIndex in range(vResolution):
                # Position data
                pA = positions[xIndex+0][yIndex+0]
                pB = positions[xIndex+1][yIndex+0]
                pC = positions[xIndex+1][yIndex+1]
                pD = positions[xIndex+0][yIndex+1]

                positionData += [pA.copy(), pB.copy(),
                                 pC.copy(), pA.copy(),
                                 pC.copy(), pD.copy()]
                # Color data
                if colorFunction == None:
                    colorData += [C1, C2, C3, C4, C5, C6]
                else:
                    cA = colorFunction(xIndex,  yIndex,   len(
                        positions), len(positions[xIndex]))
                    cB = colorFunction(xIndex+1, yIndex,
                                       len(positions), len(positions[xIndex]))
                    cC = colorFunction(xIndex+1, yIndex+1,
                                       len(positions), len(positions[xIndex]))
                    cD = colorFunction(xIndex,  yIndex+1,
                                       len(positions), len(positions[xIndex]))

                    colorData += [cA, cB, cC,
                                  cA, cC, cD]

                # UV mapping
                uvTopLeft = uvList[xIndex][yIndex]
                uvTopRight = uvList[xIndex+1][yIndex]
                uvBottomRight = uvList[xIndex+1][yIndex+1]
                uvBottomLeft = uvList[xIndex][yIndex+1]

                uvData += [uvTopLeft, uvTopRight, uvBottomRight,
                           uvTopLeft, uvBottomRight, uvBottomLeft]

                # vertex normals
                normalTL = vertexNormal[xIndex][yIndex]
                normalTR = vertexNormal[xIndex+1][yIndex]
                normalBR = vertexNormal[xIndex+1][yIndex+1]
                normalBL = vertexNormal[xIndex][yIndex+1]

                vertexNormalData += [normalTL.copy(), normalTR.copy(), normalBR.copy(),
                                     normalTL.copy(), normalBR.copy(), normalBL.copy()]

                # faceNorm
                faceNorm1 = calcNormal(pA, pB, pC)
                faceNorm2 = calcNormal(pA, pC, pD)

                faceNormalData += [faceNorm1, faceNorm1,
                                   faceNorm1, faceNorm2, faceNorm2, faceNorm2]

        self.addAttribute("vec3", "vertexNormal", vertexNormalData)
        self.addAttribute("vec3", "faceNormal", faceNormalData)

        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)

        self.addAttribute("vec2", "vertexUV", uvData)
        self.countVertices()

## Some parametric shapes ##


class PlaneGeometry(AbstractParametric):
    def __init__(self, width=1, height=1,
                 widthSegments=8, heightSegments=8):

        def S(u, v):
            return [u, v, 0]

        super().__init__(-width/2, width/2,
                         widthSegments,
                         -height/2, height/2,
                         heightSegments, S,
                         randomColor)


class EllipsoidGeometry(AbstractParametric):
    def __init__(self, width=1, height=1, depth=1,
                 radiusSegments=32, heightSegments=16,colorFunction=None):
        def S(u, v):
            return [width/2 * np.sin(u) * np.cos(v),
                    height/2 * np.sin(v),
                    depth/2 * np.cos(u) * np.cos(v)]
        super().__init__(0, 2*np.pi,
                         radiusSegments,
                         -np.pi/2, np.pi/2,
                         heightSegments, S,colorFunction=colorFunction)


class SphereGeometry(EllipsoidGeometry):
    def __init__(self, colorFunction=None, radius=1,
                 radiusSegments=32,
                 heightSegments=16):
        super().__init__(2*radius,
                         2*radius,
                         2*radius,
                         radiusSegments,
                         heightSegments,
                         colorFunction=colorFunction)


class RainbowBowlGeometry(AbstractParametric):
    def __init__(self, radius=1, uResolution=32, vResolution=16):

        def S(u, v):
            # here, i used std spherical coords
            return [radius * np.cos(u) * np.cos(v),
                    radius * np.sin(v),
                    radius * np.sin(u) * np.cos(v)]

        super().__init__(0, 2*np.pi, uResolution,
                         -np.pi/2, 0, vResolution,
                         S,
                         rainbowGradient)


class CylindricalGeometry(AbstractParametric):
    def __init__(self, radiusTop=1, radiusBottom=1,
                 height=1, radialSegments=32,
                 heightSegments=4, closedTop=True,
                 closedBottom=True,colorFunction=None):
        def S(u, v):
            return [(v*radiusTop + (1-v)*radiusBottom) * np.sin(u),
                    height * (v - 0.5),
                    (v*radiusTop + (1-v)*radiusBottom) * np.cos(u)]
        super().__init__(0, 2*np.pi,
                         radialSegments,
                         0, 1,
                         heightSegments,
                         S,colorFunction=colorFunction)

        if closedTop:
            topGeometry = PolygonGeometry(radialSegments,
                                          radiusTop)
            transform = Matrix.makeTranslation(
                0, height/2, 0) @ Matrix.makeRotationY(-math.pi/2) @ Matrix.makeRotationX(-math.pi/2)
            topGeometry.applyMatrix(transform)
            self.merge(topGeometry)

        if closedBottom:
            bottomGeometry = PolygonGeometry(radialSegments,
                                             radiusBottom)
            transform = Matrix.makeTranslation(
                0, -height/2, 0) @ Matrix.makeRotationY(-math.pi/2) @ Matrix.makeRotationX(math.pi/2)
            bottomGeometry.applyMatrix(transform)
            self.merge(bottomGeometry)


class CylinderGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1,
                 radialSegments=32,
                 heightSegments=4,
                 closed=True):
        super().__init__(radius, radius,
                         height, radialSegments,
                         heightSegments, closed, closed)


class PrismGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1,
                 sides=6, heightSegments=4,
                 closed=True):
        super().__init__(radius, radius,
                         height, sides,
                         heightSegments, closed, closed)


class ConeGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1,
                 radialSegments=32, heightSegments=4,
                 closed=True):
        super().__init__(0, radius, height,
                         radialSegments, heightSegments,
                         False, closed)


class PyramidGeometry(CylindricalGeometry):
    def __init__(self, radius=1, height=1,
                 sides=4, heightSegments=4,
                 closed=True,colorFunction=None):
        super().__init__(0, radius, height,
                         sides, heightSegments,
                         False, closed,colorFunction=colorFunction)


# for dice geometry

class DiceGeometry(AbstractGeometry):
    """A primitive box."""

    def __init__(self,
                 width=1, height=1, depth=1,
                 colorFunction=None):
        super().__init__()

        P0 = [-width/2, -height/2, -depth/2]
        P1 = [width/2, -height/2, -depth/2]
        P2 = [-width/2, height/2, -depth/2]
        P3 = [width/2, height/2, -depth/2]
        P4 = [-width/2, -height/2, depth/2]
        P5 = [width/2, -height/2, depth/2]
        P6 = [-width/2, height/2, depth/2]
        P7 = [width/2, height/2, depth/2]

        uvData = [[0, 0.34], [0.25, 0.34], [0.25, 0.66], [0, 0.34], [0.25, 0.66], [0, 0.66], [0.25, 0.34], [0.5, 0.34], [0.5, 0.66], [0.25, 0.34], [0.5, 0.66], [0.25, 0.66], [0.25, 0.0], [0.5, 0.0], [0.5, 0.34], [0.25, 0.0], [0.5, 0.34], [0.25, 0.34], [
            0.25, 0.66], [0.5, 0.66], [0.5, 1.0], [0.25, 0.66], [0.5, 1.0], [0.25, 1.0], [0.5, 0.34], [0.75, 0.34], [0.75, 0.66], [0.5, 0.34], [0.75, 0.66], [0.5, 0.66], [0.75, 0.34], [1.0, 0.34], [1.0, 0.66], [0.75, 0.34], [1.0, 0.66], [0.75, 0.66]]
        # colors for faces in order: x+, x-, y+, y-, z+, z
        if colorFunction == None:
            C1, C2 = [1, 0.5, 0.5], [0.5, 0, 0]
            C3, C4 = [0.5, 1, 0.5], [0, 0.5, 0]
            C5, C6 = [0.5, 0.5, 1], [0, 0, 0.5]

        positionData = [P5, P1, P3, P5, P3, P7, P0, P4, P6, P0,
                        P6, P2, P6, P7, P3, P6, P3, P2,
                        P0, P1, P5, P0, P5, P4, P4, P5, P7,
                        P4, P7, P6, P1, P0, P2, P1, P2, P3]
        colorData = [C1]*6 + [C2]*6 + [C3]*6 + [C4]*6 + [C5]*6 + [C6]*6
        
        # normals for faces in order: x+, x-, y+, y-, z+, z
        #similar to color
        N1, N2 = [1, 0, 0], [-1, 0, 0]
        N3, N4 = [0, 1, 0], [0, -1, 0]
        N5, N6 = [0, 0, 1], [0, 0, -1]
        normalData = [N1] * 6 + [N2] * 6 + [N3] * 6 + [N4] * 6 + [N5] * 6 + [N6] * 6

        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.addAttribute("vec2", "vertexUV", uvData)
        self.addAttribute("vec3", "vertexNormal", normalData)
        self.addAttribute("vec3", "faceNormal", normalData)
        self.countVertices()

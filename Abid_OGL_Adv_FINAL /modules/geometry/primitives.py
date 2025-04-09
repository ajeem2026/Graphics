"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from . import AbstractGeometry
import numpy as np

from ..utils.matrix import Matrix
from ..utils.vector import *
from .colorFuncs import *
import math


class RectangleGeometry(AbstractGeometry):
    """A primitive rectangle."""

    def __init__(self, width=1, height=1,
                 colorFunction=None):
        super().__init__()

        P0 = [-width/2, -height/2, 0]
        P1 = [width/2, -height/2, 0]
        P2 = [-width/2, height/2, 0]
        P3 = [width/2, height/2, 0]
        if colorFunction == None:
            C0, C1, C2, C3 = [1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]
        else:
            C0 = colorFunction(0, 0, 3.01, 3.01)
            C1 = colorFunction(1, 1, 3.01, 3.01)
            C2 = colorFunction(2, 2, 3.01, 3.01)
            C3 = colorFunction(3, 3, 3.01, 3.01)

        positionData = [P0, P1, P3, P0, P3, P2]
        colorData = [C0, C1, C3, C0, C3, C2]
        normalData = [(0, 0, 1) for x in range(6)]
        T0, T1, T2, T3 = [0, 0], [1, 0], [0, 1], [1, 1]
        uvData = [T0, T1, T3, T0, T3, T2]

        self.addAttribute("vec2", "vertexUV", uvData)

        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)

        self.addAttribute("vec3", "vertexNormal", normalData)
        self.addAttribute("vec3", "faceNormal", normalData)

        self.countVertices()


class BoxGeometry(AbstractGeometry):
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

        # colors for faces in order: x+, x-, y+, y-, z+, z
        if colorFunction == None:
            C1, C2 = [1, 0.5, 0.5], [0.5, 0, 0]
            C3, C4 = [0.5, 1, 0.5], [0, 0.5, 0]
            C5, C6 = [0.5, 0.5, 1], [0, 0, 0.5]
        else:

            C1, C2 = colorFunction(
                0, 0, 5.01, 5.01), colorFunction(1, 1, 5.01, 5.01)
            C3, C4 = colorFunction(
                2, 2, 5.01, 5.01), colorFunction(3, 3, 5.01, 5.01)
            C5, C6 = colorFunction(
                4, 4, 5.01, 5.01), colorFunction(5, 5, 5.01, 5.01)

        positionData = [P5, P1, P3, P5, P3, P7, P0, P4, P6, P0,
                        P6, P2, P6, P7, P3, P6, P3, P2,
                        P0, P1, P5, P0, P5, P4, P4, P5, P7,
                        P4, P7, P6, P1, P0, P2, P1, P2, P3]
        colorData = [C1]*6 + [C2]*6 + [C3]*6 + [C4]*6 + [C5]*6 + [C6]*6

        # normals for faces in order: x+, x-, y+, y-, z+, z
        # similar to color
        N1, N2 = [1, 0, 0], [-1, 0, 0]
        N3, N4 = [0, 1, 0], [0, -1, 0]
        N5, N6 = [0, 0, 1], [0, 0, -1]
        normalData = [N1] * 6 + [N2] * 6 + [N3] * \
            6 + [N4] * 6 + [N5] * 6 + [N6] * 6

        # for texture
        T0, T1, T2, T3 = [0, 0], [1, 0], [0, 1], [1, 1]
        uvData = [T0, T1, T3, T0, T3, T2] * 6

        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.addAttribute("vec2", "vertexUV", uvData)
        self.addAttribute("vec3", "vertexNormal", normalData)
        self.addAttribute("vec3", "faceNormal", normalData)
        self.countVertices()


class PolygonGeometry(AbstractGeometry):
    """A primitive polygon."""

    def __init__(self, sides=3, radius=1, colorFunction=None):
        super().__init__()

        A = 2 * np.pi / sides
        positionData = []
        colorData = []
        uvData = []
        uvCenter = [0.5, 0.5]

        for n in range(sides):
            positionData.append([0, 0, 0])
            positionData.append([radius*np.cos(n*A),
                                 radius*np.sin(n*A),
                                 0])
            positionData.append([radius*np.cos((n+1)*A),
                                 radius*np.sin((n+1)*A),
                                 0])

            if colorFunction == None:
                colorData.append([1, 1, 1])
                colorData.append([1, 0, 0])
                colorData.append([0, 0, 1])
                uvData.append(uvCenter)
                uvData.append([np.cos(n*A)*0.5 + 0.5, np.sin(n*A)*0.5 + 0.5])
                uvData.append([np.cos((n+1)*A)*0.5 + 0.5,
                              np.sin((n+1)*A)*0.5 + 0.5])
            else:
                colorData.append([1, 1, 1])
                colorData.append(colorFunction(n,   n,   sides+1, sides+1))
                colorData.append(colorFunction(n+1, n+1, sides+1, sides+1))

        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.addAttribute("vec2", "vertexUV", uvData)

        self.countVertices()

        # ============================================================
    # for extra credit


class TorusGeometry(AbstractGeometry):
    """
    fornmula: https://en.wikipedia.org/wiki/Torus#Geometry
    https://www.songho.ca/opengl/gl_torus.html 
    https://gamedev.stackexchange.com/questions/159434/how-to-calculate-vertex-positions-of-a-torus
    """

    def __init__(self, majorRadius=1.0, minorRadius=0.3, uResolution=32, vResolution=16, colorFunction=None):
        super().__init__()
        
#helpder fyunction to do the calculations
        def S(u, v):
            x = (majorRadius+minorRadius*np.cos(v))*np.cos(u)
            y = (majorRadius+minorRadius*np.cos(v))*np.sin(u)
            z = minorRadius*np.sin(v)
            return [x, y, z]
        deltaU=2*np.pi/uResolution
        deltaV=2*np.pi/vResolution
        
        positions = []
        vertexNormals = []
        uvData = []
        uvGrid = []

        for uIndex in range(uResolution + 1):
            posRow = []
            normalRow = []
            uvRow = []
            u = uIndex * deltaU
            for vIndex in range(vResolution + 1):
                
                v = vIndex * deltaV
                point = S(u, v)
                posRow.append(point)

                p0 = S(u,v)
                p1 = S(u+0.001,v)
                p2 = S(u,v+0.001)
                normal = calcNormal(p0, p1, p2)
                normalRow.append(normal)
                uv = [uIndex / uResolution, vIndex / vResolution]
                uvRow.append(uv)
                
            positions.append(posRow)
            vertexNormals.append(normalRow)
            uvGrid.append(uvRow)
            
    
    #same structure as the others

        positionData = []
        colorData = []
        vertexNormalData = []
        faceNormalData = []
        flatUVs = []

        for i in range(uResolution):
            for j in range(vResolution):
                pA = positions[i][j]
                pB = positions[i+1][j]
                pC = positions[i+1][j+1]
                pD = positions[i][j+1]

                positionData += [pA, pB, pC, pA, pC, pD]

                nA = vertexNormals[i][j]
                nB = vertexNormals[i+1][j]
                nC = vertexNormals[i+1][j+1]
                nD = vertexNormals[i][j+1]

                vertexNormalData += [nA, nB, nC, nA, nC, nD]

                if colorFunction is None:
                    C1, C2, C3 = [1, 0, 0], [0, 1, 0], [0, 0, 1]
                    C4, C5, C6 = [0, 1, 1], [1, 0, 1], [1, 1, 0]
                    colorData += [C1, C2, C3, C4, C5, C6]
                else:
                    cA = colorFunction(i, j, uResolution, vResolution)
                    cB = colorFunction(i+1, j, uResolution, vResolution)
                    cC = colorFunction(i+1, j+1, uResolution, vResolution)
                    cD = colorFunction(i, j+1, uResolution, vResolution)
                    colorData += [cA, cB, cC, cA, cC, cD]

                uvA = uvGrid[i][j]
                uvB = uvGrid[i+1][j]
                uvC = uvGrid[i+1][j+1]
                uvD = uvGrid[i][j+1]
                flatUVs += [uvA, uvB, uvC, uvA, uvC, uvD]

                fn1 = calcNormal(pA, pB, pC)
                fn2 = calcNormal(pA, pC, pD)
                faceNormalData += [fn1, fn1, fn1, fn2, fn2, fn2]

        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexNormal", vertexNormalData)
        self.addAttribute("vec3", "faceNormal", faceNormalData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.addAttribute("vec2", "vertexUV", flatUVs)
        self.countVertices()

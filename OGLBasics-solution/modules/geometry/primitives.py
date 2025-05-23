"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from . import AbstractGeometry
import numpy as np

class RectangleGeometry(AbstractGeometry):
    """A primitive rectangle."""
    
    def __init__(self, width=1, height=1,
                 colorFunction=None):
        super().__init__()
        
        P0 = [-width/2, -height/2, 0]
        P1 = [ width/2, -height/2, 0]
        P2 = [-width/2, height/2, 0]
        P3 = [ width/2, height/2, 0]
        if colorFunction == None:
            C0, C1, C2, C3 = [1,1,1], [1,0,0], [0,1,0], [0,0,1]
        else:
            C0 = colorFunction(0,0,3.01,3.01)
            C1 = colorFunction(1,1,3.01,3.01)
            C2 = colorFunction(2,2,3.01,3.01)
            C3 = colorFunction(3,3,3.01,3.01)

        positionData = [P0,P1,P3, P0,P3,P2]
        colorData    = [C0,C1,C3, C0,C3,C2]
        
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        
        self.countVertices()

class BoxGeometry(AbstractGeometry):
    """A primitive box."""
    
    def __init__(self, 
                 width=1, height=1, depth=1, 
                 colorFunction=None):
        super().__init__()
        
        P0 = [-width/2, -height/2, -depth/2]
        P1 = [ width/2, -height/2, -depth/2]
        P2 = [-width/2, height/2, -depth/2]
        P3 = [ width/2, height/2, -depth/2]
        P4 = [-width/2, -height/2, depth/2]
        P5 = [ width/2, -height/2, depth/2]
        P6 = [-width/2, height/2, depth/2]
        P7 = [ width/2, height/2, depth/2]
        
        # colors for faces in order: x+, x-, y+, y-, z+, z
        if colorFunction == None:
            C1, C2 = [1, 0.5, 0.5], [0.5, 0, 0]
            C3, C4 = [0.5, 1, 0.5], [0, 0.5, 0]
            C5, C6 = [0.5, 0.5, 1], [0, 0, 0.5]
        else:
            
            C1, C2 = colorFunction(0,0,5.01,5.01), colorFunction(1,1,5.01,5.01)
            C3, C4 = colorFunction(2,2,5.01,5.01), colorFunction(3,3,5.01,5.01)
            C5, C6 = colorFunction(4,4,5.01,5.01), colorFunction(5,5,5.01,5.01)
        
        positionData = [ P5,P1,P3,P5,P3,P7, P0,P4,P6,P0,
                        P6,P2,P6,P7,P3,P6,P3,P2,
                        P0,P1,P5,P0,P5,P4,P4,P5,P7,
                        P4,P7,P6, P1,P0,P2,P1,P2,P3 ]
        colorData = [C1]*6 + [C2]*6 + [C3]*6 + [C4]*6 + [C5]*6 + [C6]*6
        
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        
        self.countVertices()

class PolygonGeometry(AbstractGeometry):
    """A primitive polygon."""
    
    def __init__(self, sides=3, radius=1, colorFunction=None):
        super().__init__()
        
        A = 2 * np.pi / sides
        positionData = []
        colorData    = []
        
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
            else:
                colorData.append([1,1,1])
                colorData.append(colorFunction(n,   n,   sides+1, sides+1))
                colorData.append(colorFunction(n+1, n+1, sides+1, sides+1))
            
        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        
        self.countVertices()
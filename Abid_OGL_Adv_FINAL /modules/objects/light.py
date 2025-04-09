from . import Object3D, Camera
from ..utils.vector import vec

from OpenGL.GL import *


class Light(Object3D):
    DIRECTIONAL = 1
    POINT = 2
    def __init__(self, color=vec(1,1,1),
                 attenuation=vec(1,0,0),
                 lightType = 1):
        super().__init__()
        self.lightType   = lightType
        self.color       = vec(*color)
        self.attenuation = vec(*attenuation)

class DirectionalLight(Light):
    def __init__(self, direction, color=vec(1,1,1),
                 resolution=[1600,1600],
                 cameraBounds=[-6, 6, -6, 6, -6, 6],
                 bias=0.005):
        super().__init__(color=color,
                         lightType=Light.DIRECTIONAL)
        
        self.setDirection(direction)
        
class PointLight(Light):
    def __init__(self, position, color=vec(1,1,1),
                 attenuation=vec(1,0,0.1)):
        super().__init__(color=color,
                         attenuation=attenuation,
                         lightType=Light.POINT)
        self.position = vec(*position)
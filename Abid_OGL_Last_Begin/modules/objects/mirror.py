"""Place in objects module and add to __init__ imports"""


from . import Camera
from ..materials import DepthMaterial, PhongMaterial
from ..oGL.renderTarget import RenderTarget
from ..utils.vector import normalize, magnitude, vec
from ..utils.definitions import EPSILON
from OpenGL.GL import *
import numpy as np

class Mirror(object):
    def __init__(self, position, normal,
                 resolution=[512,512],
                 size = [1,1]):
        super().__init__()
        self.camera = Camera()
        self.camera.setScaleAsymmetric(-1,1,1)
        
        self.position = vec(*position)
        self.normal = normalize(vec(*normal))
        self.size = np.array(size)
        self.up = vec(0,1,0)
        self.rt = normalize(np.cross(self.up, self.normal))
        self.up = normalize(np.cross(self.normal, self.rt))
        
        self.left   = position - self.rt * self.size[0] / 2
        self.right  = position + self.rt * self.size[0] / 2
        self.bottom = position - self.up * self.size[1] / 2
        self.top    = position + self.up * self.size[1] / 2
        
        self.renderTarget = RenderTarget(resolution,
                            properties={"wrap": GL_CLAMP_TO_BORDER} )
        
    
    def update(self, viewRig):
        
        self.camera.updateViewMatrix()        
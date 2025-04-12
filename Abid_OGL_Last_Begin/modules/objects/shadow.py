"""Place in objects module and add to __init__ imports"""


from . import Camera
from ..materials import DepthMaterial
from ..oGL.renderTarget import RenderTarget
from OpenGL.GL import *

class Shadow(object):
    
    def __init__(self, lightSource=None, strength=0.5,
                 resolution=[512,512],
                 cameraBounds=[-10, 10, -10, 10, -10, 10],
                 bias=0.01, dummy=False):
        super().__init__()
        self.dummy=dummy
        # must be directional light
        
        self.lightSource = lightSource
        # camera used to render scene from perspective of light
        self.camera = Camera()
        left, right, bottom, top, near, far = cameraBounds
        self.camera.setOrthographic(left, right, bottom, top, near, far)
        # self.lightSource.add(self.camera)
        if not self.dummy:
            self.camera.setRotate(*self.lightSource.rotation)
        
        # target used during the shadow pass,
        # contains depth texture
        self.renderTarget = RenderTarget(resolution,
                            properties={"wrap": GL_CLAMP_TO_BORDER} )
        # used to avoid visual artifacts
        # due to rounding/sampling precision issues
        self.bias = bias
    
    def getDirection(self):
        if self.dummy:
            return (0,0,0,0)
        return self.lightSource.getDirection()
    
    def updateDirection(self):
        if self.dummy:
            return
        self.camera.setRotate(*self.lightSource.rotation)
        self.camera.updateViewMatrix()
        
    
    
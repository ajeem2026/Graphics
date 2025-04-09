from . import AbstractMaterial
from OpenGL.GL import *

#mimic phong.py for this one 
class BumpMaterial(AbstractMaterial):
    def __init__(self, texture, bumpTexture, bumpStrength=1.0, properties={}, numLights=1, lambert=False):
        super().__init__(
            "bumpMap.vert", ["light.glsl","lightCalcPhong.frag", "bumpMap.frag"]
        )

        #textures base image and bump map
        self.addUniform("sampler2d", "textures", texture.textureRef)
        self.addUniform("sampler2d", "bumpTexture", bumpTexture.textureRef)

        for i in range(max(numLights, 1)):
            self.addUniform("light", f"light{i}", None)
        self.addUniform("int",   "numLights", numLights)
            
        #self.addUniform("vec3", "viewPosition", [0, 0, 0])
        self.addUniform("float", "ambMul", 0.3)
        self.addUniform("float", "specMul", 1.5)
        self.addUniform("float", "specularStrength", 1)
        self.addUniform("float", "shininess", 300)
        self.addUniform("bool", "useFaceNormals", True)
        #self.addUniform("bool", "shaded", True)
        
        #for image texture
        self.addUniform("bool", "useBumpTexture", True)
        self.addUniform("bool", "useVertexColors", False)
        self.addUniform("bool", "shaded", True)
        self.addUniform("vec3", "baseColor", [1.0, 1.0, 1.0])
        self.addUniform("vec2", "repeatUV", [1.0, 1.0])
        self.addUniform("vec2", "offsetUV", [0.0, 0.0])
        
    
        self.locateUniforms()
        
        # Render vertices as surface
        self.settings["drawStyle"] = GL_TRIANGLES
        
        # Render both sides? default: front side only
        # Vertices ordered counterclockwise
        self.settings["doubleSide"] = True
        
        # Render triangles as wireframe?
        self.settings["wireframe"] = False
        
        # Line thickness for wireframe rendering
        self.settings["lineWidth"] = 1
        
        
        self.setProperties(properties)
        
        
    def updateRenderSettings(self):
        if self.settings["doubleSide"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)
            
        if self.settings["wireframe"]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        glLineWidth(self.settings["lineWidth"])

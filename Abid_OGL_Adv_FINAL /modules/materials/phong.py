"""
Author: Liz Matthews
"""

from . import AbstractMaterial
from OpenGL.GL import *

class PhongMaterial(AbstractMaterial):
    
    def __init__(self, properties={}, numLights=1):        
        super().__init__("basicNormals.vert", ["light.glsl", "lightCalcPhong.frag", "phong.frag"])
        
        for i in range(max(numLights, 1)):
            self.addUniform("light", f"light{i}", None)
        self.addUniform("int",   "numLights", numLights)
            
        self.addUniform("vec3", "viewPosition", [0, 0, 0])
        self.addUniform("float", "ambMul", 0.3)
        self.addUniform("float", "specMul", 1.5)
        self.addUniform("float", "specularStrength", 1)
        self.addUniform("float", "shininess", 300)
        self.addUniform("bool", "useFaceNormals", True)
        self.addUniform("bool", "shaded", True)
    
        self.locateUniforms()
        
        # Render vertices as surface
        self.settings["drawStyle"] = GL_TRIANGLES
        
        # Render both sides? default: front side only
        # Vertices ordered counterclockwise
        self.settings["doubleSide"] = False
        
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

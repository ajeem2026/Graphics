"""Place in materials module and add to __init__ imports"""

from . import AbstractMaterial 
from OpenGL.GL import *

class DepthMaterial(AbstractMaterial):
    def __init__(self, texture=None, properties={}):
        vShaderCode = """
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
        in vec3 vertexPosition;
        void main() {
            gl_Position = projectionMatrix * viewMatrix *
                          modelMatrix * vec4(vertexPosition, 1);                         
          
        }
        """
        fShaderCode = """
        out vec4 fragColor;
        void main()
        {
            float z = gl_FragCoord.z;
            fragColor = vec4(z, z, z, 1);
        }
        """
        
        super().__init__(vShaderCode, fShaderCode)
        
        self.locateUniforms()
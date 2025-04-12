"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

from OpenGL.GL import *

class Uniform(object):
    
    TEXTURE_UNIT_REF = 0
    
    @classmethod
    def resetTextureUnit(cls):
        cls.TEXTURE_UNIT_REF = 0

    def __init__(self, dataType, data):
        # type of data:
        #  int | bool | float | vec2 | vec3 | vec4 | mat4
        self.dataType = dataType
        
        self.data = data
        
        self.variableRef = None
    
    def locateVariable(self, programRef, variableName):
        self.variableRef = glGetUniformLocation(programRef,
                                                variableName)
        if self.dataType == "light":
            self.variableRef = {}
            self.variableRef["lightType"] = glGetUniformLocation(
                programRef, "lightTypes"
            )
            self.variableRef["color"] = glGetUniformLocation(programRef, "lightColors")
            self.variableRef["direction"] = glGetUniformLocation(
                programRef, "lightDirections"
            )
            self.variableRef["position"] = glGetUniformLocation(
                programRef, "lightPositions"
            )
            self.variableRef["attenuation"] = glGetUniformLocation(
                programRef, "lightAttenuations"
            )
        else:
            self.variableRef = glGetUniformLocation(programRef, variableName)
    
    def uploadData(self):
        if self.variableRef == -1:
            return

        if self.dataType == "int":
            glUniform1i(self.variableRef, self.data)
        elif self.dataType == "bool":
            glUniform1i(self.variableRef, self.data)
        elif self.dataType == "float":
            glUniform1f(self.variableRef, self.data)
        elif self.dataType == "vec2":
            glUniform2f(self.variableRef, *self.data)
        elif self.dataType == "vec3":
            glUniform3f(self.variableRef, *self.data)
        elif self.dataType == "vec4":
            glUniform4f(self.variableRef, *self.data)
        elif self.dataType == "mat4":
            glUniformMatrix4fv(self.variableRef, 1, GL_TRUE, self.data)

        elif self.dataType == "light":
            index, data = self.data
            glUniform1i(self.variableRef["lightType"] + index, int(data.lightType))
            glUniform3f(self.variableRef["color"] + index, *data.color)
            direction = data.getDirection()
            glUniform3f(self.variableRef["direction"] + index, *direction[:3])
            position = data.getPosition()
            glUniform3f(self.variableRef["position"] + index, *position)
            glUniform3f(self.variableRef["attenuation"] + index, *data.attenuation)
        elif self.dataType == "sampler2d":
            #print(Uniform.TEXTURE_UNIT_REF)
            glActiveTexture(GL_TEXTURE0 + Uniform.TEXTURE_UNIT_REF)

            glBindTexture(GL_TEXTURE_2D, self.data)

            glUniform1i(self.variableRef, Uniform.TEXTURE_UNIT_REF)
                    
            Uniform.TEXTURE_UNIT_REF += 1
        
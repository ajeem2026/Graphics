import pygame

from OpenGL.GL import *

class Texture(object):
    def __init__(self, fileName=None, properties={}):
        self.surface = None
        
        self.textureRef = glGenTextures(1)
        
        self.properties = {
            "magFilter" : GL_LINEAR,
            "minFilter" : GL_LINEAR_MIPMAP_LINEAR,
            "wrap"      : GL_REPEAT
        }
        
        self.setProperties(properties)
        if fileName is not None:
            self.loadImage(fileName)
            self.uploadData()
            
    def loadImage(self, fileName):
        self.surface = pygame.image.load(fileName)
        
    # set property values
    def setProperties(self, props):
        for name, data in props.items():
            if name in self.properties.keys():
                self.properties[name] = data
                
            else: # unknown property type
                raise Exception("Texture has no property with" + \
                                f" name: {name}")
                
                
    def uploadData(self):
            width = self.surface.get_width()
            height = self.surface.get_height()
            
            pixelData = pygame.image.tostring(self.surface, "RGBA", 1)
            
            glBindTexture(GL_TEXTURE_2D, self.textureRef)
            
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                        0, GL_RGBA, GL_UNSIGNED_BYTE, pixelData)
            
            glGenerateMipmap(GL_TEXTURE_2D)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                            self.properties["magFilter"])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                            self.properties["minFilter"])
            
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,
                            self.properties["wrap"])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,
                            self.properties["wrap"])
            
            glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR,
                            [1,1,1,1])


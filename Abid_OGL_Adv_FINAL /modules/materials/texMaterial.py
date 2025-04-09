#from material.material import Material
from . import AbstractMaterial
from OpenGL.GL import *
class TextureMaterial(AbstractMaterial):
    def __init__(self, texture, shaded = False, properties={},numLights=1, lambert=False):


        # vertexShaderCode = """
        # uniform mat4 projectionMatrix;
        # uniform mat4 viewMatrix;
        # uniform mat4 modelMatrix;
        # uniform vec3 baseColor;
        # uniform vec2 repeatUV;
        # uniform vec2 offsetUV;
        # uniform bool useVertexColors;
        # uniform bool useFaceNormals;
        # in vec3 vertexColor;
        # in vec3 vertexPosition;
        # in vec3 vertexNormal;
        # in vec3 faceNormal;
        # in vec2 vertexUV;
        # out vec3 color;
        # out vec3 normal;
        # out vec3 position;
        # out vec2 UV;

        # void main() {
        #     gl_Position = projectionMatrix * viewMatrix *
        #             modelMatrix * vec4(vertexPosition, 1);

        #     position = vec3(modelMatrix * vec4(vertexPosition, 1));

        #     if (useFaceNormals)
        #         normal = normalize(mat3(modelMatrix) * faceNormal);
        #     else
        #         normal = normalize(mat3(modelMatrix) * vertexNormal);

        #     color = baseColor;
        #     if (useVertexColors)
        #         color *= vertexColor;

        #     UV = vertexUV * repeatUV + offsetUV;
        # }
        # """
        # fragmentShaderCode = """
        # uniform vec3 baseColor;
        # uniform sampler2D textures;
        # in vec2 UV;
        # out vec4 fragColor;

        # void main()
        # {
        #     vec4 color = vec4(baseColor, 1.0) * texture(textures, UV);
        #     if (color.a < 0.10)
        #         discard;
        #     fragColor = color;
        # }
        # """
        
        
        super().__init__("tex.vert", ["light.glsl","lightCalcPhong.frag","tex.frag"])

        # #for debugging overlapping textures 
        # #setting up a unit texture for each instance of textmAT and using them independently
        # from OpenGL.GL import GL_TEXTURE0
        # if textureUnit is None:
        #     from modules.oGL.uniform import Uniform
        #     textureUnit = Uniform.TEXTURE_UNIT_REF
        #     Uniform.TEXTURE_UNIT_REF += 1
        
        # self.textureUnit = textureUnit
        # self.texture = texture

        self.addUniform("vec3", "baseColor", [1.0,
                                            1.0, 1.0])
        #self.addUniform("sampler2D", "textures", texture.textureRef)
        self.addUniform("sampler2d", "textures", texture.textureRef)

        self.addUniform("vec2", "repeatUV", [1.0,
                                            1.0])
        self.addUniform("vec2", "offsetUV", [0.0,
                                            0.0])
        
        for i in range(max(numLights, 1)):
            self.addUniform("light", f"light{i}", None)
            self.addUniform("int",   "numLights", numLights)
            
        self.addUniform("bool", "shaded", True)

        self.locateUniforms()
        # render both sides?
        self.settings["doubleSide"] = True
        # render triangles as wireframe?
        self.settings["wireframe"] = False
        # line thickness for wireframe rendering
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


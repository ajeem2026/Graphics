uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform mat4 modelMatrix;
uniform vec3 baseColor;
uniform vec2 repeatUV;
uniform vec2 offsetUV;
uniform bool useVertexColors;
uniform bool useFaceNormals;
in vec3 vertexColor;
in vec3 vertexPosition;
in vec3 vertexNormal;
in vec3 faceNormal;
in vec2 vertexUV;
out vec3 color;
out vec3 normal;
out vec3 position;
out vec2 UV;

void main() {
    gl_Position = projectionMatrix * viewMatrix *
        modelMatrix * vec4(vertexPosition, 1);

    position = vec3(modelMatrix * vec4(vertexPosition, 1));

    if(useFaceNormals)
        normal = normalize(mat3(modelMatrix) * faceNormal);
    else
        normal = normalize(mat3(modelMatrix) * vertexNormal);

    color = baseColor;
    if(useVertexColors)
        color *= vertexColor;

    UV = vertexUV * repeatUV + offsetUV;
}
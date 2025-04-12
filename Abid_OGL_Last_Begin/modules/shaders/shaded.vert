uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform mat4 modelMatrix;
uniform vec3 baseColor;
uniform bool useVertexColors;
uniform bool useFaceNormals;2
in vec3 vertexPosition;
in vec3 vertexColor;
in vec3 faceNormal;
in vec3 vertexNormal;
out vec3 color;
out vec3 normal;
out vec3 position;


void main() {
    gl_Position = projectionMatrix * viewMatrix *
              modelMatrix * vec4(vertexPosition, 1);           
    position = vec3(modelMatrix * vec4(vertexPosition,1));
    
    if (useFaceNormals)
        normal =normalize(mat3(modelMatrix)*faceNormal);
    else
        normal =normalize(mat3(modelMatrix)*vertexNormal);
    
    color = baseColor;
    if (useVertexColors)
        color *= vertexColor;    
}

uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform mat4 modelMatrix;
uniform vec3 baseColor;
uniform bool useVertexColors;
in vec3 vertexPosition;
in vec3 vertexColor;
out vec3 color;
void main() {
    gl_Position = projectionMatrix * viewMatrix *
                  modelMatrix * vec4(vertexPosition, 1);
                  
    
    color = baseColor;
    if (useVertexColors)
        color *= vertexColor;
    
}

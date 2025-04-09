
uniform float ambMul; 
in vec3 position;
in vec3 normal;
in vec3 color;
out vec4 fragColor;
void main()
{
    vec3 diffuse = color;
    vec3 total = diffuse * ambMul;
    for (int i = 0; i < min(MAX_LIGHTS, numLights); i++) {
        total = lightCalc(i, total, diffuse,
                          position, normal);            
    }  

    
    fragColor = vec4(total, 1);
}

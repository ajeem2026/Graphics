uniform float ambMul; 
uniform float specMul;
in vec3 position;
in vec3 normal;
in vec3 color;
out vec4 fragColor;
void main()
{
    vec3 diffuse = color;
    vec3 specular = (diffuse + vec3(0.1,0.1,0.1)) * specMul;
    vec3 total = diffuse * ambMul;
    for (int i = 0; i < min(MAX_LIGHTS, numLights); i++) {
        total = lightCalc(i, total, diffuse, specular,
                          position, normal);            
    }  

    
    fragColor = vec4(total, 1);
}

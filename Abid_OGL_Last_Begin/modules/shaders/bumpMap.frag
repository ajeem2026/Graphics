uniform sampler2D bumpTexture;
uniform sampler2D textures;
uniform bool useBumpTexture;
uniform bool useLambert;
uniform vec3 baseColor;
uniform float ambMul;
uniform float specMul;
in vec3 color;
in vec3 normal;
in vec3 bitangent;
in vec3 position;
in vec2 UV;
out vec4 fragColor;

void main()
{
    vec3 norm = normal;
    vec3 tangent = normalize(cross(bitangent, norm));
    mat3 TBN = mat3(tangent, bitangent, norm);
    vec3 bump = texture(bumpTexture, UV).rgb * 2.0 - 1.0;

    norm = normalize(TBN * bump);

    vec3 diffuse = color;
    vec3 specular = (diffuse + vec3(0.1, 0.1, 0.1)) * specMul;
    vec3 total = diffuse * ambMul;
    for (int i = 0; i < min(MAX_LIGHTS, numLights); i++) {
        total = lightCalc(i, total, diffuse, specular,
                position, norm);
    }

    fragColor = vec4(total, 1.0) * texture(textures, UV);
}
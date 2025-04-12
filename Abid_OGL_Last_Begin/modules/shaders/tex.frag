uniform vec3 baseColor;
uniform sampler2D textures;
in vec2 UV;
out vec4 fragColor;

void main()
    {
        vec4 color = vec4(baseColor, 1.0) * texture(textures, UV);
        if (color.a < 0.10)
            discard;
        fragColor = color;
    }
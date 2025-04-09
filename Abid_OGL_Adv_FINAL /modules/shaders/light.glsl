
const int MAX_LIGHTS = 4;

uniform int numLights;
uniform int lightTypes[MAX_LIGHTS];
uniform vec3 lightColors[MAX_LIGHTS];
uniform vec3 lightDirections[MAX_LIGHTS];
uniform vec3 lightPositions[MAX_LIGHTS];
uniform vec3 lightAttenuations[MAX_LIGHTS];
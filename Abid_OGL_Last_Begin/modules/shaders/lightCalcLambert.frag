vec3 lightCalc(int lightIndex,
               vec3 startingColor,
               vec3 diffuse,
               vec3 pointPosition,
               vec3 pointNormal)
{

    int  lType = lightTypes[lightIndex];
    vec3 lColor = lightColors[lightIndex];
    vec3 lDirection = lightDirections[lightIndex];
    vec3 lPosition = lightPositions[lightIndex];
    vec3 lAttenuation = lightAttenuations[lightIndex];
    
    
    vec3 totalColor = startingColor;
    
    
    return lColor * totalColor;
}
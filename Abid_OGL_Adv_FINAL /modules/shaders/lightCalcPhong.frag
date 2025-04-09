uniform vec3 viewPosition;
uniform float specularStrength;
uniform float shininess;

// Set variables for totalColor, diffuseValue, specularValue, attenuation, lightDirection

vec3 lightCalc(int lightIndex,
               vec3 startingColor,
               vec3 diffuse,
               vec3 specular,
               vec3 pointPosition,
               vec3 pointNormal)
{

    int  lType = lightTypes[lightIndex];
    vec3 lColor = lightColors[lightIndex];
    vec3 lDirection = lightDirections[lightIndex];
    vec3 lPosition = lightPositions[lightIndex];
    vec3 lAttenuation = lightAttenuations[lightIndex];
    
    vec3 totalColor = startingColor;
    float attenuation = 1.0;

    // Calculate attenuation and light direction

//If the light's type is a directional light:
// Set lightDirection to the normalized value of the light parameter's direction
    if(lType==1){
        lDirection= normalize(lDirection);
    } 

//Otherwise, the light is a point light:
    else {
//Set lightDirection to the normalized value of a vector from the light's position to the point's position
        lDirection= normalize(pointPosition-lPosition);

//Set attenuation, using the light's attenuation values and distance to the light's position
        float distance=length(lPosition-pointPosition);
        attenuation=1.0/(lAttenuation.x+lAttenuation.y*distance+lAttenuation.z*distance*distance);
    }

// normalize point normal and Calculate the diffuse value as max(dot(pointNormal, lightDirection), 0.0)
    float diffValue= max(dot(normalize(pointNormal), -lDirection),0.0);

//Multiply the diffuse value by the attenuation value
    diffValue*=attenuation;

    // Calculate the total color increase for diffuse and add it to total color
    
    totalColor+=(diffuse-totalColor)*diffValue;

    //If the diffuse value is greater than zero:
    if (diffValue > 0)
    {
        // Calculate the normalized view direction
        vec3 viewDir= normalize(viewPosition-pointPosition);
        // Calculate the reflected direction
        vec3 reflectDir= reflect(lDirection, normalize(pointNormal));
        // Calculate the specular value as max(dot(viewDirection, reflectDirection), 0.0)
        float specularValue=max(dot(viewDir,reflectDir),0.0);
        //Set the specular value equal to the specular strength times the specular value taken to the power of shininess
        // Calculate final specular value 
        float specFinal=specularStrength*pow(specularValue,shininess);
        
        // Calculate the total color increase for specular and add it to total color
        totalColor+=(specular-totalColor)*specFinal;

    }

    // Return the total color times the light's color
    return totalColor * lColor;

}
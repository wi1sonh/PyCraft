#version 410 core

layout (location = 0) out vec4 fragColor;

const vec3 CLOUD_COLOR = vec3(1);
const float FADING_FACTOR = -0.00001;

uniform vec3 u_bg_color;

void main() {
    // fading
    float dist = gl_FragCoord.z / gl_FragCoord.w;
    vec3 col = mix(CLOUD_COLOR, u_bg_color, 1.0 - exp(FADING_FACTOR * dist * dist));

    fragColor = vec4(col, 0.8);
}
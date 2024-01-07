#version 410 core

layout (location = 0) out vec4 fragColor;

const vec3 GAMMA = vec3(2.2);
const vec3 GAMMA_INV = 1 / GAMMA;
const vec3 WATER_COLOR = vec3(0.0, 0.3, 1.0);

const float FADING_FACTOR = -0.00001;  // fading 

uniform sampler2DArray u_texture_array_0;
uniform vec3 u_bg_color;

in vec3 block_color;
in vec2 uv;
in float shading;

flat in int face_id;
flat in int block_id;


void main(){
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;
    vec3 tex_color = texture(u_texture_array_0, vec3(face_uv, block_id)).rgb;

    // gamma correction
    tex_color = pow(tex_color, GAMMA);

    vec3 tex_color_flat = tex_color;

    tex_color *= shading;

    // inverse gamma correction 1
    tex_color_flat = pow(tex_color, GAMMA_INV);

    // fog fading
    float dist = gl_FragCoord.z / gl_FragCoord.w;
    tex_color = mix(tex_color, u_bg_color, (1.0 - exp2(FADING_FACTOR * dist * dist)));

    // inverse gamma correction 2
    tex_color = pow(tex_color, GAMMA_INV);

    fragColor = vec4(tex_color, 1);
    vec4 fragFlatColor = vec4(tex_color_flat, 1);
    fragColor.a = (fragFlatColor.r + fragFlatColor.b + fragFlatColor.g <= 0.1) ? 0.0: 1.0;

    if (block_id == 8){
        fragColor.a = 0.5;
    }
}
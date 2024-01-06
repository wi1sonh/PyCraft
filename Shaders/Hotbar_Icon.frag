#version 410 core

layout (location = 0) out vec4 fragColor;

const int face_id = 2;
const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

uniform sampler2DArray u_texture_array_0;
uniform int voxel_id;

in vec2 uv;

void main(){
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

    vec3 tex_col = texture(u_texture_array_0, vec3(face_uv, voxel_id)).rgb;

    fragColor = vec4(tex_col, 1);
}
#version 410 core

layout (location = 0) out vec4 fragColor;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;
uniform vec3 bg_color;

uniform sampler2DArray u_texture_array_0;

in vec3 voxel_color;
in vec2 uv;
in float shading;

flat in int face_id;
flat in int voxel_id;

void main(){
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

    vec3 tex_col = texture(u_texture_array_0, vec3(face_uv, voxel_id)).rgb;
    tex_col = pow(tex_col, gamma);
    vec3 tex_col_flat = tex_col;

    tex_col *= shading;

    tex_col_flat = pow(tex_col, inv_gamma);

    //fog
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    tex_col = mix(tex_col, bg_color, (1.0 - exp2(-0.00001 * fog_dist * fog_dist)));

    tex_col = pow(tex_col, inv_gamma);

    fragColor = vec4(tex_col, 1);

    vec4 fragFlatColor = vec4(tex_col_flat, 1);
    fragColor.a = (fragFlatColor.r + fragFlatColor.b + fragFlatColor.g <= 0.1) ? 0.0: 1.0;

    if (voxel_id == 8){
        fragColor.a = 0.5;
    }


}
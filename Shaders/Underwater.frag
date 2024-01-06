#version 410 core

layout (location = 0) out vec4 fragColor;

uniform sampler2D u_texture_0;

in vec2 uv;

void main(){

    fragColor = texture(u_texture_0, uv);
}
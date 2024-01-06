#version 410 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 tex_coords;

out vec2 uv;

void main() {
    uv = vec2(tex_coords.x, tex_coords.y);
    gl_Position = vec4(in_position, 1.0);
}
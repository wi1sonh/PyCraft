#version 410 core

layout (location = 0) in vec2 in_tex_coord_0;
layout (location = 1) in vec3 in_position;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

out vec3 marker_color;
out vec2 uv;

void main(){
    uv = in_tex_coord_0;
    marker_color = vec3(0.5, 0.5, 0.5);
    
    gl_Position = m_proj * m_view * m_model * vec4((in_position - 0.5) * 1.01 + 0.5, 1.0);
}
#version 410 core

layout (location = 0) in vec3 in_position;

uniform mat4 m_proj;
uniform mat4 m_view;

uniform int u_center;
uniform float u_time;
uniform float u_cloud_scale;

void main() {
    vec3 pos = vec3(in_position);
    
    pos.xz -= u_center;
    pos.xz *= u_cloud_scale;
    pos.xz += u_center;

    // dynamic movement
    float time = 3000 * sin(0.01 * u_time);
    pos.xz += time;
    gl_Position = m_proj * m_view * vec4(pos, 1.0);
}
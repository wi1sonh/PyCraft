from Settings import *
from Frustum import Frustum

class Camera:
    def __init__(self, position, yaw, pitch):
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)

        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0 , 0)
        self.forward = glm.vec3(0, 0, -1)

        self.m_proj = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.m_view = glm.mat4()

        self.frustum = Frustum(self)

    def update(self):
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def update_vectors(self):
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self. up = glm.normalize(glm.cross(self.right, self.forward))

    def rotate_pitch(self, delta_y):
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x):
        self.yaw += delta_x

    def move_left(self, velocity):
        leftaabb = self.app.scene.get_voxel_id(glm.ivec3(self.position - self.right )- glm.ivec3(0, 1, 0))[0]
        if  leftaabb == VOID or leftaabb == WATER or leftaabb >= 45:
            self.position -= self.right * velocity

    def move_right(self, velocity):
        rightaabb = self.app.scene.get_voxel_id(glm.ivec3(self.position + self.right )- glm.ivec3(0, 1, 0))[0]
        if rightaabb == VOID or rightaabb == WATER or rightaabb >= 45:
            self.position += self.right * velocity

    def move_up(self, velocity):
        upaabb = self.app.scene.get_voxel_id(glm.ivec3(self.position))[0]
        if upaabb == VOID or upaabb == WATER or upaabb >= 45:
            self.position += glm.vec3(0, 1, 0) * 0.5 * 0.98

    def move_down(self, velocity):
        downaabb = self.app.scene.get_voxel_id(glm.ivec3(self.position - glm.vec3(0, 2, 0)))[0]
        if downaabb == VOID or downaabb == WATER or downaabb >= 45:
            self.position -= glm.vec3(0, 1, 0) * velocity * 10

    def move_forward(self, velocity):
        forwardaabb = self.app.scene.get_voxel_id(glm.ivec3(self.position + glm.normalize(glm.vec3(self.forward.x, 0, self.forward.z))) - glm.ivec3(0, 1, 0))[0]
        if forwardaabb == VOID or forwardaabb == WATER or forwardaabb >= 45:
            self.position += glm.normalize(glm.vec3(self.forward.x, 0, self.forward.z)) * velocity


    def move_back(self, velocity):
        backaabb = self.app.scene.get_voxel_id(glm.ivec3(self.position - glm.normalize(glm.vec3(self.forward.x, 0, self.forward.z))) - glm.ivec3(0, 1, 0))[0]
        if backaabb == VOID or backaabb == WATER or backaabb >= 45:
            self.position -= glm.normalize(glm.vec3(self.forward.x, 0, self.forward.z)) * velocity


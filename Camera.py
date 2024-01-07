from Constants import *


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

    # 左移
    def move_left(self, velocity):
        leftaabb = self.app.scene.get_block_id(glm.ivec3(self.position - self.right )- glm.ivec3(0, 1, 0))[0]
        if  leftaabb == VOID or leftaabb == WATER or leftaabb >= 45:
            self.position -= self.right * velocity

    # 右移
    def move_right(self, velocity):
        rightaabb = self.app.scene.get_block_id(glm.ivec3(self.position + self.right )- glm.ivec3(0, 1, 0))[0]
        if rightaabb == VOID or rightaabb == WATER or rightaabb >= 45:
            self.position += self.right * velocity

    # 跳跃(起飞)
    def move_up(self, velocity):
        upaabb = self.app.scene.get_block_id(glm.ivec3(self.position))[0]
        if upaabb == VOID or upaabb == WATER or upaabb >= 45:
            self.position += glm.vec3(0, 1, 0) * 0.05 * 0.98

    # 下降
    def move_down(self, velocity):
        downaabb = self.app.scene.get_block_id(glm.ivec3(self.position - glm.vec3(0, 2, 0)))[0]
        if downaabb == VOID or downaabb == WATER or downaabb >= 45:
            self.position -= glm.vec3(0, 1, 0) * velocity * 10

    # 前进
    def move_forward(self, velocity):
        forwardaabb = self.app.scene.get_block_id(glm.ivec3(self.position + glm.normalize(glm.vec3(self.forward.x, 0, self.forward.z))) - glm.ivec3(0, 1, 0))[0]
        if forwardaabb == VOID or forwardaabb == WATER or forwardaabb >= 45:
            self.position += glm.normalize(glm.vec3(self.forward.x, 0, self.forward.z)) * velocity

    # 后退
    def move_back(self, velocity):
        backaabb = self.app.scene.get_block_id(glm.ivec3(self.position - glm.normalize(glm.vec3(self.forward.x, 0, self.forward.z))) - glm.ivec3(0, 1, 0))[0]
        if backaabb == VOID or backaabb == WATER or backaabb >= 45:
            self.position -= glm.normalize(glm.vec3(self.forward.x, 0, self.forward.z)) * velocity


class Frustum:
    def __init__(self, camera):
        self.camera = camera

        self.factor_y = 1.0 / math.cos(V_FOV * 0.5)
        self.tan_y = math.tan(V_FOV * 0.5)

        self.factor_x = 1.0 / math.cos(H_FOV * 0.5)
        self.tan_x = math.tan(H_FOV * 0.5)

    def is_on_frustum(self, chunk):
        # 球心距离向量
        sphere_vec = chunk.center - self.camera.position

        # 近远平面之外
        sphere_z = glm.dot(sphere_vec, self.camera.forward)
        if not (NEAR - CHUNK_SPHERE_RADIUS <= sphere_z <= FAR + CHUNK_SPHERE_RADIUS):
            return False

        # 上下
        sphere_y = glm.dot(sphere_vec, self.camera.up)
        dist_y = self.factor_y * CHUNK_SPHERE_RADIUS + sphere_z * self.tan_y
        if not (-dist_y <= sphere_y <= dist_y):
            return False

        # 左右
        sphere_x = glm.dot(sphere_vec, self.camera.right)
        dist_x = self.factor_x * CHUNK_SPHERE_RADIUS + sphere_z * self.tan_x
        if not (-dist_x <= sphere_x <= dist_x):
            return False

        return True


import pygame as pg
from camera import Camera
from settings import *


class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app
        self.voxels = None
        super().__init__(position, yaw, pitch)

    def hit_detection_chunk(self, voxels_chunk, x1, y1, z1):
        index_c = x1 + CHUNK_SIZE * z1 + CHUNK_AREA * y1
        if index_c >= len(voxels_chunk):
            return 0
        if voxels_chunk[index_c] == 0 or voxels_chunk[index_c] is None:
            return 0
        else:
            return 1

    def hit_detection(self, pre_positon, position):
        x = int(position.x) // CHUNK_SIZE
        y = int(position.y) // CHUNK_SIZE
        z = int(position.z) // CHUNK_SIZE
        # index = x + WORLD_W * z + WORLD_AREA * y
        index_w = x + WORLD_W * z + WORLD_AREA * y
        if index_w > len(self.voxels):
            return 0
        voxels_chunk = self.voxels[index_w]
        x1 = int(position.x) % CHUNK_SIZE
        y1 = int(position.y) % CHUNK_SIZE
        z1 = int(position.z) % CHUNK_SIZE
        index_c = x1 + CHUNK_SIZE * z1 + CHUNK_AREA * y1
        if index_c > len(self.voxels[index_w]):
            return 0
        return self.hit_detection_chunk(voxels_chunk, x1, y1, z1)

    def update(self):
        self.keyboard_control()
        self.mouse_control()
        super().update()

    def handle_event(self, event):
        # adding and removing voxels with clicks
        if event.type == pg.MOUSEBUTTONDOWN:
            voxel_handler = self.app.scene.world.voxel_handler
            if event.button == 1:
                voxel_handler.set_voxel()
            if event.button == 3:
                voxel_handler.switch_mode()

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

    def is_water(self):
        x = int(self.position.x / CHUNK_SIZE)
        y = int(self.position.y / CHUNK_SIZE)
        z = int(self.position.z / CHUNK_SIZE)
        index_w = x + WORLD_W * z + WORLD_AREA * y
        if index_w > len(self.voxels):
            return 0
        voxels_chunk = self.voxels[index_w]
        x1 = int(self.position.x) % CHUNK_SIZE
        y1 = int(self.position.y) % CHUNK_SIZE
        z1 = int(self.position.z) % CHUNK_SIZE
        index_c = x1 + CHUNK_SIZE * z1 + CHUNK_AREA * y1
        if index_c > len(self.voxels[index_w]):
            return 0
        if (voxels_chunk[index_c] == 0 or voxels_chunk[index_c] is None) and self.position.y < WATER_LINE:
            return 1
        else:
            return 0

    def keyboard_control(self):
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.app.delta_time
        positon = glm.vec3(self.position.x, self.position.y, self.position.z)
        position1 = glm.vec3(self.position.x, self.position.y, self.position.z)
        up = glm.vec3(0, 1, 0)
        right = glm.vec3(1, 0, 0)
        forward = glm.vec3(0, 0, -1)
        # if result == 1:
        #    vel *= 0.2
        if key_state[pg.K_UP] or key_state[pg.K_w]:
            position1 += forward * vel
        if key_state[pg.K_DOWN] or key_state[pg.K_s]:
            position1 -= forward * vel
        if key_state[pg.K_RIGHT] or key_state[pg.K_d]:
            position1 += right * vel
        if key_state[pg.K_LEFT] or key_state[pg.K_a]:
            position1 -= right * vel
        if key_state[pg.K_1] or key_state[pg.K_KP1]:
            position1 += up * vel
        if key_state[pg.K_0] or key_state[pg.K_KP0]:
            position1 -= up * vel

        position1.x += 0.2
        result1 = self.hit_detection(positon, position1)
        position1.x -= 0.4
        result2 = self.hit_detection(positon, position1)
        position1.x += 0.2
        position1.y += 0.5
        result3 = self.hit_detection(positon, position1)
        position1.y -= 1
        result4 = self.hit_detection(positon, position1)
        position1.y += 0.5
        position1.z += 0.2
        result5 = self.hit_detection(positon, position1)
        position1.z -= 0.4
        result6 = self.hit_detection(positon, position1)
        position1.z += 0.2
        if max(result1, result2, result3, result4, result5, result6) == 1:
            return

        if self.is_water():
            vel = vel*0.5
        if key_state[pg.K_UP] or key_state[pg.K_w]:
            self.move_forward(vel)
        if key_state[pg.K_DOWN] or key_state[pg.K_s]:
            self.move_back(vel)
        if key_state[pg.K_RIGHT] or key_state[pg.K_d]:
            self.move_right(vel)
        if key_state[pg.K_LEFT] or key_state[pg.K_a]:
            self.move_left(vel)
        if key_state[pg.K_1] or key_state[pg.K_KP1]:
            self.move_up(vel)
        if key_state[pg.K_0] or key_state[pg.K_KP0]:
            self.move_down(vel)

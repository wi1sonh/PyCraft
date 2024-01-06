import pygame as pg
from Camera import Camera
from Settings import *

class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app
        super().__init__(position, yaw, pitch)
        #self.underwater_mesh = UnderwaterMesh(app)
        self.open_inventory = False
        self.underwater = False
        self.vel = PLAYER_SPEED
        self.action = 0
        # if self.app.scene:
        #     self.chunks = self.app.scene.world.chunks


    def update(self, pg):
        self.keyboard_controls()
        self.mouse_control(pg)
        super().update()

        # player_pos = glm.ivec3(int(self.position.x),int(self.position.y), int(self.position.z))
        # voxel_id = self.get_voxel_id(player_pos)

        # if self.chunks:
        # voxel_type = self.get_voxel_id(self.position)
        # print("Voxel Type: ", voxel_type)

        # if voxel_type[0] == VOID:
        #     self.position.y = self.position.y - 0.5
        # else:
        #     self.app.player.underwater = False

    def render(self):
        pass
        #self.underwater_mesh.render()

    def get_voxel_id(self, voxel_world_pos):
        cx, cy, cz = chunk_pos = voxel_world_pos / CHUNK_SIZE

        if 0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D:
            chunk_index = int(cx + WORLD_W * cz + WORLD_AREA * cy)
            chunk = self.chunks[chunk_index]

            lx, ly, lz = voxel_local_pos = voxel_world_pos - chunk_pos * CHUNK_SIZE

            voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
            voxel_id = chunk.voxels[voxel_index]

            return voxel_id, voxel_index, voxel_local_pos, chunk
        return 0, 0, 0, 0

    def handle_event(self, event, pg):
        voxel_handler = self.app.scene.world.voxel_handler
        inventory = self.app.scene.inventory

        # 打开背包
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                inventory.toggle_visible()
                self.open_inventory = 1 - self.open_inventory
                if self.open_inventory:
                    pg.mouse.set_visible(True)
                else:
                    pg.mouse.set_visible(False)
                    pg.mouse.set_pos(WIN_RES.x / 2, WIN_RES.y / 2)
                    pg.mouse.get_rel()

        # 鼠标按下
        if event.type == pg.MOUSEBUTTONDOWN:
            self.action = 1

            if event.button == 1:      # 左键 移除方块
                voxel_handler.remove_voxel(pg, self.app.sounds)
            if event.button == 3:      # 右键 放置方块
                voxel_handler.add_voxel(pg, self.app.sounds)

        # 鼠标释放,恢复手形
        if event.type == pg.MOUSEBUTTONUP:
            self.action = 0

        # 键盘快捷键切换物品
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last1)
                self.app.scene.hotbar.select = 1
            if event.key == pg.K_2:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last2)
                self.app.scene.hotbar.select = 2
            if event.key == pg.K_3:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last3)
                self.app.scene.hotbar.select = 3
            if event.key == pg.K_4:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last4)
                self.app.scene.hotbar.select = 4
            if event.key == pg.K_5:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last5)
                self.app.scene.hotbar.select = 5
            if event.key == pg.K_6:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last6)
                self.app.scene.hotbar.select = 6
            if event.key == pg.K_7:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last7)
                self.app.scene.hotbar.select = 7
            if event.key == pg.K_8:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last8)
                self.app.scene.hotbar.select = 8
            if event.key == pg.K_9:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last9)
                self.app.scene.hotbar.select = 9
            # 调试模式, 切换所有其他物品
            if event.key == pg.K_F1:
                voxel_handler.set_voxel_id(voxel_handler.new_voxel_id + 1)
            if event.key == pg.K_F2:
                voxel_handler.set_voxel_id(voxel_handler.new_voxel_id - 1)


        # 鼠标滚轮切换物品
        if event.type == pg.MOUSEWHEEL:
            # print(event.x, event.y)
            if event.y == 1:
                # voxel_handler.set_voxel_id(voxel_handler.new_voxel_id + 1)
                self.app.scene.hotbar.select -= 1
                if self.app.scene.hotbar.select == 0:
                    self.app.scene.hotbar.select = 9

            if event.y == -1:
                # voxel_handler.set_voxel_id(voxel_handler.new_voxel_id - 1)
                self.app.scene.hotbar.select += 1
                if self.app.scene.hotbar.select == 10:
                    self.app.scene.hotbar.select = 1

            if self.app.scene.hotbar.select == 1:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last1)
            if self.app.scene.hotbar.select == 2:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last2)
            if self.app.scene.hotbar.select == 3:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last3)
            if self.app.scene.hotbar.select == 4:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last4)
            if self.app.scene.hotbar.select == 5:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last5)
            if self.app.scene.hotbar.select == 6:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last6)
            if self.app.scene.hotbar.select == 7:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last7)
            if self.app.scene.hotbar.select == 8:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last8)
            if self.app.scene.hotbar.select == 9:
                voxel_handler.set_voxel_id(self.app.scene.hotbar.last9)



    # 鼠标移动控制视角变换
    def mouse_control(self, pg):
        if self.open_inventory:
            return

        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

        pg.mouse.set_pos(WIN_RES.x / 2, WIN_RES.y / 2)

    def keyboard_controls(self):
        if self.open_inventory:
            return

        key_state = pg.key.get_pressed()

        # 加速
        if key_state[pg.K_LCTRL]:
            self.vel = 2 * PLAYER_SPEED * self.app.delta_time
        else:
            self.vel = PLAYER_SPEED * self.app.delta_time

        if key_state[pg.K_w]: # 前进
            self.move_forward(self.vel)
        if key_state[pg.K_s]: # 后退
            self.move_back(self.vel)
        if key_state[pg.K_a]: # 左走
            self.move_left(self.vel)
        if key_state[pg.K_d]: # 右走
            self.move_right(self.vel)
        if key_state[pg.K_SPACE]: # 跳跃(起飞)
            self.move_up(self.vel * self.app.delta_time * 0.098 * 5)
        if key_state[pg.K_f]: # 下降
            self.move_down(self.vel)
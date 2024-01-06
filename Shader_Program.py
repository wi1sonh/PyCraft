from Settings import *

# 用于初始化以及更新可编程渲染管线的相关参数
class ShaderProgram:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.player = app.player

        #---------shaders-------------#
        self.chunk        = self.get_program(shader_name='Chunk')
        self.voxel_marker = self.get_program(shader_name='Voxel_Marker')
        self.quad         = self.get_program(shader_name='Quad')
        self.hotbar       = self.get_program(shader_name='Hotbar')
        self.hotbar_icon  = self.get_program(shader_name='Hotbar_Icon')
        self.inventory    = self.get_program(shader_name='Inventory')
        self.underwater   = self.get_program(shader_name='Underwater')
        self.clouds       = self.get_program(shader_name='Clouds')
        self.hand         = self.get_program(shader_name='Hand')
        self.select       = self.get_program(shader_name='Hotbar')
        #-----------------------------#

        # 开始初始化
        self.set_uniforms_on_init()

    # 初始化可编程渲染管线的参数
    def set_uniforms_on_init(self):

        # 用于定位方块的方框
        self.voxel_marker['m_proj'].write(self.player.m_proj)
        self.voxel_marker['m_model'].write(glm.mat4())
        self.voxel_marker['u_texture_0'] = 0
        # 区块
        self.chunk['m_proj'].write(self.player.m_proj)
        self.chunk['bg_color'].write(BG_COLOR)
        self.chunk['m_model'].write(glm.mat4())
        self.chunk['u_texture_array_0'] = 1
        # 准星
        self.quad['u_texture_0'] = 2
        # 物品栏
        self.hotbar['u_texture_0'] = 3
        # 物品栏的物品
        self.hotbar_icon['u_texture_array_0'] = 1
        # 背包
        self.inventory['u_texture_0'] = 5
        # 水下后处理
        self.underwater['u_texture_0'] = 6
        # 手
        self.hand['u_texture_0'] = 7
        # 物品栏框选
        self.select['u_texture_0'] = 8
        # 云
        self.clouds['m_proj'].write(self.player.m_proj)
        self.clouds['center'] = CENTER_XZ
        self.clouds['bg_color'].write(BG_COLOR)
        self.clouds['cloud_scale'] = CLOUD_SCALE

    # 需要实时更新给可编程渲染管线的参数, 即玩家的观察视角
    def update(self):
        self.chunk['m_view'].write(self.player.m_view)
        self.voxel_marker['m_view'].write(self.player.m_view)
        self.clouds['m_view'].write(self.player.m_view)

    # 获取可编程渲染管线的文件内容
    def get_program(self, shader_name):

        with open(f'Shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'Shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        # 将顶点着色器和片段着色器绑定到一个program中
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
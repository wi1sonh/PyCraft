import pygame as pg  # 可用于图像加载
import moderngl as mgl # 可用于纹理管理

class Textures:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx

        # 加载材质
        self.texture_0           = self.load('Frame.png')
        self.texture_array_0     = self.load('Tex_Array.png', is_tex_array=True)
        self.crosshair_texture   = self.load('Crosshair.png')
        self.hotbar_texture      = self.load('Item_Frame.png')
        self.hotbar_icon_texture = self.load('Bricks.png')
        self.inventory_texture   = self.load('Inventory.png')
        self.underwater_texture  = self.load('Underwater.png')
        self.hand_texture        = self.load('Hand.png')
        self.select_texture      = self.load('Select.png')

        # 将纹理分配给特定的纹理单元，以便在渲染过程中使用
        self.texture_0.use(location=0)
        self.texture_array_0.use(location=1)
        self.crosshair_texture.use(location=2)
        self.hotbar_texture.use(location=3)
        self.hotbar_icon_texture.use(location=4)
        self.inventory_texture.use(location=5)
        self.underwater_texture.use(location=6)
        self.hand_texture.use(location=7)
        self.select_texture.use(location=8)

    def load(self, file_name, is_tex_array=False):
        # 加载图像文件，并将图像调整为水平翻转
        texture = pg.image.load(f'Resources/{file_name}')
        texture = pg.transform.flip(texture, flip_x=True, flip_y=False)

        # 如果需要将纹理作为纹理数组加载，计算纹理层数（每个层3个纹理）
        if is_tex_array:
            num_layers = 3 * texture.get_height() // texture.get_width()  # 计算总共有多少层
            # 使用moderngl的texture_array方法将图像数据转换为纹理对象
            texture = self.app.ctx.texture_array(
                size=(texture.get_width(), texture.get_height() // num_layers, num_layers),
                components=4,
                data=pg.image.tostring(texture, 'RGBA')
            )
        else:
            # 使用moderngl的texture方法将图像数据转换为纹理对象
            texture = self.ctx.texture(
                size=texture.get_size(),
                components=4,
                data=pg.image.tostring(texture, 'RGBA', False)
            )

        # 对纹理进行一些后处理，例如设置纹理的纹理归一化、构建多级纹理表等
        texture.anisotropy = 32.0
        texture.build_mipmaps()
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        return texture  # 返回纹理对象
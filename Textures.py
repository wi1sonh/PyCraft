import pygame as pg
import moderngl as mgl

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

        # assign texture unit
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
        texture = pg.image.load(f'Resources/{file_name}')
        texture = pg.transform.flip(texture, flip_x=True, flip_y=False)

        if is_tex_array:
            num_layers = 3 * texture.get_height() // texture.get_width() # 3 textures per layer
            texture = self.app.ctx.texture_array(
                size=(texture.get_width(), texture.get_height() // num_layers, num_layers),
                components=4,
                data=pg.image.tostring(texture, 'RGBA')
            )
        else:
            texture = self.ctx.texture(
                size=texture.get_size(),
                components=4,
                data=pg.image.tostring(texture, 'RGBA', False)
            )
        texture.anisotropy = 32.0
        texture.build_mipmaps()
        texture.filter = (mgl.NEAREST, mgl.NEAREST)
        return texture
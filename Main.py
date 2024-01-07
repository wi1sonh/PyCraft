from Constants import *
import moderngl as mgl
import pygame as pg
import sys
from Shader_Program import ShaderProgram
from Scene import Scene
from Player import Player
from Textures import Textures

class BlockEngine:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, NUM_SAMPLES)

        self.game_display = pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()

        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = 'auto'

        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        sounds = {}
        # 方块破坏声
        block_sound = pg.mixer.Sound("Resources/Music/Block.mp3")
        # 花花草草破坏声
        grass_sound = pg.mixer.Sound("Resources/Music/Grass.mp3")
        block_sound.set_volume(0.2)

        sounds["Block"] = block_sound
        sounds["Grass"]  = grass_sound

        self.sounds = sounds

        # 播放背景音乐
        pg.mixer.music.load("Resources/Music/Sweden.mp3")
        pg.mixer.music.play(loops=-1)

        self.is_running = True
        self.on_init()

    def on_init(self):
        self.textures = Textures(self)
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)


    def update(self):
        self.player.update(pg)
        self.shader_program.update()
        self.scene.update()

        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        pg.display.set_caption(f'{self.clock.get_fps() :.0f}')


    def render(self):
        self.ctx.clear(color=BG_COLOR)
        self.scene.render()
        self.player.render()
        pg.display.flip()



    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False
            self.player.handle_event(event=event, pg=pg)

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()

if __name__ == '__main__':
    app = BlockEngine()
    app.run()
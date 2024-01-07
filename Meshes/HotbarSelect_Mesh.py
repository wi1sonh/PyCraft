from Constants import *
from Meshes.Base_Mesh import BaseMesh
from array import array

class Select(BaseMesh):
    def __init__(self, app, x=0):
        super().__init__()

        self.app = app;
        self.ctx = app.ctx
        self.program = app.shader_program.select
        self.x = x

        self.vbo_format = '3f 3f'
        self.attrs = ('in_position', 'tex_coords',)
        self.vao = self.get_vao()

    def get_vertex_data(self):

        length = 0.1 * ASPECT_RATIO - 0.01
        vertices = [

            (-0.315 + self.x, -0.82, 0.0), (-0.405 + self.x, -0.82, 0.0), (-0.405 + self.x, -0.82 - length, 0.0),
            (-0.315 + self.x, -0.82, 0.0), (-0.405 + self.x, -0.82 - length, 0.0), (-0.315 + self.x, -0.82 - length, 0.0)
        ]
        tex_coords = [
            (1, 1, 0), (0, 1, 0), (0, 0, 0),
            (1, 1, 0), (0, 0, 0), (1, 0, 0)
        ]

        vertex_data = np.hstack([vertices, tex_coords], dtype='float32')
        return vertex_data
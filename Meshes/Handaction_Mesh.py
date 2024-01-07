from Constants import *
from Meshes.Base_Mesh import BaseMesh

# 手部动作
class HandactionMesh(BaseMesh):
    def __init__(self, app):
        super().__init__()

        self.app = app;
        self.ctx = app.ctx
        self.program = app.shader_program.hand

        self.vbo_format = '3f 3f'
        self.attrs = ('in_position', 'tex_coords',)
        self.vao = self.get_vao()

    def get_vertex_data(self):

        vertices = [
            (0.95, -0.1, 0.0), (0.35, -0.1, 0.0), (0.35, -1, 0.0),
            (0.95, -0.1, 0.0), (0.35, -1, 0.0), (0.95, -1, 0.0)
        ]
        tex_coords = [
            (1, 1, 0), (0, 1, 0), (0, 0, 0),
            (1, 1, 0), (0, 0, 0), (1, 0, 0)
        ]

        vertex_data = np.hstack([vertices, tex_coords], dtype='float32')
        return vertex_data
from Settings import *
from Meshes.Base_Mesh import BaseMesh
from array import array

class QuadMesh(BaseMesh):
    def __init__(self, app):
        super().__init__()

        self.app = app;
        self.ctx = app.ctx
        self.program = app.shader_program.quad

        self.vbo_format = '3f 3f'
        self.attrs = ('in_position', 'tex_coords',)
        self.vao = self.get_vao()

    def get_vertex_data(self):

        length = 0.1 * ASPECT_RATIO
        vertices = [
            (0.1, length, 0.0), (-0.1, length, 0.0), (-0.1, -length, 0.0),
            (0.1, length, 0.0), (-0.1, -length, 0.0), (0.1, -length, 0.0)
        ]
        tex_coords = [
            (1, 1, 0), (0, 1, 0), (0, 0, 0),
            (1, 1, 0), (0, 0, 0), (1, 0, 0)
        ]


        # tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        # tex_coord_indices = [
        #     (0, 2, 3), (0, 1, 2),
        #     (0, 2, 3), (0, 1, 2),
        #     (0, 1, 2), (2, 3, 0),
        #     (2, 3, 0), (2, 0, 1),
        #     (0, 2, 3), (0, 1, 2),
        #     (3, 1, 2), (3, 0, 1),
        # ]
        # tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        # quad_buffer = [
        #     -1.0, 1.0, 0.0, 0.0,
        #     1.0, 1.0, 1.0, 0.0,
        #     -1.0, -1.0, 1.0,
        #     1.0, -1.0, 1.0, 1.0,
        # ]
        # vertex_data = np.array(quad_buffer, dtype='float16')
        vertex_data = np.hstack([vertices, tex_coords], dtype='float32')
        # return vertex_data
        return vertex_data
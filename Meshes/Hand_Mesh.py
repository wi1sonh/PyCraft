from Constants import *
from Meshes.Base_Mesh import BaseMesh

class HandMesh(BaseMesh):
    def __init__(self, app):
        super().__init__() # 调用父类的构造函数，以初始化基类

        # 设置手部几何模型的OpenGL上下文、着色器程序和顶点数据格式
        self.app = app;
        self.ctx = app.ctx
        self.program = app.shader_program.hand

        self.vbo_format = '3f 3f'
        self.attrs = ('in_position', 'tex_coords',)
        self.vao = self.get_vao()

    # 返回表示手部几何模型的顶点数据
    def get_vertex_data(self):

        # 定义了一些顶点和纹理坐标
        vertices = [
            (0.95, -0.4, 0.0), (0.45, -0.4, 0.0), (0.45, -1, 0.0),
            (0.95, -0.4, 0.0), (0.45, -1, 0.0), (0.95, -1, 0.0)
        ]
        tex_coords = [
            (1, 1, 0), (0, 1, 0), (0, 0, 0),
            (1, 1, 0), (0, 0, 0), (1, 0, 0)
        ]

        # 将它们组合成一个NumPy数组
        vertex_data = np.hstack([vertices, tex_coords], dtype='float32')
        return vertex_data
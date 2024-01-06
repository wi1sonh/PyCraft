import numpy as np

# BaseMesh类定义了一个基本的框架，用于表示OpenGL顶点和片段着色器的几何对象
# 子类需要实现get_vertex_data方法来提供顶点数据，然后使用这些数据来创建顶点数组对象
# 最后，子类可以覆盖render方法来定义自己的渲染逻辑
class BaseMesh:
    def __init__(self) -> None:
        # OpenGL上下文对象，用于管理图形资源
        self.ctx = None
        # 着色器程序对象，用于渲染几何对象
        self.program = None
        # 顶点数据格式字符串, 表示顶点数据中每个属性的数据类型和数量, 格式统一为"3f 3f"
        self.vbo_format = None
        # 属性名称元组, 表示与vbo_format中的格式字符串相对应的属性名称, 如("in_position", "in_color")
        self.attrs: tuple[str, ...] = None
        # vertex array object顶点数组对象
        self.vao = None

    # 返回一个表示顶点数据的一维NumPy数组
    # 这个方法需要在子类中实现，以便在渲染过程中使用
    def get_vertex_data(self) -> np.array: ...

    # 返回一个表示顶点数组对象的顶点数组对象
    def get_vao(self):
        # 首先调用get_vertex_data方法来获取顶点数据
        vertex_data = self.get_vertex_data()

        # 然后使用这些数据创建一个缓冲对象vbo
        vbo = self.ctx.buffer(vertex_data)

        # 最后使用ctx.vertex_array方法创建一个顶点数组对象vao
        # 并将缓冲对象与顶点数据格式和属性名称关联起来
        vao = self.ctx.vertex_array(
            self.program, [(vbo, self.vbo_format, *self.attrs)], skip_errors=True
            )
        return vao

    # 公共方法，该方法使用vao对象来渲染几何对象
    def render(self):
        self.vao.render()
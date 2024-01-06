from Meshes.Base_Mesh import BaseMesh
from Meshes.Chunk_Mesh_Builder import build_chunk_mesh

class ChunkMesh(BaseMesh):
    def __init__(self, chunk, transparent=False):
        super().__init__()
        self.app = chunk.app
        self.chunk = chunk
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.chunk
        self.is_transparent = transparent

        self.vbo_format = '1u4'
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attrs = ('packed_data',)
        self.vao = self.get_vao()

    def rebuild(self):
        self.vao = self.get_vao()

    def get_vertex_data(self):
        mesh = build_chunk_mesh(
            chunk_voxels=self.chunk.voxels,
            format_size=self.format_size,
            chunk_pos=self.chunk.position,
            world_voxels=self.chunk.world.voxels,
            transparent=self.is_transparent
        )
        return mesh
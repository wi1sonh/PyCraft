from Constants import *
from Meshes.Hand_Mesh import HandMesh
from Meshes.Handaction_Mesh import HandactionMesh

class Hand:
    def __init__(self, block_handler):
        self.app = block_handler.app
        self.handler = block_handler

        self.handm = HandMesh(self.app)
        self.handaction = HandactionMesh(self.app)

    def update(self):
        pass

    def render(self):

        if self.app.player.action == 1:
            self.handaction.render()
        else:
            self.handm.render()
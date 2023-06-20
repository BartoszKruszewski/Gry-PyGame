from game_object import GameObject

class Ground(GameObject):
    def __init__(self,pos,id,type):
        super().__init__(pos, id, type, "ground","neutral")
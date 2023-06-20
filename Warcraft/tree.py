from game_object import GameObject

class Tree(GameObject):
    def __init__(self,pos,id):
        super().__init__(pos, id, "tree", "tree","neutral")
        self.actual_health = 10
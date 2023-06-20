from game_object import GameObject
from CONST import BUILDING_TILES, BUILDING_STATS

class Building(GameObject):
    def __init__(self,pos,id,type,side):
        self.build_timer = 20
        self.build = False
        self.health = BUILDING_STATS[type]["health"]
        self.actual_health = self.health
        self.destroyed = 0
        self.destroy_timer = 0

        if BUILDING_TILES[type] == 4:
            self.tiles = [
                [pos[0],pos[1]],
                [pos[0] + 1,pos[1]],
                [pos[0],pos[1] + 1],
                [pos[0] + 1,pos[1] + 1]
            ]
        elif BUILDING_TILES[type] == 9:
            self.tiles = [
                [pos[0], pos[1]],
                [pos[0] + 1, pos[1]],
                [pos[0] + 2, pos[1]],
                [pos[0], pos[1] + 1],
                [pos[0] + 1, pos[1] + 1],
                [pos[0] + 2, pos[1] + 1],
                [pos[0], pos[1] + 2],
                [pos[0] + 1, pos[1] + 2],
                [pos[0] + 2, pos[1] + 2],
            ]

        super().__init__(pos, id, type, "building",side)

    def update(self, dt):
        if self.actual_health <= 0:
            self.destroy_timer += dt
            if self.destroy_timer >= 5:
                self.destroy_timer = 0
                self.destroyed += 1
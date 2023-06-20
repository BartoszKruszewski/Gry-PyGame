from CONST import SCALE, HITBOX_MARGIN, TROOP_FRAME_SIZE, BUILDING_TILES
import pygame

class GameObject():
    def __init__(self,pos,id,type,object_type,side):
        self.pos = pos
        self.global_pos = [pos[0] * SCALE, pos[1] * SCALE]
        self.id = id
        self.type = type
        self.selected = False
        self.object_type = object_type
        self.side = side
        self.focusing_by = [0]

        if object_type == "building":
            if BUILDING_TILES[self.type] == 4:
                size = 2
            elif BUILDING_TILES[self.type] == 9:
                size = 3
            self.hitbox = pygame.Rect(self.global_pos[0] + HITBOX_MARGIN * 2, self.global_pos[1] + HITBOX_MARGIN * 2, size * SCALE - HITBOX_MARGIN * 4, size * SCALE - HITBOX_MARGIN * 4)
            self.clickbox = pygame.Rect(self.global_pos[0], self.global_pos[1], size * SCALE, size * SCALE)

        elif object_type == "troop":
            self.hitbox = pygame.Rect(self.global_pos[0] + HITBOX_MARGIN + SCALE/2, self.global_pos[1] + HITBOX_MARGIN + SCALE/2,SCALE - HITBOX_MARGIN * 2, SCALE - HITBOX_MARGIN * 2)
            self.clickbox = pygame.Rect(self.global_pos[0], self.global_pos[1], TROOP_FRAME_SIZE[0], TROOP_FRAME_SIZE[1])

        elif type == "tree" or type == "water":
            self.hitbox = pygame.Rect(self.global_pos[0] + HITBOX_MARGIN, self.global_pos[1] + HITBOX_MARGIN,SCALE - HITBOX_MARGIN * 2, SCALE - HITBOX_MARGIN * 2)
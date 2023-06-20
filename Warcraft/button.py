import pygame
from CONST import BUTTONS_VISIBLE, BUTTONS_BLOCKED


class Button():
    def __init__(self,type,category,pos,size):
        self.type = type
        self.base_pos = pos.copy()
        self.category = category
        self.click = False
        self.light = 0
        self.true_light = 0
        self.target_light = 0
        self.hitbox = pygame.Rect(pos[0],pos[1],size[0],size[1])
        self.hold = False
        if type in BUTTONS_BLOCKED.keys():
            self.blocked = True
        else:
            self.blocked = False

        if type in BUTTONS_VISIBLE.keys():
            self.visible = False
        else:
            self.visible = True

    def update(self,mouse,dt):
        if mouse.hitbox.colliderect(self.hitbox):
            overlaped = True
        else:
            overlaped = False

        if overlaped:
            self.target_light = 50
        else:
            self.target_light = 0

        self.true_light += (self.target_light - self.true_light) / 20 * dt
        self.true_light = max(self.true_light,0)
        self.true_light = min(self.true_light,255)
        self.light = int(round(self.true_light))

        self.click = (mouse.click[0] and overlaped)
        self.hold = (mouse.hold[0] and overlaped)
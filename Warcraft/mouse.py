import pygame
from CONST import SCREEN_RESOLUTION, GAME_RESOLUTION

class Mouse():
    def __init__(self,visible):
        self.pos = [0,0]
        self.click = [False,False]
        self.hold = [False,False]
        self.hitbox = pygame.Rect(0,0,1,1)
        self.scroll = 0
        pygame.mouse.set_visible(visible)

    def update(self):
        scale = GAME_RESOLUTION[0] / SCREEN_RESOLUTION[0]
        pos = pygame.mouse.get_pos()
        self.pos[0] = pos[0] * scale
        self.pos[1] = pos[1] * scale

        self.hitbox.x = int(round(self.pos[0]))
        self.hitbox.y = int(round(self.pos[1]))

        pressed = pygame.mouse.get_pressed(5)

        if pressed[0]:
            if not self.hold[0]:
                self.click[0] = True
            else:
                self.click[0] = False
            self.hold[0] = True
        else:
            self.hold[0] = False
            self.click[0] = False

        if pressed[2]:
            if not self.hold[1]:
                self.click[1] = True
            else:
                self.click[1] = False
            self.hold[1] = True
        else:
            self.hold[1] = False
            self.click[1] = False
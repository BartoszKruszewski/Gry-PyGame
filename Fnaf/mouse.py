import pygame
from CONST import GAME_RESOLUTION

class Mouse():
    def __init__(self):
        self.hitbox = pygame.Rect(0,0,1,1)
        self.click = False
        self.switch = False
        info = pygame.display.Info()
        self.mult = GAME_RESOLUTION[0] / info.current_w

    def update(self):
        pos = pygame.mouse.get_pos()
        self.hitbox.x = pos[0] * self.mult
        self.hitbox.y = pos[1] * self.mult

        pressed = pygame.mouse.get_pressed(3)[0]

        if pressed:
            if not self.switch:
                self.click = True
                self.switch = True
            else:
                self.click = False
        else:
            self.click = False
            self.switch = False


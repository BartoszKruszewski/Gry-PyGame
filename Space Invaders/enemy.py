import pygame
from CONST import *

class Enemy(pygame.Rect):
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.h = 32
        self.w = 32
        self.direction = True
        self.type = type

    def move(self):
        if self.direction:
            self.x += 10
            if self.x >= DRAW_SCREEN_SIZE[0] - 40:
                self.y += 20
                self.direction = False
        else:
            self.x -= 10
            if self.x <= 40:
                self.y += 20
                self.direction = True



import pygame
from CONST import *

class Projectile(pygame.Rect):
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.type = type
        self.h = 8
        self.w = 5

    def update(self,dt):
        if self.type == 1:
            self.y += dt * PROJECTILE_SPEED
        else:
            self.y -= dt * PROJECTILE_SPEED
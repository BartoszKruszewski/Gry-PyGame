import pygame
from CONST import *

class Player(pygame.Rect):
    def __init__(self):
        self.x = int(DRAW_SCREEN_SIZE[0] / 2)
        self.y = 150
        self.hp = 3
        self.h = 32
        self.w = 32

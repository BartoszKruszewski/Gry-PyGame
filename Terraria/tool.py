import pygame
from STATS import *

class Tool(pygame.Rect):
    def __init__(self,type):
        self.width = 16
        self.height = 16
        self.type = type
        self.img = pygame.image.load("img/blocks/" + self.type + ".png")
        self.in_hand = False
        self.power = TOOLS[type]["power"]
        self.speed = TOOLS[type]["speed"]

    def update(self,player):
        self.x = player.tool_point_x - 1
        self.y = player.tool_point_y - 9
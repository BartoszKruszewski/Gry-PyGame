import pygame, random

class Background():
    def __init__(self,type,x):
        if type == 1:
            self.img_index = 4
            self.horizon = 8
        elif type == 2:
            self.img_index = 3
            self.horizon = 6
        elif type == 3:
            self.img_index = 2
            self.horizon = 4
        elif type == 4:
            self.img_index = 1
            self.horizon = 2

        self.y = -20
        self.x = 0




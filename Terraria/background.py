import pygame

SCALE1 = 5
SCALE2 = 10
SCALE3 = 15

class Background():
    def __init__(self):
        self.type = "woodland"
        self.alpha = 510
        self.x1 = 0
        self.x2 = 0
        self.x3 = 0
        self.pos1_1 = [0,0]
        self.pos2_1 = [0,0]
        self.pos3_1 = [0,0]
        self.pos1_2 = [0,0]
        self.pos2_2 = [0,0]
        self.pos3_2 = [0,0]
        self.img1 = pygame.image.load("img/background/woodland/woodland1.png")
        self.img2 = pygame.image.load("img/background/woodland/woodland2.png")
        self.img3 = pygame.image.load("img/background/woodland/woodland3.png")

    def update(self,scroll):

        # 1 layer
        if self.pos1_1[0] >= 320:
            self.x1 -= 320
        if self.pos1_1[0] < 0:
            self.x1 += 320
        self.pos1_1[0] = self.x1 - int(scroll[0] // SCALE1)
        self.pos1_1[1] = 10 - int(scroll[1] // SCALE1)
        self.pos1_2[0] = self.x1 - int(scroll[0] // SCALE1) - 320
        self.pos1_2[1] = 10 - int(scroll[1] // SCALE1)

        # 2 layer
        if self.pos2_1[0] >= 320:
            self.x2 -= 320
        if self.pos2_1[0] < 0:
            self.x2 += 320
        self.pos2_1[0] = self.x2 - int(scroll[0] // SCALE2)
        self.pos2_1[1] = 15 - int(scroll[1] // SCALE2)
        self.pos2_2[0] = self.x2 - int(scroll[0] // SCALE2) - 320
        self.pos2_2[1] = 15 - int(scroll[1] // SCALE2)

        # 3 layer
        if self.pos3_1[0] >= 320:
            self.x3 -= 320
        if self.pos3_1[0] < 0:
            self.x3 += 320
        self.pos3_1[0] = self.x3 - int(scroll[0] // SCALE3)
        self.pos3_1[1] = 20 - int(scroll[1] // SCALE3)
        self.pos3_2[0] = self.x3 - int(scroll[0] // SCALE3) - 320
        self.pos3_2[1] = 20 - int(scroll[1] // SCALE3)




import pygame,random

class Particle(pygame.Rect):
    def __init__(self,x,y,type):
        self.center = (x + random.randint(0,8) -4, y + random.randint(0,8) -4)
        self.type = type
        if type == "blood":
            self.color = (255,0,0)
            self.s = random.randint(2, 5)
            self.speed_x = random.randint(0, 20) / 10 - 1
            self.speed_y = random.randint(0, 10) / 10 - 1
        elif type == "dust":
            self.color = (200,200,200)
            self.s = random.randint(1, 3)
            self.speed_x = (random.randint(0, 20) / 10 - 1)
            self.speed_y = 0
        elif type == "body":
            colors = [(238,195,154),(22,36,123),(105,106,106),(67,101,91)]
            self.color = random.choice(colors)
            self.s = random.randint(4, 7)
            self.speed_x = (random.randint(0, 20) / 10 - 1)
            self.speed_y = (random.randint(0, 10) / 10 - 1)
        elif type == "fire":

            colors = [(255,255,255),(255,0,0),(255,90,0),(255,154,0),(255,206,0),(255,232,8)]
            self.color = random.choice(colors)
            self.s = random.randint(1, 3)
            self.speed_x = 0
            self.speed_y = random.randint(0, 1) / 10
            self.center = (x + random.randint(0, 2) - 1, y + + random.randint(0,2) - 2)

    def update(self,gamemap):
        self.height = int(self.s)
        self.width = int(self.s)
        self.s *= 0.95
        if self.type == "blood":
            self.speed_x *= 1.01
            self.speed_y *= 1.05
        elif self.type == "dust":
            self.speed_x *= 0.1
        elif self.type == "body":
            self.speed_x *= 1.01
            self.speed_y *= 1.01
        elif self.type == "fire":
            self.speed_x *= 0.1
            self.speed_y *= 0.5
        self.centerx += self.speed_x
        self.centery -= self.speed_y
        if self.s < 1:
            gamemap.particles.remove(self)
            del self

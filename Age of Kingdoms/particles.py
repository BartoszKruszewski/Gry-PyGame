import pygame, random
from CONST import *

class Particle(pygame.Rect):
    def __init__(self,type,x,y):
        size = random.randint(PARTILCES[type][0][0],PARTILCES[type][0][1])
        self.w = size
        self.h = size
        self.x = x + random.randint(0,PARTILCES[type][1][0] * 2) - PARTILCES[type][1][0]
        self.y = y + random.randint(0, PARTILCES[type][1][1] * 2) - PARTILCES[type][1][1]
        self.real_x = self.x
        self.real_y = self.y
        if PARTILCES[type][6][0]:
            directionx = random.randint(0,2) -1
        else:
            directionx = 1
        if PARTILCES[type][6][1]:
            directiony = random.randint(0, 2) - 1
        else:
            directiony = 1
        self.speed = [PARTILCES[type][2][0] * directionx,PARTILCES[type][2][1] * directiony]
        self.max_time = PARTILCES[type][3] * FRAMERATE
        self.time = self.max_time
        self.color = random.choice(PARTILCES[type][4])
        self.opacity = 255
        self.acc = (PARTILCES[type][5][0] * directionx,PARTILCES[type][5][0] * directiony)

    def update(self,dt,particles):
        self.time -= dt
        self.opacity -= self.max_time * FRAMERATE / 500 / dt
        self.opacity = max(0,self.opacity)
        self.speed[0] += self.acc[0] * dt
        self.speed[1] += self.acc[1] * dt
        if not self.real_y > GROUND_LVL:
            self.real_x += self.speed[0] * dt
            self.real_y += self.speed[1] * dt
            self.x = int(self.real_x)
            self.y = int(self.real_y)

        if self.time <= 0:
            particles.remove(self)


import pygame,random

class Particle():
    def __init__(self,x,color,y = 140):
        self.s = random.randint(1, 3)
        self.y = y
        self.real_y = self.y
        self.x = x
        self.real_x = self.x
        if y == 140:
            self.speed_x = (random.randint(0,20) - 10) / 10
        else:
            self.speed_x = (random.randint(0,2) - 1) / 10
        self.speed_y = random.randint(0,10) / 10
        self.timer = random.randint(0, 250)
        self.color = (color[0],color[1],color[2],self.timer)


    def update(self,dt,particles,scrool):
        self.color = (self.color[0], self.color[1], self.color[2], self.timer)
        self.timer -= dt * 5
        self.real_x += self.speed_x * dt
        self.real_y += self.speed_y * dt
        self.x = round(self.real_x) + scrool
        self.y = round(self.real_y)
        if self.timer < 0:
            self.timer = 0
        if self.timer == 0:
            particles.remove(self)
            del self
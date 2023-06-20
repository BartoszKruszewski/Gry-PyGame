import pygame, random, math
from CONST import *

class Grain():
    def __init__(self,x):
        self.x = x + random.randint(0,16) -8
        self.y = 314
        self.size = random.randint(8,10) / 10
        self.img = "grain" + str(random.randint(1,4))
        self.angle = 0
        self.last_player_pos = (0,0)
        self.target_angle = self.angle
        self.rotation_full = False
        self.in_range = False

    def collide(self,rect):
        if rect.direction == "right":
            distance = rect.centerx - SOLDIERS_OFFSET[rect.type][1] - self.x
        else:
            distance = rect.centerx - self.x
        if abs(distance) < 35:
            self.in_range = True
            temp_target = 0
            if distance <= 0:
                temp_target = 70 - distance * 3.5
            if distance > 0:
                temp_target = -70 - distance * 3.5
            self.target_angle = min(self.target_angle + temp_target, 80)
            self.target_angle = max(self.target_angle, -80)


    def update(self,soldiers,dt,wind_speed):
        self.in_range = False
        for soldier in soldiers:
            self.collide(soldier)
            if self.in_range:
                break
        if not self.in_range:
            self.check_wind(wind_speed)
        self.angle += (self.target_angle - self.angle) /20 * dt

    def check_wind(self,wind):
        speed = (wind+3) * random.randint(7,10) /60
        if not self.rotation_full:
            self.target_angle += speed
        else:
            self.target_angle -= speed
        if self.target_angle > (20 + (wind / 2)):
            self.rotation_full = True
        if self.target_angle < int(-20 - (wind / 2)):
            self.rotation_full = False
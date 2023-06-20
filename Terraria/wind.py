import pygame, random

class Wind():
    def __init__(self):
        self.speed = 1

    def update(self):
        if random.randint(1,300) == 1:
            if random.randint(1,2) == 1:
                if self.speed > 1:
                    self.speed -= 1
            else:
                if self.speed < 5:
                    self.speed += 1
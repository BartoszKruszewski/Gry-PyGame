import pygame
from gui import Gui
from CONST import *

class Building(pygame.Rect):
    def __init__(self,type,texture):
        self.width = 60
        self.height = 120
        self.x = BUILDING_POS[type][0]
        self.y = BUILDING_POS[type][1]
        self.gui = Gui(type)
        self.type = type
        self.state = "normal"
        self.clicked = False
        self.sound_hover = pygame.mixer.Sound("sounds/pop.wav")
        self.sound_hover.set_volume(0.2)
        self.sound_click = pygame.mixer.Sound("sounds/click.wav")
        self.sound_played = False
        self.actual_light = 0
        self.target_light = 0
        self.mask = pygame.mask.from_surface(texture)

    def update(self,mouse,scrool,dt):
        if self.state != "disabled" and self.collide(mouse,scrool):
            self.state = "on"
            if not self.sound_played:
                self.sound_played = True
                self.sound_hover.play()
        elif self.state == "on":
            self.state = "normal"
            self.sound_played = False

        if self.state == "on" and mouse.left_click:
            self.clicked = True
            self.sound_click.play()

        self.actual_light += (self.target_light - self.actual_light) / 30 * dt
        self.actual_light = min(255,self.actual_light)
        self.actual_light = max(0, self.actual_light)

    def collide(self,mouse,scrool):
        return self.mask.overlap(mouse.mask,(mouse.x - self.x - scrool,mouse.y - self.y))

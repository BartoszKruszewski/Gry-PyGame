import pygame

class Button():
    def __init__(self,name,scene,rect_properties,is_moving):
        self.hitbox = pygame.Rect(rect_properties[0],rect_properties[1],rect_properties[2],rect_properties[3])
        self.clicked = False
        self.hold = False
        self.overlaped = False
        self.name = name
        self.visible = False
        self.scene = scene
        self.is_moving = is_moving
        self.sound_played = False

    def update(self, mouse, scroll):

        hitbox = mouse.hitbox.copy()
        if self.is_moving:
            hitbox.x += scroll
        self.overlaped = self.hitbox.colliderect(hitbox)
        if self.overlaped:
            self.clicked = mouse.click
            self.hold = mouse.switch
        else:
            self.clicked = False
            self.hold = False
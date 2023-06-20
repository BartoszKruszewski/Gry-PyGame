import pygame

class Gui():
    def __init__(self,type):

        self.buttons = []

        if type == "game":
            # button_img_units
            self.buttons.append(Button((219,8),"unit1"))
            self.buttons.append(Button((238, 8),"unit2"))
            self.buttons.append(Button((257, 8),"unit3"))

            # upgrade
            self.buttons.append(Button((219, 27),"upgrade1"))
            self.buttons.append(Button((238, 27),"upgrade2"))
            self.buttons.append(Button((257, 27),"upgrade3"))

            # turret
            self.buttons.append(Button((286, 8),"turret"))

            # gold mine
            self.buttons.append(Button((286, 27),"gold"))

            # next age
            self.buttons.append(Button((276, 48),"age"))

            # special attack
            self.buttons.append(Button((296, 48),"special"))
        elif type == "menu":
            self.buttons.append(Button((115, 68), "easy",90,20))
            self.buttons.append(Button((115, 103), "normal",90,20))
            self.buttons.append(Button((115, 138), "hard",90,20))

class Button(pygame.Rect):
    def __init__(self,pos,type,width=16,height=16):
        self.width = width
        self.height = height
        self.x = pos[0]
        self.y = pos[1]
        self.type = type
        self.state = "normal"
        self.clicked = False
        self.sound_hover = pygame.mixer.Sound("sounds/pop.wav")
        self.sound_hover.set_volume(0.2)
        self.sound_click = pygame.mixer.Sound("sounds/click.wav")
        self.sound_played = False

    def update(self,mouse):

        if self.state != "disabled" and self.colliderect(mouse):
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
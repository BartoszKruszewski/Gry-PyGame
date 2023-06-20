import pygame

class Gui():
    def __init__(self,type):

        self.type = type
        self.buttons = []

        if type == "base":
            self.buttons.append(Button((438, 16), "knight"))
            self.buttons.append(Button((479, 16), "archer"))
            self.buttons.append(Button((520, 16), "paladin"))
            self.buttons.append(Button((561, 16), "mage"))
            self.buttons.append(Button((602, 16), "griffin"))

        elif type == "farm":
            self.buttons.append(Button((438, 16), "plows"))
            self.buttons.append(Button((479, 16), "flock"))
            self.buttons.append(Button((520, 16), "cattle"))
            self.buttons.append(Button((561, 16), "granary"))
            self.buttons.append(Button((602, 16), "windmill"))

        elif type == "guild":
            self.buttons.append(Button((438, 16), "tools"))
            self.buttons.append(Button((479, 16), "learning"))
            self.buttons.append(Button((520, 16), "fortifications"))
            self.buttons.append(Button((561, 16), "finances"))

        elif type == "town_hall":
            self.buttons.append(Button((438, 16), "archery"))
            self.buttons.append(Button((479, 16), "blacksmith"))
            self.buttons.append(Button((520, 16), "mage_tower"))
            self.buttons.append(Button((561, 16), "griffin_rampart"))
            self.buttons.append(Button((602, 16), "tower1"))
            self.buttons.append(Button((602, 16), "tower2"))
            self.buttons.append(Button((602, 16), "tower3"))

        elif type == "archery":
            self.buttons.append(Button((438, 16), "range"))
            self.buttons.append(Button((479, 16), "fire_arrows"))
            self.buttons.append(Button((520, 16), "sharpshooters"))

        elif type == "blacksmith":
            self.buttons.append(Button((438, 16), "swords"))
            self.buttons.append(Button((479, 16), "armor"))
            self.buttons.append(Button((520, 16), "shields"))
            self.buttons.append(Button((561, 16), "fencing"))

        elif type == "mage_tower":
            self.buttons.append(Button((438, 16), "lightning"))

        elif type == "griffin_rampart":
            self.buttons.append(Button((438, 16), "frenzy"))

class Button(pygame.Rect):
    def __init__(self,pos,type,width=32,height=32):
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
        self.actual_light = 0
        self.target_light = 0

        if self.type == "archer" or self.type == "paladin" or self.type == "mage" or self.type == "griffin" or self.type == "tower2" or self.type == "tower3":
            self.state = "disabled"

    def update(self,mouse,dt):

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

        if self.state == "on":
            self.target_light = 255
        else:
            self.target_light = 0

        self.actual_light += (self.target_light - self.actual_light) / 30 * dt
        self.actual_light = min(255, self.actual_light)
        self.actual_light = max(0, self.actual_light)
import pygame, os

class Menu():
    def __init__(self,type):
        if type == "skill_sheet":
            self.background = pygame.image.load("img/menu/skill_sheet.png")
        else:
            self.background = pygame.image.load("img/menu/main_menu.png")

        self.buttons = []
        self.menu_x = 112
        self.menu_y = 19

        if type == "main":
            self.buttons.append(Button(self.menu_x, self.menu_y,"New World"))
            self.buttons.append(Button(self.menu_x, self.menu_y + (30 + 7), "Load World"))
            self.buttons.append(Button(self.menu_x, self.menu_y + (30 + 7) * 2, "Skill Sheet"))
            self.buttons.append(Button(self.menu_x, self.menu_y + (30 + 7) * 3, "Save and Exit"))
        elif type == "new_world":
            self.buttons.append(Text_Box(self.menu_x-2,50))
            self.buttons.append(Button(self.menu_x, 75, "Save"))
        elif type == "load_world":
            saves =  list(os.listdir("saves"))
            i = -1
            for save in saves:
                i += 1
                self.buttons.append(World_Button(self.menu_x-2,15 + 25 * i,save))
            self.buttons.append(Button(self.menu_x, 135, "Back"))
        elif type == "skill_sheet":
            self.buttons.append(Skill_Button(92, 20, "blood_lust"))
            self.buttons.append(Skill_Button(92, 40, "regeneration"))
            self.buttons.append(Skill_Button(92, 60, "holy_aura"))
            self.buttons.append(Skill_Button(92, 80, "dark_portal"))
            self.buttons.append(Skill_Button(72, 100, "dark_forge"))
            self.buttons.append(Skill_Button(52, 120, "exp_forge"))
            self.buttons.append(Skill_Button(32, 140, "forge"))
            self.buttons.append(Skill_Button(112, 100, "super_speed"))
            self.buttons.append(Skill_Button(132, 120, "double_jump"))
            self.buttons.append(Skill_Button(152, 140, "shoes"))

class Button(pygame.Rect):
    def __init__(self,x,y,text):
        self.x = x
        self.y = y
        self.text = text
        self.width = 96
        self.height = 30
        self.img1 = pygame.image.load("img/menu/button1.png")
        self.img2 = pygame.image.load("img/menu/button2.png")
        self.img = self.img1
        self.collide = False
        self.sound1 = pygame.mixer.Sound("sounds/gui/click1.wav")
        self.sound2 = pygame.mixer.Sound("sounds/gui/click2.wav")
        self.played = False

    def update(self,mouse):
        if self.colliderect(mouse.rect):
            self.img = self.img2
            self.collide = True
            if not self.played:
                self.played = True
                self.sound1.play()
            if mouse.left_click:
                self.sound2.play()
                return True
        else:
            self.played = False
            self.collide = False
            self.img = self.img1
        return False

class Text_Box(pygame.Rect):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.height = 20
        self.width = 100
        self.img_off = pygame.image.load("img/menu/text-box1.png")
        self.img_on = pygame.image.load("img/menu/text-box2.png")
        self.img = self.img_off
        self.on = False
        self.text = ""
        self.sound = pygame.mixer.Sound("sounds/gui/click1.wav")

    def update(self,mouse):

        if self.colliderect(mouse.rect) and mouse.left_click and not self.on:
            self.sound.play()
            self.on = True
            self.img = self.img_on

        if not self.colliderect(mouse.rect) and mouse.left_click and self.on:
            self.sound.play()
            self.on = False
            self.img = self.img_off

        return False

class World_Button(pygame.Rect):
    def __init__(self, x, y, text):
        self.x = x
        self.y_start = y
        self.y = y
        self.text = text
        self.width = 100
        self.height = 20
        self.img1 = pygame.image.load("img/menu/text-box1.png")
        self.img2 = pygame.image.load("img/menu/text-box2.png")
        self.img = self.img1
        self.sound1 = pygame.mixer.Sound("sounds/gui/click1.wav")
        self.sound2 = pygame.mixer.Sound("sounds/gui/click2.wav")
        self.played = False
        self.collide = False

    def update(self, mouse,scroll=0):
        if self.text != "Back":
            self.y = self.y_start + scroll

        if self.colliderect(mouse.rect):
            self.img = self.img2
            self.collide = True
            if not self.played:
                self.sound1.play()
                self.played = True
            if mouse.left_click:
                self.sound2.play()
                return True
        else:
            self.collide = False
            self.played = False
            self.img = self.img1
        return False

class Skill_Button(pygame.Rect):
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.type = type
        self.width = 18
        self.height = 18
        self.img1 = pygame.image.load("img/menu/skill_button1.png")
        self.img2 = pygame.image.load("img/menu/skill_button2.png")
        self.img = self.img1
        self.sound1 = pygame.mixer.Sound("sounds/gui/click1.wav")
        self.sound2 = pygame.mixer.Sound("sounds/gui/click2.wav")
        self.played = False
        self.collide = False

    def update(self,mouse):
        if self.colliderect(mouse.rect):
            self.img = self.img2
            self.collide = True
            if not self.played:
                self.sound1.play()
                self.played = True
            if mouse.left_click:
                self.sound2.play()
                return True
        else:
            self.img = self.img1
            self.collide = False
            self.played = False
        return False


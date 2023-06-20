import pygame, sys, random, os
from mouse import Mouse
from background import Background
from soldier import Soldier
from gui import Gui
from particle import Particle
from projectile import Projectile
from STATS import *

FRAMERATE = 144
SCREEN_RESOLUTION = (1280, 720)
FULLSCREEN = True
VERSION = "1.0"

class Game():
    def __init__(self):

        # pre init
        pygame.mixer.pre_init(44100,-16,2,512)
        pygame.init()

        # screen
        self.screen_size = SCREEN_RESOLUTION
        if FULLSCREEN:
            self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.screen_size)

        pygame.display.set_caption("Age of War")
        pygame.display.set_icon(pygame.image.load("icon.png"))

        self.draw_screen = pygame.Surface((320, 180))

        # clock and mouse
        self.clock = pygame.time.Clock()
        self.dt = 1
        self.mouse = Mouse()

        # fonts
        self.FONT = pygame.font.Font("Minimal3x5.ttf",16)
        self.FONT_INFO = pygame.font.Font("Minimal3x5.ttf", 8)
        self.FONT_COLOR = pygame.Color("white")

        # init
        self.running = False
        self.load_textures()
        self.load_sounds()
        self.menu()

    def end_game(self,win):

        self.running = False

        # load end game screen
        won = pygame.image.load("img/text2.png")
        lose = pygame.image.load("img/text1.png")
        rect = won.get_rect(center = (160,90))

        while True:
            self.check_keys()

            self.draw_screen.fill((0,0,0))

            if win:
                self.draw_screen.blit(won,rect)
            else:
                self.draw_screen.blit(lose,rect)

            self.refresh_screen()


    def create_background(self):

        self.background = []
        self.background.append(Background(1,100))
        self.background.append(Background(2,200))
        self.background.append(Background(3,300))
        self.background.append(Background(4, 300))

    def menu(self):
        self.gui = Gui("menu")

        while True:
            self.check_events()
            self.check_keys()
            self.mouse.update(self.screen_size)

            self.draw_menu()
            self.refresh_screen()

    def game(self):

        # load and play music
        pygame.mixer_music.load("music.wav")
        pygame.mixer_music.set_volume(0.5)
        pygame.mixer_music.play(-1)

        # init
        self.gui = Gui("game")
        self.running = True

        self.true_scrool = 0
        self.scrool = 0

        self.create_background()
        self.particles = []
        self.projectiles = []

        # set stats
        self.gold = START_GOLD
        self.gold_mine = 1

        self.player_age = 1
        self.player_turret = False
        self.player_turret_frame = 1
        self.turret_timer = 0
        self.player_base_health = BASE_HP
        self.queue = []
        self.soldiers = []

        self.computer_age = 1
        self.computer_turret = False
        self.computer_turret_frame = 1
        self.computer_turret_timer = 0
        self.computer_base_health = BASE_HP
        self.computer_queue = []
        self.enemy_soldiers = []

        self.loot_timer = 0
        self.loot = 0
        self.loot_pos = 0

        self.unit1_lvl = False
        self.unit2_lvl = False
        self.unit3_lvl = False

        self.unit_timer = 0
        self.unit_time = 0

        self.special_timer = (SPECIAL_TIMER[self.difficulty] * FRAMERATE * 60)

        # set events
        self.ADD_GOLD = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADD_GOLD, 1000)

        self.COMPUTER_BUY = pygame.USEREVENT + 3
        pygame.time.set_timer(self.COMPUTER_BUY, 10000)

        self.COMPUTER_AGE = pygame.USEREVENT + 4
        pygame.time.set_timer(self.COMPUTER_AGE, NEW_AGE_TIME[self.difficulty + "_2"] * 60000)

        # game loop
        while self.running:

            # update stuff
            self.check_events()
            self.check_keys()
            self.mouse.update(self.screen_size)

            # scrool
            if self.mouse.x > 300:
                self.true_scrool -= self.dt
            elif self.mouse.x < 20:
                self.true_scrool += self.dt

            if self.true_scrool < -320:
                self.true_scrool = -320
            elif self.true_scrool > 0:
                self.true_scrool = 0

            self.scrool = int(self.true_scrool)

            # update soldiers
            for soldier in self.soldiers:
                self.computer_base_health -= soldier.update(self.soldiers,self.enemy_soldiers,self.dt,self.particles,self.projectiles)

            for soldier in self.enemy_soldiers:
                self.player_base_health -= soldier.update(self.soldiers,self.enemy_soldiers,self.dt,self.particles,self.projectiles)

            # turret timer
            self.computer_turret_timer += self.dt
            if self.computer_turret_timer > 25920:
                self.computer_turret = True

            # update projectiles
            for projectile in self.projectiles:
                projectile.update(self.dt,self.soldiers,self.enemy_soldiers,self.projectiles,self.particles)

            # queue timer
            self.unit_timer += self.dt
            if len(self.queue) > 0:
                if self.queue[0].lvl == 1:
                    self.unit_time = 250
                elif self.queue[0].lvl == 2:
                    self.unit_time = 500
                elif self.queue[0].lvl == 3:
                    self.unit_time = 1000

                if self.unit_timer >= self.unit_time:
                    self.soldiers.append(self.queue[0])
                    self.queue.remove(self.queue[0])
                    self.unit_timer = 0
            else:
                self.unit_timer = 0

            # special timer
            if self.special_timer < (SPECIAL_TIMER[self.difficulty] * FRAMERATE * 60):
                self.special_timer += self.dt


            # check base health
            if self.player_base_health <= 0:
                self.end_game(False)
            elif self.computer_base_health <= 0:
                self.end_game(True)

            # check killed soldiers and set loot
            self.loot_timer -= self.dt

            if len(self.soldiers) > 0 and self.soldiers[0].actual_health <= 0:
                self.soldiers.pop(0)

            if len(self.enemy_soldiers) > 0 and self.enemy_soldiers[0].actual_health <= 0:
                self.loot = int(PRICES[self.enemy_soldiers[0].type] / 2)
                self.loot_pos = self.enemy_soldiers[0].centerx
                self.loot_timer = 250
                self.gold += self.loot
                self.enemy_soldiers.pop(0)

            # draw
            self.draw_game()
            self.refresh_screen()

    def check_events(self):
        for event in pygame.event.get():

            # click on exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            # add gold to player
            if self.running and event.type == self.ADD_GOLD:
                self.gold += GOLD["lvl" + str(self.gold_mine)]

            # computer buy unit
            if self.running and event.type == self.COMPUTER_BUY and len(self.enemy_soldiers) < 10:

                if len(self.computer_queue) == 0:

                    if self.difficulty == "easy":
                        for i in range(13):
                            self.computer_queue.append(str(self.computer_age) + "_1")
                        for i in range(5):
                            self.computer_queue.append(str(self.computer_age) + "_2")
                        for i in range(2):
                            self.computer_queue.append(str(self.computer_age) + "_3")

                    elif self.difficulty == "normal":
                        for i in range(13):
                            lvl_up = ""
                            if random.randint(1,4) == 1:
                                lvl_up = "+"
                            self.computer_queue.append(str(self.computer_age) + "_1" + lvl_up)
                        for i in range(5):
                            lvl_up = ""
                            if random.randint(1, 6) == 1:
                                lvl_up = "+"
                            self.computer_queue.append(str(self.computer_age) + "_2")
                        for i in range(2):
                            lvl_up = ""
                            if random.randint(1, 4) == 1 and self.computer_age != 4:
                                lvl_up = "+"
                            self.computer_queue.append(str(self.computer_age) + "_3")

                    elif self.difficulty == "hard":
                        for i in range(13):
                            lvl_up = ""
                            if random.randint(1,2) == 1:
                                lvl_up = "+"
                            self.computer_queue.append(str(self.computer_age) + "_1" + lvl_up)
                        for i in range(5):
                            lvl_up = ""
                            if random.randint(1, 3) == 1:
                                lvl_up = "+"
                            self.computer_queue.append(str(self.computer_age) + "_2")
                        for i in range(2):
                            lvl_up = ""
                            if random.randint(1, 3) == 1 :
                                lvl_up = "+"
                            self.computer_queue.append(str(self.computer_age) + "_3")

                choice = random.choice(self.computer_queue)
                self.computer_queue.remove(choice)
                self.enemy_soldiers.append(Soldier(NAMES[choice], "left", self.soldiers_animations[NAMES[choice]]["idle"][0],self.soldiers_sounds[choice.replace("+","")]))

                pygame.time.set_timer(self.COMPUTER_BUY, random.randint(3500,5500))

            # compuer next age
            if self.running and event.type == self.COMPUTER_AGE and self.computer_age < 4:
                self.computer_queue.clear()
                self.computer_turret = False
                self.computer_age += 1
                if self.computer_age < 4:
                    pygame.time.set_timer(self.COMPUTER_AGE, NEW_AGE_TIME[self.difficulty + "_" + str(self.computer_age + 1)] * 60000)

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit(0)

    def load_sounds(self):

        # soldiers sounds
        self.soldiers_sounds = {}
        for dir in os.listdir("sounds/soldiers"):
            sounds = []
            for sound in os.listdir("sounds/soldiers/" + dir):
                sounds.append(pygame.mixer.Sound("sounds/soldiers/" + dir + "/" + sound))
            self.soldiers_sounds[dir] = sounds

        # turret sounds
        self.turret_sounds = {}
        hit = []
        for i in range(4):
            hit.append(pygame.mixer.Sound("sounds/turrets/hit" + str(i+1) + ".wav"))

        fire = []
        for i in range(4):
            fire.append(pygame.mixer.Sound("sounds/turrets/fire" + str(i+1) + ".wav"))

        self.turret_sounds["hit"] = hit
        self.turret_sounds["fire"] = fire

        # special sounds
        self.special_sounds = []
        for i in range(4):
            self.special_sounds.append(pygame.mixer.Sound("sounds/special/" + str(i+1) + ".wav"))

    def load_textures(self):

        # load textures
        self.textures = {}
        for dir in os.listdir("img"):
            if dir != "soldiers":
                if dir[-4:] == ".png":
                    self.textures[dir.replace(".png", "")] = pygame.image.load("img/" + dir)
                else:
                    textures = {}
                    for file in os.listdir("img/" + dir):
                        textures[file.replace(".png","")] = pygame.image.load("img/" + dir + "/" + file)
                    self.textures[dir] = textures

        # load soldiers animations
        self.soldiers_animations = {}
        types = ["caveman","stoneman","beast","swordsman","archer","knight","traper","comando","tank","blademaster","laserman","mech","brutal","axeman","berserk","paladin","ranger","champion","marine","sniper","artilery","executor","cyborg","titan"]
        for type in types:
            self.soldiers_animations[type] = self.load_animations(type)

    def load_animations(self,type):
        animations = {}
        types = ["idle","walk","attack"]
        for i in types:
            animation = []
            animation.append(pygame.image.load("img/soldiers/" + type + "/" + i + "/" + i + "1.png"))
            animation.append(pygame.image.load("img/soldiers/" + type + "/" + i + "/" + i + "2.png"))
            animations[i] = animation
        return animations

    def get_info(self,type):
        if type == "unit1" or type == "unit2" or type == "unit3":

            unit_id = str(self.player_age) + "_" + type[4]
            if (type == "unit1" and self.unit1_lvl) or (type == "unit2" and self.unit2_lvl) or (type == "unit3" and self.unit3_lvl):
                unit_id += "+"
            troop = NAMES[unit_id]
            name = "train " + troop
            price = PRICES[troop]

        elif type == "turret":
            name = "build turret"
            price = PRICES["turret" + str(self.player_age)]

        elif type == "age":
            name = "Next Age"
            price = PRICES["age" + str(self.player_age + 1)]

        elif type == "gold":
            name = "Gold Mine LVL " + str(self.gold_mine + 1)
            price = PRICES["gold" + str(self.gold_mine + 1)]

        elif type == "upgrade1" or type == "upgrade2" or type == "upgrade3":
            unit_id = str(self.player_age) + "_" + type[7] + "+"
            troop = NAMES[unit_id]
            name = "upgrade to " + troop
            price = PRICES["upgrade" + type[7] + "_" + str(self.player_age)]

        elif type == "special":
                name = "Use special"
                price = "Attack"

        return name, price

    def draw_menu(self):

        # background
        self.draw_screen.blit(self.textures["menu"]["background"],(0,0))

        # buttons
        for button in self.gui.buttons:
            button.update(self.mouse)

            # state
            if button.state == "normal":
                self.draw_screen.blit(self.textures["menu"]["button_normal"],(button.x,button.y))
            else:
                self.draw_screen.blit(self.textures["menu"]["button_on"], (button.x, button.y))

            # text
            text = self.FONT_INFO.render(button.type, False, (255, 255, 255))
            text_rect = text.get_rect(center = (button.x + 45, button.y + 11))
            self.draw_screen.blit(text, text_rect)

            # click
            if button.clicked:
                self.difficulty = button.type
                self.game()

        # credits
        text = self.FONT_INFO.render("GAME MADE BY SKORPION", False, (255, 255, 255))
        self.draw_screen.blit(text, (5,170))

        # version
        text = self.FONT_INFO.render("VERSION " + VERSION, False, (255, 255, 255))
        self.draw_screen.blit(text, (275, 170))

        # mouse
        self.draw_screen.blit(self.textures["cursor"]["cursor" + str(self.mouse.texture_index + 1)],(self.mouse.x - 1, self.mouse.y - 2))

    def draw_game(self):

        # background
        self.draw_screen.fill(pygame.Color("skyblue3"))

        # parallax background
        for element in self.background:
            self.draw_screen.blit(self.textures["background"]["terrain" + str(element.img_index)],(int(element.x + (self.scrool / element.horizon)) ,element.y))

        # floor
        self.draw_screen.blit(self.textures["floor"], (self.scrool, 150))

        # base
        base_id = "base" + str(self.player_age)
        self.draw_screen.blit(self.textures["base"][base_id], (self.scrool, 110))
        state = round(self.player_base_health / BASE_HP * 10)
        self.draw_screen.blit(self.textures["health_bar"]["health_bar" + str(state)], (self.scrool + 5, 100))

        base_id = "base" + str(self.computer_age)
        state = round(self.computer_base_health / BASE_HP * 10)
        self.draw_screen.blit(self.textures["health_bar"]["health_bar" + str(state)], (self.scrool + 623, 100))
        self.draw_screen.blit(pygame.transform.flip(self.textures["base"][base_id],True,False),(self.scrool + 610, 110))

        # turret
        if self.player_turret:
            if len(self.enemy_soldiers) and self.enemy_soldiers[0].x < 200:
                self.turret_timer += self.dt
                if self.turret_timer >= 70:
                    self.turret_timer = 0
                    if self.player_turret_frame == 1:
                        self.player_turret_frame = 2
                        self.turret_sounds["fire"][self.player_age-1].play()
                        self.projectiles.append(Projectile(20,"right","lvl" + str(self.player_age),self.turret_sounds["hit"][self.player_age-1]))
                    else:
                        self.player_turret_frame = 1
            else:
                self.player_turret_frame = 1

            turret_id = "turret" + str(self.player_age) + "_" + str(self.player_turret_frame)
            self.draw_screen.blit(self.textures["turret"][turret_id], (self.scrool, 110))

        if self.computer_turret:
            if len(self.soldiers) and self.soldiers[0].x > 440:
                self.turret_timer += self.dt
                if self.turret_timer >= 70:
                    self.turret_timer = 0
                    if self.computer_turret_frame == 1:
                        self.computer_turret_frame = 2
                        self.turret_sounds["fire"][self.computer_age - 1].play()
                        self.projectiles.append(Projectile(620,"left","lvl" + str(self.computer_age),self.turret_sounds["hit"][self.computer_age-1]))
                    else:
                        self.computer_turret_frame = 1

            turret_id = "turret" + str(self.computer_age) + "_" + str(self.computer_turret_frame)
            self.draw_screen.blit(pygame.transform.flip(self.textures["turret"][turret_id],True,False), (self.scrool + 610, 110))

        # soldiers
        for soldier in self.soldiers:
            self.draw_screen.blit(self.soldiers_animations[soldier.type][soldier.actual_animation][soldier.actual_frame],(soldier.x + self.scrool,soldier.y))
            state = round(soldier.actual_health / soldier.health * 10)
            if state != 10 and state >= 0:
                self.draw_screen.blit(self.textures["health_bar"]["health_bar" + str(state)],(soldier.x + self.scrool + int(soldier.width/2) - 6 ,soldier.y - 5))
        for soldier in self.enemy_soldiers:
            state = round(soldier.actual_health / soldier.health * 10)
            if state != 10 and state >= 0:
                self.draw_screen.blit(self.textures["health_bar"]["health_bar" + str(state)], (soldier.x + self.scrool + int(soldier.width/2) - 6 , soldier.y - 5))
            self.draw_screen.blit(pygame.transform.flip(self.soldiers_animations[soldier.type][soldier.actual_animation][soldier.actual_frame],True,False) ,(soldier.x + self.scrool,soldier.y))

        # particles
        for particle in self.particles:
            particle.update(self.dt,self.particles,self.scrool)
            surf = pygame.Surface((int(particle.s),int(particle.s)),pygame.SRCALPHA)
            surf.fill(particle.color)
            self.draw_screen.blit(surf,(particle.x,particle.y))

        # loot
        if self.loot_timer > 0:
            text = self.FONT_INFO.render("+" + str(self.loot),False,(255,255,255))
            rect = text.get_rect(center = (self.loot_pos + self.scrool + 4, 110 - int((250 - self.loot_timer)/25)))
            self.draw_screen.blit(self.textures["gui"]["coin2"],(rect.left - 9,rect.top - 1))
            self.draw_screen.blit(text,rect)

        # projectiles
        for projectile in self.projectiles:
            img = self.textures["projectiles"][projectile.type]
            if projectile.direction == "left":
                img = pygame.transform.flip(img,True,False)
            self.draw_screen.blit(img,(projectile.x + self.scrool,projectile.y))


        # gui background
        self.draw_screen.blit(self.textures["gui"]["gui"], (216, 5))
        name = None

        # buttons
        for button in self.gui.buttons:
            button.update(self.mouse)

            if button.type == "age" and self.player_age == 4:
                button.state = "disabled"
            if button.type == "gold" and self.gold_mine == 5:
                button.state = "disabled"
            elif button.type == "turret":
                if self.player_turret:
                    button.state = "disabled"
                elif button.state == "disabled":
                    button.state = "normal"
            elif button.type == "upgrade1":
                if self.unit1_lvl:
                    button.state = "disabled"
                elif button.state == "disabled":
                    button.state = "normal"
            elif button.type == "upgrade2":
                if self.unit2_lvl:
                    button.state = "disabled"
                elif button.state == "disabled":
                    button.state = "normal"
            elif button.type == "upgrade3":
                if self.unit3_lvl:
                    button.state = "disabled"
                elif button.state == "disabled":
                    button.state = "normal"

            if button.state == "normal":
                self.draw_screen.blit(self.textures["gui"]["button_normal"], (button.x,button.y))

            elif button.state == "on":
                type = button.type
                name, price = self.get_info(type)
                self.draw_screen.blit(self.textures["gui"]["button_on"], (button.x,button.y))

                if button.type == "unit1" or button.type == "unit2" or button.type == "unit3":
                    self.draw_screen.blit(self.textures["gui"]["info_bar"], (154, 5))

                    unit_id = str(self.player_age) + "_" + button.type[4]
                    if (button.type == "unit1" and self.unit1_lvl) or (button.type == "unit2" and self.unit2_lvl) or (button.type == "unit3" and self.unit3_lvl):
                        unit_id += "+"
                    troop = NAMES[unit_id]
                    self.draw_screen.blit(self.textures["button_img_units"][troop], (158, 9))

                    self.draw_screen.blit(self.FONT_INFO.render(str(STATS[troop]["dmg"]),False,(255,255,255)), (183, 28))
                    self.draw_screen.blit(self.FONT_INFO.render(str(STATS[troop]["hp"]), False, (255, 255, 255)),(183, 35))
                    self.draw_screen.blit(self.FONT_INFO.render(str(int((STATS[troop]["speed"] + 70)/10)), False, (255, 255, 255)),(183, 42))
                    self.draw_screen.blit(self.FONT_INFO.render(str(int((STATS[troop]["rate"] + 70)/10)), False, (255, 255, 255)),(183, 49))
                    self.draw_screen.blit(self.FONT_INFO.render(str(STATS[troop]["range"]), False, (255, 255, 255)),(183, 56))

                elif button.type == "upgrade1" or button.type == "upgrade2" or button.type == "upgrade3":
                    self.draw_screen.blit(self.textures["gui"]["info_bar"], (154, 5))
                    self.draw_screen.blit(self.textures["button_img"][button.type], (158, 9))

                    unit_id = str(self.player_age) + "_" + button.type[7]
                    troop1 = NAMES[unit_id + "+"]
                    troop2 = NAMES[unit_id]

                    self.draw_screen.blit(self.FONT_INFO.render(str(STATS[troop2]["dmg"]),False,(255,255,255)), (183, 28))
                    self.draw_screen.blit(self.FONT_INFO.render(str(STATS[troop2]["hp"]), False, (255, 255, 255)),(183, 35))
                    self.draw_screen.blit(self.FONT_INFO.render(str(int((STATS[troop2]["speed"] + 70)/10)), False, (255, 255, 255)),(183, 42))
                    self.draw_screen.blit(self.FONT_INFO.render(str(int((STATS[troop2]["rate"] + 70)/10)), False, (255, 255, 255)),(183, 49))
                    self.draw_screen.blit(self.FONT_INFO.render(str(STATS[troop2]["range"]), False, (255, 255, 255)),(183, 56))

                    if STATS[troop1]["dmg"] - STATS[troop2]["dmg"] > 0:
                        self.draw_screen.blit(self.FONT_INFO.render("+" + str(STATS[troop1]["dmg"] - STATS[troop2]["dmg"]), False, (0, 255, 0)),(196, 28))
                    if STATS[troop1]["hp"] - STATS[troop2]["hp"] > 0:
                        self.draw_screen.blit(self.FONT_INFO.render("+" + str(STATS[troop1]["hp"] - STATS[troop2]["hp"]), False, (0, 255, 0)),(196, 35))
                    if STATS[troop1]["speed"] - STATS[troop2]["speed"] > 0:
                        self.draw_screen.blit(self.FONT_INFO.render("+" + str(int((STATS[troop1]["speed"] - STATS[troop2]["speed"])/ 10)), False, (0, 255, 0)),(196, 42))
                    if STATS[troop1]["rate"] - STATS[troop2]["rate"] > 0:
                        self.draw_screen.blit(self.FONT_INFO.render("+" + str(int((STATS[troop1]["rate"] - STATS[troop2]["rate"]) /10)), False, (0, 255, 0)),(196, 49))
                    if STATS[troop1]["range"] - STATS[troop2]["range"] > 0:
                        self.draw_screen.blit(self.FONT_INFO.render("+" + str(STATS[troop1]["range"] - STATS[troop2]["range"]), False, (0, 255, 0)),(196, 56))

                elif button.type == "gold":
                    self.draw_screen.blit(self.textures["gui"]["info_bar2"], (158, 5))
                    self.draw_screen.blit(self.textures["button_img"][button.type], (162, 9))
                    self.draw_screen.blit(self.FONT_INFO.render(str(GOLD["lvl" + str(self.gold_mine + 1)]) + " Gold", False, (0, 255, 0)), (181, 14))

                elif button.type == "special":
                    # special timer
                    state = round(self.special_timer / (SPECIAL_TIMER[self.difficulty] * FRAMERATE * 60) * 10) + 1
                    self.draw_screen.blit(self.textures["hourglass"]["hourglass" + str(state)], (296, 75))

            elif button.state == "disabled":
                self.draw_screen.blit(self.textures["gui"]["button_disabled"], (button.x, button.y))

            if button.state != "disabled":
                if button.type == "unit1" or button.type == "unit2" or button.type == "unit3":
                    unit_id = str(self.player_age) + "_" + button.type[4]
                    if (button.type == "unit1" and self.unit1_lvl) or (button.type == "unit2" and self.unit2_lvl) or (button.type == "unit3" and self.unit3_lvl):
                        unit_id += "+"
                    troop = NAMES[unit_id]
                    self.draw_screen.blit(self.textures["button_img_units"][troop], (button.x, button.y))
                else:
                    self.draw_screen.blit(self.textures["button_img"][button.type],(button.x,button.y))

            if button.clicked:
                if button.type == "unit1" or button.type == "unit2" or button.type == "unit3":
                    if len(self.queue) < 5 and len(self.soldiers) < 10:

                        unit_id = str(self.player_age) + "_" + button.type[4]
                        if (button.type == "unit1" and self.unit1_lvl) or (button.type == "unit2" and self.unit2_lvl) or (button.type == "unit3" and self.unit3_lvl):
                            unit_id += "+"
                        troop = NAMES[unit_id]

                        if unit_id == "4_3+":
                            sound_id = "titan"
                        else:
                            sound_id = unit_id.replace("+","")

                        if self.gold >= PRICES[troop]:
                            self.gold -= PRICES[troop]
                            self.queue.append(Soldier(troop, "right", self.soldiers_animations[troop]["idle"][0],self.soldiers_sounds[sound_id]))

                elif button.type == "upgrade1" or button.type == "upgrade2" or button.type == "upgrade3":

                    id = "upgrade" + button.type[7] + "_" + str(self.player_age)

                    if self.gold >= PRICES[id]:
                        self.gold -= PRICES[id]
                        if button.type == "upgrade1":
                            self.unit1_lvl = True
                        elif button.type == "upgrade2":
                            self.unit2_lvl = True
                        elif button.type == "upgrade3":
                            self.unit3_lvl = True


                elif button.type == "turret":
                    id = "turret" + str(self.player_age)
                    if self.gold >= PRICES[id]:
                        self.gold -= PRICES[id]
                        self.player_turret = True

                elif button.type == "gold":
                    id = "gold" + str(self.gold_mine + 1)
                    if self.gold >= PRICES[id]:
                        self.gold -= PRICES[id]
                        self.gold_mine += 1

                elif button.type == "age":
                    id = "age" + str(self.player_age + 1)
                    if self.gold >= PRICES[id]:
                        self.gold -= PRICES[id]
                        self.player_age += 1
                        self.player_turret = False
                        self.unit1_lvl = False
                        self.unit2_lvl = False
                        self.unit3_lvl = False

                elif button.type == "special":
                    if self.special_timer >= SPECIAL_TIMER[self.difficulty] * FRAMERATE * 60:
                        self.special_timer = 0
                        for i in range(0,640,64):
                            self.projectiles.append(Projectile(i,"right","special" + str(self.player_age),self.special_sounds[self.player_age-1],0-i))

            button.clicked = False

        # info about button
        if name != None:
            text = self.FONT_INFO.render(name, False, (0,0,0))
            rect = text.get_rect(center = (265, 79))
            self.draw_screen.blit(text, rect)
            text = self.FONT_INFO.render(str(price), False, (0,0,0))
            rect = text.get_rect(center=(265, 89))
            self.draw_screen.blit(text, rect)

        # gold info
        gold = self.FONT.render(str(self.gold),False,self.FONT_COLOR)
        self.draw_screen.blit(self.textures["gui"]["coin"],(5,5))
        self.draw_screen.blit(gold,(24,8))
        self.draw_screen.blit(self.textures["gui"]["coin2"], (9, 25))
        self.draw_screen.blit(self.FONT_INFO.render(str(GOLD["lvl" + str(self.gold_mine)]), False, (255, 255, 255)), (20, 26))

        # queue
        self.draw_screen.blit(self.textures["queue"]["queue" + str(len(self.queue) + 1)], (224,52))
        if len(self.queue) > 0:
            if self.queue[0].lvl == 1:
                max_time = 250
            elif self.queue[0].lvl == 2:
                max_time = 500
            elif self.queue[0].lvl == 3:
                max_time = 1000
            state = round(self.unit_timer/max_time * 10)
            self.draw_screen.blit(self.textures["load_bar"]["load_bar" + str(state)] , (229,63))


        # mouse
        self.draw_screen.blit(self.textures["cursor"]["cursor" + str(self.mouse.texture_index + 1)],(self.mouse.x - 1, self.mouse.y - 2))

    def refresh_screen(self):
        self.screen.blit(pygame.transform.scale(self.draw_screen,self.screen_size),(0,0))
        pygame.display.update()
        self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000

Game()
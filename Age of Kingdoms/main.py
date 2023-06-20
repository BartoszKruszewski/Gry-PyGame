import pygame, sys, random, os
from mouse import Mouse
from background import Background
from soldier import Soldier
from gui import Gui
from CONST import *
from STATS import *
from building import Building
from grain import Grain
from FUNCTIONS import *
from arrow import Arrow


SCREEN_RESOLUTION = (1280,720)
FULLSCREEN = True
VERSION = "1.0"

class Game():
    def __init__(self):

        # pre init
        pygame.mixer.pre_init(44100,-16,2,512)

        pygame.init()
        pygame.mixer.set_num_channels(110)

        # screen
        self.screen_size = SCREEN_RESOLUTION
        if FULLSCREEN:
            self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.screen_size)

        pygame.display.set_caption("Age of Kingdoms")
        pygame.display.set_icon(pygame.image.load("icon.png"))

        self.draw_screen = pygame.Surface((640, 360))

        # load textures and sounds
        self.load_textures()
        self.load_sounds()

        # clock and mouse
        self.clock = pygame.time.Clock()
        self.dt = 1
        self.mouse = Mouse(self.textures["cursor"]["cursor1"])

        # fonts
        self.FONT = pygame.font.Font("Minimal3x5.ttf",16)
        self.FONT_TITLE = pygame.font.Font("Minimal3x5.ttf", 64)
        self.FONT_INFO = pygame.font.Font("Minimal3x5.ttf", 8)
        self.FONT_COLOR = pygame.Color("white")

        # init
        self.running = False

        self.menu()

    def end_game(self,win):

        self.running = False
        self.start = False
        background = self.draw_screen.copy()
        for i in range(25):
            background = blurSurf(background,2.0)
            self.draw_screen.blit(background, (0, 0))
            self.refresh_screen()

        while True:
            if win:
                self.draw_caption("YOU WIN",background)
            else:
                self.draw_caption("YOU LOOSE",background)

    def draw_caption(self, caption,background):
        length = self.FONT_TITLE.render(caption, False, (255, 255, 255)).get_width()
        pos = ((640 - length) / 2, 180)
        timer = len(caption) * 15
        while timer > 0:
            if self.start:
                break
            timer -= self.dt
            p = 1 - (timer / len(caption) / 15)
            lighten = int(len(caption) * p)
            if lighten >= len(caption):
                lighten = len(caption) - 1
            self.check_keys()
            self.draw_screen.blit(background,(0,0))
            text = self.FONT_TITLE.render(caption[:lighten], False, (255, 255, 255))
            rect = text.get_rect(midleft=pos)
            self.draw_screen.blit(text, rect)
            text = self.FONT_TITLE.render(caption[lighten], False, (255, 150, 0))
            rect = text.get_rect(midleft=rect.midright)
            self.draw_screen.blit(text, rect)
            text = self.FONT_TITLE.render(caption[lighten + 1:], False, (255, 255, 255))
            rect = text.get_rect(midleft=rect.midright)
            self.draw_screen.blit(text, rect)
            self.refresh_screen()
            self.check_events()

    def create_background(self):
        self.grains = []
        AMOUNT = 300
        for i in range(AMOUNT):
            self.grains.append(Grain(420 + 860/AMOUNT*i))
        self.background = []
        for i in range(6):
            self.background.append(Background(i + 1))

    def pre_init(self):
        self.true_scrool = -1 * BASE_POS[0]
        self.scrool = -1 * BASE_POS[0]
        self.target_scrool = -1 * BASE_POS[0]
        self.wind = 0
        self.create_background()
        self.particles = []
        self.projectiles = []
        self.soldier_ids = []

        for i in range(1,50):
            self.soldier_ids.append(i)
        self.main_channel = pygame.mixer.Channel(0)

        # set stats
        self.gold = START_GOLD
        self.food = START_FOOD

        self.player_base_health = BASE_HP
        self.max_base_health = BASE_HP
        self.buildings = [Building("farm",self.textures["buildings"]["farm"]),Building("town_hall",self.textures["buildings"]["town_hall"]),Building("base",self.textures["buildings"]["base"]),Building("guild",self.textures["buildings"]["guild"])]
        self.upgrades = []
        self.queue = []
        self.soldiers = []
        self.dead_soldiers = []
        self.tower_lvl = 0
        self.tower_timer = TOWER_ATTACK_SPEED[0]

        self.computer_base_health = BASE_HP
        self.computer_queue = []
        self.enemy_soldiers = []
        self.computer_phase = 0
        self.computer_units_to_spawn = []

        self.loot_timer = 0
        self.loot = 0
        self.loot_pos = 0

        self.unit_timer = 0
        self.unit_time = 0
        self.draw_game()

    def menu(self):

        pygame.mixer_music.load("music/soundtrack2.wav")
        pygame.mixer_music.set_volume(0.1)
        pygame.mixer_music.play()

        self.gui = Gui("menu")
        self.start = False
        self.pre_init()

        # background
        background = self.draw_screen.copy()
        background_blured = blurSurf(background, 6.0)

        while not self.start:
            self.draw_caption("PRESS SPACE TO START", background_blured)
            self.check_events()
            self.check_keys()
            self.mouse.update(self.screen_size)

        # blur out
        for i in range(25,0,-1):
            background_blured = blurSurf(background, 1 + i/5)
            self.draw_screen.blit(background_blured, (0, 0))
            self.refresh_screen()

        # start the game
        self.game()

    def game(self):
        self.music = ["music/soundtrack1.wav","music/soundtrack3.wav"]
        # load and play music
        pygame.mixer_music.load(random.choice(self.music))
        pygame.mixer_music.play()

        # init
        self.gui = Gui("game")
        self.running = True

        self.COMPUTER_BUY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.COMPUTER_BUY, START_SPAWN_DELAY)

        self.CHANGE_PHASE = pygame.USEREVENT + 2
        pygame.time.set_timer(self.CHANGE_PHASE, PHASE_CHANGE_TIME[0])

        self.ADD_FOOD = pygame.USEREVENT + 3
        pygame.time.set_timer(self.ADD_FOOD, 1000)

        # game loop
        while self.running:
            # music
            if not pygame.mixer.music.get_busy():
                pygame.mixer_music.load(random.choice(self.music))
                pygame.mixer_music.play()

            # update stuff
            self.check_events()
            self.check_keys()
            self.mouse.update(self.screen_size)

            # scrool
            if self.mouse.x > 620:
                self.target_scrool -= self.dt * 3
            elif self.mouse.x < 20:
                self.target_scrool += self.dt * 3

            self.target_scrool = min(self.target_scrool,0)
            self.target_scrool = max(self.target_scrool,-640)

            self.true_scrool += (self.target_scrool - self.true_scrool) / 20 * self.dt

            self.scrool = int(self.true_scrool)

            # update soldiers
            for soldier in self.soldiers:
                self.computer_base_health -= soldier.update(self.soldiers,self.enemy_soldiers,self.dt,self.projectiles,self.particles,self.sounds,self.scrool)
            for soldier in self.enemy_soldiers:
                self.player_base_health -= soldier.update(self.soldiers,self.enemy_soldiers,self.dt,self.projectiles,self.particles,self.sounds,self.scrool)

            # update projectiles
            for projectile in self.projectiles:
                if projectile.direction == "right":
                    self.computer_base_health -= int(projectile.update(self.dt,self.soldiers,self.enemy_soldiers,self.projectiles,self.upgrades,self.particles,self.sounds["archer"]["hit"]))
                else:
                    self.player_base_health -= int(projectile.update(self.dt,self.soldiers,self.enemy_soldiers,self.projectiles,self.upgrades,self.particles,self.sounds["archer"]["hit"]))

            # update wind
            if random.randint(1,500) == 1:
                self.wind += random.randint(1,200) -100
                self.wind = max(self.wind,0)
                self.wind = min(self.wind,100)

            # queue timer
            self.unit_timer += self.dt
            if len(self.queue) > 0:
                self.unit_time = min(self.unit_time,self.queue[0].time)
                self.unit_time = self.queue[0].time

                if self.unit_timer >= self.unit_time and (len(self.soldiers) == 0 or self.soldiers[-1].x > BASE_POS[0] + self.queue[0].w):
                    self.soldiers.append(self.queue[0])
                    self.sounds[self.queue[0].type]["start"][0].play()
                    self.queue.remove(self.queue[0])
                    self.unit_timer = 0
            else:
                self.unit_timer = 0

            # spawn computer units
            if len(self.computer_units_to_spawn) > 0:
                if len(self.computer_units_to_spawn) > 2:
                    self.computer_units_to_spawn.pop(-1)
                if len(self.enemy_soldiers) == 0 or self.enemy_soldiers[-1].x < BASE_POS[1] - self.computer_units_to_spawn[0].w:
                    self.enemy_soldiers.append(self.computer_units_to_spawn[0])
                    self.computer_units_to_spawn.pop(0)

            # tower
            if self.tower_lvl > 0:
                self.tower_timer -= self.dt
                self.tower_timer = max(self.tower_timer,0)
                range = TOWER_RANGE[self.tower_lvl -1]
                if "range" in self.upgrades:
                    range *= UPGRADES["range"]
                if len(self.enemy_soldiers) > 0 and self.enemy_soldiers[0].left - BASE_POS[0] < range  and self.tower_timer == 0:
                    self.main_channel.play(random.choice(self.sounds["archer"]["shot"]))
                    if self.tower_lvl > 1:
                        self.projectiles.append(Arrow(BASE_POS[0] + 40,"tower" + str(self.tower_lvl),self.enemy_soldiers[0].centerx))
                    self.projectiles.append(Arrow(BASE_POS[0] + 70, "tower" + str(self.tower_lvl), self.enemy_soldiers[0].centerx))
                    self.tower_timer = TOWER_ATTACK_SPEED[self.tower_lvl -1]

            # loot
            self.loot_timer -= self.dt

            if len(self.enemy_soldiers) > 0 and self.enemy_soldiers[0].actual_health <= 0:
                self.loot = int((PRICES[self.enemy_soldiers[0].type][0] + PRICES[self.enemy_soldiers[0].type][1]) * GOLD_DROP_MULT)
                if "finances" in self.upgrades:
                    self.loot = int(self.loot * UPGRADES["finances"])
                self.loot_pos = self.enemy_soldiers[0].centerx
                self.loot_timer = 250
                self.gold += self.loot

            # remove soldiers
            if len(self.soldiers) > 0 and self.soldiers[0].actual_health <= 0:
                self.dead_soldiers.append(self.soldiers[0])
                self.dead_soldiers[-1].actual_frame = 0
                self.soldiers.pop(0)

            if len(self.enemy_soldiers) > 0 and self.enemy_soldiers[0].actual_health <= 0:
                self.dead_soldiers.append(self.enemy_soldiers[0])
                self.dead_soldiers[-1].actual_frame = 0
                self.enemy_soldiers.pop(0)

            # update dead soldiers
            for soldier in self.dead_soldiers:
                soldier.update(self.soldiers,self.enemy_soldiers,self.dt,self.projectiles,self.particles,self.sounds,self.scrool)
                if soldier.actual_frame == SOLDIERS_SHOT_FRAMES[soldier.type]["dead"] and not soldier.sound_played:
                    soldier.sound_played = True
                    soldier.channel.play(self.sounds[soldier.type]["dead"][0])
                if soldier.end:
                    self.dead_soldiers.remove(soldier)
                    self.soldier_ids.append(soldier.id)

            # draw
            self.draw_game()
            self.refresh_screen()

            # check base health
            if self.player_base_health <= 0:
                self.end_game(False)
            elif self.computer_base_health <= 0:
                self.end_game(True)

    def check_events(self):
        for event in pygame.event.get():

            # click on exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            # computer buy unit
            if self.running and event.type == self.COMPUTER_BUY and len(self.enemy_soldiers) < 10:
                if len(self.computer_queue) == 0:
                    for i in range(ENEMY_SPAWN[self.computer_phase][0]):
                        self.computer_queue.append("knight")
                    for i in range(ENEMY_SPAWN[self.computer_phase][1]):
                        self.computer_queue.append("archer")
                    for i in range(ENEMY_SPAWN[self.computer_phase][2]):
                        self.computer_queue.append("paladin")
                    for i in range(ENEMY_SPAWN[self.computer_phase][3]):
                        self.computer_queue.append("mage")
                    for i in range(ENEMY_SPAWN[self.computer_phase][4]):
                        self.computer_queue.append("griffin")

                choice = random.choice(self.computer_queue)
                self.computer_queue.remove(choice)
                id = self.soldier_ids[0]
                self.soldier_ids.pop(0)
                self.computer_units_to_spawn.append(Soldier(choice, "left",id))
                pygame.time.set_timer(self.COMPUTER_BUY, random.randint(ENEMY_SPAWN_RATE[self.computer_phase][0], ENEMY_SPAWN_RATE[self.computer_phase][1]))

            if self.running and event.type == self.ADD_FOOD:
                self.food += FOOD_ADD
                if "plows" in self.upgrades:
                    self.food += UPGRADES["plows"]
                if "flock" in self.upgrades:
                    self.food += UPGRADES["flock"]
                if "cattle" in self.upgrades:
                    self.food += UPGRADES["cattle"]
                if "granary" in self.upgrades:
                    self.food += UPGRADES["granary"]
                if "windmill" in self.upgrades:
                    self.food += UPGRADES["windmill"]
                if "tools" in self.upgrades:
                    self.player_base_health += UPGRADES["tools"]
                    self.player_base_health = min(self.player_base_health,self.max_base_health)


            if self.running and event.type == self.CHANGE_PHASE:
                self.computer_phase += 1
                self.computer_phase = min(4,self.computer_phase)
                if self.computer_phase < 4:
                    pygame.time.set_timer(self.CHANGE_PHASE, PHASE_CHANGE_TIME[self.computer_phase])

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit(0)
        if keys[pygame.K_SPACE] and self.gui.type == "menu":
            self.start = True

    def load_sounds(self):
        self.sounds = {}
        other = {}
        for dir in os.listdir("sounds"):
            if dir[-4:] == ".wav":
                other[dir.replace(".wav", "")] = pygame.mixer.Sound("sounds/" + dir)
            else:
                soldier = {}
                for sub_dir in os.listdir("sounds/" + dir):
                    sounds = []
                    for file in os.listdir("sounds/" + dir + "/" + sub_dir):
                        sounds.append(pygame.mixer.Sound("sounds/" + dir + "/" + sub_dir + "/" + file))
                    soldier[sub_dir] = sounds
                self.sounds[dir] = soldier
        self.sounds["other"] = other

    def load_textures(self):

        # load textures
        self.textures = {}
        for dir in os.listdir("img"):
            if dir != "soldiers":
                if dir[-4:] == ".png":
                    self.textures[dir.replace(".png", "")] = pygame.image.load("img/" + dir).convert_alpha()
                else:
                    textures = {}
                    for file in os.listdir("img/" + dir):
                        textures[file.replace(".png","")] = pygame.image.load("img/" + dir + "/" + file).convert_alpha()
                    self.textures[dir] = textures

        # load soldiers animations
        self.soldiers_animations = {}
        types = ["knight","paladin","archer","griffin","mage"]
        for type in types:
            self.soldiers_animations[type] = self.load_animations(type,False)

        self.enemy_soldiers_animations = {}
        types = ["knight", "paladin", "archer", "griffin", "mage"]
        for type in types:
            self.enemy_soldiers_animations[type] = self.load_animations(type,True)

    def load_animations(self,name,enemy=False):
        animations = {}
        img = pygame.image.load("img/soldiers/" + name + ".png").convert_alpha()
        types = ["idle","walk","dead","attack"]
        current_frame = 0
        for type in types:
            animation = []
            for frame in range(SOLDIERS_ANIMATIONS[name][type]):
                frame_img = pygame.Surface(SOLDIERS_IMG[name],pygame.SRCALPHA)
                frame_img.blit(img,(SOLDIERS_IMG[name][0]*current_frame*-1,0))
                current_frame += 1
                if enemy:
                    frame_img = pygame.transform.flip(frame_img, True, False)
                    if not name == "griffin":
                        for color in COLORS[name]:
                            frame_img = change_pallete(frame_img,color[0],color[1])
                animation.append(frame_img)
            animations[type] = animation
        return animations

    def draw_game(self):

        # background
        self.draw_screen.fill(pygame.Color("skyblue3"))

        # parallax background
        for element in self.background:
            self.draw_screen.blit(self.textures["background"]["terrain" + str(element.img_index)],(int(element.x + (self.scrool / element.horizon)) ,element.y))

        # enemy base and base hp
        state = self.player_base_health / BASE_HP
        self.draw_screen.blit(liveBar(state,BASE_BAR_SIZE,(172,50,50),self.max_base_health), (self.scrool + BASE_POS[0] + 8, 180))

        state = self.computer_base_health / BASE_HP
        self.draw_screen.blit(liveBar(state,BASE_BAR_SIZE,(172,50,50),BASE_HP), (self.scrool + BASE_POS[1] + 40, 180))
        self.draw_screen.blit(pygame.transform.flip(self.textures["buildings"]["base"],True,False),(self.scrool + BASE_POS[1], 193))

        # buildings
        selected = None
        sorted_buildings = []
        building_types =[]

        # sort
        for order in BUILDING_ORDER:
            for building in self.buildings:
                if building.type == order:
                    building_types.append(building.type)
                    sorted_buildings.append(building)

        # draw
        for building in sorted_buildings:
                building.update(self.mouse,self.scrool,self.dt)
                if building.state == "on":
                    selected = building
                if building.type == "base" and self.tower_lvl > 0:
                    light = self.textures["buildings"]["base_tower" + str(self.tower_lvl)].copy().convert_alpha()
                    intense = int(building.actual_light)
                    light.fill((int(intense / 4), int(intense / 3), intense), special_flags=pygame.BLEND_RGBA_MULT)
                    img = self.textures["buildings"]["base_tower" + str(self.tower_lvl)].copy().convert_alpha()
                    img.blit(light,(0,0),special_flags=pygame.BLEND_RGBA_ADD)
                    self.draw_screen.blit(img,(self.scrool + building.x, building.y))
                else:
                    light = self.textures["buildings"][building.type].copy().convert_alpha()
                    intense = int(building.actual_light)
                    light.fill((int(intense / 4), int(intense / 3), intense), special_flags=pygame.BLEND_RGBA_MULT)
                    img = self.textures["buildings"][building.type].copy().convert_alpha()
                    img.blit(light, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                    self.draw_screen.blit(img, (self.scrool + building.x, building.y))
                if building.clicked:
                    self.gui = building.gui
                building.clicked = False

        for building in self.buildings:
            if building == selected:
                building.target_light = 255
            else:
                building.target_light = 0

        info_on = False

        # draw selected
        if selected != None:
            info_on = True
            surf = self.FONT.render(selected.type.replace("_", "  "), False, (255, 255, 255))
            self.draw_screen.blit(surf, getRect(surf, (INFO_POS[0], INFO_POS[1])))
            lines = split_lines(INFO_BUILDING[selected.type], 20)
            for line in lines:
                surf = self.FONT.render(line, False, (255, 255, 255))
                self.draw_screen.blit(surf, getRect(surf, (INFO_POS[2], INFO_POS[3] + lines.index(line) * INFO_POS[4])))

        # soldiers
        for soldier in self.soldiers:
            self.draw_screen.blit(self.soldiers_animations[soldier.type][soldier.actual_animation][soldier.actual_frame],(soldier.x + self.scrool,soldier.y))
            if soldier.actual_health > 0:
                state = soldier.actual_health / soldier.health
                if state < 1:
                    surf = liveBar(state,HEALTH_BAR_SIZE,(172,50,50),STATS[soldier.type]["hp"])
                    rect = surf.get_rect(center = (soldier.centerx + self.scrool, GROUND_LVL - soldier.height - 1))
                    self.draw_screen.blit(surf,rect)

        for soldier in self.enemy_soldiers:
            self.draw_screen.blit(self.enemy_soldiers_animations[soldier.type][soldier.actual_animation][soldier.actual_frame],(soldier.x + self.scrool, soldier.y))
            if soldier.actual_health > 0:
                state = soldier.actual_health / soldier.health
                if state < 1:
                    surf = liveBar(state, HEALTH_BAR_SIZE, (172, 50, 50), STATS[soldier.type]["hp"])
                    rect = surf.get_rect(center=(soldier.centerx + self.scrool, GROUND_LVL - soldier.height - 1))
                    self.draw_screen.blit(surf, rect)

        for soldier in self.dead_soldiers:
            if soldier.direction == "right":
                self.draw_screen.blit(self.soldiers_animations[soldier.type][soldier.actual_animation][soldier.actual_frame],(soldier.x + self.scrool,soldier.y))
            else:
                self.draw_screen.blit(self.enemy_soldiers_animations[soldier.type][soldier.actual_animation][soldier.actual_frame],(soldier.x + self.scrool, soldier.y))

        # grains
        for grain in self.grains:
            grain.update(self.soldiers + self.enemy_soldiers,self.dt,self.wind)
            img_org = self.textures["grains"][grain.img].copy()
            texture = rotCenter(img_org, grain.angle * -1)
            self.draw_screen.blit(texture, (self.scrool + grain.x, grain.y))

        # floor
        self.draw_screen.blit(self.textures["floor"], (self.scrool, 0))

        # loot
        if self.loot_timer > 0:
            text = self.FONT_INFO.render("+" + str(self.loot),False,(255,255,255))
            rect = text.get_rect(center = (self.loot_pos + self.scrool + 14, 250 - int((250 - self.loot_timer)/25)))
            self.draw_screen.blit(self.textures["gui"]["gold_info"],(rect.left - 16,rect.top - 5))
            self.draw_screen.blit(text,rect)

        # projectiles
        for projectile in self.projectiles:
            img = rotCenter(self.textures["arrow"],projectile.angle)
            if projectile.direction == "left":
                img = pygame.transform.flip(img,True,False)
            self.draw_screen.blit(img,(projectile.x + self.scrool,projectile.y))

        # particles
        for particle in self.particles:
            particle.update(self.dt,self.particles)
            surf = pygame.Surface((particle.w,particle.h),pygame.SRCALPHA)
            surf.fill(particle.color)
            surf.set_alpha(int(particle.opacity))
            self.draw_screen.blit(surf,(particle.x + self.scrool,particle.y))

        # gui background
        self.draw_screen.blit(self.textures["gui"]["gui"], (432, 10))

        # buttons
        for button in self.gui.buttons:

            # unlocks
            if button.type == "tower2" and self.tower_lvl == 1 and not self.mouse.left_click:
                button.state = "normal"
            elif button.type == "tower3" and self.tower_lvl == 2 and not self.mouse.left_click:
                button.state = "normal"
            elif button.type == "archer" and "archery" in building_types:
                button.state = "normal"
            elif button.type == "paladin" and "blacksmith" in building_types:
                button.state = "normal"
            elif button.type == "mage" and "mage_tower" in building_types:
                button.state = "normal"
            elif button.type == "griffin" and "griffin_rampart" in building_types:
                button.state = "normal"

            button.update(self.mouse,self.dt)
            img = self.textures["gui"]["button_normal"].copy()
            img.convert_alpha()
            intense = int(button.actual_light)
            img.fill((int(intense/4), int(intense/3), intense), special_flags=pygame.BLEND_RGBA_ADD)
            if button.state == "on":

                # info text
                if not self.gui.type == "base" or len(self.queue) == 0:
                    info_on = True
                    surf = self.FONT.render(button.type.replace("_", "  "), False, (255, 255, 255))
                    self.draw_screen.blit(surf, getRect(surf,(INFO_POS[0], INFO_POS[1])))
                    lines = split_lines(INFO_BUTTON[button.type],20)
                    for line in lines:
                        surf = self.FONT.render(line, False, (255, 255, 255))
                        rect = getRect(surf,(INFO_POS[2], INFO_POS[3] + lines.index(line) * INFO_POS[4]))
                        self.draw_screen.blit(surf, rect)

                    if PRICES[button.type][0] > 0:
                        food = self.FONT.render(str(PRICES[button.type][0]), False, self.FONT_COLOR)
                        if PRICES[button.type][1] > 0:
                            self.draw_screen.blit(self.textures["gui"]["food_info"], (479, rect.bottom + 3))
                            self.draw_screen.blit(food, (500, rect.bottom + 6))
                        else:
                            self.draw_screen.blit(self.textures["gui"]["food_info"], (515, rect.bottom + 3))
                            self.draw_screen.blit(food, (536, rect.bottom + 6))

                    if PRICES[button.type][1] > 0:
                        gold = self.FONT.render(str(PRICES[button.type][1]), False, self.FONT_COLOR)
                        if PRICES[button.type][0] > 0:
                            self.draw_screen.blit(self.textures["gui"]["gold_info"], (544, rect.bottom + 3))
                            self.draw_screen.blit(gold, (565, rect.bottom + 6))
                        else:
                            self.draw_screen.blit(self.textures["gui"]["gold_info"], (515, rect.bottom + 3))
                            self.draw_screen.blit(gold, (536, rect.bottom + 6))

                # info bars
                if self.gui.type == "base":
                    self.draw_screen.blit(self.textures["gui"]["info_bar"], (310, 10))
                    troop = button.type
                    self.draw_screen.blit(self.textures["button_img"][troop], (318, 18))

                    stats = {
                        "dmg":STATS[troop]["dmg"],
                        "hp":STATS[troop]["hp"],
                        "speed":STATS[troop]["speed"],
                        "rate":STATS[troop]["rate"],
                        "range":STATS[troop]["range"]
                    }

                    if "armor" in self.upgrades:
                        stats["hp"] = int(stats["hp"] * UPGRADES["armor"])
                    if "swords" in self.upgrades:
                        stats["dmg"] = int(stats["dmg"] * UPGRADES["swords"])
                    if "range" in self.upgrades:
                        stats["range"] = int(stats["range"] * UPGRADES["range"])
                    if troop != "archer" and "fencing" in self.upgrades:
                        stats["range"] = int(stats["range"] + UPGRADES["fencing"])
                    if troop == "griffin" and "frenzy" in self.upgrades:
                        stats["rate"] = stats["rate"] + UPGRADES["frenzy"][1]
                    if troop == "griffin" and "frenzy" in self.upgrades:
                        stats["speed"] = stats["speed"] + UPGRADES["frenzy"][0]
                    if troop == "archer" and "sharpshooters" in self.upgrades:
                        stats["rate"] = stats["rate"] + UPGRADES["sharpshooters"][0]
                    if troop == "archer" and "sharpshooters" in self.upgrades:
                        stats["dmg"] = int(stats["dmg"] * UPGRADES["sharpshooters"][1])
                    if troop == "mage" and "lightning" in self.upgrades:
                        stats["dmg"] = int(stats["dmg"] * UPGRADES["lightning"])

                    i = 0
                    for key in stats.keys():
                        if key == "speed" or key == "rate":
                            info = str(int(stats[key]*100)) + " %"
                        else:
                            info = str(stats[key])
                        if stats[key] == STATS[troop][key]:
                            self.draw_screen.blit(self.FONT.render(info,False,(255,255,255)), (366, 56 + i * 14))
                        else:
                            self.draw_screen.blit(self.FONT.render(info, False, (0, 255, 0)),(366, 56 + i * 14))
                        i += 1

            elif button.state == "disabled":
                img = self.textures["gui"]["button_disabled"].copy()

            if not((button.type == "tower2" and self.tower_lvl != 1) or (button.type == "tower3" and self.tower_lvl != 2)):
                self.draw_screen.blit(img, (button.x, button.y))

            if button.state != "disabled":
                self.draw_screen.blit(self.textures["button_img"][button.type], (button.x, button.y))

            if button.clicked:
                if self.food >= PRICES[button.type][0] and self.gold >= PRICES[button.type][1]:
                    if self.gui.type == "base":
                        if len(self.queue) < 5 and len(self.soldiers) < 10:
                            self.food -= PRICES[button.type][0]
                            self.gold -= PRICES[button.type][1]
                            id = self.soldier_ids[0]
                            self.soldier_ids.pop(0)
                            self.queue.append(Soldier(button.type, "right", id, self.upgrades))

                    elif self.gui.type == "town_hall":
                        self.food -= PRICES[button.type][0]
                        self.gold -= PRICES[button.type][1]
                        if button.type[:-1] == "tower":
                            self.tower_lvl += 1
                        else:
                            self.buildings.append(Building(button.type,self.textures["buildings"][button.type]))
                        button.state = "disabled"
                        self.main_channel.play(self.sounds["other"]["build"])

                    else:
                        self.food -= PRICES[button.type][0]
                        self.gold -= PRICES[button.type][1]
                        self.upgrades.append(button.type)
                        button.state = "disabled"
                        self.main_channel.play(self.sounds["other"]["upgrade"])
                        if button.type == "fortifications":
                            self.max_base_health = BASE_HP + UPGRADES["fortifications"]
                            self.player_base_health += UPGRADES["fortifications"]
                            self.player_base_health = min(self.player_base_health,self.max_base_health)

            button.clicked = False

        # gold info
        gold = self.FONT.render(str(self.gold),False,self.FONT_COLOR)
        self.draw_screen.blit(self.textures["gui"]["gold_info"],(16,16))
        self.draw_screen.blit(gold,(36,18))

        # food info
        food = self.FONT.render(str(self.food), False, self.FONT_COLOR)
        self.draw_screen.blit(self.textures["gui"]["food_info"], (16, 35))
        self.draw_screen.blit(food, (36, 37))

        # queue
        if not info_on:
            if len(self.queue) > 0:
                self.draw_screen.blit(self.textures["queue"]["queue" + str(len(self.queue))], (492, 60))
                state = self.unit_timer/self.queue[0].time
                self.draw_screen.blit(liveBar(state,(68,8),(238,195,154)), (502,80))

        # mouse
        self.draw_screen.blit(self.textures["cursor"]["cursor" + str(self.mouse.texture_index + 1)],(self.mouse.x - 1, self.mouse.y - 2))

    def refresh_screen(self):
        self.screen.blit(pygame.transform.scale(self.draw_screen,self.screen_size),(0,0))
        pygame.display.update()
        self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000



Game()
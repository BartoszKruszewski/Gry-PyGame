import pygame, sys ,os, time, random
from tile import Tile
from player import Player
from background import Background
from wind import Wind
from game_map import Game_Map
from game_map import Chunk
from mouse import Mouse
from backpack import Backpack
from mob import Mob
from backpack import Item
from menu import Menu
from menu import Button
from tool import Tool
from particle import Particle
from STATS import *

def top(x):
    if int(x) < x:
        return int(x) + 1
    else:
        return int(x)

def get_red_points(img):
    img_size = img.get_size()
    points = []
    for y in range(img_size[1]):
        for x in range(img_size[0]):
            if img.get_at((x,y)) == (255,0,0):
                points.append((x,y))
    return points

class Game:

    def __init__(self):
        # initialization
        pygame.mixer.pre_init(48000,-16,2,512)
        pygame.init()
        pygame.mixer.set_num_channels(10)
        self.clock = pygame.time.Clock()
        self.dt = 1
        self.current_menu = "game"
        self.click = False
        read = open("last_save.txt","r")
        self.last_save = read.readline()
        read.close()

        # screen
        self.display_info = pygame.display.Info()
        self.screen_size = (1280, 720)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.draw_screen = pygame.Surface((320,180))

        # font
        self.FONT = pygame.font.Font("Minimal3x5.ttf",8)
        self.FONT_COLOR = pygame.Color("white")

        # mouse
        self.mouse = Mouse()
        pygame.mouse.set_visible(False)

        # sounds
        self.load_sounds()
        self.load_music()
        self.sounds_on = True

        # menus
        self.menu_main = Menu("main")
        self.menu_new_world = Menu("new_world")
        self.menu_load_world = Menu("load_world")
        self.menu_skill_sheet = Menu("skill_sheet")

        if self.last_save == "":
            self.game(False)
        else:
            self.game(True)

    def game(self,load):

        # init
        self.current_menu = "game"
        self.play_music()
        self.load_blocks_textures()

        self.game_map = {}
        self.game_map["normal"] = Game_Map()

        self.blood_rect = pygame.Surface((320, 180), pygame.SRCALPHA)
        self.blood_rect_alpha = 0
        self.light_map = pygame.Surface((320, 180), pygame.SRCALPHA)
        self.light_map_alpha = 0

        self.background = Background()

        if load:
            if self.load_world(self.last_save):
                print("World Loaded Correct")
            else:
                print("World Load Failed")
                self.player = Player()
                self.actual_quest = 0
        else:
            self.player = Player()
            self.time = 255
            self.actual_quest = 0

        # scroll
        self.scroll = [0, 0]

        # events
        self.ANIMATEPLAYER = pygame.USEREVENT
        pygame.time.set_timer(self.ANIMATEPLAYER, int(1000 / len(self.player.animations[self.player.actual_animation])))

        self.UPDATELEAVES = pygame.USEREVENT + 1
        if DYNAMIC_TREES:
            pygame.time.set_timer(self.UPDATELEAVES, 200)
            self.rendered_tree_types = []
        else:
            self.rendered_tree_types = []
            for type in TILES.keys():
                if type[-5:] == "_tree":
                    self.rendered_tree_types.append(type)
            self.update_tree_textures()

        # wind
        self.wind = Wind()

        self.pass_portal = True

        # first draw
        self.draw_game()

        # game loop
        while self.current_menu == "game":

            for item in self.player.backpack.items:
                if item[0].type in QUESTS[self.actual_quest][1]:
                    self.actual_quest += 1
                    if self.actual_quest > len(QUESTS) - 1:
                        self.actual_quest = len(QUESTS) - 1

            if self.pass_portal:
                self.pass_portal = False
                self.game_map["dark"] = Game_Map("dark")
                self.player.actual_world = "dark"
                self.player.real_y = -50
                self.player.real_x = 0
                self.player.backpack.add_item("obsydian_pickaxe", False, 1)
                self.player.backpack.tools.append(Tool("obsydian_pickaxe"))

            # change time
            self.time += self.dt / 100
            if self.time > 510:
                self.time = 0

            if self.player.actual_world == "dark":
                self.time = 25

            # play music
            if not pygame.mixer.music.get_busy:
                self.play_music()

            # check stuff
            self.check_events()
            self.mouse.update(self.player, self.current_menu)
            self.check_keys("straight")

            self.wind.update()

            # change scroll
            self.scroll[0] += (self.player.x - self.scroll[0] - 166) / 30 * self.dt
            self.scroll[1] += (self.player.y - self.scroll[1] - 106) / 30 * self.dt

            # change player
            self.set_timers()
            self.player.update(self.game_map[self.player.actual_world], self.scroll, self.mouse, self.blocks_textures, self.dt,self.sounds_on)

            # change gui
            self.player.backpack.update(self.mouse, self.game_map[self.player.actual_world], self.player,self.dt)

            # draw
            self.draw_game()
            self.refresh_screen()

    def main_menu(self):
        self.current_menu = "main"

        while self.current_menu == "main":
            # play music
            if not pygame.mixer.music.get_busy():
                self.play_music()

            self.check_events()
            if self.current_menu == "main":
                self.draw_menu()
            self.refresh_screen()

    def skill_sheet(self):

        self.current_menu = "skill_sheet"

        while self.current_menu == "skill_sheet":
            self.check_events()
            if self.current_menu == "skill_sheet":
                self.draw_skill_sheet()
            self.refresh_screen()

    def new_world(self):
        self.current_menu = "new_world"

        self.user_text = ""

        while self.current_menu == "new_world":
            self.check_events()
            self.draw_new_world_menu()
            self.refresh_screen()

    def load_world_menu(self):

        self.current_menu = "load_world"

        self.menu_scroll = 0
        self.mouse.update(None,self.current_menu)

        while self.current_menu == "load_world":
            self.check_events()
            self.draw_load_world_menu()
            self.refresh_screen()

    def set_timers(self):
        if self.player.last_animation != self.player.actual_animation:

            if self.player.actual_animation == "jump-end":
                pygame.time.set_timer(self.ANIMATEPLAYER, 100)
            elif self.player.actual_animation == "use":
                pygame.time.set_timer(self.ANIMATEPLAYER, 250)
            elif self.player.actual_animation == "idle":
                pygame.time.set_timer(self.ANIMATEPLAYER, 500)
            else:
                pygame.time.set_timer(self.ANIMATEPLAYER,int(400 / len(self.player.animations[self.player.actual_animation])))

    def save_world(self,worldname):
        try:
            f = open("saves/" + worldname + "/blocks.txt","w")
        except:
            os.mkdir("saves/" + worldname)
            f = open("saves/" + worldname + "/blocks.txt", "w")
        for chunk in self.game_map["normal"].chunks:
            for block in self.game_map["normal"].chunks[chunk].blocks:
                f.write(str(block.x) + ";" + str(block.y) + ";" + str(block.type) + ";" + str(block.x_in_chunk) + ";" + str(block.y_in_chunk) + ";" + str(block.chunk_x) + ";" + str(block.chunk_y) + ";" + str(block.biom))
                f.write("\n")
        f.close()

        f = open("saves/" + worldname + "/mobs.txt","w")
        for mob in self.game_map["normal"].mobs:
            f.write(mob.type + ";" + str(mob.x) + ";" + str(mob.y))
            f.write("\n")
        f.close()

        f = open("saves/" + worldname + "/items.txt", "w")
        for item in self.player.backpack.items:
            f.write(str(item[0].pos) + ";" + item[0].type + ";" + str(item[1]))
            f.write("\n")
        f.close()

        f = open("saves/" + worldname + "/skills.txt", "w")
        for skill in self.player.skills.keys():
            f.write(str(self.player.skills[skill]))
            f.write("\n")
        f.close()

        f = open("saves/" + worldname + "/other.txt", "w")
        f.write(str(int(self.time)) + "\n")
        f.write(str(self.player.x) + ";" + str(self.player.y) + "\n")
        f.write(str(int(self.player.exp)) + "\n")
        f.write(str(int(self.player.lvl)) + "\n")
        f.write(str(int(self.player.skill_points)) + "\n")
        f.write(str(int(self.actual_quest)) + "\n")
        f.close()

    def load_world(self,worldname):
        f = open("saves/" + worldname + "/blocks.txt","r")
        blocks_string = f.readlines()
        for block_string in blocks_string:
            block_list = block_string.split(";")
            block_list[7] = block_list[7].replace("\n","")
            tile = Tile(int(block_list[0]),int(block_list[1]),block_list[2],int(block_list[3]),int(block_list[4]),int(block_list[5]),int(block_list[6]),block_list[7])
            target_chunk = str(tile.chunk_x) + ";" + str(tile.chunk_y)
            if target_chunk not in self.game_map["normal"].chunks:
                blocks = []
                blocks.append(tile)
                self.game_map["normal"].chunks[target_chunk] = Chunk(tile.chunk_x,tile.chunk_y,blocks,tile.biom)
            else:
                self.game_map["normal"].chunks[target_chunk].blocks.append(tile)
        f.close()
        f = open("saves/" + worldname + "/mobs.txt", "r")
        mobs_string = f.readlines()
        for mob_string in mobs_string:
            mob_list = mob_string.split(";")
            mob_list[2] = mob_list[2].replace("\n","")
            mob = Mob(mob_list[0],int(mob_list[1]),int(mob_list[2]))
            self.game_map["normal"].mobs.append(mob)
        f.close()

        f = open("saves/" + worldname + "/skills.txt", "r")
        data = f.readlines()
        skills = {}
        skill_names = []
        for skill_name in SKILLS.keys():
            skill_names.append(skill_name)
        for skill in skill_names:
            if data[skill_names.index(skill)].rstrip() == "False":
                skills[skill] = False
            else:
                skills[skill] = True
        f.close()

        f = open("saves/" + worldname + "/other.txt", "r")
        data = f.readlines()
        self.time = int(data[0].rstrip())
        pos = data[1].split(";")
        exp = int(data[2].rstrip())
        lvl = int(data[3].rstrip())
        points = int(data[4].rstrip())
        self.actual_quest = int(data[5].rstrip())
        self.player = Player(int(pos[0]), int(pos[1].rstrip()), skills,exp,lvl,points)
        f.close()

        f = open("saves/" + worldname + "/items.txt", "r")
        items_string = f.readlines()

        for item_string in items_string:
            item_list = item_string.split(";")

            item_list[2] = item_list[2].replace("\n", "")
            item = Item(int(item_list[0]), item_list[1])
            self.player.backpack.items.append((item,int(item_list[2])))
            if item.type in TOOLS.keys():
                self.player.backpack.tools.append(Tool(item.type))
        f.close()

        return True

    def refresh_screen(self):
        self.screen.blit(pygame.transform.scale(self.draw_screen, self.screen_size), (0, 0))
        pygame.display.update()
        self.dt = self.clock.tick(FRAMERATE) * 144 / 1000

    def check_keys(self,type):
        keys = pygame.key.get_pressed()
        if self.current_menu == "game":

            if type == "straight":
                self.player.moving = False
                if keys[pygame.K_d]:
                    self.player.speed_x = 0.5
                    if self.player.skills["shoes"]:
                        self.player.speed_x = 0.6
                    self.player.moving = True
                    if self.player.speed_x > 0:
                        self.player.direction = "right"
                    else:
                        self.player.direction = "left"
                    if keys[pygame.K_LCTRL] and self.player.skills["super_speed"]:
                        self.player.speed_x *= 2
                        self.game_map[self.player.actual_world].particles.append(Particle(self.player.rect.centerx - 1, self.player.rect.bottom, "fire"))
                if keys[pygame.K_a]:
                    self.player.moving = True
                    self.player.speed_x = -0.5
                    if self.player.skills["shoes"]:
                        self.player.speed_x = -0.6
                    if self.player.speed_x > 0:
                        self.player.direction = "right"
                    else:
                        self.player.direction = "left"
                    if keys[pygame.K_LCTRL] and self.player.skills["super_speed"]:
                        self.player.speed_x *= 2
                        self.game_map[self.player.actual_world].particles.append(Particle(self.player.rect.centerx + 1, self.player.rect.bottom, "fire"))
                if keys[pygame.K_SPACE]:
                    if self.player.jump_end:
                        self.player.speed_y = 2
                        self.player.jump_end = False
                        self.player.double_jump = False
                    elif not self.player.double_jump and self.player.air_time > 20 and self.player.skills["double_jump"]:
                        self.player.speed_y = 2
                        self.player.double_jump = True
            else:


                if keys[pygame.K_e]:
                    if self.player.backpack.full_open == False:
                        self.player.backpack.full_open = True
                    else:
                        self.player.backpack.full_open = False

                if keys[pygame.K_ESCAPE]:
                        if self.player.backpack.full_open:
                            self.player.backpack.full_open = False
                        else:
                            self.main_menu()



        elif self.current_menu == "main" or self.current_menu == "skill_sheet":
            if keys[pygame.K_ESCAPE]:
                self.current_menu = "game"

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.last_save == "":
                    self.new_world()
                    self.last_save = self.user_text
                self.save_world(self.last_save)
                file = open("last_save.txt", "w")
                file.write(self.last_save)
                file.close()
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN and not self.click:
                self.click = True
                self.check_keys("single")

            if event.type == pygame.KEYUP:
                self.click = False

            if self.current_menu == "new_world" and self.menu_new_world.buttons[0].on:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    elif len(self.user_text)<23:
                        self.user_text += event.unicode

            if self.current_menu == "game":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4 and not self.player.backpack.full_open:
                        if self.player.backpack.rounded_item_number < 8:
                            self.player.backpack.rounded_item_number += 1
                        else:
                            self.player.backpack.rounded_item_number = 1
                    if event.button == 5 and not self.player.backpack.full_open:
                        if self.player.backpack.rounded_item_number > 1:
                            self.player.backpack.rounded_item_number -= 1
                        else:
                            self.player.backpack.rounded_item_number = 8
                if event.type == self.ANIMATEPLAYER:
                    if self.player.texture_index < len(self.player.animations[self.player.actual_animation]) - 1:
                        self.player.texture_index += 1
                    else:
                        self.player.texture_index = 0
                if event.type == self.UPDATELEAVES:
                    pygame.time.set_timer(self.UPDATELEAVES, int(1000 / (self.wind.speed+3)))
                    self.update_tree_textures()

            elif self.current_menu == "load_world":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.menu_scroll -= 10
                    if event.button == 5:
                        self.menu_scroll += 10

    def draw_background(self):
        # draw background
        if self.time <= 255:
            tone = self.time
        else:
            tone = -1 * (self.time - 510)
        self.draw_screen.fill((0, tone//2, tone))

        # background
        try:
            x = self.player.actual_chunk_x
            y = self.player.actual_chunk_y
            if self.player.actual_chunk_x < 0:
                x -= 1
            background_biom = self.game_map[self.player.actual_world].chunks[str(x) + ";" + str(y)].biom
        except:
            background_biom = "woodland"
        if background_biom == "none" or background_biom == "cave" or background_biom == "underground" or background_biom == "dark_underground":
            background_biom = "woodland"

        if self.background.type != background_biom and self.background.alpha > 0:
            self.background.alpha -= 17
            if self.background.alpha > 255:
                shadow = pygame.Surface((320,160),pygame.SRCALPHA)
                shadow.fill((0,0,0,510 - self.background.alpha))
                img1 = pygame.image.load("img/background/" + self.background.type + "/" + self.background.type + "1.png")
                img1.blit(shadow,(0,0),special_flags=pygame.BLEND_RGBA_SUB)
                img2 = pygame.image.load("img/background/" + self.background.type + "/" + self.background.type + "2.png")
                img2.blit(shadow,(0,0),special_flags=pygame.BLEND_RGBA_SUB)
                img3 = pygame.image.load("img/background/" + self.background.type + "/" + self.background.type + "3.png")
                img3.blit(shadow,(0,0),special_flags=pygame.BLEND_RGBA_SUB)

                self.background.img1 = img1
                self.background.img2 = img2
                self.background.img3 = img3

            elif self.background.alpha <= 255:
                shadow = pygame.Surface((320, 160), pygame.SRCALPHA)
                shadow.fill((0, 0, 0, self.background.alpha))
                img1 = pygame.image.load("img/background/" + background_biom + "/" + background_biom + "1.png")
                img1.blit(shadow, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
                img2 = pygame.image.load("img/background/" + background_biom + "/" + background_biom + "2.png")
                img2.blit(shadow, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
                img3 = pygame.image.load("img/background/" + background_biom + "/" + background_biom + "3.png")
                img3.blit(shadow, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

                self.background.img1 = img1
                self.background.img2 = img2
                self.background.img3 = img3
        else:
            self.background.alpha = 510
            self.background.type = background_biom
            self.background.img1 = pygame.image.load("img/background/" + background_biom + "/" + background_biom + "1.png")
            self.background.img2 = pygame.image.load("img/background/" + background_biom + "/" + background_biom + "2.png")
            self.background.img3 = pygame.image.load("img/background/" + background_biom + "/" + background_biom + "3.png")

        self.background.update(self.scroll)

        self.draw_screen.blit(self.background.img3, self.background.pos3_1)
        self.draw_screen.blit(self.background.img3, self.background.pos3_2)

        self.draw_screen.blit(self.background.img2, self.background.pos2_1)
        self.draw_screen.blit(self.background.img2, self.background.pos2_2)

        self.draw_screen.blit(self.background.img1, self.background.pos1_1)
        self.draw_screen.blit(self.background.img1, self.background.pos1_2)

    def draw_light(self,drawn_chunks):
        if self.player.y > 120:
            if self.light_map_alpha < 255:
                self.light_map_alpha += 5
            if self.sounds_on and self.channel_weather.get_busy():
                self.channel_weather.stop()
        else:
            if self.time <= 255:
                tone = self.time
            else:
                tone = -1 * (self.time - 510)
            self.light_map_alpha = -1 * (tone - 255)

            if self.sounds_on and not self.channel_weather.get_busy():
                self.channel_weather.play(self.sounds["weather"]["wind"])

        if self.light_map_alpha < 0:
            self.light_map_alpha = 0
        elif self.light_map_alpha > 255:
            self.light_map_alpha = 255

        self.light_map.fill((0,0,0,int(self.light_map_alpha)))
        if self.light_map_alpha > 0:
            size = -1.5 * (self.light_map_alpha - 255)
            if self.player.y <= 120:
                size = size * size / 5
            if size < 80:
                size = 80
            # draw round
            for i in range(10):
                pygame.draw.circle(self.light_map, (0, 0, 0, self.light_map_alpha - (i * 0.1 * self.light_map_alpha)), (self.player.x + 6 - int(self.scroll[0]), self.player.y + 16 - int(self.scroll[1])), size - i)
                for chunk in drawn_chunks:
                    for torch in self.game_map[self.player.actual_world].chunks[chunk].torches:
                        pygame.draw.circle(self.light_map, (0, 0, 0, self.light_map_alpha - (i * 0.1 * self.light_map_alpha)),(torch[0] - int(self.scroll[0]), torch[1] - int(self.scroll[1])), 40 - i)
        self.draw_screen.blit(self.light_map,(0,0))

    def draw_skill_sheet(self):
        # draw menu
        self.draw_screen.blit(self.pause_background, (0, 0))
        self.draw_screen.blit(self.menu_skill_sheet.background, (12, 12))
        text = self.FONT.render("Research Points:  " + str(self.player.skill_points), False, self.FONT_COLOR)
        text_rect = text.get_rect(midright=(300, 24))
        self.draw_screen.blit(text, text_rect)
        text = self.FONT.render("Actual Quest:  ", False, self.FONT_COLOR)
        text_rect = text.get_rect(midright=(300, 54))
        self.draw_screen.blit(text, text_rect)
        text = self.FONT.render(QUESTS[self.actual_quest][0], False, self.FONT_COLOR)
        text_rect = text.get_rect(midright=(300, 64))
        self.draw_screen.blit(text, text_rect)
        info = QUESTS[self.actual_quest][2].split("/")
        for line in info:
            text = self.FONT.render(line, False, self.FONT_COLOR)
            text_rect = text.get_rect(midright=(300, info.index(line) * 10 + 80))
            self.draw_screen.blit(text, text_rect)
        self.draw_screen.blit(self.blocks_textures[QUESTS[self.actual_quest][1][0]], (284, text_rect.bottom + 5))


        self.mouse.update(None, self.current_menu)


        for button in self.menu_skill_sheet.buttons:
            draw = True
            if SKILLS[button.type] != None:
                for skill in SKILLS[button.type]:
                    if not self.player.skills[skill]:
                        draw = False

            if button.update(self.mouse):
                if draw and self.player.skill_points > 0 and not self.player.skills[button.type]:
                    self.player.skill_points -= 1
                    self.player.skills[button.type] = True

            self.draw_screen.blit(button.img, (button.x, button.y))


            if draw:
                self.draw_screen.blit(self.skill_textures[button.type], (button.x + 1, button.y + 1))
                if button.collide:
                    text = self.FONT.render(INFO[button.type], False, self.FONT_COLOR)
                    text_rect = text.get_rect(midright=(300, 34))
                    self.draw_screen.blit(text, text_rect)
            else:
                self.draw_screen.blit(self.skill_textures["unknown"], (button.x + 1, button.y + 1))
                if button.collide:
                    if button.type != "dark_portal":
                        info = "Research previous skill to unlock"
                    else:
                        info = "Research all other skills to unlock"
                    text = self.FONT.render(info, False, self.FONT_COLOR)
                    text_rect = text.get_rect(midright=(300, 34))
                    self.draw_screen.blit(text, text_rect)

        # draw mouse
        self.draw_screen.blit(self.mouse.images[self.mouse.image_index], (self.mouse.x - 8, self.mouse.y - 8))

    def draw_load_world_menu(self):
        # draw menu
        self.draw_screen.blit(self.pause_background, (0, 0))
        self.draw_screen.blit(self.menu_load_world.background, (105, 12))

        self.mouse.update(None, self.current_menu)

        for button in self.menu_load_world.buttons:
            if button.update(self.mouse):
                if button.text == "Back":
                    self.current_menu = "main"
                elif button.y >= 15 and button.y <= 95:
                    self.last_save = button.text
                    self.game(True)
            if button.y >= 15 and button.y <= 95 or button.text == "Back":
                self.draw_screen.blit(button.img, (button.x, button.y))
                text = self.FONT.render(button.text, False, self.FONT_COLOR)
                text_rect = text.get_rect(center=button.center)
                self.draw_screen.blit(text, text_rect)

        # draw mouse
        self.mouse.update(None, self.current_menu)
        self.draw_screen.blit(self.mouse.images[self.mouse.image_index], (self.mouse.x - 8, self.mouse.y - 8))

    def draw_new_world_menu(self):

        # draw menu
        self.draw_screen.blit(self.pause_background, (0, 0))
        self.draw_screen.blit(self.menu_new_world.background, (105, 12))

        self.mouse.update(None, self.current_menu)

        for button in self.menu_new_world.buttons:
            if button.update(self.mouse):
                if button.text == "Save":
                    self.current_menu = "end_game"

            self.draw_screen.blit(button.img,(button.x,button.y))
            text = self.FONT.render(button.text, False, self.FONT_COLOR)
            text_rect = text.get_rect(center=button.center)
            self.draw_screen.blit(text, text_rect)

        text = self.FONT.render(self.user_text,False,self.FONT_COLOR)
        self.draw_screen.blit(text,(self.menu_new_world.buttons[0].x+5,self.menu_new_world.buttons[0].y+7))

        # draw mouse
        self.mouse.update(None, self.current_menu)
        self.draw_screen.blit(self.mouse.images[self.mouse.image_index], (self.mouse.x - 8, self.mouse.y - 8))

    def draw_menu(self):
        # draw menu
        self.draw_screen.blit(self.pause_background, (0, 0))
        self.draw_screen.blit(self.menu_main.background, (105, 12))

        self.mouse.update(None, self.current_menu)

        for button in self.menu_main.buttons:
            if button.update(self.mouse):
                if button.text == "New World":
                    self.save_world(self.last_save)
                    self.last_save = ""
                    self.game(False)
                elif button.text == "Load World":
                    self.load_world_menu()

                elif button.text == "Skill Sheet":
                    self.skill_sheet()
                else:
                    print(self.last_save)
                    if self.last_save == "":
                        self.new_world()
                        self.last_save = self.user_text
                    self.save_world(self.last_save)
                    file = open("last_save.txt", "w")
                    file.write(self.last_save)
                    file.close()
                    pygame.quit()
                    sys.exit(0)

            self.draw_screen.blit(button.img, (button.x, button.y))
            text = self.FONT.render(button.text, False, self.FONT_COLOR)
            text_rect = text.get_rect(center=button.center)
            self.draw_screen.blit(text, text_rect)

        # draw mouse
        self.mouse.update(None, self.current_menu)
        self.draw_screen.blit(self.mouse.images[self.mouse.image_index], (self.mouse.x - 8, self.mouse.y - 8))

    def load_music(self):
        self.soundtracks = []
        for soundtrack in os.listdir("music/soundtracks"):
            self.soundtracks.append(soundtrack)

    def play_music(self):
        pygame.mixer.music.load("music/soundtracks/" + random.choice(self.soundtracks))
        pygame.mixer.music.play(1)
        pygame.mixer.music.set_volume(0.2)

    def load_sounds(self):
        self.sounds = {}
        weather = {}
        other = {}

        weather["wind"] = pygame.mixer.Sound("sounds/weather/wind.ogg")
        other["fire"] = pygame.mixer.Sound("sounds/fire/fire.ogg")

        self.sounds["weather"] = weather
        self.sounds["other"] = other

        self.channel_weather = pygame.mixer.Channel(9)
        self.channel_weather.set_volume(0.1)
        self.channel_fire = pygame.mixer.Channel(8)

    def load_blocks_textures(self):

        # blocks textures
        self.blocks_textures = {}
        self.tree_points = {}
        self.tree_textures = {}
        for entry in os.scandir('img/blocks'):
            if entry.is_file():
                type = entry.name[:-4]
                img = pygame.image.load("img/blocks/" + type + ".png").convert_alpha()
                self.blocks_textures[type] = img
                if type[-5:] == "_tree":
                    self.tree_points[type] = get_red_points(img)
                    new_img = img.copy()
                    for point in self.tree_points[type]:
                        new_img.set_at(point, new_img.get_at((point[0] + 1, point[1] + 1)))
                    self.tree_textures[type] = new_img

        # destroy textures
        self.destroy_textures = []
        texture = pygame.image.load("img/destroy/destroy1.png")
        self.destroy_textures.append(texture)
        texture = pygame.image.load("img/destroy/destroy2.png")
        self.destroy_textures.append(texture)
        texture = pygame.image.load("img/destroy/destroy3.png")
        self.destroy_textures.append(texture)
        texture = pygame.image.load("img/destroy/destroy4.png")
        self.destroy_textures.append(texture)

        # grains
        self.grains_textures = {}
        for file in os.listdir('img/blocks'):
            if file[-4:] != ".png":
                textures = []
                for img in os.listdir("img/blocks/" + file):
                    textures.append(pygame.image.load("img/blocks/" + file + "/" + img))
                self.grains_textures[file] = textures

        # custom images in EQ
        self.custom_textures = {}
        self.custom_textures["door_close"] = pygame.transform.scale(pygame.image.load("img/blocks/door_open.png"),(8,16))

        # exp bar
        self.exp_bar_textures = []
        for i in range(11):
            self.exp_bar_textures.append(pygame.image.load("img/gui/exp_bar/exp_bar" + str(i + 1) + ".png"))

        # skill textures
        self.skill_textures = {}
        for img in os.listdir("img/menu/skill_img"):
            self.skill_textures[img.replace(".png","")] = pygame.image.load("img/menu/skill_img/" + img)

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def dynamic_transform(self,type):
        points = self.tree_points[type]
        mask = pygame.Surface((3, 3), pygame.SRCALPHA)
        img = self.tree_textures[type].copy()
        new_img = img.copy()
        for point in points:
            mask.blit(img, (-1 * point[0], -1 * point[1]))
            new_img.blit(mask, (point[0] + random.randint(-2, 2), point[1] + random.randint(-2, 2)))
        return new_img

    def update_tree_textures(self):
        for type in list(set(self.rendered_tree_types)):
            if type[-5:] == "_tree":
                self.blocks_textures[type] = self.dynamic_transform(type)
        self.rendered_tree_types = []

    def draw_game(self):
        # draw background
        self.draw_background()

        # draw map
        grains = []
        drawn_chunks = []

        for y in range(4):
            for x in range(5):
                # select chunk
                target_x = x - 1 + int(round(self.scroll[0] / (CHUNK_SIZE * TEXTURE_RESOLUTION)))
                target_y = y - 1 + int(round(self.scroll[1] / (CHUNK_SIZE * TEXTURE_RESOLUTION)))
                target_chunk = str(target_x) + ";" + str(target_y)

                if not target_chunk in self.game_map[self.player.actual_world].chunks.keys():
                    self.game_map[self.player.actual_world].add_chunk((target_x,target_y),self.blocks_textures)

                self.game_map[self.player.actual_world].chunks[target_chunk].remove_items(self.player)

                # draw blocks
                drawn_chunks.append(target_chunk)
                for block in self.game_map[self.player.actual_world].chunks[target_chunk].blocks:
                    pos = (block.x - int(self.scroll[0]), block.y - int(self.scroll[1]))

                    if block.type == "dark_portal" and self.player.rect.colliderect(block):
                        self.pass_portal = True

                    if block.img == None:
                        if DYNAMIC_TREES and block.type[-5:] == "_tree":
                            self.rendered_tree_types.append(block.type)

                        if "animated" in TILES[block.type].keys():
                            for grain in block.grains:
                                grains.append(grain)
                        else:
                            if block.direction == "left":
                                img = pygame.transform.flip(self.blocks_textures[block.type],True,False)
                            else:
                                img = self.blocks_textures[block.type]
                            rect = img.get_rect()
                            self.draw_screen.blit(img,(pos[0] - ((rect.width-16)/2),pos[1] - rect.height + 16))
                    else:
                        self.draw_screen.blit(block.img,pos)


                    # draw destroy's textures
                    if block.destroy > 0:
                        fps = self.clock.get_fps()
                        frame = None
                        if block.destroy / fps / block.hardness <= 0.25:
                            frame = 0
                        elif block.destroy / fps / block.hardness <= 0.5 and block.destroy / 60 / block.hardness > 0.25:
                            frame = 1
                        elif block.destroy / fps / block.hardness <= 0.75 and block.destroy / 60 / block.hardness > 0.5:
                            frame = 2
                        elif block.destroy / fps / block.hardness >= 0.75:
                            frame = 3
                        if frame != None:
                            self.draw_screen.blit(self.destroy_textures[frame],pos)


                # draw dropped items
                for item in self.game_map[self.player.actual_world].chunks[target_chunk].dropped_items:
                    item.update(self.game_map[self.player.actual_world],self.dt)
                    self.draw_screen.blit(item.img,(int(item.x - self.scroll[0]),int(item.y - self.scroll[1])))

        # add fire to torch
        for chunk in drawn_chunks:
            for torch in self.game_map[self.player.actual_world].chunks[chunk].torches:
                if not self.channel_fire.get_busy():
                    self.channel_fire.play(self.sounds["other"]["fire"])
                self.game_map[self.player.actual_world].particles.append(Particle(torch[0] - 1, torch[1] - 3, "fire"))

        # draw player
        if not self.player.dead:
            texture = self.player.animations[self.player.actual_animation][self.player.texture_index][0]
            if self.player.direction == "left":
                texture = pygame.transform.flip(texture,True,False)
            self.draw_screen.blit(texture, (self.player.x - int(self.scroll[0]),self.player.y - int(self.scroll[1])))

        # draw tool in hand
        if not self.player.dead and self.player.tool != None:
            texture = self.player.tool.img
            if self.player.direction == "left":
                texture = pygame.transform.flip(texture, True, False)
            self.draw_screen.blit(texture, (int(self.player.tool_point_x - 1) - int(self.scroll[0]), int(self.player.tool_point_y - 9) - int(self.scroll[1])))
            if self.player.tool.speed == 0 and self.player.skills["holy_aura"]:
                if self.player.direction == "left":
                    self.game_map[self.player.actual_world].particles.append(Particle(self.player.tool_point_x - 1, self.player.tool_point_y - 11, "fire"))
                    self.game_map[self.player.actual_world].particles.append(Particle(self.player.tool_point_x + 1, self.player.tool_point_y - 9, "fire"))
                    self.game_map[self.player.actual_world].particles.append(Particle(self.player.tool_point_x + 3, self.player.tool_point_y - 7, "fire"))
                    self.game_map[self.player.actual_world].particles.append(Particle(self.player.tool_point_x + 5, self.player.tool_point_y - 5, "fire"))
                else:
                    self.game_map[self.player.actual_world].particles.append(Particle(self.player.tool_point_x + 9, self.player.tool_point_y - 9, "fire"))
                    self.game_map[self.player.actual_world].particles.append(Particle(self.player.tool_point_x + 7, self.player.tool_point_y - 9, "fire"))
                    self.game_map[self.player.actual_world].particles.append(Particle(self.player.tool_point_x + 5, self.player.tool_point_y - 7, "fire"))
                    self.game_map[self.player.actual_world].particles.append(Particle(self.player.tool_point_x + 3, self.player.tool_point_y - 5, "fire"))

        elif not self.player.dead and self.player.food != None and self.player.actual_animation == "idle":
            texture = pygame.transform.scale(self.blocks_textures[self.player.food.type],(8,8))
            if self.player.direction == "left":
                texture = pygame.transform.flip(texture, True, False)
            self.draw_screen.blit(texture, (int(self.player.tool_point_x - 2) - int(self.scroll[0]), int(self.player.tool_point_y - 5) - int(self.scroll[1])))

        # draw mobs
        mobs_on_screen = []
        for mob in self.game_map[self.player.actual_world].mobs:
            mob.actual_chunk_x = int(mob.x / 128)
            mob.actual_chunk_y = int(mob.y / 128)
            x = mob.actual_chunk_x
            y = mob.actual_chunk_y
            chunk = str(x) + ";" + str(y)
            if chunk in drawn_chunks:
                mobs_on_screen.append(mob)
        for mob in mobs_on_screen:
            mob.update(self.game_map[self.player.actual_world],self.scroll,self.player,mobs_on_screen,self.clock,self.dt)
            texture = mob.animations[mob.actual_animation][mob.animation_index]
            if mob.direction == "left":
                texture = pygame.transform.flip(texture, True, False)
            self.draw_screen.blit(texture, (mob.x - int(self.scroll[0]), mob.y - int(self.scroll[1]) - mob.shift))


        # draw grains
        for grain in grains:
            grain.update(self.player, self.wind, self.dt)
            img_org = self.grains_textures[grain.type][grain.img_index-1]
            texture = self.rot_center(img_org,grain.angle * -1)
            self.draw_screen.blit(texture, (grain.x - int(self.scroll[0]), grain.y - int(self.scroll[1])))



        # draw particles
        for particle in self.game_map[self.player.actual_world].particles:
            particle.update(self.game_map[self.player.actual_world])
            pygame.draw.rect(self.draw_screen,particle.color,(particle.x - int(self.scroll[0]),particle.y - int(self.scroll[1]),particle.width,particle.height))

        # draw light
        self.draw_light(drawn_chunks)

        # draw gui
        self.draw_screen.blit(self.player.backpack.img, (int(self.player.backpack.x), int(self.player.backpack.y)))
        self.draw_screen.blit(self.player.backpack.craft_img, (int(self.player.backpack.x) + 153, int(self.player.backpack.y)))
        if self.player.backpack.y == -74:
            self.draw_screen.blit(self.player.backpack.round_img, (self.player.backpack.round_x, 5))
        if self.player.backpack.light_visible:
            self.draw_screen.blit(self.player.backpack.light_img, self.player.backpack.light_pos)

        # draw exp bar
        if self.player.backpack.y == -74:
            exp_lvl = self.player.exp
            if exp_lvl > 10:
                exp_lvl = 10
            self.draw_screen.blit(self.exp_bar_textures[exp_lvl], (108 ,28))
            text = self.FONT.render(str(self.player.lvl), False, self.FONT_COLOR)
            self.draw_screen.blit(text, ((320 - text.get_rect().width)/2 + 4, 32))

        # draw items in EQ
        for item in self.player.backpack.items:
            if item[0].type in TOOLS.keys():
                self.draw_screen.blit(item[0].img, (int(item[0].x + 2), int(item[0].y + 2)))
            elif item[0].type == "door_close":
                self.draw_screen.blit(self.custom_textures["door_close"],(int(item[0].x + 4), int(item[0].y)))
                self.draw_screen.blit(self.FONT.render(str(item[1]), False, self.FONT_COLOR),(int(item[0].x + 8), int(item[0].y + 10)))
            else:
                self.draw_screen.blit(item[0].img, (int(item[0].x), int(item[0].y)))
                self.draw_screen.blit(self.FONT.render(str(item[1]), False, self.FONT_COLOR),(int(item[0].x + 8), int(item[0].y + 10)))
        # draw hearts
        for i in range(min(int(self.player.health),5)):
            self.draw_screen.blit(self.player.backpack.heart_img, (20 + i * 9, 3))
        for i in range(int(self.player.health) - 5):
            self.draw_screen.blit(self.player.backpack.armor_heart_img, (20 + i * 9, 3))
        for i in range(int(top(self.player.hunger))):
            self.draw_screen.blit(self.player.backpack.hunger_img, (20 + i * 9, 14))

        if self.player.dead:
            if self.blood_rect_alpha < 255:
                self.blood_rect_alpha += 2
            self.blood_rect.fill((120,0,0,self.blood_rect_alpha))
            self.draw_screen.blit(self.blood_rect,(0,0))
            if self.blood_rect_alpha >= 250:
                self.player.dead = False
        else:
            self.blood_rect_alpha = 0

        self.pause_background = self.draw_screen.copy()

        # draw mouse
        self.draw_screen.blit(self.mouse.images[self.mouse.image_index],(self.mouse.x - 8,self.mouse.y - 8))

        # draw info
        if self.player.backpack.y == 3:
            for item in self.player.backpack.items:
                if abs(item[0].x + 8 - self.mouse.x) <= 8 and abs(item[0].y + 8 - self.mouse.y) <= 8:
                    name = item[0].type
                    name = name.replace("_"," ")
                    if name == "door close":
                        name = "door"
                    text = self.FONT.render(name,False,self.FONT_COLOR)
                    self.draw_screen.blit(text,(text.get_rect(center = (160,70))))
                    break


        text = self.FONT.render(str(int(self.clock.get_fps())),False,self.FONT_COLOR)
        self.draw_screen.blit(text,(5,5))
        if self.player.backpack.y == -74:
            text1 = self.FONT.render("X: " + str(int(self.player.x/16)), False, self.FONT_COLOR)
            self.draw_screen.blit(text1, (320 - text1.get_rect().width - 5, 5))
            text2 = self.FONT.render("Y: " + str(int(self.player.y/16)), False, self.FONT_COLOR)
            self.draw_screen.blit(text2, (320 - text2.get_rect().width - text1.get_rect().width - 10, 5))


Game()
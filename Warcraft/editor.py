import pygame, os, sys, random
from mouse import Mouse
from button import Button
from CONST import *
from FUNCTIONS import *

class Program():
    def __init__(self):
        # init
        pygame.init()
        self.screen = pygame.display.set_mode((1280,720))
        self.draw_screen = pygame.Surface((320,180))
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.timer = 0
        self.mouse = Mouse(True)
        self.load_textures()
        self.load_fonts()
        self.create_stuff()

        self.buttons_scroll = 0
        self.brush = "grass0"
        self.map = {}
        self.side = "player"
        self.actual_gui = "tiles"
        self.map_name = ""
        self.typing_name = False
        self.last_letter = ""
        self.action_type = ""
        self.freeze_draw_screen = self.draw_screen.copy()

        self.scroll = [0,0]
        self.true_scroll = [0,0]
        self.target_scroll = [0,0]
        self.click_cooldown = 0
        while True:
            self.update()

    def create_stuff(self):
        def create_buttons():
            self.buttons.append(Button("save","menu",[246,20],(19,9)))
            self.buttons.append(Button("load","menu",[271,20],(19,9)))
            self.buttons.append(Button("erase","menu",[296,20],(16,16)))

            self.buttons.append(Button("player", "menu", [246, 2], (16, 16)))
            self.buttons.append(Button("enemy", "menu", [246, 2], (16, 16)))
            self.buttons.append(Button("buildings", "menu", [266, 2], (16, 16)))
            self.buttons.append(Button("troops", "menu", [266, 2], (16, 16)))
            self.buttons.append(Button("tiles", "menu", [266, 2], (16, 16)))

            self.buttons.append(Button("grass0","tiles",[246,40],(16,16)))
            self.buttons.append(Button("grass1","tiles",[266,40],(16,16)))
            self.buttons.append(Button("grass2","tiles",[286,40],(16,16)))
            self.buttons.append(Button("tree","tiles",[246,60],(16,16)))
            self.buttons.append(Button("water","tiles",[266,60],(16,16)))
            self.buttons.append(Button("path","tiles",[286,60],(16,16)))
            self.buttons.append(Button("goldmine", "buildings", [246, 40], (27, 19)))
            self.buttons.append(Button("townhall", "buildings", [279, 40], (27, 19)))
            self.buttons.append(Button("farm", "buildings", [246, 65], (27, 19)))
            self.buttons.append(Button("barrack", "buildings", [279, 65], (27, 19)))
            self.buttons.append(Button("lumbermill", "buildings", [246, 90], (27, 19)))
            self.buttons.append(Button("blacksmith", "buildings", [279, 90], (27, 19)))
            self.buttons.append(Button("tower", "buildings", [246, 115], (27, 19)))
            self.buttons.append(Button("stables", "buildings", [279, 115], (27, 19)))

            self.buttons.append(Button("peasant", "troops", [246, 40], (27, 19)))
            self.buttons.append(Button("swordsman", "troops", [279, 40], (27, 19)))
            self.buttons.append(Button("archer", "troops", [246, 65], (27, 19)))
            self.buttons.append(Button("catapult", "troops", [279, 65], (27, 19)))
            self.buttons.append(Button("knight", "troops", [246, 90], (27, 19)))

        self.buttons = []
        create_buttons()

    def save_map(self,name):
        file = open(name + ".txt","w")
        keys = self.map.keys()
        for key in keys:
            tile = self.map[key]
            if len(key.split("_")) > 1:
                line = key.split("_")[1] + ":" + tile.split("_")[0] + "_" + key.split("_")[0]
            else:
                line = key + ":" + tile.split("_")[0]
            file.write(line + "\n")
        file.close()

    def load_map(self,name):
        try:
            file = open(name + ".txt","r")
            data = file.readlines()
            file.close()
            self.map.clear()
            for line in data:
                info = line.split(":")
                info[2] = info[2].rstrip()
                if len(info[2].split("_")) > 1:
                    self.map[info[2].split("_")[1] + "_" + info[0] + ":" + info[1]] = info[2].split("_")[0]
                else:
                    self.map[info[0] + ":" + info[1]] = info[2]
            self.update_map()
        except:
            print("Can't load map!")

    def update_map(self):
        for key in self.map.keys():
            if len(key.split("_")) == 1:
                type = self.map[key].split("_")[0]
                self.map[key] = type + "_" + str(self.get_direction(pos_to_int(key), type))

    def get_direction(self, adress, type):
        is_around = [False, False, False, False]
        around = [
            [adress[0], adress[1] - 1],
            [adress[0] + 1, adress[1]],
            [adress[0], adress[1] + 1],
            [adress[0] - 1, adress[1]],
        ]
        i = 0
        for adress in around:
            key = pos_to_string(adress)
            if key in self.map.keys():
                tile_type = self.map[key].split("_")[0]
                if tile_type == type or (tile_type == "grass2" and type == "grass1"):
                    is_around[i] = True
            elif adress[0] < 0 or adress[1] < 0 or adress[0] >= MAP_SIZE[0] or adress[1] >= MAP_SIZE[1]:
                is_around[i] = True
            i += 1

        if type == "path":
            direction = 1
        else:
            direction = 4

        if not is_around[0] and is_around[1] and is_around[2] and not is_around[3]:
            direction = 0
        elif not is_around[0] and is_around[1] and is_around[2] and is_around[3]:
            direction = 1
        elif not is_around[0] and is_around[1] and not is_around[2] and is_around[3]:
            direction = 1
        elif not is_around[0] and not is_around[1] and is_around[2] and is_around[3]:
            direction = 2
        elif is_around[0] and is_around[1] and is_around[2] and not is_around[3]:
            direction = 3
        elif is_around[0] and not is_around[1] and is_around[2] and not is_around[3]:
            direction = 3
        elif is_around[0] and is_around[1] and is_around[2] and is_around[3]:
            direction = 4
        elif is_around[0] and not is_around[1] and is_around[2] and is_around[3]:
            direction = 5
        elif is_around[0] and not is_around[1] and is_around[2] and not is_around[3]:
            direction = 5
        elif is_around[0] and is_around[1] and not is_around[2] and not is_around[3]:
            direction = 6
        elif is_around[0] and is_around[1] and not is_around[2] and is_around[3]:
            direction = 7
        elif not is_around[0] and is_around[1] and not is_around[2] and is_around[3]:
            direction = 7
        elif is_around[0] and not is_around[1] and not is_around[2] and is_around[3]:
            direction = 8

        return direction


    def update(self):

        def update_click_cooldown():
            self.click_cooldown -= self.delta_time
            self.click_cooldown = max(self.click_cooldown,0)

        def add_tile(target):
            if target[0] >= 0 and target[0] < MAP_SIZE[0] and target[1] >= 0 and target[1] < MAP_SIZE[1]:
                adress = pos_to_string(target)
                if self.brush == "erase":
                    for key in self.map.keys():
                        if adress == key:
                            self.map.pop(key)
                            break
                elif len(self.brush.split("_")) == 1:
                    if self.brush == "grass0":
                        if random.randint(0,5) == 0:
                            direction = random.randint(0,8)
                        else:
                            direction = 5

                        if adress not in self.map.keys() or self.map[adress].split("_")[0] != "grass0":
                            self.map[adress] = self.brush + "_" + str(direction)
                    else:
                        if adress not in self.map.keys() or self.map[adress].split("_")[0] != self.brush:
                            self.map[adress] = self.brush + "_" + str(self.get_direction(target,self.brush))
                            around = get_points_in_radius(target, 2)
                            around.remove(target)
                            for point in around:
                                key = pos_to_string(point)
                                if key in self.map.keys():
                                    type = self.map[key].split("_")[0]
                                    if type == self.brush:
                                        self.map[key] = type + "_" + str(self.get_direction(point, type))
                elif self.brush.split("_")[0][1] == "b":
                    pos = target
                    if BUILDING_TILES[self.brush.split("_")[1]] == 4:
                        tiles = [
                            [pos[0], pos[1]],
                            [pos[0] + 1, pos[1]],
                            [pos[0], pos[1] + 1],
                            [pos[0] + 1, pos[1] + 1]
                        ]
                    elif BUILDING_TILES[self.brush.split("_")[1]] == 9:
                        tiles = [
                            [pos[0], pos[1]],
                            [pos[0] + 1, pos[1]],
                            [pos[0] + 2, pos[1]],
                            [pos[0], pos[1] + 1],
                            [pos[0] + 1, pos[1] + 1],
                            [pos[0] + 2, pos[1] + 1],
                            [pos[0], pos[1] + 2],
                            [pos[0] + 1, pos[1] + 2],
                            [pos[0] + 2, pos[1] + 2],
                        ]
                    can_add = True
                    for tile in tiles:
                        if pos_to_string(tile) in self.map.keys() and (self.map[pos_to_string(tile)].split("_")[0] == "tree" or self.map[pos_to_string(tile)].split("_")[0] == "water"):
                            can_add = False
                    if can_add:
                        self.map[self.side[0] + "b_" + adress] = self.brush.split("_")[1]

                elif self.brush.split("_")[0][1] == "t":
                    if not (adress in self.map.keys() and (self.map[adress].split("_")[0] == "tree" or self.map[adress].split("_")[0] == "water")):
                        self.map[self.side[0] + "t_" + adress] = self.brush.split("_")[1]

        def update_scroll():
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                self.target_scroll[0] += self.delta_time * SCROLL_SPEED
            elif keys[pygame.K_LEFT]:
                self.target_scroll[0] -= self.delta_time * SCROLL_SPEED
            if keys[pygame.K_DOWN]:
                self.target_scroll[1] += self.delta_time * SCROLL_SPEED
            elif keys[pygame.K_UP]:
                self.target_scroll[1] -= self.delta_time * SCROLL_SPEED

            self.target_scroll[0] = max(self.target_scroll[0],0)
            self.target_scroll[0] = min(self.target_scroll[0],MAP_SIZE[0] * SCALE - GAME_RESOLUTION[0] + 80)
            self.target_scroll[1] = max(self.target_scroll[1], 0)
            self.target_scroll[1] = min(self.target_scroll[1], MAP_SIZE[1] * SCALE - GAME_RESOLUTION[1] + 80)

            self.true_scroll[0] += (self.target_scroll[0] - self.true_scroll[0]) / 5 / self.delta_time
            self.true_scroll[1] += (self.target_scroll[1] - self.true_scroll[1]) / 5 / self.delta_time

            self.scroll[0] = int(round(self.true_scroll[0]))
            self.scroll[1] = int(round(self.true_scroll[1]))

        def update_textbox():
            if self.last_letter != "":
                self.map_name += self.last_letter
                self.last_letter = ""

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.typing_name = False
                if self.action_type == "save":
                    self.save_map(self.map_name)
                elif self.action_type == "load":
                    self.load_map(self.map_name)
                self.map_name = ""
                self.action_type = ""

        self.pre_progam_update()
        if self.typing_name:
            update_textbox()
        else:
            update_scroll()
            update_click_cooldown()
            if self.mouse.hold[1]:
                target = [0, 0]
                target[0] = int((self.mouse.pos[0] + self.scroll[0]) / SCALE)
                target[1] = int((self.mouse.pos[1] + self.scroll[1]) / SCALE)
                add_tile(target)
        self.draw()
        self.late_program_update()

    def late_program_update(self):
        self.screen.blit(pygame.transform.scale(self.draw_screen, (1280,720)), (0, 0))
        self.delta_time = self.clock.tick(60) * 60 / 1000
        self.timer += self.delta_time
        pygame.display.update()

    def pre_progam_update(self):
        def check_events():
            use_scroll = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.MOUSEWHEEL:
                    use_scroll = True
                    self.mouse.scroll = event.y

                if event.type == pygame.KEYDOWN:
                    self.last_letter = event.unicode
                    if event.key == pygame.K_BACKSPACE:
                        self.map_name = self.map_name[:-1]

            if not use_scroll:
                self.mouse.scroll = 0

        def update_buttons():
            for button in self.buttons:

                if self.side == "enemy":
                    if button.type == "player":
                        button.visible = True
                    elif button.type == "enemy":
                        button.visible = False
                elif self.side == "player":
                    if button.type == "player":
                        button.visible = False
                    elif button.type == "enemy":
                        button.visible = True

                if self.actual_gui == "buildings":
                    if button.type == "buildings":
                        button.visible = False
                    elif button.type == "troops":
                        button.visible = True
                    elif button.type == "tiles":
                        button.visible = False
                elif self.actual_gui == "troops":
                    if button.type == "troops":
                        button.visible = False
                    elif button.type == "buildings":
                        button.visible = False
                    elif button.type == "tiles":
                        button.visible = True
                elif self.actual_gui == "tiles":
                    if button.type == "troops":
                        button.visible = False
                    elif button.type == "buildings":
                        button.visible = True
                    elif button.type == "tiles":
                        button.visible = False

                if button.visible and (button.category == self.actual_gui or button.category == "menu"):
                    button.update(self.mouse, self.delta_time)
                    if button.click and self.click_cooldown == 0:
                        self.click_cooldown = CLICK_COOLDOWN
                        if button.category == "tiles":
                            self.brush = button.type
                        elif button.category == "buildings":
                            self.brush = self.side[0] + "b_" + button.type
                        elif button.category == "troops":
                            self.brush = self.side[0] + "t_" + button.type
                        elif button.type == "erase":
                            self.brush = "erase"
                        elif button.type == "save":
                            self.typing_name = True
                            self.action_type = "save"
                            self.freeze_draw_screen = modify_surf(self.draw_screen, "darken")
                        elif button.type == "load":
                            self.typing_name = True
                            self.action_type = "load"
                            self.freeze_draw_screen = modify_surf(self.draw_screen, "darken")
                        elif button.type == "player":
                            self.side = "player"
                        elif button.type == "enemy":
                            self.side = "enemy"
                        elif button.type == "buildings":
                            self.actual_gui = "buildings"
                        elif button.type == "troops":
                            self.actual_gui = "troops"
                        elif button.type == "tiles":
                            self.actual_gui = "tiles"

        check_events()
        self.mouse.update()
        update_buttons()

    def draw(self):
        def draw_map():
            keys = self.map.keys()
            for key in keys:
                if len(key.split("_")) > 1:
                    if key.split("_")[0][1] == "b":
                        pos = pos_to_int(key.split("_")[1])
                        if BUILDING_TILES[self.map[key]] == 4:
                            tiles = [
                                [pos[0], pos[1]],
                                [pos[0] + 1, pos[1]],
                                [pos[0], pos[1] + 1],
                                [pos[0] + 1, pos[1] + 1]
                            ]
                        elif BUILDING_TILES[self.map[key]] == 9:
                            tiles = [
                                [pos[0], pos[1]],
                                [pos[0] + 1, pos[1]],
                                [pos[0] + 2, pos[1]],
                                [pos[0], pos[1] + 1],
                                [pos[0] + 1, pos[1] + 1],
                                [pos[0] + 2, pos[1] + 1],
                                [pos[0], pos[1] + 2],
                                [pos[0] + 1, pos[1] + 2],
                                [pos[0] + 2, pos[1] + 2],
                            ]
                        i = 0
                        for tile in tiles:
                            self.draw_screen.blit(self.textures["buildings"][self.map[key] + "_" + str(i)],(tile[0] * SCALE - self.scroll[0], tile[1] * SCALE - self.scroll[1]))
                            i += 1
                    else:
                        pos = pos_to_int(key.split("_")[1])
                        if key.split("_")[0][0] == "p":
                            self.draw_screen.blit(self.textures["troops"][self.map[key]],(pos[0] * SCALE - self.scroll[0], pos[1] * SCALE - self.scroll[1]))
                        elif key.split("_")[0][0] == "e":
                            self.draw_screen.blit(self.textures["enemy_troops"][self.map[key]],(pos[0] * SCALE - self.scroll[0], pos[1] * SCALE - self.scroll[1]))
                else:
                    pos = pos_to_int(key)
                    self.draw_screen.blit(self.textures["tiles"][self.map[key]],(pos[0] * SCALE - self.scroll[0],pos[1] * SCALE - self.scroll[1]))

        def draw_brush():
            def set_color(surf, color):
                new_surf = surf.copy()
                for y in range(surf.get_height()):
                    for x in range(surf.get_width()):
                        pre_color = surf.get_at((x, y))
                        if pre_color[3] > 0:
                            new_color = (min(pre_color[0] + color[0], 255), min(pre_color[1] + color[1], 255),
                                         min(pre_color[2] + color[2], 255))
                            new_surf.set_at((x, y), new_color)
                return new_surf

            target = [0, 0]
            target[0] = int(self.mouse.pos[0] / SCALE)
            target[1] = int(self.mouse.pos[1] / SCALE)
            if len(self.brush.split("_")) > 1:
                pos = [0, 0]
                pos[0] = int((self.mouse.pos[0] + self.scroll[0]) / SCALE)
                pos[1] = int((self.mouse.pos[1] + self.scroll[1]) / SCALE)
                if self.brush.split("_")[0][1] == "b":
                    if BUILDING_TILES[self.brush.split("_")[1]] == 4:
                        tiles = [
                            [pos[0], pos[1]],
                            [pos[0] + 1, pos[1]],
                            [pos[0], pos[1] + 1],
                            [pos[0] + 1, pos[1] + 1]
                        ]
                    elif BUILDING_TILES[self.brush.split("_")[1]] == 9:
                        tiles = [
                            [pos[0], pos[1]],
                            [pos[0] + 1, pos[1]],
                            [pos[0] + 2, pos[1]],
                            [pos[0], pos[1] + 1],
                            [pos[0] + 1, pos[1] + 1],
                            [pos[0] + 2, pos[1] + 1],
                            [pos[0], pos[1] + 2],
                            [pos[0] + 1, pos[1] + 2],
                            [pos[0] + 2, pos[1] + 2],
                        ]

                    i = 0
                    for tile in tiles:
                        if pos_to_string(tile) in self.map.keys() and (self.map[pos_to_string(tile)].split("_")[0] == "tree" or self.map[pos_to_string(tile)].split("_")[0] == "water"):
                            color = (100, 0, 0)
                        else:
                            color = (0, 100, 0)
                        self.draw_screen.blit(set_color(self.textures["buildings"][self.brush.split("_")[1] + "_" + str(i)], color),(tile[0] * SCALE - self.scroll[0], tile[1] * SCALE - self.scroll[1]))
                        i += 1
                else:
                    if self.side == "player":
                        surf = self.textures["troops"][self.brush.split("_")[1]]
                    elif self.side == "enemy":
                        surf = self.textures["enemy_troops"][self.brush.split("_")[1]]

                    if (pos_to_string(pos) in self.map.keys() and (self.map[pos_to_string(pos)].split("_")[0] == "tree" or self.map[pos_to_string(pos)].split("_")[0] == "water")):
                        color = (100, 0, 0)
                    else:
                        color = (0, 100, 0)
                    self.draw_screen.blit(set_color(surf,color),(target[0] * SCALE, target[1] * SCALE))

            else:
                self.draw_screen.blit(self.textures["buttons"][self.brush],(target[0] * SCALE, target[1] * SCALE))

        def draw_buttons():
            for button in self.buttons:
                if button.visible and (button.category == self.actual_gui or button.category == "menu"):
                    self.draw_screen.blit(self.textures["buttons"][button.type],(button.hitbox.x, button.hitbox.y))
                    light = pygame.Surface((button.hitbox.w, button.hitbox.h), flags=pygame.SRCALPHA)
                    light.fill((0, 0, 0, 50 - button.light))
                    self.draw_screen.blit(light, (button.hitbox.x, button.hitbox.y))

        def draw_textbox():
            self.draw_screen.blit(self.freeze_draw_screen,(0,0))
            if int(self.timer/10) % 2 == 1:
                edit_bar = "_"
            else:
                edit_bar = ""
            surf = self.fonts["pixel_32"].render(self.map_name,False,(227,227,211))
            rect = surf.get_rect(center = (GAME_RESOLUTION[0]/2,GAME_RESOLUTION[1]/2))
            self.draw_screen.blit(surf,rect)
            surf = self.fonts["pixel_32"].render(edit_bar, False, (227, 227, 211))
            rect = surf.get_rect(topleft=rect.topright)
            self.draw_screen.blit(surf, rect)

        if self.typing_name:
            draw_textbox()
        else:
            self.draw_screen.fill((0, 0, 0))
            draw_map()
            self.draw_screen.blit(self.textures["gui"]["editor_background"], (0, 0))
            draw_buttons()
            if self.mouse.pos[0] < 240:
                draw_brush()

    def load_fonts(self):
        self.fonts = {}

        for file in os.listdir("fonts"):
            name = file[:-4]
            for size in FONTS[name]:
                font = pygame.font.Font("fonts/" + file, size)
                self.fonts[name + "_" + str(size)] = font

    def load_textures(self):
        def change_pallete(surf, building=False):
            new_surf = surf.copy()
            if building:
                COLOR1 = [(8, 18, 67), (2, 17, 80), (3, 17, 86), (3, 18, 83), (3, 18, 93), (1, 16, 90),
                          (15, 29, 97), (10, 27, 119), (2, 28, 133), (1, 28, 140), (5, 28, 141), (2, 28, 149),
                          (0, 30, 141), (1, 27, 148), (3, 28, 152), (1, 28, 142), (9, 32, 168), (11, 33, 176)]
                COLOR2 = [(67, 13, 8), (80, 6, 2), (86, 10, 3), (83, 8, 3), (93, 11, 3), (90, 8, 1),
                          (97, 21, 15), (119, 20, 10), (133, 9, 2), (140, 9, 1), (141, 16, 5), (149, 13, 2),
                          (141, 5, 0), (148, 12, 1), (152, 15, 3), (142, 9, 1), (168, 26, 9), (176, 30, 11)]
            else:
                COLOR1 = [(0, 8, 36), (0, 16, 65), (0, 28, 97), (0, 40, 130), (8, 40, 154), (24, 40, 182),
                          (48, 44, 207), (93, 73, 235)]
                COLOR2 = [(36, 3, 0), (65, 3, 0), (97, 1, 0), (130, 0, 1), (154, 20, 8), (182, 24, 27), (207, 62, 44),
                          (235, 106, 73)]
            for i in range(8):
                new_surf = change_color(new_surf, COLOR1[i], COLOR2[i])
            return new_surf

        def change_color(surf, color1, color2):
            new_surf = surf.copy()
            for x in range(new_surf.get_width()):
                for y in range(new_surf.get_height()):
                    if new_surf.get_at((x, y)) == color1:
                        new_surf.set_at((x, y), color2)
            return new_surf

        self.textures = {}

        for dir in os.listdir("textures"):
            if dir[-4:] == ".png":
                self.textures[dir.replace(".png", "")] = pygame.image.load("textures/" + dir).convert_alpha()
            else:
                if dir == "troops":
                    textures = {}
                    for file in os.listdir("textures/" + dir):
                            sheet = pygame.image.load("textures/" + dir + "/" + file).convert_alpha()
                            textures[file.replace(".png", "")] = sheet.subsurface((0, 0, TROOP_FRAME_SIZE[0], TROOP_FRAME_SIZE[1]))
                    self.textures["troops"] = textures
                    textures = {}
                    for file in os.listdir("textures/" + dir):
                            sheet = pygame.image.load("textures/" + dir + "/" + file).convert_alpha()
                            textures[file.replace(".png", "")] = change_pallete(sheet.subsurface((0, 0, TROOP_FRAME_SIZE[0], TROOP_FRAME_SIZE[1])))
                    self.textures["enemy_troops"] = textures
                else:
                    textures = {}
                    for file in os.listdir("textures/" + dir):
                        textures[file.replace(".png", "")] = pygame.image.load("textures/" + dir + "/" + file).convert_alpha()
                    self.textures[dir] = textures

Program()
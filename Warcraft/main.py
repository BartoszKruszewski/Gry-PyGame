import pygame, os, sys, math, random
from flow_map import FlowMap
from troop import Troop
from mouse import Mouse

from building import Building
from tree import Tree
from ground import Ground
from game_object import GameObject
from button import Button
from CONST import *
from FUNCTIONS import *

class Game():
    def __init__(self):
        # init
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_RESOLUTION)
        self.draw_screen = pygame.Surface(GAME_RESOLUTION)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.mouse = Mouse(False)
        self.load_assests()
        self.create_stuff()

        # objects
        self.tiles = {}
        self.buildings = []
        self.flow_maps = {1:FlowMap()}
        self.troops = []
        self.grouping_rect = pygame.Rect(0, 0, 0, 0)
        self.discovered_map = []
        self.visible_map = []
        self.selected_objects = []
        self.colliders = []
        self.obstacles = []
        self.focused_objects = []
        self.updates = []

        # variables
        self.flow_map_id = 1
        self.game_object_id = 1
        self.timer = 0
        self.walk_point = [0,0]
        self.walk_point_timer = 0

        self.grouping_rect_start_point = (0,0)
        self.grouping = False

        self.scroll = [0,0]
        self.true_scroll = [0,0]
        self.target_scroll = [0,0]

        self.actual_gui = ""

        self.build_brush = ""
        self.build_pos = [0,0]

        self.button_clicked = False
        self.click_cooldown = CLICK_COOLDOWN

        self.lumber = 10000
        self.gold = 10000
        self.population_limit = 5

        self.load_map("map1")

        while True:
            self.update()

    def load_assests(self):
        def load_textures():
            def change_pallete(surf,building=False):
                new_surf = surf.copy()
                if building:
                    COLOR1 = [(8, 18, 67),(2, 17, 80),(3, 17, 86),(3, 18, 83),(3, 18, 93),(1,16,90),
                              (15, 29, 97), (10, 27, 119), (2, 28, 133), (1, 28, 140), (5, 28, 141), (2, 28, 149),
                              (0, 30, 141), (1, 27, 148), (3, 28, 152), (1, 28, 142), (9, 32, 168), (11, 33, 176)]
                    COLOR2 = [(67, 13, 8),(80, 6, 2),(86, 10, 3),(83, 8, 3),(93, 11, 3),(90,8,1),
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

            def load_animation(name):
                sheet = pygame.image.load("textures/troops/" + name + ".png").convert_alpha()

                info = TROOPS_ANIMATIONS[name]

                animations = {}
                enemy_animations = {}
                animation_number = 0

                SIDES = ["up","right","down"]

                for animation_name in info:
                    for side in SIDES:
                        enemy_animation = []
                        animation = []
                        for frame_number in range(5):
                            frame = pygame.Surface(TROOP_FRAME_SIZE,flags=pygame.SRCALPHA)
                            frame.blit(sheet,((-5 * animation_number - frame_number) * TROOP_FRAME_SIZE[0],0))
                            animation.append(frame)
                            enemy_animation.append(change_pallete(frame))
                        animations[animation_name + "_" + side] = animation
                        enemy_animations[animation_name + "_" + side] = enemy_animation
                        if side == "right":
                            enemy_animation = []
                            animation = []
                            for frame_number in range(5):
                                frame = pygame.Surface(TROOP_FRAME_SIZE,flags=pygame.SRCALPHA)
                                frame.blit(sheet, ((-5 * animation_number - frame_number) * TROOP_FRAME_SIZE[0], 0))
                                frame = pygame.transform.flip(frame,True,False)
                                animation.append(frame)
                                enemy_animation.append(change_pallete(frame))
                            animations[animation_name + "_left"] = animation
                            enemy_animations[animation_name + "_left"] = enemy_animation
                        animation_number += 1
                self.troops_animations[name] = animations
                self.enemy_troops_animations[name] = enemy_animations

            for dir in os.listdir("textures"):
                if dir[-4:] == ".png":
                    self.textures[dir.replace(".png", "")] = pygame.image.load("textures/" + dir).convert_alpha()
                else:
                    if dir == "troops":
                        for file in os.listdir("textures/troops"):
                            load_animation(file[:-4])
                    else:
                        textures = {}
                        for file in os.listdir("textures/" + dir):
                            image = pygame.image.load("textures/" + dir + "/" + file).convert_alpha()
                            textures[file.replace(".png", "")] = image
                        self.textures[dir] = textures

        def load_fonts():
            for file in os.listdir("fonts"):
                name = file[:-4]
                for size in FONTS[name]:
                    font = pygame.font.Font("fonts/" + file,size)
                    self.fonts[name + "_" + str(size)] = font

        def load_sounds():
            for dir in os.listdir("sounds"):
                if dir[-4:] == ".wav":
                    self.sounds[dir.replace(".wav", "")] = pygame.mixer.Sound("sounds/" + dir)
                else:
                    sounds = {}
                    for file in os.listdir("sounds/" + dir):
                        sounds[file.replace(".wav", "")] = pygame.mixer.Sound("sounds/" + dir + "/" + file)
                    self.sounds[dir] = sounds

        def load_music():
            for file in os.listdir("music"):
                self.music[file.replace(".wav", "")] = pygame.mixer.Sound("music/" + file)

        self.textures = {}
        self.troops_animations = {}
        self.enemy_troops_animations = {}
        self.sounds = {}
        self.music = {}
        self.fonts = {}

        load_textures()
        load_sounds()
        load_music()
        load_fonts()

    def create_stuff(self):
        def create_buttons():
            self.buttons.append(Button("farm","peasant",[4,105],(27,19)))
            self.buttons.append(Button("barrack","peasant",[38,105],(27,19)))
            self.buttons.append(Button("lumbermill","peasant",[4,129],(27,19)))
            self.buttons.append(Button("blacksmith","peasant",[38,129],(27,19)))
            self.buttons.append(Button("stables","peasant",[4,153],(27,19)))
            self.buttons.append(Button("tower","peasant",[38,153],(27,19)))

            self.buttons.append(Button("swordsman", "barrack", [4, 105], (27, 19)))
            self.buttons.append(Button("archer", "barrack", [38, 105], (27, 19)))
            self.buttons.append(Button("catapult", "barrack", [4, 129], (27, 19)))
            self.buttons.append(Button("knight", "barrack", [38, 129], (27, 19)))

            self.buttons.append(Button("peasant", "townhall", [4, 105], (27, 19)))

            self.buttons.append(Button("swords1", "blacksmith", [4, 105], (27, 19)))
            self.buttons.append(Button("armor1", "blacksmith", [38, 105], (27, 19)))
            self.buttons.append(Button("swords2", "blacksmith", [4, 105], (27, 19)))
            self.buttons.append(Button("armor2", "blacksmith", [38, 105], (27, 19)))
            self.buttons.append(Button("swords3", "blacksmith", [4, 105], (27, 19)))
            self.buttons.append(Button("armor3", "blacksmith", [38, 105], (27, 19)))
            self.buttons.append(Button("fireballs", "blacksmith", [4, 129], (27, 19)))

            self.buttons.append(Button("bows1", "lumbermill", [4, 105], (27, 19)))
            self.buttons.append(Button("bows2", "lumbermill", [4, 105], (27, 19)))
            self.buttons.append(Button("bows3", "lumbermill", [4, 105], (27, 19)))

            self.buttons.append(Button("horses1", "stables", [4, 105], (27, 19)))
            self.buttons.append(Button("horses2", "stables", [4, 105], (27, 19)))


        self.buttons = []
        create_buttons()

    def load_map(self,name):
        file = open(name + ".txt","r")
        data = file.readlines()
        file.close()

        for line in data:
            info = line.split(":")
            info[2] = info[2].rstrip()
            x = int(info[0])
            y = int(info[1])
            type = info[2]
            if len(type.split("_")) > 1:
                if type.split("_")[0] == "goldmine":
                    side = "neutral"
                elif type.split("_")[1][0] == "p":
                    side = "player"
                elif type.split("_")[1][0] == "e":
                    side = "enemy"

                if type.split("_")[1][1] == "b":
                    gameobject = Building([x, y], self.game_object_id, type.split("_")[0],side)
                    gameobject.build_timer = 0
                    self.buildings.append(gameobject)
                elif type.split("_")[1][1] == "t":
                    gameobject = Troop([x, y], self.game_object_id, type.split("_")[0],side)
                    self.troops.append(gameobject)
            else:
                if type == "tree":
                    gameobject = Tree([x,y],self.game_object_id)
                else:
                    gameobject = Ground([x,y],self.game_object_id,type)
                self.tiles[pos_to_string([x,y])] = gameobject
            self.game_object_id += 1

        self.update_map()

    def get_mouse_tile_pos(self):
        return [int((self.mouse.pos[0] + self.scroll[0]) / SCALE) , int((self.mouse.pos[1] + self.scroll[1]) / SCALE)]

    def get_nearest(self,pos,object_type,type,side):
        target_tile = None
        if object_type == "ground" or object_type == "tree":
            r = 1
            close_points = []
            while len(close_points) == 0 and r < MAP_SIZE[0]:
                around = get_points_in_radius(pos,r)
                for point in around:
                    if pos_to_string(point) in self.tiles:
                        tile = self.tiles[pos_to_string(point)]
                        if tile.type.split("_")[0] == type:
                            close_points.append(point)
                r += 1
            target_tile = self.tiles[pos_to_string(get_nearest(close_points,pos))]


        elif object_type == "building":
            avalible = []
            for building in self.buildings:
                if building.type == type and (building.side == side or building.side == "neutral"):
                    avalible.append(building.pos)
            best_pos = get_nearest(avalible,pos)
            for building in self.buildings:
                if building.pos == best_pos:
                    target_tile = building
                    break

        return target_tile


    def is_only_selected(self,type):
        is_only = True
        for game_object in self.selected_objects:
            if game_object.type != type:
                is_only = False
                break
        return  is_only

    def overlap(self, rect1, rect2):
        scrolled_rect = rect1.copy()
        scrolled_rect.x += self.scroll[0]
        scrolled_rect.y += self.scroll[1]
        return scrolled_rect.colliderect(rect2)

    def update_map(self):
        for key in self.tiles.keys():
            tile = self.tiles[key]
            type = tile.type.split("_")[0]
            if type == "grass0":
                direction = 5
                if random.randint(0,15) == 0:
                    direction = random.randint(0,8)
                tile.type = type + "_" + str(direction)
            else:
                tile.type = type + "_" + str(self.get_direction(pos_to_int(key), type))

        self.update_vision()

        for key in self.tiles.keys():
            tile = self.tiles[key]
            if tile.type.split("_")[0] == "tree" or tile.type.split("_")[0] == "water":
                self.obstacles.append(tile.pos)
        for building in self.buildings:
            for tile in building.tiles:
                self.obstacles.append(tile)

    def update_tiles_around(self,tile):
        around = get_points_in_radius(tile.pos,1.5)
        for point in around:
            adress = pos_to_string(point)
            if adress in self.tiles.keys():
                tile = self.tiles[adress]
                type = tile.type.split("_")[0]
                if type != "grass0":
                    tile.type = type + "_" + str(self.get_direction(point, type))

    def update_vision(self):
        def update_troops_vision():
            if len(self.visible_map) == 0:
                for troop in self.troops:
                    if troop.side == "player":
                        points = get_points_in_radius(troop.pos, 4)
                        for point in points:
                            if not point in self.visible_map:
                                self.visible_map.append(point.copy())

                for point in self.visible_map:
                    if point not in self.discovered_map:
                        self.discovered_map.append(point)

        def update_buildings_vision():
            for building in self.buildings:
                if building.side == "player":
                    points = get_points_in_radius(building.pos, 4)
                    for point in points:
                        if not point in self.visible_map:
                            self.visible_map.append(point.copy())

            for point in self.visible_map:
                if point not in self.discovered_map:
                    self.discovered_map.append(point)

        update_troops_vision()
        update_buildings_vision()

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
            if key in self.tiles.keys():
                tile_type = self.tiles[key].type.split("_")[0]
                if tile_type == type or (tile_type == "grass2" and type == "grass1"):
                    is_around[i] = True
            elif adress[0] < 0 or adress[1] < 0 or adress[0] >= MAP_SIZE[0] or adress[1] >= MAP_SIZE[1]:
                is_around[i] = True
            i += 1

        if type == "path":
            direction = 1
        else:
            direction = 7

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
        def update_colliders():
            self.colliders.clear()
            self.colliders.extend(self.buildings)

        def update_click_cooldown():
            self.click_cooldown -= self.delta_time
            self.click_cooldown = max(self.click_cooldown,0)

        def update_build():
            if self.build_brush != "":
                if self.mouse.click[0] and self.click_cooldown == 0:
                    if self.gold >= PRICES[self.build_brush][0] and self.gold >= PRICES[self.build_brush][1]:
                        self.build_pos = self.get_mouse_tile_pos()
                        building = Building(self.build_pos, self.game_object_id, self.build_brush,"player")
                        can_build = True
                        for tile in building.tiles:
                            if tile in self.obstacles:
                                can_build = False
                                break
                        if can_build:
                            self.buildings.append(building)
                            self.game_object_id += 1
                            self.gold -= PRICES[self.build_brush][0]
                            self.lumber -= PRICES[self.build_brush][1]
                            self.build_brush = ""
                            focus_on_object(self.selected_objects[0],building)
                            if building.type == "farm":
                                self.population_limit += FARM_CAPACITY
                if self.mouse.click[1] and self.click_cooldown == 0:
                    self.build_brush = ""

        def check_vision():
            for troop in self.troops:
                if troop.state == "move" or troop.state == "use":
                    self.visible_map.clear()
                    self.update_vision()
                    break

        def update_gui():
            on = False
            for troop in self.troops:
                if troop.flow_map_id == self.flow_map_id:
                    self.actual_gui = troop.type
                    self.selected_troop = troop
                    on = True
                    break
            if not on:
                for building in self.buildings:
                    if building.selected:
                        self.actual_gui = building.type
                        self.selected_troop = building
                        on = True
                        break
                if not on:
                    self.actual_gui = ""

        def update_troops():
            for troop in self.troops:
                troop.update(self.delta_time,self.updates)
                if troop.dead_timer == 0:
                    if troop.flow_map_id != 0 and troop.flow_map_id in self.flow_maps.keys() and self.flow_maps[troop.flow_map_id].start and troop.state == "move":
                        direction = self.flow_maps[troop.flow_map_id].map[pos_to_string(troop.pos)]
                        if direction == "target":
                            troop.target_reached = True
                            troop.state = "idle"
                            troop.frame = 0
                        else:
                            troop.direction = direction
                            troop.state = "move"
                            near_colliders = []
                            for collider in self.colliders:
                                if collider.id != troop.id:
                                    if distance(collider.global_pos, troop.global_pos) < SCALE * 1.5:
                                        near_colliders.append(collider.hitbox)
                            troop.update_position(self.delta_time, near_colliders)

                    if troop.state == "idle" or troop.state == "move":
                        if troop.chopped_tree >= 10:
                            troop.animation = "wood"
                        elif troop.collected_gold >= 10:
                            troop.animation = "gold"
                        else:
                            troop.animation = "move"

                    elif troop.state == "attack":
                        if troop.type == "peasant":
                            troop.animation = "use"
                        else:
                            troop.animation = "attack"

                    elif troop.state == "chopping" or troop.state == "building":
                        troop.animation = "use"

                else:
                    if troop.dead_timer >= DEAD_VISIBLE_TIME:
                        self.troops.remove(troop)


        def update_troop_moving():
            self.walk_point_timer -= self.delta_time
            self.walk_point_timer = max(self.walk_point_timer,0)

            if self.mouse.click[1]:
                if len(self.selected_objects) > 0:
                    if self.tiles[pos_to_string(self.get_mouse_tile_pos())].type.split("_")[0] == "tree":
                        if self.is_only_selected("peasant") and len(self.selected_objects) == 1:
                            nearest_tree = self.tiles[pos_to_string(self.get_mouse_tile_pos())]
                            for troop in self.selected_objects:
                                focus_on_object(troop,nearest_tree)
                    else:
                        selected_building = None
                        for building in self.buildings:
                            if self.overlap(self.mouse.hitbox,building.clickbox):
                                selected_building = building
                                break

                        if selected_building != None:
                            for troop in self.selected_objects:
                                focus_on_object(troop,selected_building)
                        else:
                            focused_enemy = None
                            for troop in self.troops:
                                if troop.side == "enemy" and troop.dead_timer == 0:
                                    if self.overlap(self.mouse.hitbox,troop.clickbox):
                                        focused_enemy = troop
                                        break
                            if focused_enemy != None:
                                for troop in self.selected_objects:
                                    focus_on_object(troop,focused_enemy)
                            elif self.flow_map_id in self.flow_maps.keys():
                                self.flow_maps[self.flow_map_id].update(normalize_target(self.get_mouse_tile_pos(),self.obstacles,self.selected_objects[0].pos,2),self.obstacles)
                                self.flow_maps[self.flow_map_id].start = True
                                self.walk_point = self.get_mouse_tile_pos()
                                self.walk_point_timer = WALK_POINT_TIME
                                for troop in self.selected_objects:
                                    troop.state = "move"
                                    if [troop.focused_object, troop.flow_map_id] in self.focused_objects:
                                        self.focused_objects.remove([troop.focused_object, troop.flow_map_id])
                                    troop.focused_object = None

        def focus_on_object(troop,object):
            if object.object_type == "building":
                target = get_best_near_pos(object.tiles, self.obstacles, troop.pos, 2)
            else:
                target = normalize_target(object.pos, self.obstacles, troop.pos,1.5)

            troop.focused_object = object
            self.flow_maps[troop.flow_map_id].update(target, self.obstacles)
            self.flow_maps[troop.flow_map_id].start = True
            troop.state = "move"
            object.focusing_by.append(troop.id)
            self.focused_objects.append(object)

        def update_focused_objects():

            deleted_trees = []
            updated_troops = []

            for object in self.focused_objects:
                if object.object_type == "building":
                    near_troops = get_around_objects(self.troops, object.tiles, 2.5)
                else:
                    near_troops = get_around_objects(self.troops, [object.pos], 1.5)

                if object in near_troops:
                    near_troops.remove(object)

                troop = None
                for id in object.focusing_by:
                    for near_troop in near_troops:
                        if near_troop.id == id and not troop in updated_troops:
                            troop = near_troop
                            updated_troops.append(troop)
                            break

                    if troop != None:
                        troop.direction = get_direction(troop.global_pos, object.global_pos)

                        if object.object_type == "tree":
                            troop.state = "chopping"
                            if troop.frame == 0 and troop.timer == 0:
                                object.actual_health -= 1
                                troop.chopped_tree += 1
                                if object.actual_health <= 0:
                                    if object.pos in self.obstacles:
                                        self.obstacles.remove(object.pos)
                                        self.game_object_id += 1
                                        self.tiles[pos_to_string(object.pos)] = Ground(object.pos, self.game_object_id, "grass0_5")
                                        deleted_trees.append(object)
                                        target = self.get_nearest(troop.pos, "building", "townhall", troop.side)
                                        focus_on_object(troop,target)
                        elif object.object_type == "building":
                            if troop.side == object.side or object.side == "neutral":
                                if troop.type == "peasant":
                                    if object.build_timer > 0:
                                        object.build_timer -= self.delta_time
                                        troop.state = "building"
                                        object.build_timer = max(object.build_timer, 0)
                                    else:
                                        if not object.build:
                                            troop.state = "idle"
                                            self.obstacles.extend(object.tiles)
                                        object.build = True
                                        if troop.collected_gold > 0:
                                            if object.type == "townhall":
                                                self.gold += troop.collected_gold
                                                troop.collected_gold = 0
                                                focus_on_object(troop,self.get_nearest(troop.pos, "building", "goldmine",troop.side))
                                        elif troop.chopped_tree > 0:
                                            if object.type == "lumbermill" or object.type == "townhall":
                                                self.lumber += troop.chopped_tree
                                                troop.chopped_tree = 0
                                                target = self.get_nearest(troop.pos, "tree", "tree",troop.side)
                                                focus_on_object(troop, target)
                                        elif object.type == "goldmine":
                                            troop.collecting_gold_timer -= self.delta_time
                                            if troop.collecting_gold_timer <= 0:
                                                troop.collecting_gold_timer = COLLECTING_GOLD_TIME
                                                troop.collected_gold += 10
                                                troop.visible = True
                                                focus_on_object(troop,self.get_nearest(troop.pos, "building", "townhall", troop.side))
                                            else:
                                                troop.visible = False
                                        elif object.actual_health < object.health:
                                            troop.state = "building"
                                            object.actual_health += self.delta_time * REPAIRING_SPEED
                                            if object.actual_health >= object.health:
                                                object.actual_health = object.health
                                                troop.focused_object = None
                                                object.focusing_by.remove(troop.id)
                                                troop.state = "idle"
                                else:
                                    troop.focused_object = None
                                    object.focusing_by.remove(troop.id)
                            else:
                                troop.state = "attack"
                                if troop.frame == 2 and troop.timer == 0:
                                    object.actual_health -= troop.stats["damage"]
                                if object.actual_health <= 0:
                                    troop.state = "idle"
                                    troop.frame = 0

                        elif object.object_type == "troop":
                            troop.state = "attack"
                            if troop.frame == 2 and troop.timer == 0:
                                object.actual_health -= troop.stats["damage"]
                            if object.actual_health <= 0:
                                troop.state = "idle"
                                troop.frame = 0

            objects = []
            for object in self.focused_objects:
                for troop in self.troops:
                    if object.actual_health > 0 and troop.id in object.focusing_by and troop.focused_object != None and troop.focused_object.id == object.id:
                        already_is = False
                        for o in objects:
                            if o.id == object.id:
                                already_is = True
                                break
                        if not already_is:
                            objects.append(object)
                        break

            self.focused_objects = objects.copy()

            for tree in deleted_trees:
                self.update_tiles_around(tree)

        def update_troop_grouping():
            overlaped = None
            if self.mouse.click[0]:
                if not self.button_clicked:
                    for troop in self.troops:
                        if troop.dead_timer == 0:
                            if troop.side == "player":
                                troop.selected = False
                                if self.overlap(self.mouse.hitbox,troop.clickbox):
                                    overlaped = troop
                    for building in self.buildings:
                        if building.destroyed == 0:
                            if building.side == "player":
                                building.selected = False
                                if self.overlap(self.mouse.hitbox,building.clickbox):
                                    overlaped = building

                    if overlaped != None:
                        self.flow_map_id += 1
                        if overlaped.object_type == "troop":
                            overlaped.flow_map_id = self.flow_map_id
                            self.flow_maps[self.flow_map_id] = FlowMap()
                        overlaped.selected = True
                        self.selected_objects.clear()
                        self.selected_objects.append(overlaped)

            if self.mouse.click[0] and self.mouse.pos[0] > 70 and self.build_brush == "" and overlaped == None and not self.grouping:
                self.grouping_rect_start_point = (self.mouse.pos[0] + self.scroll[0],self.mouse.pos[1] + self.scroll[1])
                self.grouping = True
                self.gui_changed = False

            if self.grouping and self.mouse.hold[0]:
                mouse_scrolled_pos = [self.mouse.pos[0] + self.scroll[0],self.mouse.pos[1] + self.scroll[1]]

                self.grouping_rect.width = abs(self.grouping_rect_start_point[0] - mouse_scrolled_pos[0])
                self.grouping_rect.height = abs(self.grouping_rect_start_point[1] - mouse_scrolled_pos[1])
                if self.grouping_rect_start_point[0] >= mouse_scrolled_pos[0] and self.grouping_rect_start_point[1] >= mouse_scrolled_pos[1]:
                    self.grouping_rect.bottomright = self.grouping_rect_start_point
                elif self.grouping_rect_start_point[0] > mouse_scrolled_pos[0] and self.grouping_rect_start_point[1] < mouse_scrolled_pos[1]:
                    self.grouping_rect.topright = self.grouping_rect_start_point
                elif self.grouping_rect_start_point[0] < mouse_scrolled_pos[0] and self.grouping_rect_start_point[1] > mouse_scrolled_pos[1]:
                    self.grouping_rect.bottomleft = self.grouping_rect_start_point
                elif self.grouping_rect_start_point[0] < mouse_scrolled_pos[0] and self.grouping_rect_start_point[1] < mouse_scrolled_pos[1]:
                    self.grouping_rect.topleft = self.grouping_rect_start_point

            if self.grouping and not self.mouse.hold[0]:
                self.flow_map_id += 1
                ids = []
                self.selected_objects.clear()
                for troop in self.troops:
                    if troop.side == "player":
                        if troop.side == "player":
                            if self.grouping_rect.colliderect(troop.clickbox):
                                troop.flow_map_id = self.flow_map_id
                                troop.selected = True
                                self.selected_objects.append(troop)
                            ids.append(troop.flow_map_id)

                keys = list(self.flow_maps.keys()).copy()
                for key in keys:
                    if key not in ids:
                        self.flow_maps.pop(key)

                self.flow_maps[self.flow_map_id] = FlowMap()
                self.grouping = False

        def update_buildings():
            for building in self.buildings:
                building.update(self.delta_time)
                if building.destroyed >= 17:
                    for tile in building.tiles:
                        self.obstacles.remove(tile)
                    self.buildings.remove(building)
                    if building.type == "farm":
                        self.population_limit -= FARM_CAPACITY

        def update_minimap_scroll():
            if self.mouse.hold[0]:
                if self.mouse.pos[0] < 69 and self.mouse.pos[1] < 72:
                    in_minimap_pos = [(self.mouse.pos[0] - 2) * SCALE/2,(self.mouse.pos[1] - 4) * SCALE/2]
                    self.target_scroll[0] = int(round(in_minimap_pos[0] - GAME_RESOLUTION[0] + 9))
                    self.target_scroll[1] = int(round(in_minimap_pos[1] - GAME_RESOLUTION[1] + 9))

        def update_scroll():
            if not self.mouse.hold[0]:
                if self.mouse.pos[0] > GAME_RESOLUTION[0] - 20:
                    self.target_scroll[0] += self.delta_time * SCROLL_SPEED
                elif self.mouse.pos[0] < 90 and self.mouse.pos[0] > 70:
                    self.target_scroll[0] -= self.delta_time * SCROLL_SPEED
                if self.mouse.pos[1] > GAME_RESOLUTION[1] - 20:
                    self.target_scroll[1] += self.delta_time * SCROLL_SPEED
                elif self.mouse.pos[1] < 20:
                    self.target_scroll[1] -= self.delta_time * SCROLL_SPEED

            self.target_scroll[0] = max(self.target_scroll[0], -70)
            self.target_scroll[0] = min(self.target_scroll[0],MAP_SIZE[0] * SCALE - GAME_RESOLUTION[0] + 9)
            self.target_scroll[1] = max(self.target_scroll[1], -9)
            self.target_scroll[1] = min(self.target_scroll[1], MAP_SIZE[1] * SCALE - GAME_RESOLUTION[1] + 9)

            self.true_scroll[0] += (self.target_scroll[0] - self.true_scroll[0]) / 1 / self.delta_time
            self.true_scroll[1] += (self.target_scroll[1] - self.true_scroll[1]) / 1 / self.delta_time

            self.scroll[0] = int(round(self.true_scroll[0]))
            self.scroll[1] = int(round(self.true_scroll[1]))

        self.pre_progam_update()
        update_scroll()
        update_minimap_scroll()
        update_colliders()
        update_troop_grouping()
        update_troop_moving()
        update_troops()
        update_buildings()
        update_build()
        update_focused_objects()
        update_gui()
        update_click_cooldown()
        check_vision()
        self.draw()
        self.late_program_update()

    def draw(self):
        def draw_flow_map():
            for tile_adress in self.flow_maps[self.flow_map_id].map.keys():
                split = tile_adress.split(":")
                path_adress = (int(split[0]), int(split[1]))
                self.draw_screen.blit(self.textures["arrows"][self.flow_maps[self.flow_map_id].map[tile_adress]],(path_adress[0] * SCALE + 4 - self.scroll[0], path_adress[1] * SCALE + 4 - self.scroll[1]))

        def draw_fog():
            shadow = pygame.Surface((16, 16), flags=pygame.SRCALPHA)
            shadow.fill((0, 0, 0, 100))
            for x in range(MAP_SIZE[0]):
                for y in range(MAP_SIZE[1]):
                    if [x,y] not in self.visible_map:
                        self.draw_screen.blit(shadow,(x * SCALE - self.scroll[0],y * SCALE - self.scroll[1]))

        def draw_game_objects():
            def draw_tile(tile):
                self.draw_screen.blit(self.textures["tiles"][tile.type],
                                      (tile.global_pos[0] - self.scroll[0], tile.global_pos[1] - self.scroll[1]))

            def draw_troop(troop):
                if troop.visible:
                    if troop.dead_timer > 0:
                        self.draw_screen.blit(
                            self.textures["dead"],(troop.global_pos[0] - self.scroll[0], troop.global_pos[1] - self.scroll[1]))
                    else:
                        if troop.side == "player":
                            self.draw_screen.blit(
                                self.troops_animations[troop.type][troop.animation + "_" + troop.direction][troop.frame],
                                (troop.global_pos[0] - self.scroll[0], troop.global_pos[1] - self.scroll[1]))
                        elif troop.side == "enemy":
                            self.draw_screen.blit(
                                self.enemy_troops_animations[troop.type][troop.animation + "_" + troop.direction][
                                    troop.frame],
                                (troop.global_pos[0] - self.scroll[0], troop.global_pos[1] - self.scroll[1]))
                        rect = troop.hitbox.copy()
                        rect.x -= self.scroll[0]
                        rect.y -= self.scroll[1]
                        #pygame.draw.rect(self.draw_screen, (255, 0, 0), rect)
                        rect = troop.clickbox.copy()
                        rect.x -= self.scroll[0]
                        rect.y -= self.scroll[1]
                        #pygame.draw.rect(self.draw_screen, (255, 0, 255), rect)
                        if troop.selected:
                            pygame.draw.rect(self.draw_screen, (227, 227, 211, 0), rect, 1)
                        #pygame.draw.rect(self.draw_screen, (255, 0, 0), pygame.Rect(troop.pos[0] * SCALE - self.scroll[0],troop.pos[1] * SCALE - self.scroll[1], 2,2))
                    if ((troop.focused_object != None and troop.focused_object.object_type == "troop" ) or troop.danger_timer > 0) and troop.dead_timer == 0:
                        state = troop.actual_health/troop.stats["health"]
                        color = (0, 197, 0)
                        if state < 0.7:
                            color = (197, 144, 0)
                        if state < 0.4:
                            color = (197, 3, 0)
                        self.draw_screen.blit(liveBar(state,(16,4),color),(troop.global_pos[0] - self.scroll[0] + 8, troop.global_pos[1] - self.scroll[1] +3))

            def draw_building(building):

                if building.destroyed > 0:
                    self.draw_screen.blit(self.textures["destroy"]["destroy_" + str(building.destroyed)],
                                          (building.global_pos[0] - self.scroll[0], building.global_pos[1] - self.scroll[1]))
                else:
                    i = 0
                    for tile in building.tiles:
                        if building.build_timer == 0:
                            self.draw_screen.blit(self.textures["buildings"][building.type + "_" + str(i)],
                                                  (tile[0] * SCALE - self.scroll[0], tile[1] * SCALE - self.scroll[1]))
                        else:
                            self.draw_screen.blit(
                                self.textures["in_build"]["build" + str(len(building.tiles)) + "_" + str(i)],
                                (tile[0] * SCALE - self.scroll[0], tile[1] * SCALE - self.scroll[1]))
                        if building.actual_health / building.health <= 0.5:
                            self.draw_screen.blit(self.textures["fire"]["fire_" + str(int((self.timer / 5) % 4))],
                                                  (tile[0] * SCALE - self.scroll[0], tile[1] * SCALE - self.scroll[1]))
                        i += 1
                rect = building.hitbox.copy()
                rect.x -= self.scroll[0]
                rect.y -= self.scroll[1]
                #pygame.draw.rect(self.draw_screen, (255, 0, 0), rect)
                rect = building.clickbox.copy()
                rect.x -= self.scroll[0]
                rect.y -= self.scroll[1]
                #pygame.draw.rect(self.draw_screen, (0, 0, 255), rect)
                if building.selected:
                    pygame.draw.rect(self.draw_screen, (227, 227, 211, 150), rect, 1)

            game_objects = []
            game_objects.extend(self.troops)
            game_objects.extend(self.tiles.values())
            game_objects.extend(self.buildings)

            def order(e):
                if e.object_type == "ground":
                    return 0
                else:
                    return e.hitbox.bottom
            game_objects.sort(key=order)

            for game_object in game_objects:
                if game_object.pos in self.discovered_map:
                    if game_object.object_type == "troop":
                        draw_troop(game_object)
                    elif game_object.object_type == "ground" or game_object.object_type == "tree":
                        draw_tile(game_object)
                    elif game_object.object_type == "building":
                        draw_building(game_object)

        def draw_grouping_rectangle():
            rect = pygame.Rect(self.grouping_rect.x - self.scroll[0],self.grouping_rect.y - self.scroll[1],self.grouping_rect.w,self.grouping_rect.h)
            pygame.draw.rect(self.draw_screen,(255,255,255),rect,1)

        def draw_build_brush():
            def set_color(surf,color):
                new_surf = surf.copy()
                for y in range(surf.get_height()):
                    for x in range(surf.get_width()):
                        pre_color = surf.get_at((x,y))
                        if pre_color[3] > 0:
                            new_color = (min(pre_color[0] + color[0],255),min(pre_color[1] + color[1],255),min(pre_color[2] + color[2],255))
                            new_surf.set_at((x,y),new_color)
                return new_surf

            i = 0
            target = [0, 0]
            target[0] = int(round((self.mouse.pos[0] + self.scroll[0]) / SCALE))
            target[1] = int(round((self.mouse.pos[1] + self.scroll[1]) / SCALE))
            building = Building(target, 0, self.build_brush,"player")
            for tile in building.tiles:
                if tile in self.obstacles:
                    color = (100,0,0)
                else:
                    color = (0,100,0)
                self.draw_screen.blit(set_color(self.textures["buildings"][building.type + "_" + str(i)],color),(tile[0] * SCALE - self.scroll[0], tile[1] * SCALE - self.scroll[1]))
                i += 1

        def draw_cursor():
            if len(self.selected_objects) > 0 and self.selected_objects[0].object_type == "troop":
                collide = False
                for troop in self.troops:
                    if troop.side == "enemy" and self.overlap(self.mouse.hitbox,troop.clickbox):
                        collide = True
                        break
                if collide:
                    type = "attack_" + str(int(self.timer/10 % 2))
                else:
                    type = "walk_" + str(int(self.timer /10 % 2))
            else:
                if self.mouse.hold[0]:
                    type = "click"
                else:
                    type = "main"
            self.draw_screen.blit(self.textures["cursor"][type],(self.mouse.pos[0],self.mouse.pos[1]))

        def draw_walk_point():
            if self.walk_point_timer > 0:
                self.draw_screen.blit(self.textures["walk_point"]["walk_point_" + str(7 - int(self.walk_point_timer/4))],(self.walk_point[0] * SCALE - self.scroll[0],self.walk_point[1] * SCALE - self.scroll[1]))

        def draw_gui():
            def draw_resources():
                shadow = self.fonts["pixel_8"].render("Lumber: " + str(self.lumber), False, (0, 0, 0))
                self.draw_screen.blit(shadow, (149, 2))
                surf = self.fonts["pixel_8"].render("Lumber: " + str(self.lumber), False, (227, 227, 211))
                self.draw_screen.blit(surf, (148,1))

                shadow = self.fonts["pixel_8"].render("Gold: " + str(self.gold), False, (0, 0, 0))
                self.draw_screen.blit(shadow, (249, 2))
                surf = self.fonts["pixel_8"].render("Gold: " + str(self.gold), False, (227, 227, 211))
                self.draw_screen.blit(surf, (248, 1))

                population = 0
                for troop in self.troops:
                    if troop.side == "player":
                        population += 1

                shadow = self.fonts["pixel_8"].render("Food: " + str(population) + "/" + str(self.population_limit), False, (0, 0, 0))
                self.draw_screen.blit(shadow, (84, 2))
                surf = self.fonts["pixel_8"].render("Food: " + str(population) + ":" + str(self.population_limit), False, (227, 227, 211))
                self.draw_screen.blit(surf, (83, 1))

            def draw_minimap():
                minimap = pygame.Surface((32,32))
                ally = []
                enemy = []
                neutral = []
                for troop in self.troops:
                    if troop.dead_timer == 0:
                        if troop.side == "player":
                            ally.append(pos_to_string(troop.pos))
                        elif troop.side == "enemy":
                            enemy.append(pos_to_string(troop.pos))
                        elif troop.side == "neutral":
                            neutral.append(pos_to_string(troop.pos))
                for building in self.buildings:
                    if building.destroyed == 0:
                        for tile in building.tiles:
                            if building.side == "player":
                                ally.append(pos_to_string(tile))
                            elif building.side == "enemy":
                                enemy.append(pos_to_string(tile))
                            elif building.side == "neutral":
                                neutral.append(pos_to_string(tile))


                for y in range(MAP_SIZE[0]):
                    for x in range(MAP_SIZE[1]):
                        adress = pos_to_string([x,y])
                        if [x,y] not in self.discovered_map:
                            color = (0, 0, 0)
                        elif adress in ally:
                            color = (0,255,0)
                        elif adress in enemy:
                            color = (255,0,0)
                        elif adress in neutral:
                            color = (255,255,0)
                        elif adress in self.tiles.keys():
                            color = MINIMAP_COLORS[self.tiles[adress].type.split("_")[0]]
                        minimap.set_at((x,y),color)
                self.draw_screen.blit(pygame.transform.scale(minimap,(64,64)), (3, 5))

                rect = pygame.Rect(self.scroll[0]/SCALE*2+12,self.scroll[1]/SCALE*2+7,30,20)
                pygame.draw.rect(self.draw_screen,(227, 227, 211),rect,1)

            def draw_buttons():
                for button in self.buttons:
                    if button.visible and not button.blocked:
                        if button.category == self.actual_gui:
                            if button.hold:
                                self.draw_screen.blit(self.textures["gui"]["button_frame_click"], (button.hitbox.x - 1, button.hitbox.y - 2))
                            else:
                                self.draw_screen.blit(self.textures["gui"]["button_frame"], (button.hitbox.x - 1, button.hitbox.y - 2))
                            self.draw_screen.blit(self.textures["buttons"][button.type], (button.hitbox.x, button.hitbox.y))
                            light = pygame.Surface((button.hitbox.w, button.hitbox.h), flags=pygame.SRCALPHA)
                            if self.gold >= PRICES[button.type][0] and self.lumber >= PRICES[button.type][1]:
                                light.fill((0, 0, 0, 50 - button.light))
                            else:
                                light.fill((255, 0, 0, 100))
                            self.draw_screen.blit(light, (button.hitbox.x, button.hitbox.y))

            def draw_info():
                def draw_name():
                    shadow = self.fonts["pixel_8"].render(self.selected_objects[0].type, False, (0, 0, 0))
                    rect = shadow.get_rect(center=(52, 82))
                    self.draw_screen.blit(shadow, rect)

                    surf = self.fonts["pixel_8"].render(self.selected_objects[0].type,False,(227,227,211))
                    rect = surf.get_rect(center = (51,81))
                    self.draw_screen.blit(surf,rect)

                def draw_health_bar():
                    self.draw_screen.blit(self.textures["gui"]["health_bar"], (36, 86))
                    if self.selected_objects[0].object_type == "troop":
                        state = self.selected_objects[0].actual_health / self.selected_objects[0].stats["health"]
                    elif self.selected_objects[0].object_type == "building":
                        state = self.selected_objects[0].actual_health / self.selected_objects[0].health
                    rect = pygame.Rect(37,87,int(27 * state),3)
                    color = (0,197,0)
                    if state < 0.7:
                        color = (197,144,0)
                    if state < 0.4:
                        color = (197, 3, 0)
                    pygame.draw.rect(self.draw_screen,color,rect)

                def draw_stats():
                    if len(self.selected_objects) == 1:
                        if self.selected_objects[0].object_type == "troop" and self.selected_objects[0].type != "peasant":
                            troop = self.selected_objects[0]
                            i = 0
                            for stat in TROOPS_STATS[troop.type].keys():
                                color = (227, 227, 211)
                                for update in self.updates:
                                    if UPGRADES[update][0] == stat and troop.type in UPGRADES[update][1]:
                                        color = (0,197,0)
                                        break

                                shadow = self.fonts["pixel_8"].render(stat + ": " + str(troop.stats[stat]), False, (0, 0, 0))
                                rect = shadow.get_rect(topleft=(5, 106 + i * 8))
                                self.draw_screen.blit(shadow, rect)

                                surf = self.fonts["pixel_8"].render(stat + ": ", False, (227, 227, 211))
                                rect = surf.get_rect(topleft=(4, 105 + i * 8))
                                self.draw_screen.blit(surf, rect)

                                surf = self.fonts["pixel_8"].render(str(troop.stats[stat]), False, color)
                                rect = surf.get_rect(topleft = rect.topright)
                                self.draw_screen.blit(surf, rect)

                                i += 1

                            self.draw_screen.blit(self.textures["gui"]["stats_frame"], (2, 103))

                self.draw_screen.blit(self.textures["gui"]["info"], (2, 71))

                self.draw_screen.blit(self.textures["gui"]["button_frame"], (5, 74))
                self.draw_screen.blit(self.textures["buttons"][self.selected_objects[0].type], (6, 76))
                draw_health_bar()
                draw_stats()
                draw_name()

            def draw_selected_troops():
                POS = [[4, 74],[38, 74],[4, 98],[38, 98],[4, 122],[38, 122],[4, 146],[38, 146]]
                i = 0
                for troop in self.selected_objects:
                    self.draw_screen.blit(self.textures["gui"]["button_frame"], (POS[i][0] -1, POS[i][1] -2))
                    self.draw_screen.blit(self.textures["buttons"][troop.type], (POS[i][0], POS[i][1]))
                    i += 1


            self.draw_screen.blit(self.textures["gui"]["gui"], (0, 0))
            if len(self.selected_objects) > 0:
                if len(self.selected_objects) > 1:
                    draw_selected_troops()
                else:
                    draw_info()
                    draw_buttons()
            draw_minimap()
            draw_resources()

        self.draw_screen.fill((0, 0, 0))
        draw_game_objects()
        draw_fog()
        if self.grouping:
            draw_grouping_rectangle()
        if self.build_brush != "":
            draw_build_brush()
        draw_gui()
        draw_walk_point()
        draw_cursor()

    def late_program_update(self):
        def check_events():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

        check_events()
        self.screen.blit(pygame.transform.scale(self.draw_screen,SCREEN_RESOLUTION),(0,0))
        self.delta_time = self.clock.tick(60) * 60 / 1000
        self.timer += self.delta_time
        pygame.display.update()

    def pre_progam_update(self):
        def update_buttons():
            self.button_clicked = False
            for button in self.buttons:
                if button.type in BUTTONS_VISIBLE.keys() and BUTTONS_VISIBLE[button.type] in self.updates:
                    button.visible = True
                buildings_types = []
                for building in self.buildings:
                    if building.side == "player":
                        buildings_types.append(building.type)
                if button.type in BUTTONS_BLOCKED.keys() and BUTTONS_BLOCKED[button.type] in buildings_types:
                    button.blocked = False
                if button.visible:
                    button.update(self.mouse,self.delta_time)
                    if button.click and not button.blocked:
                        self.button_clicked = True
                        if self.click_cooldown == 0 and self.actual_gui == button.category:
                            self.click_cooldown = CLICK_COOLDOWN
                            if self.gold >= PRICES[button.type][0] and self.lumber >= PRICES[button.type][1]:
                                if button.category == "peasant":
                                    self.build_brush = button.type
                                elif button.category == "barrack" or button.category == "townhall":
                                    population = 0
                                    for troop in self.troops:
                                        if troop.side == "player":
                                            population += 1

                                    if population < self.population_limit:
                                        colliders = []
                                        colliders.extend(self.obstacles)
                                        for troop in self.troops:
                                            colliders.append(troop.pos)

                                        free_pos = get_free_near_pos(self.selected_objects[0].tiles,colliders,2.5)
                                        if len(free_pos) > 0:
                                            self.gold -= PRICES[button.type][0]
                                            self.lumber -= PRICES[button.type][1]
                                            self.game_object_id += 1
                                            new_troop = Troop(free_pos[0],self.game_object_id,button.type,"player")
                                            self.troops.append(new_troop)
                                elif button.category == "lumbermill" or button.category == "blacksmith" or button.category == "stables":
                                    self.updates.append(button.type)
                                    self.buttons.remove(button)
        self.mouse.update()
        update_buttons()
Game()

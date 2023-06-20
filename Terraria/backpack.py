import pygame
from tile import Droped_Item
from tool import Tool
from STATS import *

class Backpack():
    def __init__(self):
        self.x = 92
        self.target_y = -74
        self.y = -74
        self.real_y = -74
        self.img = pygame.image.load("img/gui/gui.png")
        self.round_img = pygame.image.load("img/gui/round.png")
        self.heart_img = pygame.image.load("img/gui/heart.png")
        self.armor_heart_img = pygame.image.load("img/gui/heart_armor.png")
        self.hunger_img = pygame.image.load("img/gui/hunger.png")
        self.craft_img = pygame.image.load("img/gui/gui_crafting.png")
        self.light_img = pygame.image.load("img/gui/light.png")
        self.sound1 = pygame.mixer.Sound("sounds/gui/click1.wav")
        self.light_visible = False
        self.light_pos = (0,0)
        self.round_x = 95
        self.full_open = False

        # items
        self.items = []
        self.tools = []
        self.rounded_item_number = 1
        self.crafting1 = None
        self.crafting2 = None
        self.crafted = None
        self.one_item_craft = False

    def check_crafting(self,mouse,skills):
        c_e = False
        crafting1_exist = False
        crafting2_exist = False
        for item in self.items:
            if item[0].x_in_backpack == 9:
                self.crafting1 = item
                crafting1_exist = True
            elif item[0].x_in_backpack == 10:
                self.crafting2 = item
                crafting2_exist = True
            elif item[0].crafted:
                c_e = True
                self.crafted = item

        if not crafting1_exist:
            self.crafting1 = None
        if not crafting2_exist:
            self.crafting2 = None

        if (not c_e) and self.crafted != None:
            if self.crafting1 != None:
                if self.crafting1[1] > 1:
                    self.items[self.items.index(self.crafting1)] = (self.crafting1[0],self.crafting1[1] - 1)
                else:
                    self.items.remove(self.crafting1)

            if self.crafting2 != None:
                if self.crafting2[1] > 1:
                    self.items[self.items.index(self.crafting2)] = (self.crafting2[0], self.crafting2[1] - 1)
                else:
                    self.items.remove(self.crafting2)

            self.crafting1 = None
            self.crafting2 = None
            self.crafted = None

        if (self.crafting1 != None or self.crafting2 != None) and self.crafted == None:
            self.check_recipe(mouse,skills)

        if self.one_item_craft and self.crafting1 != None and self.crafting2 != None:
            self.check_recipe(mouse,skills)

        if self.crafting1 == None and self.crafting2 == None:
            if self.crafted in self.items:
                self.items.remove(self.crafted)


    def check_recipe(self,mouse,skills):
        one_item_craft = False
        try:
            item1 = self.crafting1[0].type
            item2 = self.crafting2[0].type
        except:
            one_item_craft = True
            try:
                item1 = self.crafting1[0].type
                item2 = ""

            except:
                item1 = ""
                item2 = self.crafting2[0].type

        for recipe in RECIPES:
            if (item1 == recipe[0] and item2 == recipe[1]) or (item1 == recipe[1] and item2 == recipe[0]):
                can_make = True
                if len(recipe) > 4:
                    if not skills[recipe[4]]:
                        can_make = False
                if can_make:
                    if self.one_item_craft:
                        for item in self.items:
                            if item[0].crafted:
                                self.items.remove(item)
                    self.add_item(recipe[2], True, recipe[3], -3)
                    if recipe[2] in TOOLS.keys():
                        self.tools.append(Tool(recipe[2]))
                    if one_item_craft:
                        self.one_item_craft = True
                    else:
                        self.one_item_craft = False
                    break

    def add_item(self,type, new_place=False, number=1 ,pos=-1):
        if number > 64:
            self.add_item(type,True,number - 64)
            number -= 64
        current_item = Item(24, type)

        if not new_place:
            new_place = True
            if not (type == "sword" or type == "pickaxe"):
                for item in self.items:
                    if current_item.type == item[0].type and item[1] < 64:
                        new_place = False
        if new_place:
            if pos == -1:
                collide = True
                while collide:
                    collide = False
                    for item in self.items:
                        if current_item.pos == item[0].pos:
                            collide = True
                            break
                    if collide:
                        if current_item.pos == 31:
                            current_item.pos = 0
                        else:
                            current_item.pos += 1

                if current_item.pos <= 32:
                    place = (current_item, number)
                    self.items.append(place)
            else:
                collide = False
                i = -1
                for item in self.items:
                    i += 1
                    if item[0].pos == pos:
                        if item[0].type == type and item[1] < 64:
                            self.items[i] = (item[0],item[1] + 1)
                        collide = True
                        break
                if not collide:
                    if pos == -3:
                        current_item = Item(pos,type,True)
                    else:
                        current_item = Item(pos, type)
                    place = (current_item, number)
                    self.items.append(place)
        elif not (type == "sword" or type == "pickaxe"):
            i = -1
            for item in self.items:
                i += 1
                if current_item.type == item[0].type and item[1] < 64:
                    place = (item[0],item[1] + number)
                    self.items[i] = place
                    break


    def update(self,mouse,gamemap,player,dt):
        self.round_x = 95 + (self.rounded_item_number - 1) * 17
        if self.full_open:
            self.target_y = 3
        else:
            self.target_y = -74
        self.real_y += (self.target_y - self.real_y) / 30 * dt
        self.y = round(self.real_y)
        self.light_visible = False
        for item in self.items:
            item[0].update(self.target_y,mouse,self,gamemap,player,dt)
            if self.full_open:
                if item[0].new_pos != None:
                    self.light_visible = True
                    x = item[0].new_pos % 8
                    y = int(item[0].new_pos/8)
                    pos_x = 96 + x * 17
                    pos_y = (y * 17) + 7
                    if item[0].new_pos >= 24:
                        pos_y = 83
                    if item[0].x > 240 and item[0].y < 24:
                        if item[0].new_pos == 9:
                            if (249, 7) != self.light_pos:
                                self.sound1.play()
                            self.light_pos = (249, 7)
                        else:
                            if (266, 7) != self.light_pos:
                                self.sound1.play()
                            self.light_pos = (266, 7)
                    elif item[0].x < 90 or (item[0].x > 217 and item[0].x < 255) or item[0].y > 110 or (item[0].x > 220 and item[0].y > 30):
                        self.light_visible = False
                    else:
                        if (pos_x,pos_y) != self.light_pos:
                            self.sound1.play()
                        self.light_pos = (pos_x,pos_y)
        self.check_crafting(mouse,player.skills)

class Item():
    def __init__(self,pos,type,crafted=False):
        self.pos = pos
        self.x = 96
        self.y = -16
        self.real_y = -16
        self.x_in_backpack = 0
        self.y_in_backpack = 0
        self.last_pos = pos
        self.type = type
        self.img = self.load_texture()
        self.selected = False
        self.in_crafting = False
        self.switch = True
        self.crafted = crafted
        self.new_pos = None
        self.sound = pygame.mixer.Sound("sounds/gui/click2.wav")

        if self.type in ITEMS or self.type in TOOLS.keys():
            self.placable = False
        else:
            self.placable = True
            self.physics = TILES[type]["physics"]

        self.food = 0
        for food in FOOD:
            if self.type == food[0]:
                self.food = food[1]

    def load_texture(self):
        texture = pygame.image.load("img/blocks/" + self.type + ".png")
        if not self.type in TOOLS.keys():
            texture = pygame.transform.scale(texture,(16,16))
        return texture

    def update(self,target_y,mouse,backpack, gamemap, player,dt):

        if self.in_crafting:
            self.x = 96 + self.x_in_backpack * 17
            self.y = 6
        else:
            self.x_in_backpack = (self.pos % 8)
            self.y_in_backpack = int(self.pos / 8)
            self.x = 96 + self.x_in_backpack * 17

        if self.pos == -3:
            self.y = 6
            self.x = 295

        if self.pos >= 24 and not self.in_crafting:
            y = 25
        else:
            y = 0
        self.follow_backpack(target_y + y,dt,backpack)
        self.check_drag(backpack, mouse, gamemap, player)

    def follow_backpack(self,target_y,dt,backpack):
        if not backpack.y == 3:
            self.real_y += (target_y + (self.y_in_backpack * 17) + 4 - self.real_y ) / 30 * dt
        else:
            self.real_y = target_y + (self.y_in_backpack * 17) + 4
        self.y = round(self.real_y)

    def drop(self,mouse,backpack,gamemap,player,number=-1):
        if self.x < 90 or (self.x > 220 and self.x < 255) or self.y > 110 or (self.x > 220 and self.y > 30):
            if mouse.x > 160:
                distance = 20
            else:
                distance = -20


            i = -1
            for item in backpack.items:
                i += 1
                if item[0] == self:
                    if number == -1:
                        number = item[1]
                        backpack.items.remove((item[0], number))
                    break

            item = Droped_Item(player.x + distance, player.y + 10, self.type)
            chunk_id = str(player.actual_chunk_x) + ";" + str(player.actual_chunk_y)

            for j in range(number):
                gamemap.chunks[chunk_id].dropped_items.append(item)
            return True
        elif player.dead:
            backpack.items.remove((self, number))

            item = Droped_Item(player.x, player.y, self.type)
            chunk_id = str(player.actual_chunk_x) + ";" + str(player.actual_chunk_y)
            for j in range(number):
                gamemap.chunks[chunk_id].dropped_items.append(item)
            return True

        return False

    def check_drag(self,backpack,mouse,gamemap,player):
        if abs(self.x + 8 - mouse.x) <= 8 and abs(self.y + 8 - mouse.y) <= 8 and mouse.left_click and backpack.full_open:
            keys = pygame.key.get_pressed()
            if not keys[pygame.K_LSHIFT]:
                can = True
                for item in backpack.items:
                    if item[0].selected:
                        can = False
                        break
                if can:
                    self.sound.play()
                    self.selected = True
                    self.last_pos = self.pos
            elif self.switch and len(backpack.items) < 32:
                self.sound.play()
                self.switch = False
                i = -1
                for item in backpack.items:
                    i += 1
                    if item[0] == self:
                        number = item[1]
                        break
                if number > 1:
                    if number % 2 == 0:
                        true_number = number / 2
                    else:
                        true_number = (number - 1) / 2 + 1
                    backpack.items[i] = (self, int(true_number))
                    backpack.add_item(self.type,True, int(true_number - (number % 2)))


        if self.selected and not mouse.left_click:
            self.sound.play()
            self.new_pos = None
            self.crafted = False
            self.selected = False
            self.y = mouse.y - 8
            self.x = mouse.x - 8

            self.in_crafting = False
            if self.x > 240 and self.y < 24:
                self.in_crafting = True

            if self.in_crafting:
                self.x_in_backpack = 9
                if self.x >= 255:
                    self.x_in_backpack = 10
                self.y_in_backpack = 0
            else:
                self.x_in_backpack = round((self.x - 90) / 17)
                self.y_in_backpack = round((self.y - 6)  / 17)


                self.drop(mouse,backpack,gamemap,player)

                if self.y > 80 and self.y <= 110:
                    self.y_in_backpack = 3
                self.pos = self.y_in_backpack * 8 + self.x_in_backpack


                for item in backpack.items:
                    if item[0] == self:
                        number = item[1]
                        break

                i = -1
                for item in backpack.items:
                    i += 1
                    if self.pos == item[0].pos and not item[0] == self:
                        if item[0].type == self.type and item[1] < 64 and number < 64:
                            backpack.items[i] = (item[0],item[1] + number)
                            backpack.items.remove((self,number))
                        else:
                            new_item = item[0]
                            new_item.pos = self.last_pos
                            backpack.items[i] = (new_item,item[1])
                        break
        if self.selected:
            self.y = mouse.y - 8
            self.x = mouse.x - 8
            new_x_in_backpack = round((self.x - 90) / 17)
            new_y_in_backpack = round((self.y - 6) / 17)

            if self.y > 80 and self.y <= 110:
                new_y_in_backpack = 3

            self.new_pos = new_y_in_backpack * 8 + new_x_in_backpack

            if mouse.right_click:
                if not self.drop(mouse, backpack, gamemap, player, 1):

                    backpack.add_item(self.type, True, 1, self.new_pos,)

                i = -1
                for item in backpack.items:
                    i += 1
                    if item[0] == self:
                        number = item[1]
                        break

                if number > 1:
                    backpack.items[i] = (self,number - 1)
                else:
                    backpack.items.remove((self,1))
                    del self

        if not mouse.left_click:
            self.switch = True

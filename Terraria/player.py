import pygame, time, random, math, os
from particle import Particle
from backpack import Backpack
from STATS import *

class Player():

    def __init__(self,x=0,y=-128,skills = None,exp=0,lvl=0,points=0):
        # pos
        self.actual_chunk_x = 0
        self.actual_chunk_y = 0
        self.x = x
        self.y = y
        self.real_x = self.x
        self.real_y = self.y
        self.actual_world = "normal"

        # speed
        self.speed_x = 0
        self.speed_y = -1
        self.max_speed = 1.5
        self.actual_max_speed = self.max_speed

        # collisions
        self.rect = pygame.Rect(self.x,self.y,12,32)
        self.jump_end = False
        self.air_time = 0
        self.previous_air_time = 0
        self.moving = False
        self.double_jump = False

        self.collide_top = False
        self.collide_bottom = False
        self.collide_left = False
        self.collide_right = False

        # textures
        self.load_textures()
        self.load_sounds()
        self.texture_index = 0
        self.direction = "right"
        self.using_tool = False

        # items
        self.backpack = Backpack()
        self.tool_point_x = 0
        self.tool_point_y = 0
        self.tool = None
        self.food = None

        # stats
        self.max_health = 5
        self.health = self.max_health
        self.hunger = 5
        self.last_health = self.health
        self.dead = False
        if skills == None:
            self.skills = {}
            for key in SKILLS.keys():
                self.skills[key] = False
        else:
            self.skills = skills

        self.timer = 0
        self.ground = "grass"
        self.accurate_hit = False
        self.breaking = False
        self.removed_block = None
        self.place_block = False

        self.exp = exp
        self.lvl = lvl
        self.skill_points = 0

    def load_sounds(self):
        self.sounds = {}
        for type in os.listdir("sounds/player"):
            if type == "break" or type == "step":
                sound_groups = {}
                for block_type in os.listdir("sounds/player/" + type):
                    sounds = []
                    for name in os.listdir("sounds/player/" + type + "/" + block_type):
                        sound = pygame.mixer.Sound("sounds/player/" + type + "/" + block_type + "/" + name)
                        sounds.append(sound)
                    sound_groups[block_type] = sounds
                self.sounds[type] = sound_groups
            else:
                sounds = []
                for name in os.listdir("sounds/player/" + type):
                    sound = pygame.mixer.Sound("sounds/player/" + type + "/" + name)
                    sounds.append(sound)
                self.sounds[type] = sounds

        self.channel_block = pygame.mixer.Channel(5)
        self.channel_other = pygame.mixer.Channel(4)
        self.channel_walk = pygame.mixer.Channel(3)

    def update(self,game_map,scroll,mouse,blocks_textures,dt,sounds_on):
        if self.jump_end:
            self.double_jump = False

        if self.exp > 10:
            self.exp = 0
            self.lvl += 1
            self.skill_points += 1

        self.timer += 1
        if self.timer >= 40 / dt:
            self.hunger -= 0.001
            if self.skills["regeneration"]:
                self.health += 0.001
                if self.health > self.max_health:
                    self.health = self.max_health
            if self.hunger < -1:
                self.hunger = 0
                self.health -= 1
            self.timer = 0
            self.channel_block.stop()
            self.channel_other.stop()
            self.channel_walk.stop()

        if self.health <= 0:
            self.death(game_map,mouse)

        self.actual_chunk_x = int(self.x / 128)
        self.actual_chunk_y = int(self.y / 128)

        self.move(game_map,dt)
        self.change_animation(game_map,mouse)
        if sounds_on:
            self.play_sound()

        self.update_tool_point()

        tool_in_hand = False
        food_in_hand = False
        armor_in_hand = None
        for item in self.backpack.items:
            if item[0].pos == 23 + self.backpack.rounded_item_number:
                if item[0].type in TOOLS.keys():
                    for tool in self.backpack.tools:
                        if tool.type == item[0].type:
                            tool_in_hand = True
                            tool.update(self)
                            self.tool = tool
                elif item[0].food > 0:
                    self.food = item[0]
                    food_in_hand = True
                elif item[0].type in ARMOR.keys():
                    armor_in_hand = item

        if not food_in_hand:
            self.food = None

        if not tool_in_hand:
            self.tool = None

        self.place_block = False
        if not self.backpack.full_open:
            if mouse.right_click and self.food != None:
                for item in self.backpack.items:
                    if item[0].pos == 23 + self.backpack.rounded_item_number:
                        place = item
                        index = self.backpack.items.index(item)
                        break
                if place[1] > 1:
                    self.backpack.items[index] = (place[0],place[1] - 1)
                else:
                    self.backpack.items.remove(place)
                self.hunger += self.food.food
                if self.hunger > 5:
                    self.hunger = 5
            elif mouse.right_click and armor_in_hand != None:
                self.backpack.items.remove(armor_in_hand)
                self.load_textures(armor_in_hand[0].type)
                self.max_health = 5 + ARMOR[armor_in_hand[0].type][0]
                self.health = self.max_health
            elif mouse.left_click and (self.tool == None or self.tool.speed != 0):
                self.remove_block(mouse,game_map, scroll, dt)
            if mouse.right_click:
                self.add_block(game_map, mouse, scroll, blocks_textures)

        self.last_health = self.health

    def load_textures(self,type="player"):
        material = None
        if type[-6:] == "_armor":
            material = type
            type = "player-armor"
        self.animations = {}
        self.actual_animation = "idle"
        self.last_animation = "idle"
        for animation in os.listdir("img/" + type):
            frames = []
            for frame in os.listdir("img/" + type + "/" + animation):
                texture = pygame.image.load("img/" + type + "/" + animation + "/" + frame)
                if material != None:
                    texture = self.change_armor_pallete(material,texture)
                tool_point = self.get_tool_point(texture)
                texture.set_at(tool_point, (238, 195, 154))
                frames.append((texture, tool_point))
            self.animations[animation] = frames

    def change_armor_pallete(self,material,texture):
        img = texture.copy()
        img_size = img.get_size()
        for y in range(img_size[1]):
            for x in range(img_size[0]):
                if img.get_at((x, y)) == (255, 100, 255):
                    img.set_at((x,y),ARMOR[material][1])
                elif img.get_at((x, y)) == (255, 0, 255):
                    img.set_at((x, y), ARMOR[material][2])
        return img

    def get_tool_point(self,img):
        img_size = img.get_size()
        for y in range(img_size[1]):
            for x in range(img_size[0]):
                if img.get_at((x,y)) == (255,0,0):
                    return (x,y)
        return (0,0)

    def update_tool_point(self):
        if self.direction == "right":
            self.tool_point_x = self.x + self.animations[self.actual_animation][self.texture_index][1][0]
            self.tool_point_y = self.y + self.animations[self.actual_animation][self.texture_index][1][1]
        else:
            self.tool_point_x = self.x - self.animations[self.actual_animation][self.texture_index][1][0] + 2
            self.tool_point_y = self.y + self.animations[self.actual_animation][self.texture_index][1][1] - 1

    def change_animation(self,gamemap,mouse):
        self.last_animation = self.actual_animation

        if (not self.backpack.full_open) and mouse.left_click:
            self.using_tool = True
        else:
            self.using_tool = False

        if self.using_tool:
            self.actual_animation = "use"

        elif self.jump_end:
            if self.air_time == 0 and self.previous_air_time > 3:
                self.actual_animation = "jump-end"
            elif (not self.actual_animation == "jump-end") or (self.actual_animation == "jump-end" and self.texture_index == 3):
                if self.moving:
                    self.actual_animation = "walk"
                    gamemap.particles.append(Particle(self.x + 6, self.y + 32, "dust"))
                else:
                    self.actual_animation = "idle"
        else:
            if self.speed_y > 0:
                self.actual_animation = "jump-idle-up"
            else:
                self.actual_animation = "jump-idle-down"

        if self.actual_animation == "jump-end" and self.texture_index == 3:
            self.jump_end = True

        if self.actual_animation != self.last_animation:
            self.texture_index = 0

    def play_sound(self):
        if not self.channel_block.get_busy():
            if self.breaking:
                block = TILES[self.removed_block]["sound"]
                self.channel_block.play(random.choice(self.sounds["break"][block]))
            elif self.place_block:
                block = TILES[self.removed_block]["sound"]
                self.channel_block.play(random.choice(self.sounds["step"][block]))

        if not self.channel_walk.get_busy():
            if self.actual_animation == "walk" or self.actual_animation == "jump-end" or (self.actual_animation == "use" and self.collide_bottom and self.moving):
                block = TILES[self.ground]["sound"]
                self.channel_walk.play(random.choice(self.sounds["step"][block]))

        if not self.channel_other.get_busy():
            if self.last_health > self.health:
                self.channel_other.play(random.choice(self.sounds["hurt"]))
            elif self.actual_animation == "use" and self.tool != None and self.tool.speed == 0 and self.texture_index == 2:
                self.channel_other.play(random.choice(self.sounds["missed"]))
            elif self.air_time == 0 and self.previous_air_time > 3:
                self.channel_other.play(random.choice(self.sounds["jump-end"]))

    def death(self,gamemap,mouse):
        if not self.dead:
            self.health = self.max_health
            self.hunger = 5
            for i in range(100):
                gamemap.particles.append(Particle(self.x + 6, self.y + 12, "body"))
            self.dead = True
            for i in range(len(self.backpack.items)):
                self.backpack.items[0][0].drop(mouse,self.backpack,gamemap,self,self.backpack.items[0][1])
            self.x = 0
            self.y = -128
            self.real_x = 0
            self.real_y = -128

    def collision_test(self,rect,game_map,remove_deco=False,ramps=False):
        hit_list = []
        chunks = []

        chunk = str(self.actual_chunk_x) + ";" + str(self.actual_chunk_y)
        chunks.append(chunk)
        chunk = str(self.actual_chunk_x + 1) + ";" + str(self.actual_chunk_y)
        chunks.append(chunk)
        chunk = str(self.actual_chunk_x) + ";" + str(self.actual_chunk_y + 1)
        chunks.append(chunk)
        chunk = str(self.actual_chunk_x - 1) + ";" + str(self.actual_chunk_y)
        chunks.append(chunk)
        chunk = str(self.actual_chunk_x) + ";" + str(self.actual_chunk_y - 1)
        chunks.append(chunk)

        chunk = str(self.actual_chunk_x + 1) + ";" + str(self.actual_chunk_y + 1)
        chunks.append(chunk)
        chunk = str(self.actual_chunk_x + 1) + ";" + str(self.actual_chunk_y - 1)
        chunks.append(chunk)
        chunk = str(self.actual_chunk_x - 1) + ";" + str(self.actual_chunk_y - 1)
        chunks.append(chunk)
        chunk = str(self.actual_chunk_x - 1) + ";" + str(self.actual_chunk_y + 1)
        chunks.append(chunk)

        for chunk in chunks:
            if chunk in game_map.chunks:
                for block in game_map.chunks[chunk].blocks:
                    if rect.colliderect(block):
                        if ramps:
                            if block.physics == "ramp":
                                hit_list.append(block)
                        else:
                            if not remove_deco:
                                if block.physics == "solid":
                                    hit_list.append(block)
                            else:
                                if block.physics == "solid" or block.physics == "deco" or block.physics == "ramp" or (block.physics == "back" and block.type != "underground"):
                                    hit_list.append(block)

        return hit_list

    def move(self,game_map,dt):
        if self.jump_end:
            self.rect.y += 1
            hit_list = self.collision_test(self.rect, game_map)
            if len(hit_list) == 0:
                self.jump_end = False
            self.rect.y -= 1
        # change speed
        if not self.jump_end:
            self.speed_y -= GRAVITY * dt
        else:
            self.speed_y = 0

        self.speed_x = round(self.speed_x, 2)
        self.speed_y = round(self.speed_y, 2)

        if not self.moving:
            self.speed_x = 0

        self.collide_left = False
        self.collide_right = False
        self.collide_top = False
        self.collide_bottom = False

        self.real_x += self.speed_x * dt
        self.rect.x = self.real_x
        hit_list = self.collision_test(self.rect,game_map)

        for block in hit_list:
            if self.speed_x > 0:
                self.rect.right = block.left
                self.collide_right = True
            elif self.speed_x < 0:
                self.rect.left = block.right
                self.collide_left = True
            self.real_x = self.rect.x

        self.real_y -= self.speed_y * dt
        self.rect.y = self.real_y
        hit_list = self.collision_test(self.rect,game_map)

        for block in hit_list:
            if self.speed_y <= 0:
                self.rect.bottom = block.top
                self.collide_bottom = True
                self.jump_end = True
                self.ground = block.type
            elif self.speed_y > 0:
                self.rect.top = block.bottom
                self.collide_top = True
            self.real_y = self.rect.y

        ramps = self.collision_test(self.rect,game_map,False,True)

        for ramp in ramps:
            self.jump_end = True
            rel_x = self.rect.x - ramp.x


            if ramp.direction == "left":
                pos_height = rel_x + self.rect.width
            elif ramp.direction == "right":
                pos_height = 16 - rel_x


            pos_height = min(pos_height, 16)
            pos_height = max(pos_height, 0)

            target_y = ramp.y + 16 - pos_height

            if self.rect.bottom > target_y:
                self.rect.bottom = target_y
                self.real_y = self.rect.y
                self.collide_bottom = True

        self.previous_air_time = self.air_time

        if self.jump_end:
            self.air_time = 0
        else:
            self.air_time += 1

        self.x = int(self.real_x)
        self.y = int(self.real_y)

    def remove_block(self,mouse,game_map,scroll,dt):
        m_block = pygame.Rect(mouse.rect.x + scroll[0] ,mouse.rect.y + scroll[1],1,1)
        self.breaking = False
        hit_list = self.collision_test(m_block,game_map,True)
        if len(hit_list) > 0:
            block = hit_list[0]
            if self.tool == None:
                power = 0
            else:
                power = self.tool.power
            if power >= block.resistance:
                block.destroy = mouse.click_time
                if self.tool != None:
                    block.destroy *= self.tool.speed
                if block.destroy >= block.hardness * FRAMERATE / dt:
                    self.breaking = True
                    self.removed_block = block.type
                    target_chunk = str(block.chunk_x) + ";" + str(block.chunk_y)
                    game_map.chunks[target_chunk].remove_block(block,game_map)
                    mouse.click_time = 0

    def add_block(self,game_map,mouse,scroll, blocks_textures):

        m_block = pygame.Rect(mouse.rect.x + scroll[0] - 8 ,mouse.rect.y + scroll[1] - 8,16,16)
        current_item = None
        for item in self.backpack.items:
            if item[0].pos == 23 + self.backpack.rounded_item_number:
                current_item = item[0]
                break

        if current_item:
            keys = pygame.key.get_pressed()
            if current_item.placable and (not m_block.colliderect(self.rect) or keys[pygame.K_LSHIFT]):
                pos_x = (int(round((mouse.x + scroll[0] - 24) / 16)))
                pos_y = (int(round((mouse.y + scroll[1] - 24) / 16)))
                chunk_x = int(pos_x / 8)
                chunk_y = int(pos_y / 8)

                if chunk_x < 0:
                    chunk_x -= 1
                if chunk_x == 0 and pos_x <= 0:
                    chunk_x = -1

                if chunk_y < 0:
                    chunk_y -= 1
                if chunk_y == 0 and pos_y <= 0:
                    chunk_y = -1

                if pos_x <= 0 and pos_x % 8 == 0:
                    chunk_x += 1

                if pos_y <= 0 and pos_y % 8 == 0:
                    chunk_y += 1

                chunk_id = str(chunk_x) + ";" + str(chunk_y)

                keys = pygame.key.get_pressed()

                if current_item.physics == "ramp":
                    if self.x - mouse.x - scroll[0] > 0:
                        direction = "right"
                    else:
                        direction = "left"
                else:
                    direction = "right"

                if game_map.chunks[chunk_id].add_block(((pos_x % 8) + 1, (pos_y % 8) + 1), current_item.type, game_map,blocks_textures,keys[pygame.K_LSHIFT],pos_x,pos_y,direction):
                    self.place_block = True
                    self.removed_block = current_item.type
                    i = -1
                    for item in self.backpack.items:
                        i += 1
                        if self.backpack.items[i][0] == current_item:
                            if self.backpack.items[i][1] == 1:
                                self.backpack.items.remove(self.backpack.items[i])
                            else:
                                place = (current_item,self.backpack.items[i][1] -1)
                                self.backpack.items[i] = place
                            break
        else:
            pos_x = (int(round((mouse.x + scroll[0] - 24) / 16)))
            pos_y = (int(round((mouse.y + scroll[1] - 24) / 16)))
            chunk_x = int(pos_x / 8)
            chunk_y = int(pos_y / 8)

            if chunk_x < 0:
                chunk_x -= 1
            if chunk_x == 0 and pos_x <= 0:
                chunk_x = -1

            if chunk_y < 0:
                chunk_y -= 1
            if chunk_y == 0 and pos_y <= 0:
                chunk_y = -1

            if pos_x <= 0 and pos_x % 8 == 0:
                chunk_x += 1

            if pos_y <= 0 and pos_y % 8 == 0:
                chunk_y += 1

            chunk_id = str(chunk_x) + ";" + str(chunk_y)

            for block in game_map.chunks[chunk_id].blocks:
                if m_block.colliderect(block):
                    if block.type == "door_close":
                        game_map.chunks[chunk_id].remove_block(block, game_map)
                        game_map.chunks[chunk_id].add_block((block.x_in_chunk, block.y_in_chunk), "door_open",game_map)
                        random.choice(self.sounds["door_open"]).play()
                        break
                    elif block.type == "door_open":
                        game_map.chunks[chunk_id].remove_block(block, game_map)
                        game_map.chunks[chunk_id].add_block((block.x_in_chunk, block.y_in_chunk), "door_close",game_map)
                        random.choice(self.sounds["door_close"]).play()
                        break


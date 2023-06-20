import pygame, math, random, os
from particle import Particle
from tile import Droped_Item
from STATS import *

class Mob(pygame.Rect):

    def __init__(self,type,x,y):

        # position
        self.x = x
        self.y = y
        self.real_x = x
        self.real_y = y
        self.actual_chunk_x = 0
        self.actual_chunk_y = 0

        # type
        self.type = type

        self.width = MOBS[type]["width"]
        self.height = MOBS[type]["height"]

        attitude = random.choice(MOBS[type]["attitude"])

        if attitude == "monster":
            self.attitude = "agressive"
            self.monster = True
        else:
            self.monster = False
            self.attitude = attitude

        self.health = MOBS[type]["health"]
        self.shift = MOBS[type]["shift"]
        self.max_speed = MOBS[type]["max_speed"]
        self.drop = MOBS[type]["drop"]
        self.exp = MOBS[type]["exp"]

        self.actual_max_speed = self.max_speed

        if self.attitude == "passive":
            self.move_direction = "stop"

        self.rect = pygame.Rect(x,y,self.width,self.height)

        # animations
        self.load_textures()
        self.animation_index = 0
        self.actual_animation = "idle"
        self.last_animation = None
        self.direction = "right"
        self.timer = 0

        # speed
        self.speed_x = 0
        self.speed_y = 0
        self.previous_speed_y = self.speed_y
        self.moving = False
        self.jump_end = True
        self.air_time = 0
        self.wait = False


        # collision rects
        self.rect_top = pygame.Rect(0, 0, self.width - 2, 1)
        self.rect_bottom = pygame.Rect(0, 0, self.width - 2, 1)
        self.rect_left = pygame.Rect(0, 0, 1, int(self.height/2))
        self.rect_right = pygame.Rect(0, 0, 1, int(self.height/2))

        self.collide_left = False
        self.collide_right = False
        self.collide_top = False
        self.collide_bottom = False

        # collisions
        self.on_ground = False
        self.hitted = False

        # behaviour
        self.agro = False
        self.attacking = False
        self.attacked = False

    def load_textures(self):
        self.animations = {}
        if self.attitude != "passive":
            self.animations["sleep"] = (self.load_animation("sleep"))
            self.animations["sleep-idle"] = (self.load_animation("sleep-idle"))
            self.animations["attack"] = (self.load_animation("attack"))

        self.animations["walk"] = (self.load_animation("walk"))
        self.animations["idle"] = (self.load_animation("idle"))


    def load_animation(self,name):
        animation = []
        frames = len(list(os.listdir("img/mobs/" + self.type + "/" + name)))
        for frame in range(frames):
            texture = pygame.image.load("img/mobs/" + self.type + "/" + name + "/" + self.type + "-" + name + str(frame + 1) + ".png")
            animation.append(texture)
        return animation

    def update(self,gamemap,scroll,player,mobs,clock,dt):

        if player.tool == None or player.tool.speed > 0:
            self.hitted = False
        if player.actual_animation != "use" or player.texture_index != 2:
            self.hitted = False
        if self.actual_animation != "attack" or self.animation_index != 2:
            self.attacked = False

        self.change_animation()

        self.timer += dt * 5
        if self.timer > int(1000 / len(self.animations[self.actual_animation])):
            self.timer = 0
            if self.animation_index < len(self.animations[self.actual_animation]) - 1:
                self.animation_index += 1
            else:
                self.animation_index = 0

        if self.animation_index > len(self.animations[self.actual_animation]) - 1:
            self.animation_index = 0

        self.move(gamemap,GRAVITY,clock,dt,mobs)
        self.behaviour(player, gamemap,dt)
        self.collide_sword(player,gamemap)

        if self.health <= 0:
            if self in gamemap.mobs:
                gamemap.mobs.remove(self)
            player.exp += self.exp
            item = Droped_Item(self.x,self.y,self.drop)
            target_chunk = str(self.actual_chunk_x) + ";" + str(self.actual_chunk_y)
            gamemap.chunks[target_chunk].dropped_items.append(item)
            del self

    def collision_test(self,rect,game_map,ramps=False):
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
                        elif block.physics == "solid":
                            hit_list.append(block)

        return hit_list

    def move(self,game_map,GRAVITY, clock,dt,mobs):
        if self.attitude == "passive":
            if self.agro:
                self.actual_max_speed = 3 * self.max_speed
            else:
                self.actual_max_speed = self.max_speed


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

        if not self.moving:
            self.speed_x = 0

        if abs(self.speed_x) > self.actual_max_speed:
            if self.speed_x > 0:
                self.speed_x = self.actual_max_speed
            else:
                self.speed_x = -1 * self.actual_max_speed


        self.speed_x = round(self.speed_x, 2)
        self.speed_y = round(self.speed_y, 2)


        self.collide_left = False
        self.collide_right = False
        self.collide_top = False
        self.collide_bottom = False

        for mob in mobs:
            if mob != self and not mob.wait:
                if self.colliderect(mob):
                    self.real_x -= self.speed_x / 2
                    self.wait = True
                    self.moving = True
                else:
                    self.wait = False

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

        ramps = self.collision_test(self.rect,game_map,True)

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


    def change_animation(self):


        self.last_animation = self.actual_animation
        if self.attitude == "agressive" or self.attitude == "neutral":
            if not self.agro:
                if self.last_animation != "sleep-idle":
                    if self.attitude == "neutral":
                        self.actual_animation = "sleep"
                    else:
                        self.actual_animation = "idle"
                    if self.animation_index == 2:
                        self.actual_animation = "sleep-idle"
            else:
                if self.speed_x > 0:
                    self.direction = "right"
                elif self.speed_x < 0:
                    self.direction = "left"

                if self.attacking:
                    self.actual_animation = "attack"
                elif self.moving:
                    self.actual_animation = "walk"
                else:
                    self.actual_animation = "idle"
        else:
            if self.speed_x > 0:
                self.direction = "left"
            elif self.speed_x < 0:
                self.direction = "right"

            if self.moving:
                self.actual_animation = "walk"
            else:
                self.actual_animation = "idle"

        if self.actual_animation != self.last_animation:
            self.texture_index = 0

    def collide_sword(self,player,gamemap):
        if not self.monster or player.skills["holy_aura"]:
            if player.actual_animation == "use" and player.texture_index == 2 and player.tool != None and player.tool.speed == 0 and not self.hitted:
                if self.colliderect(player.tool):
                    if self.health > 0:
                        self.health -= player.tool.power
                        if player.skills["blood_lust"]:
                            self.health -= 1
                        self.hitted = True
                        random.choice(player.sounds["hitted"]).play()
                        for i in range(20):
                            gamemap.particles.append(Particle(self.centerx,self.centery,"blood"))


    def check_agro(self,player):
        if not player.dead:
            if self.attitude == "agressive":
                distance = math.sqrt((player.x + 6 - self.centerx) ** 2 + (player.y + 26 - self.centery) ** 2)
                if distance < 80 or self.type == "king":
                    self.agro = True
                else:
                    self.agro = False
                if (self.type != "king" and distance < 30) or (self.type == "king" and abs(player.x + 6 - self.centerx) < 30):
                    self.attacking = True
                else:
                    self.attacking = False
            elif self.attitude == "neutral":
                if self.hitted:
                    self.agro = True
                if self.agro:
                    distance = math.sqrt((player.rect.centerx - self.centerx) ** 2 + (player.rect.centery + 10 - self.centery) ** 2)
                    if distance > 60:
                        self.agro = False
                    if distance < 30:
                        self.attacking = True
                    else:
                        self.attacking = False
            else:
                if self.hitted:
                    self.agro = True
        else:
            self.agro = False
            self.attacking = False

    def behaviour(self,player,game_map,dt):
        self.check_agro(player)
        if self.attitude == "agressive" or self.attitude == "neutral":
            if self.agro:
                if self.centerx - player.rect.centerx + 6 < -10:
                    move_direction = "right"
                elif self.centerx - player.rect.centerx + 6 > 10:
                    move_direction = "left"
                else:
                    move_direction = "stop"

                if self.jump_end:

                    if move_direction == "right":
                        self.moving = True
                        if self.collide_right:
                            self.speed_y = 1.5
                            self.jump_end = False
                        self.speed_x += 0.3
                    elif move_direction == "left":
                        self.moving = True
                        if self.collide_left:
                            self.speed_y = 1.5
                            self.jump_end = False
                        self.speed_x -= 0.3
                    else:
                        self.moving = False

                if self.attacking and self.animation_index == 2 and not self.attacked:
                    self.attacked = True
                    player.health -= 1
                    for i in range(20):
                        game_map.particles.append(Particle(player.x + 6,player.y + 16,"blood"))
            else:
                self.moving = False
                self.speed_x = 0
                self.jump_end = True
        elif self.attitude == "passive":
            if self.agro:
                if self.centerx - player.rect.centerx > 0:
                    self.move_direction = "right"
                elif self.centerx - player.rect.centerx < 0:
                    self.move_direction = "left"
                distance = math.sqrt((player.x + 6 - self.centerx) ** 2 + (player.y + 26 - self.centery) ** 2)
                if distance > 100:
                    self.move_direction = "stop"
                    self.agro = False
                    self.hitted = False
            else:
                if random.randint(1,200) == 1:
                    tmp = random.randint(1,3)
                    if tmp == 1:
                        self.move_direction = "left"
                        self.moving = True
                    elif tmp == 2:
                        self.move_direction = "right"
                        self.moving = True
                    else:
                        self.move_direction = "stop"
                        self.moving = False

            if self.jump_end:
                if self.move_direction == "right":
                    self.moving = True
                    if self.collide_right:
                        self.speed_y = 1.5
                        self.jump_end = False
                    self.speed_x += 0.1
                elif self.move_direction == "left":
                    self.moving = True
                    if self.collide_left:
                        self.speed_y = 1.5
                        self.jump_end = False
                    self.speed_x -= 0.1
                else:
                    self.moving = False


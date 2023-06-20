import pygame, random, math
from STATS import *

class Tile(pygame.Rect):

    def __init__(self,x,y,type,xc,yc,chunk_x,chunk_y,biom,direction = "right"):

        # pos
        self.x = x
        self.y = y
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.x_in_chunk = xc
        self.y_in_chunk = yc
        self.biom = biom

        # size
        self.width = 16
        self.height = 16

        self.type = type
        self.destroy = 0
        self.img = None
        self.direction = direction
        self.hardness = TILES[self.type]["hardness"]
        self.physics = TILES[self.type]["physics"]
        try:
            self.resistance = TILES[self.type]["resistance"]
        except:
            self.resistance = 0


        if "animated" in TILES[self.type].keys():
            self.grains = []
            for i in range(TILES[self.type]["animated"]):
                grain = Grain(self.x,self.y,self.type)
                self.grains.append(grain)

class Grain():
    def __init__(self,x,y,type):
        self.x = x + random.randint(1,16) - 16
        self.y = y
        self.size = random.randint(8,10) / 10
        self.img_index = random.randint(1,4)
        self.angle = 0
        self.last_player_pos = (0,0)
        self.target_angle = self.angle
        self.rotation_full = False
        self.type = type

    def collide(self,rect):
        rect_pos = [rect.centerx - 10, rect.bottom]
        distance = math.sqrt((rect_pos[0] - self.x) ** 2 + (rect_pos[1] - self.y) ** 2)
        if abs(rect.bottom - self.y) < 20:
            h_dis = rect_pos[0] - self.x
            if distance < 20:
                temp_target = 0
                if h_dis <= 0:
                    temp_target = 70 - h_dis * 3.5
                if h_dis > 0:
                    temp_target = -70 - h_dis * 3.5
                self.target_angle = min(self.target_angle + temp_target, 80)
                self.target_angle = max(self.target_angle, -80)

        if distance > 20 and abs(self.target_angle) > 31:
            self.target_angle = 0

    def update(self,player,wind,dt):

        self.collide(player.rect)
        self.check_wind(wind)
        self.angle += (self.target_angle - self.angle) /20 * dt

    def check_wind(self,wind):
        speed = (wind.speed+3) * random.randint(7,10) /60
        if not self.rotation_full:
            self.target_angle += speed
        else:
            self.target_angle -= speed
        if self.target_angle > 30:
            self.rotation_full = True
        if self.target_angle < -30:
            self.rotation_full = False

class Droped_Item(pygame.Rect):
    def __init__(self,x,y,type):

        # pos
        self.x = x + 4
        self.y = y + 4
        self.real_y = y + 4
        self.chunk = 0
        # size
        self.width = 8
        self.height = 8

        # custom drops
        try:
            self.type = TILES[type]["drop"]
        except:
            self.type = type

        texture = pygame.image.load("img/blocks/" + self.type + ".png")
        self.img = pygame.transform.scale(texture,(8,8))

    def update(self,game_map,dt):
        chunk_x = int(self.x/128)
        if self.x < 0:
            chunk_x -= 1
        chunk_y = int(self.y/128)
        if self.y < 0:
            chunk_y -= 1
        self.chunk = str(chunk_x) + ";" + str(chunk_y)

        # check collision
        collide = False
        if self.chunk in game_map.chunks.keys():
            for block in game_map.chunks[self.chunk].blocks:
                if block.physics == "solid":
                    if self.colliderect(block):
                        collide = True
                        break
        if not collide:
            self.real_y += dt / 3
            self.y = int(self.real_y)
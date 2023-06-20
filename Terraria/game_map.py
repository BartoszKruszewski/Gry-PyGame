import pygame, random, pickle
from tile import Tile
from tile import Droped_Item
from mob import Mob
from background import Background
from STATS import *

class Game_Map():
    def __init__(self,type="normal"):
        self.chunks = {}
        self.CHUNK_SIZE = 8
        self.type = type
        if type == "normal":
            self.biom = "woodland"
        elif type == "dark":
            self.biom = "dark_land"
            self.king_spawned = False
        self.torches = []
        self.mobs = []
        self.particles = []

    def add_chunk(self,pos,blocks_textures):
        data = self.generate_chunk(pos,blocks_textures)
        chunk = Chunk(pos[0],pos[1],data[0],data[1])
        chunk.remove_deco(self)
        chunk_id = str(pos[0]) + ";" + str(pos[1])
        self.chunks[chunk_id] = chunk

    def generate_cave(self):
        tiles = []
        size = random.randint(10,20)
        start_tile = (4,4)
        actual_tile = start_tile
        next_tiles = []
        direction = 0
        for i in range(size):
            for j in range(random.randint(1,4)):
                direction = random.randint(1,4)
                if direction == 1:
                    next_tile = (actual_tile[0],actual_tile[1]-1)
                elif direction == 2:
                    next_tile = (actual_tile[0]+1,actual_tile[1])
                elif direction == 3:
                    next_tile = (actual_tile[0],actual_tile[1]+1)
                elif direction == 4:
                    next_tile = (actual_tile[0]-1,actual_tile[1])
                next_tiles.append(next_tile)
            for tile in next_tiles:
                tiles.append(tile)
            actual_tile = random.choice(next_tiles)

        return tiles

    def generate_chunk(self,pos,blocks_textures):
        chunk = []

        if self.type == "normal":
            if random.randint(1,10) == 1 or self.biom == None:
                bioms = list(BIOMS.keys())
                bioms.remove("none")
                bioms.remove("underground")
                bioms.remove("cave")
                bioms.remove("dark_land")
                bioms.remove("dark_underground")
                self.biom = random.choice(bioms)

        if pos[1] == 0:
            biom = self.biom
        elif pos[1] < 0:
            biom = "none"
        else:
            if self.type == "normal":
                if random.randint(1,2) == 1:
                    biom = "underground"
                else:
                    biom = "cave"
                    cave_shape = self.generate_cave()
            elif self.type == "dark":
                biom = "dark_underground"

        upper_layer = BIOMS[biom]["upper_layer"]
        main_block = BIOMS[biom]["main_block"]
        decos = BIOMS[biom]["decos"]
        max_height = BIOMS[biom]["max_height"]

        height = int(max_height/2)
        block_heights = []
        for i in range(self.CHUNK_SIZE):
            if max_height != -1:
                if random.randint(1,4) == 1:
                    if random.randint(1,2) == 1:
                        if height < max_height:
                            height += 1
                        else:
                            height -= 1
                    else:
                        if height > 1:
                            height -= 1
                        else:
                            height += 1
            else:
                height = 8
            block_heights.append(height)

        if self.type == "normal":
            for mob in MOBS.keys():
                if MOBS[mob]["biom"] == biom:
                    if random.randint(1, 2) == 1:
                        self.mobs.append(Mob(mob, pos[0] * 128 + random.randint(0, 128), -100))

        elif self.type == "dark":
            if biom == "dark_land":
                if random.randint(1,3) == 1:
                    self.mobs.append(Mob("golem", pos[0] * 128 + random.randint(0, 128), -100))
                if not self.king_spawned and random.randint(1,10) == 1:
                    self.mobs.append(Mob("king", pos[0] * 128 + random.randint(0, 128), -100))
                    self.king_spawned = True

        for y in range(self.CHUNK_SIZE):
            for x in range(self.CHUNK_SIZE):
                direction = None
                tile_type = None
                global_y = (pos[1] * self.CHUNK_SIZE + y) * 16
                global_x = (pos[0] * self.CHUNK_SIZE + x) * 16

                if biom != "cave":
                    if y == 8 - block_heights[x]:
                        if pos[1] == 0:
                            if x != self.CHUNK_SIZE - 1 and x != 0 and biom != "dark_land":
                                if block_heights[x+1] < block_heights[x] and block_heights[x-1] == block_heights[x]:
                                    direction = "right"
                                elif block_heights[x+1] == block_heights[x] and block_heights[x-1] < block_heights[x]:
                                    direction = "left"
                        tile_type = upper_layer

                    elif y > 8 - block_heights[x]:
                        tile_type = main_block
                        if biom == "underground" and random.randint(1, 7) == 1:
                            mines = []
                            for mine in MINES:
                                if global_y > mine[1]:
                                    for i in range(int(mine[2]*10)):
                                        mines.append(mine[0])
                            tile_type = random.choice(mines)

                    elif y == 8 - (block_heights[x] + 1) and len(decos) > 0:
                        can_deco = True
                        if x != self.CHUNK_SIZE - 1 and x != 0:
                            if block_heights[x + 1] < block_heights[x] and block_heights[x - 1] == block_heights[x]:
                                can_deco = False
                            elif block_heights[x + 1] == block_heights[x] and block_heights[x - 1] < block_heights[x]:
                                can_deco = False
                        if can_deco:
                            if random.randint(1, 3) == 1:
                                tile_type = random.choice(decos)
                            else:
                                if upper_layer in TOPS.keys():
                                    tile_type = TOPS[upper_layer]
                else:
                    is_stone = True
                    for tile in cave_shape:
                        if x == tile[0] and y == tile[1]:
                            if random.randint(1,10) == 1:
                                tile_type = random.choice(decos)

                            else:
                                tile_type = "underground"
                            is_stone = False
                            break
                    if is_stone:
                        tile_type = "stone"

                if self.type == "dark" and global_y > 120:
                    tile_type = "obsydian"

                if tile_type != None:
                    if direction != None:
                        tile_type = upper_layer + "_ramp"
                        block = Tile(global_x, global_y, tile_type, x, y, pos[0], pos[1],biom,direction)
                    else:
                        block = Tile(global_x, global_y, tile_type, x, y, pos[0], pos[1],biom)
                    if block.type == "web":
                        img = blocks_textures["underground"].copy()
                        img.blit(blocks_textures["web"], (0, 0))
                        block.img = img

                    chunk.append(block)
        return chunk, biom

class Chunk():
    def __init__(self,x,y,blocks,type):
        self.x = x
        self.y = y
        self.blocks = blocks
        self.dropped_items = []
        self.CHUNK_SIZE = 8
        self.torches = []
        self.biom = type

    def update_blocks(self,gamemap):
        self.remove_deco(gamemap)

    def remove_deco(self,gamemap):
        decos = []
        for block in self.blocks:
            if block.physics == "deco":
                decos.append(block)
        for tile in decos:
            remove = True
            for block in self.blocks:
                if block.physics == "solid":
                    if (block.x_in_chunk == tile.x_in_chunk) and (block.y_in_chunk - tile.y_in_chunk == 1):
                        remove = False
                        break
                elif block.physics == "back":
                    if (tile.type == "torch" or tile.type == "paint_white" or tile.type == "paint_blue" or tile.type == "paint_red" or tile.type == "paint_yellow" or tile.type == "paint_green") and block.x_in_chunk == tile.x_in_chunk and block.y_in_chunk == tile.y_in_chunk:
                        remove = False
                        break
            if remove:
                self.remove_block(tile,gamemap)

    def remove_items(self,player):
        if not player.dead:
            for item in self.dropped_items:
                if player.rect.colliderect(item) and len(player.backpack.items) < 32:
                    self.dropped_items.remove(item)
                    player.backpack.add_item(item.type)
                    player.sounds["item_pick"][0].play()
                    del item

    def remove_block(self,block,gamemap):
        if block in self.blocks:
            if block.type != "underground":
                self.blocks.remove(block)
                if block.y >= 8 * 16:
                    self.add_block((block.x_in_chunk,block.y_in_chunk),"underground",gamemap)
                if block.type != "door_close" and block.type != "door_open":
                    if not ("drop" in TILES[block.type].keys() and TILES[block.type]["drop"] == "none"):
                        item = Droped_Item(block.x,block.y,block.type)
                        self.dropped_items.append(item)
                if block.type == "torch":
                    if (block.x + 8,block.y + 8) in self.torches:
                        self.torches.remove((block.x + 8,block.y + 8))
                elif block.type == "bonfire":
                    self.torches.remove((block.x + 6,block.y + 13))
                    self.torches.remove((block.x + 7, block.y + 13))
                    self.torches.remove((block.x + 8, block.y + 13))
                    self.torches.remove((block.x + 9, block.y + 13))
                    self.torches.remove((block.x + 10, block.y + 13))
                if block.physics == "solid":
                    self.update_blocks(gamemap)
                del block


    def add_block(self,pos,type,gamemap,blocks_textures=None,back=False,torch_x=0,torch_y=0,direction="right"):

        global_x = (self.x * self.CHUNK_SIZE + pos[0]) * 16
        global_y = (self.y * self.CHUNK_SIZE + pos[1]) * 16
        block = Tile(global_x, global_y, type, pos[0], pos[1], self.x,self.y,direction)
        is_block = False
        for tile in self.blocks:
            if tile.x == block.x and tile.y == block.y:
                if tile.physics == "back" or tile.physics == "liquid":
                    if not (block.physics == "deco" or block.physics == "ramp" or block.physics == "liquid"):
                        self.blocks.remove(tile)
                    if (block.physics == "deco" or block.physics == "ramp" ) and block.type != "torch":
                        img = blocks_textures[tile.type].copy()
                        dark = pygame.Surface((16, 16), pygame.SRCALPHA)
                        pygame.draw.rect(dark, (0, 0, 0, 200), (0, 0, 16, 16))
                        img.blit(dark,(0,0))
                        if block.physics == "ramp" and block.direction == "left":
                            img.blit(pygame.transform.flip(blocks_textures[block.type].copy(),True,False), (0, 0))
                        else:
                            img.blit(blocks_textures[block.type], (0, 0))
                        block.img = img
                else:
                    is_block = True

                break


        if not is_block:
            if back and block.physics == "solid":
                if block.type != "glass" and not (block.type == "oak_window" or block.type == "birch_window" or block.type == "spruce_window" or block.type == "dead_window"):
                    if block.img == None:
                        block.img =  blocks_textures[block.type].copy()
                    dark = pygame.Surface((16,16),pygame.SRCALPHA)
                    pygame.draw.rect(dark,(0,0,0,200),(0,0,16,16))
                    block.img.blit(dark,(0,0))
                elif block.type == "oak_window":
                    block.img =  blocks_textures["oak_window_back"].copy()
                elif block.type == "birch_window":
                    block.img =  blocks_textures["birch_window_back"].copy()
                elif block.type == "spruce_window":
                    block.img =  blocks_textures["spruce_window_back"].copy()
                elif block.type == "dead_window":
                    block.img =  blocks_textures["dead_window_back"].copy()
                block.physics = "back"
            self.blocks.append(block)
            if block.type == "torch":
                self.torches.append(((torch_x + 1) * 16 + 8, (torch_y + 1) * 16 + 8))
            elif block.type == "bonfire":
                self.torches.append(((torch_x + 1) * 16 + 8, (torch_y + 1) * 16 + 13))
                self.torches.append(((torch_x + 1) * 16 + 7, (torch_y + 1) * 16 + 13))
                self.torches.append(((torch_x + 1) * 16 + 9, (torch_y + 1) * 16 + 13))
                self.torches.append(((torch_x + 1) * 16 + 6, (torch_y + 1) * 16 + 13))
                self.torches.append(((torch_x + 1) * 16 + 10, (torch_y + 1) * 16 + 13))
            return True
        return False


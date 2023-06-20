import pygame

class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.left_click = False
        self.right_click = False
        self.rect = pygame.Rect(0, 0, 1, 1)
        self.click_time = 0
        self.images = []
        texture = pygame.image.load("img/cursors/cursor1.png")
        self.images.append(texture)
        texture = pygame.image.load("img/cursors/cursor2.png")
        self.images.append(texture)
        texture = pygame.image.load("img/cursors/cursor3.png")
        self.images.append(texture)
        texture = pygame.image.load("img/cursors/cursor4.png")
        self.images.append(texture)
        self.image_index = 0
        self.right_click_switch = True
        self.left_click_switch = True

    def update(self,player,current_menu):
        x, y = pygame.mouse.get_pos()
        self.x = int(x/4)
        self.y = int(y/4)
        self.rect.center = (self.x, self.y)
        keys = pygame.mouse.get_pressed()
        if current_menu != "game":
            if keys[0]:
                    if self.left_click_switch:
                        self.left_click = True
                        self.left_click_switch = False
                    else:
                        self.left_click = False
            else:
                self.left_click = False
                self.left_click_switch = True
        else:
            if keys[0]:
                self.left_click = True
                self.click_time += 1
            else:
                self.left_click = False
                self.click_time = 0

        if keys[2]:
                if self.right_click_switch:
                    self.right_click = True
                    self.right_click_switch = False
                else:
                    self.right_click = False
        else:
            self.right_click = False
            self.right_click_switch = True

        if current_menu != "game":
            self.image_index = 2
        elif player != None:
            if player.backpack.full_open:
                if self.left_click:
                    self.image_index = 3
                else:
                    self.image_index = 2
            else:
                if player.tool == "wooden_pickaxe" or player.tool == "iron_pickaxe" or player.tool == "diamond_pickaxe":
                    self.image_index = 0
                elif player.tool == "wooden_sword" or player.tool == "iron_sword" or player.tool == "diamond_sword":
                    self.image_index = 1
                else:
                    current_item = None
                    for item in player.backpack.items:
                        if item[0].pos == 23 + player.backpack.rounded_item_number:
                            current_item = item[0]
                            break
                    if current_item and current_item.placable:
                        texture = current_item.img
                        if len(self.images) > 4:
                            self.images.remove(self.images[4])
                        self.images.append(pygame.transform.scale(texture,(8,8)))
                        self.image_index = 4
                    else:
                        self.image_index = 2




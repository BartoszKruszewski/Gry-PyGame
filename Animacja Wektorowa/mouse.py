from pygame import Rect, mouse
from const import SCREEN_SIZE, DRAW_SCREEN_SIZE


class Mouse:
    def __init__(self):
        self.rect = Rect(0, 0, 1, 1)
        self.left_click = False
        self.right_click = False
        self.left_switch = False
        self.right_switch = False

    def update(self):
        pos = mouse.get_pos()
        self.rect.x = pos[0] * DRAW_SCREEN_SIZE.x / SCREEN_SIZE.x
        self.rect.y = pos[1] * DRAW_SCREEN_SIZE.y / SCREEN_SIZE.y

        buttons = mouse.get_pressed()
        if buttons[0]:
            self.left_click = not self.left_switch
            self.left_switch = True
        else:
            self.left_switch = False
        if buttons[2]:
            self.right_click = not self.right_switch
            self.right_switch = True
        else:
            self.right_switch = False

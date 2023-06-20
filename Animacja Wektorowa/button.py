from pygame import Rect, draw
from draw import Draw
from const import BUTTON_FRAME_SIZE, DRAW_SCREEN_SIZE, SCREEN_SIZE,\
    BUTTON_LIGHTEN


class Button:
    def __init__(self, pos, size, function, color, **kwargs):
        self.rect = Rect(pos.x, pos.y, size.x, size.y)
        self.function = function
        self.hovered = False
        self.switched = False
        self.color = color

    def update(self, mouse, states):
        self.hovered = mouse.rect.colliderect(self.rect)
        self.switched = self.hovered and mouse.left_switch
        if self.hovered and mouse.left_click:
            states[self.function] = True

    def draw(self, surf):
        if self.switched:
            draw.rect(
                surf, Draw.adjust_color(self.color, -BUTTON_LIGHTEN * 3),
                self.rect)
            draw.rect(
                surf, Draw.adjust_color(self.color, -BUTTON_LIGHTEN * 2),
                self.rect,
                width = round(
                    BUTTON_FRAME_SIZE * DRAW_SCREEN_SIZE.x /
                    SCREEN_SIZE.x))
        elif self.hovered:
            draw.rect(surf, Draw.adjust_color(self.color, 0), self.rect)
            draw.rect(
                surf, Draw.adjust_color(self.color, -BUTTON_LIGHTEN), self.rect,
                width = round(
                    BUTTON_FRAME_SIZE * DRAW_SCREEN_SIZE.x /
                    SCREEN_SIZE.x))
        else:
            draw.rect(
                surf, Draw.adjust_color(self.color, -BUTTON_LIGHTEN), self.rect)
            draw.rect(
                surf, Draw.adjust_color(self.color, -BUTTON_LIGHTEN * 2),
                self.rect,
                width = round(
                    BUTTON_FRAME_SIZE * DRAW_SCREEN_SIZE.x /
                    SCREEN_SIZE.x))

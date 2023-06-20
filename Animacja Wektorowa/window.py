from pygame import Rect, draw, Vector2
from button import Button
from const import DRAW_SCREEN_SIZE, BUTTONS_SIZES, \
    BUTTONS_FUNCTIONS, BUTTONS_POSITIONS, BUTTONS_COLORS
from draw import Draw


class Window:
    def __init__(self, size, pos, color, buttons_name):
        self.rect = Rect(
            round(DRAW_SCREEN_SIZE.x * pos.x) + 1,
            round(DRAW_SCREEN_SIZE.y * pos.y) + 1,
            round(DRAW_SCREEN_SIZE.x * size.x) - 2,
            round(DRAW_SCREEN_SIZE.y * size.y) - 2,
        )
        self.color = color
        self.buttons = [
            Button(
                Vector2(
                    round(BUTTONS_POSITIONS[name].x * self.rect.width) +
                    self.rect.x,
                    round(BUTTONS_POSITIONS[name].y * self.rect.height) +
                    self.rect.y),
                Vector2(
                    round(BUTTONS_SIZES[name].x * self.rect.width),
                    round(BUTTONS_SIZES[name].y * self.rect.height)),
                BUTTONS_FUNCTIONS[name],
                BUTTONS_COLORS[name])
            for name in buttons_name
        ]
        self.hovered = False

    def add_button(
            self, pos, size, function, color, template_class = Button,
            **kwargs):
        self.buttons.append(
            template_class(
                Vector2(
                    round(pos.x * self.rect.width) + self.rect.x,
                    round(pos.y * self.rect.height) + self.rect.y
                ),
                Vector2(
                    round(size.x * self.rect.width),
                    round(size.y * self.rect.height)
                ),
                function,
                color,
                **kwargs
            )
        )

    def update(self, mouse, states):
        self.hovered = mouse.rect.colliderect(self.rect)
        if self.hovered:
            for button in self.buttons:
                button.update(mouse, states)

    def draw(self, surf):
        draw.rect(surf, Draw.adjust_color(self.color, 0), self.rect)
        draw.rect(
            surf, Draw.adjust_color(self.color, -20), self.rect,
            width = 1)
        for button in self.buttons:
            button.draw(surf)

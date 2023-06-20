from button import Button
from pygame import transform, Vector2
from const import BUTTON_FRAME_SIZE, DRAW_SCREEN_SIZE, SCREEN_SIZE


class FrameButton(Button):
    def __init__(self, pos, size, function, color, **kwargs):
        super().__init__(pos, size, function, color)
        self.image = None
        self.update_image(kwargs["image"])

    def update(self, mouse, states):
        super().update(mouse, states)

    def update_image(self, image):
        self.image = transform.scale(
            image, self.rect.size - Vector2(
                4 * BUTTON_FRAME_SIZE * DRAW_SCREEN_SIZE.x /
                SCREEN_SIZE.x,
                4 * BUTTON_FRAME_SIZE * DRAW_SCREEN_SIZE.x /
                SCREEN_SIZE.x
            ))

    def draw(self, surf):
        super().draw(surf)
        surf.blit(
            self.image,
            Vector2(
                self.rect.x + 2 * round(
                    BUTTON_FRAME_SIZE * DRAW_SCREEN_SIZE.x /
                    SCREEN_SIZE.x),
                self.rect.y + 2 * round(
                    BUTTON_FRAME_SIZE * DRAW_SCREEN_SIZE.x /
                    SCREEN_SIZE.x)))

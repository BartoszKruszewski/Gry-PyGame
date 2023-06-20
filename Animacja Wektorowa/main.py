from animation import Animation
from pygame import *
from const import *


class Main:
    def __init__(self):
        init()
        self.screen = display.set_mode(SCREEN_SIZE)
        self.draw_screen = Surface(DRAW_SCREEN_SIZE)
        self.scene = self.game
        self.is_running = True
        self.dt = 1
        self.clock = time.Clock()
        self.point_maps = {}
        self.animation = Animation.load("Animations/animacja1")
        self.rendered_surfaces = {}
        self.actual_frame = 0
        self.render()

        while self.is_running:
            self.check_events()
            self.check_keys()
            self.scene()
            self.draw()
            self.display_update()

        self.animation.save("Animations/test3")

    def check_keys(self):
        pass

    def check_events(self):
        for e in event.get():
            if e.type == WINDOWCLOSE:
                self.is_running = False

    def game(self):
        self.actual_frame += self.dt
        if self.actual_frame > self.animation.length:
            self.actual_frame = 0

    def display_update(self):
        self.dt = self.clock.tick(FRAMERATE) * STANDARD_FRAMERATE / 1000
        self.screen.blit(transform.scale(self.draw_screen, SCREEN_SIZE), (0, 0))
        display.update()

    def draw(self):
        self.draw_screen.fill((0, 0, 0))
        self.draw_screen.blit(
            self.animation.get_frame(int(self.actual_frame)),
            (0, 0))

    def render(self):
        for i in range(self.animation.length + 1):
            self.animation.render(i)


if __name__ == "__main__":
    Main()

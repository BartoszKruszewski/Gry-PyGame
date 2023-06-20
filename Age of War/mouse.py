import pygame

class Mouse(pygame.Rect):
    def __init__(self):
        self.height = 1
        self.width = 1
        self.right_click = False
        self.left_click = False
        self.switch = True
        pygame.mouse.set_visible(False)

        self.texture_index = 0

    def update(self,screen_size):

        # pos
        pos = pygame.mouse.get_pos()
        scale = screen_size[0] / 320
        self.center = (pos[0] / scale, pos[1] / scale)

        # buttons
        buttons = pygame.mouse.get_pressed()
        if buttons[0]:
            if self.switch:
                self.left_click = True
                self.texture_index = 1
                self.switch = False
            else:
                self.left_click = False
        else:
            self.switch = True
            self.left_click = False
            self.texture_index = 0

        if buttons[2]:
            self.right_click = True
        else:
            self.right_click = False



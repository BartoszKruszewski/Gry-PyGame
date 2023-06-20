import pygame, os, sys, math,random, ctypes
from CONST import *
from FUNCTIONS import *
from mouse import Mouse
from button import Button
from monster import Monster

class Game():
    def __init__(self):
        # pre init
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.mixer.set_num_channels(5)

        # variables
        self.textures = {}
        self.sounds = {}
        self.music = {}
        self.fonts = {}
        self.delta_time = 0
        self.clock = pygame.time.Clock()
        self.mouse = Mouse()
        self.buttons = []
        self.monsters = []
        self.walls = [False,False,False,False]
        self.lights = [False,False,False]
        self.main_channel = pygame.mixer.Channel(0)

        self.level = 1

        self.is_running = True
        self.is_in_game = True
        self.is_in_menu = True
        self.is_win = False
        self.actual_scene = "menu"
        self.previous_scene = "menu"
        self.button_cooldown = BUTTON_COOLDOWN
        self.camera_glitch_timer = 0
        self.door_timer = [119,119]
        self.mask_on = False
        self.mask_timer = 79
        self.timer = 0
        self.mask_cooldown = 0
        self.mask_on_cooldown = 0
        self.darken_timer = 0
        self.console_timer = 0
        self.menu_timer = random.randint(MENU_ANIMATION_TIMER[0],MENU_ANIMATION_TIMER[1])
        self.can_continue = False
        self.deceive_timer = 0
        self.music_box_timer = MUSIC_BOX_OPEN_TIME
        self.phone_call = 0

        self.main_room_scroll = 0.0
        self.camera_look_at = "reception"

        self.ADD_TIME = pygame.USEREVENT

        self.power_amount = 100
        self.time = 0


        # init
        ctypes.windll.user32.SetProcessDPIAware()
        info = pygame.display.Info()
        self.screen_resolution = (info.current_w, info.current_h)

        if FULLSCREEN:
            self.screen = pygame.display.set_mode(self.screen_resolution, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.screen_resolution)

        pygame.display.set_caption(GAME_CAPTION)
        pygame.display.set_icon(pygame.image.load("icon.png"))

        self.draw_screen = pygame.Surface(GAME_RESOLUTION)

        self.load_assets()
        self.create_buttons()
        self.can_continue = self.load_level()

        # menu
        pygame.mixer.music.load("music/menu.wav")
        pygame.mixer.music.play(-1)
        while self.is_in_menu:
            self.pre_update_program()
            self.update_menu()
            self.late_update_program()
        pygame.mixer.music.fadeout(500)

        # game
        while self.level <= LEVELS:

            self.reset_variables()
            self.actual_scene = "pre_level"
            self.play_pre_level_animation()
            self.actual_scene = "main_room"
            self.run_in_game_events()

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load("music/ambient.wav")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

            while self.is_in_game:
                self.pre_update_program()
                self.update_game()
                self.late_update_program()
            self.stop_in_game_events()

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            if self.is_win:
                self.actual_scene = "level_ending"
                self.play_win_animation()
                self.play_after_night_animation()
                self.level += 1
                self.save_level()
            else:
                self.actual_scene = "jumpscare"
                for monster in self.monsters:
                    if monster.actual_room == "main_room":
                        killer = monster.name
                self.play_jumpscare(killer)

        # game end
        self.actual_scene = "game_ending"
        self.play_game_ending()

    def reset_variables(self):
        self.phone_call = 0
        self.time = 0
        self.power_amount = 100
        self.is_win = False
        self.is_in_game = True
        self.walls[0] = False
        self.walls[1] = False
        self.walls[2] = False
        self.walls[3] = False
        self.door_timer = [119, 119]
        self.lights[0] = False
        self.lights[1] = False
        self.lights[2] = False
        self.mask_on = False
        self.console_timer = 0
        self.main_room_scroll = 90
        self.monsters.clear()

    def save_level(self):
        try:
            file = open("save.txt","w")
            file.write(str(self.level))
            file.close()
        except:
            print("TO SAVE THE GAME RUN THE GAME IN ADMINISTRATOR'S MODE!")

    def load_level(self):
        try:
            file = open("save.txt","r")
            self.level = int(file.readline().rstrip())
            file.close()
            return True
        except:
            return False

    def load_assets(self):
        self.load_textures()
        self.load_sounds()
        self.load_music()
        self.load_fonts()

    def load_fonts(self):
        for file in os.listdir("fonts"):
            for size in FONTS_SIZES:
                font = pygame.font.Font("fonts/" + file,size[1])
                self.fonts[file.replace(".ttf", "") + "_" + size[0]] = font

    def load_textures(self):
        for dir in os.listdir("textures"):
            if dir[-4:] == ".png":
                self.textures[dir.replace(".png", "")] = pygame.image.load("textures/" + dir).convert_alpha()
            else:
                textures = {}
                for file in os.listdir("textures/" + dir):
                    textures[file.replace(".png", "")] = pygame.image.load("textures/" + dir + "/" + file).convert_alpha()
                self.textures[dir] = textures

    def load_sounds(self):
        for dir in os.listdir("sounds"):
            if dir[-4:] == ".wav":
                self.sounds[dir.replace(".wav", "")] = pygame.mixer.Sound("sounds/" + dir)
            else:
                sounds = {}
                for file in os.listdir("sounds/" + dir):
                    sounds[file.replace(".wav", "")] = pygame.mixer.Sound("sounds/" + dir + "/" + file)
                self.sounds[dir] = sounds

    def load_music(self):
        for file in os.listdir("music"):
            self.music[file.replace(".wav", "")] = pygame.mixer.Sound("music/" + file)

    def run_in_game_events(self):
        pygame.time.set_timer(self.ADD_TIME,1000)

    def stop_in_game_events(self):
        pygame.time.set_timer(self.ADD_TIME,0)

    def create_buttons(self):
        for button_template in BUTTONS:
            button = Button(button_template[0],button_template[1],button_template[2],button_template[3])
            self.buttons.append(button)

    def create_monsters(self):
        for monster_template in MONSTERS:
            if monster_template[0] <= self.level:
                monster = Monster(monster_template[1],monster_template[2],monster_template[3],monster_template[0])
                if monster.name != "puppet":
                    monster.active = True
                self.monsters.append(monster)

    def play_jumpscare(self,monster):
        self.sounds["jumpscare"].play()
        size = 1
        org_img = self.textures["jumpscare"][monster].copy()
        timer = 0
        while size < 5:
            timer += self.delta_time
            size += 0.1 * self.delta_time
            surf = pygame.transform.scale(org_img, (int(org_img.get_width() * size), int(org_img.get_height() * size)))
            rect = surf.get_rect(center = (160,90))
            self.draw_screen.fill((0,0,0))
            self.draw_screen.blit(surf,rect)
            self.late_update_program()

        self.sounds["glitch"].play()
        timer = 0
        while timer < 500:
            timer += self.delta_time
            self.draw_screen.fill((0, 0, 0))
            self.draw_screen.blit(self.textures["glitch"]["glitch" + str(int(timer/10) % 5)],(0,0))
            self.late_update_program()
        self.sounds["glitch"].stop()

    def play_win_animation(self):
        self.sounds["win"].play()
        timer = 0
        while timer < 70:
            timer += self.delta_time
            self.draw_screen.fill((0, 0, 0))
            self.draw_screen.blit(self.textures["win_animation"]["win_animation" + str(int(timer / 10))], (0, 0))
            self.late_update_program()
        timer = 0
        while not self.mouse.click:
            timer += self.delta_time
            self.pre_update_program()
            self.draw_screen.fill((0, 0, 0))
            self.draw_screen.blit(self.textures["win_animation"]["win_animation" + str((int(timer / 30) % 12) + 7)], (0, 0))
            self.late_update_program()
        self.sounds["win"].stop()

    def play_pre_level_animation(self):
        caption = "NIGHT " + str(self.level)
        timer = 0
        while timer < 700:
            timer += self.delta_time
            if int(timer) % 10 == 0:
                self.sounds["letter"].play()
            self.draw_screen.fill((0, 0, 0))
            surf = self.fonts["title_big"].render(caption[:int(timer/100)] + chr(int(timer/5) % 26 + 65), False , (255,0,0))
            rect = surf.get_rect(center = (160,90))
            self.draw_screen.blit(surf,rect)
            self.late_update_program()

        surf_org = self.fonts["title_big"].render(caption, False,(255, 0, 0))
        rect = surf_org.get_rect(center=(160, 90))
        self.mouse.update()

        timer = 0
        while not self.mouse.click:
            timer += self.delta_time
            self.pre_update_program()
            self.draw_screen.fill((0, 0, 0))
            if (random.randint(0,20) == 0):
                disort = surf_org.copy()
                disort.scroll(random.randint(-80,80),random.randint(-40,40))
                surf = disort.copy()
            rect.center = ((160 + int(math.sin(random.randint(-1,1) * 3)),90 + int(math.cos(random.randint(-1,1) * 3)) ))
            self.draw_screen.blit(surf, rect)
            self.late_update_program()

        self.darken_timer = 500
        self.sounds["start"].play()
        while self.darken_timer > 250:

            self.pre_update_program()

            timer += self.delta_time
            self.draw_screen.fill((0, 0, 0))
            if (random.randint(0, 20) == 0):
                disort = surf_org.copy()
                disort.scroll(random.randint(-80, 80), random.randint(-40, 40))
                surf = disort.copy()
            rect.center = (
            (160 + int(math.sin(random.randint(-1, 1) * 3)), 90 + int(math.cos(random.randint(-1, 1) * 3))))
            self.draw_screen.blit(surf, rect)

            self.darken_timer -= self.delta_time * 1.5
            opacity = 500 - self.darken_timer
            darken = pygame.Surface((320, 180), flags=pygame.SRCALPHA)
            darken.fill((0, 0, 0, opacity))
            self.draw_screen.blit(darken, (0, 0))

            self.late_update_program()

    def play_after_night_animation(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("music/animation.wav")
        pygame.mixer.music.play(-1)
        length = ANIMATIONS_LENGTH[self.level]
        timer = 0
        while timer < (length - 1) * 40:
            timer += self.delta_time
            self.draw_screen.fill((0, 0, 0))
            self.draw_screen.blit(self.textures["animation_background"],(int(math.sin(random.randint(-1, 1) * 4)), int(math.cos(random.randint(-1, 1) * 4))))
            self.draw_screen.blit(self.textures["night" + str(self.level) + "_animation"]["night" + str(self.level) + "_animation" + str(int(timer / 40))], (0, 0))
            self.draw_screen.blit(self.textures["menu_glitch"]["menu_glitch" + str(int(self.timer / 15) % 11)], (0, 0))
            self.late_update_program()

        pygame.mixer.music.stop()

        self.sounds["glitch"].play()
        timer = 0
        while timer < 500:
            timer += self.delta_time
            self.pre_update_program()
            self.draw_screen.fill((0, 0, 0))
            self.draw_screen.blit(self.textures["glitch"]["glitch" + str(int(timer / 10) % 5)], (0, 0))
            self.late_update_program()
        self.sounds["glitch"].stop()

    def play_game_ending(self):
        for caption in END_CAPTION:
            lines = split_lines(caption, 30)
            line_number = 0
            letter_number = 0
            timer = 0
            while line_number < len(lines) and letter_number < len(lines[line_number]):

                self.pre_update_program()
                rect = pygame.Rect(0, 0, 0, 0)
                self.draw_screen.fill((0, 0, 0))
                for i in range(line_number):

                    surf = self.fonts["terminal_small"].render(lines[i],False, (0, 255, 0))
                    rect = surf.get_rect(topleft=(10, rect.bottom + 10))
                    self.draw_screen.blit(surf, rect)
                if letter_number == len(lines[line_number]) - 1:
                    surf = self.fonts["terminal_small"].render(lines[line_number][:letter_number], False,(0, 255, 0))
                else:
                    surf = self.fonts["terminal_small"].render(lines[line_number][:letter_number] + chr(int(timer) % 26 + 65), False,(0, 255, 0))

                rect = surf.get_rect(topleft=(10, rect.bottom + 10))
                self.draw_screen.blit(surf, rect)
                self.late_update_program()

                timer += self.delta_time
                if int(timer) % 10 == 0:
                    letter_number += 1
                    self.sounds["letter"].play()
                if letter_number == len(lines[line_number]):
                    line_number += 1
                    letter_number = 0

            surf = self.draw_screen.copy()
            self.mouse.update()

            timer = 0
            while not self.mouse.click:
                timer += self.delta_time
                self.pre_update_program()
                self.draw_screen.blit(surf, (0,0))
                self.late_update_program()

        self.darken_timer = 500
        while self.darken_timer > 250:

            self.pre_update_program()

            timer += self.delta_time
            self.draw_screen.blit(surf, (0,0))
            self.darken_timer -= self.delta_time * 1.5
            opacity = 500 - self.darken_timer
            darken = pygame.Surface((320, 180), flags=pygame.SRCALPHA)
            darken.fill((0, 0, 0, opacity))
            self.draw_screen.blit(darken, (0, 0))

            self.late_update_program()

    def update_menu(self):
        self.draw_menu()

    def update_game(self):
        if self.actual_scene == "main_room":
            self.update_scroll()
        else:
            self.main_room_scroll = 0.0
        self.update_monsters()
        self.update_door()
        self.update_mask()
        self.update_console()
        self.update_deceive()
        self.update_sound()
        if self.music_box_timer > 0:
            self.update_music_box()
        elif self.music_box_timer == 0:
            self.music_box_timer = -1
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load("music/music_box.wav")
            pygame.mixer.music.play(-1)
        if self.power_amount == 0:
            self.actual_scene = "main_room"
            self.lights[0] = False
            self.lights[1] = False
            self.walls[0] = False
            self.walls[1] = False
            self.walls[2] = False
            self.walls[3] = False
            self.sounds["power_outage"].play()
            self.power_amount = -1
        elif self.power_amount > 0:
            self.update_power_amount()
        if self.time > 240:
            self.is_win = True
            self.is_in_game = False
        self.draw_game()

    def update_sound(self):
        if self.time == 3 and self.phone_call == 0:
            self.phone_call = 1
            self.main_channel.play(self.sounds["phone_ring"])

        if self.phone_call == 1 and not self.main_channel.get_busy():
            self.phone_call = 2
            self.main_channel.play(self.sounds["telephone"]["telephone" + str(self.level)])

        if self.phone_call == 2 and not self.main_channel.get_busy():
            self.phone_call = 3
            self.create_monsters()

    def update_music_box(self):
        if self.level >= 3 and self.phone_call == 3:
            self.music_box_timer -= self.delta_time
            self.music_box_timer = max(self.music_box_timer,0)
        if self.music_box_timer == 0:
            for monster in self.monsters:
                if monster.name == "puppet":
                    monster.active = True
                    break

    def update_deceive(self):
        self.deceive_timer -= self.delta_time
        self.deceive_timer = max(self.deceive_timer, 0)

    def update_scroll(self):
        if self.mouse.hitbox.x < BORDERS[0]:
            self.main_room_scroll -= self.delta_time
        elif self.mouse.hitbox.x > BORDERS[1]:
            self.main_room_scroll += self.delta_time

        self.main_room_scroll = min(self.main_room_scroll, 180)
        self.main_room_scroll = max(self.main_room_scroll, 0)

    def update_buttons(self):
        for button in self.buttons:
            button.visible = button.scene == self.actual_scene
            if button.name == "music_box" and self.level < 3:
                button.visible = False

            if button.overlaped:
                if not button.sound_played:
                    button.sound_played = True
                    try:
                        self.sounds["buttons"][button.name + "_overlap"].play()
                    except:
                        pass
            else:
                button.sound_played = False

            if button.name == "continue" and not self.can_continue:
                button.visible = False
            if button.name == "music_box" and self.camera_look_at != "closet3":
                button.visible = False
            if button.visible:
                button.update(self.mouse, self.main_room_scroll)
                if (self.power_amount > 0 and self.button_cooldown <= 0) or button.name == "mask_on":
                    if button.clicked:
                        self.execute_button_click(button.name)
                        try:
                            self.sounds["buttons"][button.name + "_click"].play()
                        except:
                            pass
                    elif button.hold:
                        self.execute_button_hold(button.name)
                        try:
                            self.sounds["buttons"][button.name + "_hold"].play()
                        except:
                            pass
                    else:
                        self.execute_button_not_hold(button.name)

    def update_console(self):
        if self.actual_scene == "camera_panel":
            self.console_timer += self.delta_time
        else:
            self.console_timer -= self.delta_time

        self.console_timer = max(self.console_timer,0)
        self.console_timer = min(self.console_timer,89)

    def update_monsters(self):
        other_monsters_rooms = []
        for monster in self.monsters:
            other_monsters_rooms.append((monster.name, monster.actual_room))

        for monster in self.monsters:
            if monster.active:
                monster.update(self.delta_time,self.walls, self.mask_on, other_monsters_rooms, self.deceive_timer > 0)
            if monster.end_timer <= 0:
                self.is_in_game = False

    def execute_button_not_hold(self,name):
        if name[:-1] == "light":
            self.lights[int(name[-1])] = False
        elif name == "camera_light":
            self.lights[2] = False

    def execute_button_hold(self,name):
        if name[:-1] == "light":
            self.lights[int(name[-1])] = True
        elif name == "camera_light":
            self.lights[2] = True
        elif name == "music_box" and self.music_box_timer > 0:
            self.music_box_timer += self.delta_time * MUSIC_BOX_FILL_SPEED

    def execute_button_click(self,name):
        self.button_cooldown = BUTTON_COOLDOWN
        if name == "console":
            self.actual_scene = "camera_panel"
        elif name == "close_console":
            self.actual_scene = "main_room"
        elif name == "corridor1":
            self.camera_look_at = "corridor1"
        elif name == "corridor2":
            self.camera_look_at = "corridor2"
        elif name == "kitchen":
            self.camera_look_at = "kitchen"
        elif name == "party_room":
            self.camera_look_at = "party_room"
        elif name == "closet1":
            self.camera_look_at = "closet1"
        elif name == "closet2":
            self.camera_look_at = "closet2"
        elif name == "closet3":
            self.camera_look_at = "closet3"
        elif name == "reception":
            self.camera_look_at = "reception"
        elif name[:-1] == "wall":
            self.walls[int(name[-1])] = not self.walls[int(name[-1])]
        elif name == "mask_on" and self.mask_cooldown == 0:
            self.mask_on = True
            self.mask_on_cooldown = MASK_MAX_TIME
            self.sounds["mask_on"].play()
        elif name == "new_game":
            self.is_in_menu = False
            self.level = 1
        elif name == "continue":
            self.is_in_menu = False
        elif name == "deceive":
            self.deceive_timer = 10000
            self.power_amount -= 10
            self.power_amount = max(self.power_amount, 0)

    def update_power_amount(self):
        if self.actual_scene != "camera_panel":
            self.lights[2] = False
        if self.actual_scene != "main_room":
            self.lights[0] = False
            self.lights[1] = False

        if self.actual_scene == "camera_panel":
            self.power_amount -= POWER_USE["cameras"] * self.delta_time
        if self.walls[0]:
            self.power_amount -= POWER_USE["room_walls"] * self.delta_time
        if self.walls[1]:
            self.power_amount -= POWER_USE["room_walls"] * self.delta_time
        if self.walls[2]:
            self.power_amount -= POWER_USE["other_walls"] * self.delta_time
        if self.walls[3]:
            self.power_amount -= POWER_USE["other_walls"] * self.delta_time
        if self.lights[0]:
            self.power_amount -= POWER_USE["light"] * self.delta_time
        if self.lights[1]:
            self.power_amount -= POWER_USE["light"] * self.delta_time

        self.power_amount = max(self.power_amount,0)

    def update_door(self):
        # left door
        if self.walls[0]:
            self.door_timer[0] -= self.delta_time
        else:
            self.door_timer[0] += self.delta_time

        self.door_timer[0] = max(self.door_timer[0],0)
        self.door_timer[0] = min (self.door_timer[0],119)

        # right door
        if self.walls[1]:
            self.door_timer[1] -= self.delta_time
        else:
            self.door_timer[1] += self.delta_time

        self.door_timer[1] = max(self.door_timer[1], 0)
        self.door_timer[1] = min(self.door_timer[1], 119)

    def update_mask(self):
        if self.mask_on:
            self.mask_timer -= self.delta_time
        else:
            self.mask_timer += self.delta_time

        self.mask_timer = max(self.mask_timer, 0)
        self.mask_timer = min(self.mask_timer, 79)

        if self.mask_timer == 0:
            if self.mouse.click:
                self.sounds["mask_off"].play()
                self.mask_on = False
                self.mask_cooldown = MASK_COOLDOWN

        self.mask_cooldown -= self.delta_time
        self.mask_cooldown = max(self.mask_cooldown, 0)

        self.mask_on_cooldown -= self.delta_time
        self.mask_on_cooldown = max(self.mask_on_cooldown, 0)

        if self.mask_on_cooldown == 0 and self.mask_on:
            self.mask_on = False
            self.mask_cooldown = MASK_COOLDOWN

        if self.mask_on == False:
            self.mask_on_cooldown = 0

    def draw_game(self):

        if self.actual_scene == "main_room":
            self.draw_corridor()
            self.draw_door()
            self.draw_main_room()
            self.draw_effects()
            self.draw_buttons()
            self.draw_mask()

        self.draw_console()

        if self.actual_scene == "camera_panel":

            if self.console_timer == 89:
                self.draw_camera_panel()
                self.draw_camera_image()
                self.draw_monsters_in_camera()
                self.draw_camera_glitch()
                self.draw_power_amount()

                self.draw_clock()
                self.draw_buttons()
                if self.level >= 3:
                    self.draw_music_box_bar()

    def draw_music_box_bar(self):
        state = int(self.music_box_timer / MUSIC_BOX_OPEN_TIME * 10)
        state = min(state,9)
        state = max(state,0)
        self.draw_screen.blit(self.textures["music_box_bar"]["music_box_bar" + str(state)], (293, 35))

    def draw_effects(self):
        if self.darken_timer == 0:
            for monster in self.monsters:
                if monster.actual_room == "main_room":
                    if monster.end_timer == 1:
                        self.darken_timer = 500
                    break
        self.darken_timer -= self.delta_time * 1.5
        self.darken_timer = max(self.darken_timer,0)

        if self.darken_timer > 0:
            if self.darken_timer > 250:
                opacity = 500 - self.darken_timer
            else:
                opacity = self.darken_timer
            darken = pygame.Surface((320,180),flags=pygame.SRCALPHA)
            darken.fill((0,0,0,opacity))
            self.draw_screen.blit(darken,(0,0))

    def draw_main_room(self):
        self.draw_screen.blit(self.textures["main_room"], (-self.main_room_scroll, 0))
        for monster in self.monsters:
            if monster.actual_room == "main_room":
                self.draw_screen.blit(self.textures[monster.name]["main_room"], (-self.main_room_scroll, int(monster.end_timer)))

    def draw_mask(self):
        self.draw_screen.blit(self.textures["mask_animation"]["mask_animation" + str(int(self.mask_timer / 10))],(int(math.sin(self.timer/100) * 10) - 20,int(math.cos(self.timer/100) * 10) -20))

    def draw_console(self):
        self.draw_screen.blit(self.textures["console_animation"]["console_animation" + str(int(self.console_timer / 10))],(0,0))

    def draw_camera_panel(self):
        self.draw_screen.blit(self.textures["gui"]["camera_panel"], (0, 0))
        if self.walls[0]:
            self.draw_screen.blit(self.textures["gui"]["wall_activate"], (233, 123))
        if self.walls[1]:
            self.draw_screen.blit(self.textures["gui"]["wall_activate"], (265, 123))
        if self.walls[2]:
            self.draw_screen.blit(self.textures["gui"]["wall_activate"], (221, 87))
        if self.walls[3]:
            self.draw_screen.blit(self.textures["gui"]["wall_activate"], (249, 55))

    def draw_buttons(self):
        for button in self.buttons:
            if button.visible:
                name = button.name
                if self.camera_look_at == button.name or (button.name == "camera_light" and self.lights[2]):
                    name += "_selected"
                else:
                    if button.overlaped:
                        name += "_on"
                    else:
                        name += "_normal"
                position = button.hitbox.topleft
                if button.is_moving:
                    position = (position[0] - self.main_room_scroll, position[1])
                self.draw_screen.blit(self.textures["buttons"][name],position)

    def draw_camera_image(self):
        self.draw_screen.blit(self.textures["cameras"][self.camera_look_at], (10, 10))

    def draw_monsters_in_camera(self):
        for monster in self.monsters:
            if monster.actual_room == self.camera_look_at and monster.active:
                self.draw_screen.blit(self.textures[monster.name][monster.actual_room], (10, 10))

    def draw_camera_glitch(self):
        self.camera_glitch_timer += self.delta_time
        if self.camera_glitch_timer > 100:
            self.camera_glitch_timer = 0
        self.draw_screen.blit(self.textures["camera_glitch"]["camera_glitch" + str(int(self.camera_glitch_timer/10))], (10, 10))

    def draw_power_amount(self):
        surf = self.fonts["digital_normal"].render(str(int(self.power_amount)),False,(0,255,0))
        rect = surf.get_rect(topleft=(180,10))
        self.draw_screen.blit(surf,rect)

    def draw_clock(self):
        minutes = str(self.time % 60)
        hours = str(self.time // 60 + 2)
        if len(minutes) == 1:
            minutes = "0" + minutes
        caption = hours + ":" + minutes + " AM"
        surf = self.fonts["digital_normal"].render(caption, False, (255, 255, 255))
        rect = surf.get_rect(topright=(310, 10))
        self.draw_screen.blit(surf, rect)

    def draw_door(self):
        self.draw_screen.blit(self.textures["door_animation"]["door_animation" + str(int(self.door_timer[0] / 10))], (32 - self.main_room_scroll, 0))
        self.draw_screen.blit(pygame.transform.flip(self.textures["door_animation"]["door_animation" + str(int(self.door_timer[1] / 10))],True,False), (411 - self.main_room_scroll, 0))

    def draw_corridor(self):
        self.draw_screen.fill((0,0,0))
        self.draw_screen.blit(self.textures["windows"], (-self.main_room_scroll, 0))

        for monster in self.monsters:
            if monster.actual_room == "corridor1":
                self.draw_screen.blit(self.textures[monster.name]["window1"], (-self.main_room_scroll, 0))
            elif monster.actual_room == "corridor2":
                self.draw_screen.blit(self.textures[monster.name]["window2"], (-self.main_room_scroll, 0))

        if not self.lights[0]:
            self.draw_screen.blit(self.textures["lights1"], (-self.main_room_scroll, 0))
        if not self.lights[1]:
            self.draw_screen.blit(self.textures["lights2"], (-self.main_room_scroll, 0))

    def draw_menu(self):
        self.menu_timer -= self.delta_time
        if self.menu_timer <= 0:
            self.menu_timer = random.randint(MENU_ANIMATION_TIMER[0],MENU_ANIMATION_TIMER[1])

        frame = 0
        if self.menu_timer < 40:
            frame = int(self.menu_timer / 10)
        self.draw_screen.blit(self.textures["menu_animation"]["menu_animation" + str(frame)],(int(math.sin(random.randint(-1,1))),int(math.cos(random.randint(-1,1))) ))

        self.draw_buttons()
        self.draw_screen.blit(self.textures["menu_glitch"]["menu_glitch" + str(int(self.timer/15)%11)],(0,0))

    def pre_update_program(self):
        self.check_events()
        self.mouse.update()
        self.update_buttons()

    def late_update_program(self):
        self.delta_time = self.clock.tick(FRAMERATE) * FRAMERATE / 1000
        print(self.delta_time)
        self.screen.blit(pygame.transform.scale(self.draw_screen, self.screen_resolution), (0, 0))
        pygame.display.update()

        self.button_cooldown -= self.delta_time
        self.button_cooldown = max(self.button_cooldown, 0)

        self.previous_scene = self.actual_scene
        self.timer += self.delta_time


    def check_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.is_running = False

            if event.type == self.ADD_TIME:
                self.time += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.is_running = False

        if not self.is_running:
            pygame.quit()
            sys.exit()
Game()
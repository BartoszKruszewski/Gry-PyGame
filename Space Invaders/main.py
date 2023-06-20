import pygame, os, sys, random
from CONST import *
from enemy import Enemy
from player import Player
from projectile import Projectile


class Game():
    def __init__(self):
        pygame.init()
        self.load_sounds()
        self.load_textures()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.screen_size = (DRAW_SCREEN_SIZE)
        self.draw_screen = pygame.Surface(self.screen_size)
        self.clock = pygame.time.Clock()
        self.dt = 1

        self.click = False

        self.font = pygame.font.Font("Mitochondria.ttf",20)

        self.game()

    def load_sounds(self):
        self.sounds = {}
        for path in os.listdir("sounds"):
            sound = pygame.mixer.Sound("sounds/" + path)
            self.sounds[path.replace(".wav", "")] = sound

    def load_textures(self):
        self.textures = {}
        for path in os.listdir("img"):
            img = pygame.image.load("img/" + path)
            self.textures[path.replace(".png","")] = img

    def game(self):
        self.ENEMYMOVE = pygame.USEREVENT
        pygame.time.set_timer(self.ENEMYMOVE,1000)

        self.enemies = []

        for y in range(3):
            for x in range(int((DRAW_SCREEN_SIZE[0] - 40)/40)):
                self.enemies.append(Enemy(20 + x * 40,10 + y * 20,y + 1))

        self.player = Player()

        self.projectiles = []

        self.scroll = 0

        while True:
            self.check_events()
            self.check_keys()

            for enemy in self.enemies:
                if random.randint(1, ENEMY_SHOT_RATIO) == 1:
                    self.projectiles.append(Projectile(enemy.centerx, enemy.y, 1))
                    self.sounds["shot"].play()
                if enemy.y > 180:
                    self.game_over("loose")

            for projectile in self.projectiles:
                projectile.update(self.dt)
                if projectile.type == 1 and projectile.colliderect(self.player):
                    self.player.hp -= 1
                    self.projectiles.remove(projectile)
                    self.sounds["hit"].play()
                elif projectile.type == 2:
                    for enemy in self.enemies:
                        if projectile.colliderect(enemy):
                            self.projectiles.remove(projectile)
                            self.enemies.remove(enemy)
                            self.sounds["hit"].play()
                            break
                elif projectile.y < 0 or projectile.y > 180:
                    self.projectiles.remove(projectile)

            if len(self.enemies) == 0:
                self.end("win")
            if self.player.hp <= 0:
                self.end("loose")

            self.scroll += self.dt * SCROOL_SPEED
            if self.scroll > 180:
                self.scroll = 0

            self.draw()
            self.refresh_screen()

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.x -= round(self.dt * PLAYER_SPEED)
            self.player.x = max(self.player.x,20)
        if keys[pygame.K_RIGHT]:
            self.player.x += round(self.dt * PLAYER_SPEED)
            self.player.x = min(self.player.x, 300)
        if keys[pygame.K_SPACE] and not self.click:
            self.click = True
            self.sounds["shot"].play()
            self.projectiles.append(Projectile(self.player.centerx ,self.player.y,2))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == pygame.KEYUP:
                self.click = False
            if event.type == self.ENEMYMOVE:
                for enemy in self.enemies:
                    enemy.move()

    def end(self,type):
        timer = END_SCREEN_TIME
        self.draw_screen.blit(self.textures["background"], (0, 0))
        if type == "win":
            text = "Player Wins!"
        else:
            text = "Game Over!"
        surf = self.font.render(text, False, (255, 255, 255))
        rect = surf.get_rect(center=(int(DRAW_SCREEN_SIZE[0]/2),int(DRAW_SCREEN_SIZE[1]/2)))
        self.draw_screen.blit(surf, rect)
        while timer > 0:
            timer -= self.dt
            self.refresh_screen()
        self.close()

    def close(self):
        pygame.quit()
        sys.exit(0)

    def draw(self):
        self.draw_screen.blit(self.textures["background"],(0,-180 + self.scroll))
        self.draw_screen.blit(self.textures["player"],self.player)
        for enemy in self.enemies:
            self.draw_screen.blit(self.textures["enemy" + str(enemy.type)],enemy)
        for projectile in self.projectiles:
            self.draw_screen.blit(self.textures["projectile" + str(projectile.type)], projectile)

    def refresh_screen(self):
        self.screen.blit(pygame.transform.scale(self.draw_screen,SCREEN_SIZE),(0,0))
        pygame.display.update()
        self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000

Game()
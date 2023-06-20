import pygame, random
from particle import Particle
from STATS import *

class Projectile(pygame.Rect):
    def __init__(self,x,direction,type,sound,y=137):
        self.width = 16
        self.height = 16
        self.x = x
        self.real_x = x
        self.real_y = y
        self.y = y
        self.direction = direction
        if type == "stoneman" or type == "axeman":
            self.type = "axe"
        elif type == "archer" or type == "ranger":
            self.type = "arrow"
        elif type == "laserman" or type == "cyborg":
            self.type = "laser"
        elif type == "lvl1" or type == "lvl2":
            self.type = "ball"
            if type == "lvl2":
                self.y = 150
                self.real_y = 150
        elif type == "lvl3":
            self.type = "ammo"
            self.y = 118
            self.real_y = 118
        elif type == "lvl4":
            self.type = "laser_ball"
            self.y = 120
            self.real_y = 120
        else:
            self.type = type

        if type in STATS.keys():
            self.dmg = STATS[type]["dmg"]
        elif type in TOWER.keys():
            self.dmg = TOWER[type]
        else:
            self.dmg = SPECIAL[type]
        self.sound = sound

    def update(self,dt,soldiers,enemy_soldiers,projectiles,particles):
        if self.direction == "right":
            if self.type == "axe":
                self.real_x += dt * 1.5
            elif self.type == "arrow":
                self.real_x += dt * 3
            elif self.type == "laser":
                self.real_x += dt * 5
                self.real_y += dt * 0.2
            elif self.type == "ball":
                self.real_x += dt * 2
            elif self.type == "laser_ball" or self.type == "ammo":
                self.real_x += dt * 5
                self.real_y += dt * 0.2
            elif self.type == "special1":
                self.real_y += dt
                particles.append(Particle(self.centerx - 1, (255, 0, 0),self.y + 4))
                particles.append(Particle(self.centerx - 1, (255, 90, 0), self.y + 3))
                particles.append(Particle(self.centerx - 1, (255, 154, 0), self.y + 2))
                particles.append(Particle(self.centerx - 1, (255, 206, 0), self.y + 1))
                particles.append(Particle(self.centerx - 1, (255, 232, 8), self.y))
            elif self.type == "special2":
                self.real_y += dt
                particles.append(Particle(self.centerx - 1, (255, 0, 0), self.y + 20))
                particles.append(Particle(self.centerx - 1, (255, 90, 0), self.y + 19))
                particles.append(Particle(self.centerx - 1, (255, 154, 0), self.y + 18))
                particles.append(Particle(self.centerx - 1, (255, 206, 0), self.y + 17))
                particles.append(Particle(self.centerx - 1, (255, 232, 8), self.y + 16))
            elif self.type == "special3":
                self.real_y += dt * 2
                particles.append(Particle(self.centerx - 1, (200, 200, 200),self.y ))
                particles.append(Particle(self.centerx - 1, (150, 150, 150), self.y + 1))
                particles.append(Particle(self.centerx - 1, (100, 100, 100), self.y + 2))
                particles.append(Particle(self.centerx - 1, (50, 50, 50), self.y + 3))
                particles.append(Particle(self.centerx - 1, (0, 0, 0), self.y + 4))
            elif self.type == "special4":
                self.real_y += dt * 2
                particles.append(Particle(self.centerx - 1, (54, 110, 184), self.y + 4))
                particles.append(Particle(self.centerx - 1, (41, 141, 203), self.y + 3))
                particles.append(Particle(self.centerx - 1, (72, 193, 202), self.y + 2))
                particles.append(Particle(self.centerx - 1, (255, 255, 255), self.y + 1))

            self.x = round(self.real_x)
            self.y = round(self.real_y)
            if self.type[:-1] == "special":
                if self.y > 180:
                    projectiles.remove(self)
                for soldier in enemy_soldiers:
                    if self.colliderect(soldier):
                        soldier.actual_health -= self.dmg
                        self.sound.play()
                        for i in range(20):
                            particles.append(Particle(enemy_soldiers[0].centerx, (255, 0, 0)))
                        for i in range(10):
                            particles.append(Particle(enemy_soldiers[0].centerx, (100, 100, 100)))
                        projectiles.remove(self)
                        break
            else:
                if len(enemy_soldiers) == 0:
                    projectiles.remove(self)
                elif self.colliderect(enemy_soldiers[0]):
                    enemy_soldiers[0].actual_health -= self.dmg
                    self.sound.play()
                    for i in range(20):
                        particles.append(Particle(enemy_soldiers[0].centerx, (255, 0, 0)))
                    for i in range(10):
                        particles.append(Particle(enemy_soldiers[0].centerx, (100,100,100)))
                    projectiles.remove(self)
        else:
            if self.type == "axe":
                self.real_x -= dt * 1.5
            elif self.type == "arrow":
                self.real_x -= dt * 3
            elif self.type == "laser":
                self.real_x -= dt * 5
                self.real_y -= dt * 0.1
            elif self.type == "ball":
                self.real_x -= dt * 1.5
                self.real_y -= dt * 0.1
            elif self.type == "laser_ball" or self.type == "ammo":
                self.real_x -= dt * 5
                self.real_y -= dt * 0.1

            self.x = round(self.real_x)
            self.y = round(self.real_y)
            if len(soldiers) == 0:
                projectiles.remove(self)
            elif self.colliderect(soldiers[0]):
                soldiers[0].actual_health -= self.dmg
                self.sound.play()
                for i in range(20):
                    particles.append(Particle(soldiers[0].centerx, (255, 0, 0)))
                for i in range(10):
                    particles.append(Particle(soldiers[0].centerx, (100,100,100)))
                projectiles.remove(self)



import pygame, random
from STATS import *
from FUNCTIONS import *
from CONST import *
from particles import Particle

SPEED = 4

class Arrow(pygame.Rect):
    def __init__(self,x,direction,target = None):
        self.width = 26
        self.height = 3
        self.x = x
        self.y = 284
        if direction[:-1] == "tower":
            self.y = 220
        self.real_x = x
        self.real_y = self.y
        self.direction = direction
        self.dmg = STATS["archer"]["dmg"]
        self.angle = 90
        self.target = target

    def update(self,dt,soldiers,enemy_soldiers,projectiles,upgrades,particles,sounds):
        if self.direction == "right":
            if "fire_arrows" in upgrades:
                for i in range(10):
                    particles.append(Particle("fire",self.right,self.bottom +10))
            self.real_x += dt * SPEED
            self.x = round(self.real_x)

            dmg = self.dmg

            if "fire_arrows" in upgrades:
                dmg = int(dmg * UPGRADES["fire_arrows"])
            if "sharpshooters" in upgrades:
                dmg = int(dmg * UPGRADES["sharpshooters"][1])

            if len(enemy_soldiers) > 0 and self.colliderect(enemy_soldiers[0]):
                enemy_soldiers[0].actual_health -= dmg
                random.choice(sounds).play()
                for i in range(30):
                    particles.append(Particle("blood", enemy_soldiers[0].centerx, enemy_soldiers[0].centery))
                projectiles.remove(self)
            elif self.x > BASE_POS[1]:
                projectiles.remove(self)
                random.choice(sounds).play()
                return dmg

        elif self.direction == "left":
            self.real_x -= dt * SPEED
            self.x = round(self.real_x)

            if len(soldiers) > 0 and self.colliderect(soldiers[0]):
                dmg = self.dmg
                if (soldiers[0].type == "knight" or soldiers[0].type == "paladin") and "shields" in upgrades:
                    dmg *= UPGRADES["shields"]
                soldiers[0].actual_health -= dmg
                random.choice(sounds).play()
                for i in range(30):
                    particles.append(Particle("blood", soldiers[0].centerx, soldiers[0].centery))
                projectiles.remove(self)
            elif self.x < BASE_POS[0]:
                projectiles.remove(self)
                random.choice(sounds).play()
                return self.dmg

        elif self.direction[:-1] == "tower":

            self.angle = getAngle(self.target - BASE_POS[0], 327 - 220)
            self.real_x += dt * SPEED * self.angle / 90
            self.x = round(self.real_x)
            self.real_y += dt * SPEED * (90 - self.angle) / 90
            self.y = round(self.real_y)
            if "fire_arrows" in upgrades:
                for i in range(10):
                    particles.append(Particle("fire", self.right, self.bottom + int((90 - self.angle)/2)))

            dmg = self.dmg
            if "fire_arrows" in upgrades:
                dmg = int(self.dmg * UPGRADES["fire_arrows"])

            if len(enemy_soldiers) == 0 or self.y > 350:
                projectiles.remove(self)
            elif self.colliderect(enemy_soldiers[0]):
                enemy_soldiers[0].actual_health -= dmg
                random.choice(sounds).play()
                for i in range(30):
                    particles.append(Particle("blood", enemy_soldiers[0].centerx, enemy_soldiers[0].centery))
                projectiles.remove(self)

        return 0




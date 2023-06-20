import pygame, random
from particle import Particle
from projectile import Projectile
from STATS import *

SPEED = 6

class Soldier(pygame.Rect):
    def __init__(self,type,direction,texture,sounds):

        rect = texture.get_rect()
        self.height = rect.height
        self.width = rect.width
        self.y = 167 - self.height

        self.type = type
        self.actual_frame = 0
        self.actual_animation = "idle"
        self.timer = 0
        self.direction = direction
        self.state = "idle"

        if self.direction == "right":
            self.x = 30
        else:
            self.x = 600

        self.sounds = sounds

        self.lvl = STATS[self.type]["lvl"]
        self.health = STATS[self.type]["hp"]
        self.dmg = STATS[self.type]["dmg"]
        self.speed = STATS[self.type]["speed"]
        self.range = STATS[self.type]["range"]
        self.attack_speed = STATS[self.type]["rate"]

        self.actual_health = self.health

    def update(self,soldiers,enemy_soldiers,dt,particles,projectiles):
        self.timer += dt
        if self.timer >= 70 or (self.state == "walk" and self.timer >= 70 - self.speed) or ((self.state == "attack" or self.state == "attack_base") and self.timer >= 70 - self.attack_speed):

            # update
            self.timer = 0
            if self.actual_frame == 0:
                self.actual_frame = 1
            else:
                self.actual_frame = 0

            if self.direction == "right":

                # check can walk
                can_walk = True
                can_attack = False
                if len(enemy_soldiers) > 0 and enemy_soldiers[0].left < self.right + self.range:
                    can_walk = False
                    can_attack = True
                if can_walk:
                    if self.x >= 610 - self.range - self.width:
                        can_walk = False
                if can_walk:
                    if not soldiers[0] == self:
                        if soldiers[soldiers.index(self) - 1].x - self.x <= self.width:
                            can_walk = False
                if can_walk:
                    self.state = "walk"
                else:
                    # check can attack
                    if can_attack:
                        if self.state != "attack":
                            self.actual_frame = 0
                        self.state = "attack"
                    else:
                        if self.x >= 610 - self.range - self.width:
                            self.state = "attack_base"
                        else:
                            self.state = "idle"

                # set animation and dmg
                if self.state == "walk":
                    self.x += SPEED
                    self.actual_animation = "walk"
                elif self.state == "attack":
                    self.actual_animation = "attack"
                    if self.actual_frame == 1:
                        if self.type == "stoneman" or self.type == "axeman" or self.type == "archer" or self.type == "ranger" or self.type == "laserman" or self.type == "cyborg":
                            projectiles.append(Projectile(self.centerx,self.direction,self.type,self.sounds[1]))
                        else:
                            if self.range > 0:
                                for i in range(10):
                                    particles.append(Particle(enemy_soldiers[0].centerx, (255, 255, 0)))
                            enemy_soldiers[0].actual_health -= self.dmg
                            for i in range(20):
                                particles.append(Particle(enemy_soldiers[0].centerx,(255,0,0)))
                elif self.state == "attack_base" and self.actual_frame == 1:
                    self.actual_animation = "attack"
                    sound = random.choice(self.sounds)
                    sound.play()
                    for i in range(20):
                        particles.append(Particle(620, (100, 100, 100)))
                    return self.dmg
                else:
                    self.actual_animation = "idle"

            else:

                # check can walk
                can_walk = True
                can_attack = False
                if len(soldiers) > 0 and self.left < soldiers[0].right + self.range:
                    can_walk = False
                    can_attack = True
                if can_walk:
                    if self.x <= 30 + self.range:
                        can_walk = False
                if can_walk:
                    if not enemy_soldiers[0] == self:
                        if self.x - enemy_soldiers[enemy_soldiers.index(self) - 1].x <= enemy_soldiers[enemy_soldiers.index(self) - 1].width:
                            can_walk = False
                if can_walk:
                    self.state = "walk"
                else:
                    # check can attack
                    if can_attack:
                        if self.state != "attack":
                            self.actual_frame = 0
                        self.state = "attack"
                    else:
                        if self.x <= 30 + self.range:
                            self.state = "attack_base"
                        else:
                            self.state = "idle"

                # set animation and dmg
                if self.state == "walk":
                    self.x -= SPEED
                    self.actual_animation = "walk"
                elif self.state == "attack":
                    self.actual_animation = "attack"
                    if self.actual_frame == 1:
                        if self.type == "stoneman" or self.type == "axeman" or self.type == "archer" or self.type == "ranger" or self.type == "laserman" or self.type == "cyborg":
                            projectiles.append(Projectile(self.centerx,self.direction,self.type,self.sounds[1]))
                        else:
                            if self.range > 0:
                                for i in range(10):
                                    particles.append(Particle(soldiers[0].centerx, (255, 255, 0)))
                            soldiers[0].actual_health -= self.dmg
                            for i in range(20):
                                particles.append(Particle(soldiers[0].centerx,(255,0,0)))

                elif self.state == "attack_base":
                    self.actual_animation = "attack"
                    if self.actual_frame == 1:
                        sound = random.choice(self.sounds)
                        sound.play()
                        for i in range(20):
                            particles.append(Particle(20,(100,100,100)))
                        return self.dmg
                else:
                    self.actual_animation = "idle"

            if self.actual_animation == "attack" and self.actual_frame == 1:
                if not (self.type == "stoneman" or self.type == "axeman" or self.type == "archer" or self.type == "ranger" or self.type == "laserman" or self.type == "cyborg"):
                    sound = random.choice(self.sounds)
                    sound.play()
                else:
                    self.sounds[0].play()
        return 0

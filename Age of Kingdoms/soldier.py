import pygame, random
from arrow import Arrow
from STATS import *
from CONST import *
from particles import Particle

SPEED = 4
FRAME_TIME = 15

class Soldier(pygame.Rect):
    def __init__(self,type,direction,id,upgrades=[]):

        self.height = SOLDIERS_IMG[type][1]
        self.width = SOLDIERS_IMG[type][0]
        self.y = GROUND_LVL - self.height

        self.type = type
        self.actual_frame = 0
        self.actual_animation = "idle"
        self.timer = 0
        self.direction = direction
        self.state = "idle"
        self.id = id
        self.channel = pygame.mixer.Channel(id)
        self.channel2 = pygame.mixer.Channel(50 + id)

        if self.direction == "right":
            self.x = BASE_POS[0]
        else:
            self.x = BASE_POS[1]

        self.lvl = STATS[self.type]["lvl"]
        self.health = STATS[self.type]["hp"]
        self.dmg = STATS[self.type]["dmg"]
        self.speed = STATS[self.type]["speed"]
        self.range = STATS[self.type]["range"]
        self.attack_speed = STATS[self.type]["rate"]
        self.time = STATS[self.type]["time"]
        self.end = False
        self.special = False


        if self.direction == "right":
            if "learning" in upgrades:
                self.time /= UPGRADES["learning"]
            if "armor" in upgrades:
                self.health = int(self.health * UPGRADES["armor"])
            if "swords" in upgrades:
                self.dmg = int(self.dmg * UPGRADES["swords"])
            if "range" in upgrades:
                self.range = int(self.range * UPGRADES["range"])
            if "fencing" in upgrades and self.type != "archer":
                self.range += UPGRADES["fencing"]
            if self.type == "griffin" and "frenzy" in upgrades:
                self.attack_speed = self.attack_speed + UPGRADES["frenzy"][1]
            if self.type == "griffin" and "frenzy" in upgrades:
                self.speed = self.speed + UPGRADES["frenzy"][0]
            if self.type == "archer" and "sharpshooters" in upgrades:
                self.attack_speed = self.attack_speed + UPGRADES["sharpshooters"][0]
            if self.type == "archer" and "sharpshooters" in upgrades:
                self.dmg = int(self.dmg * UPGRADES["sharpshooters"][1])
            if self.type == "mage" and "lightning" in upgrades:
                self.dmg = int(self.dmg * UPGRADES["lightning"])
            if self.type == "mage" and "lightning" in upgrades:
                self.special = True
            if self.type == "griffin" and "frenzy" in upgrades:
                self.special = True
        self.actual_health = self.health
        self.sound_played = False

    def update(self,soldiers,enemy_soldiers,dt,projectiles,particles,sounds,scrool):
        pos = self.x + scrool
        if pos < 640 and pos > 0:
            volume_left = 1
            volume_right = 1
        elif pos > 640:
            volume_right = 1 - (pos-640)/200
            volume_left = volume_right - 0.5
        else:
            volume_left = 1 + pos/200
            volume_right = volume_left - 0.5

        volume_left = max(0,volume_left)
        volume_right = max(0,volume_right)

        self.channel.set_volume(volume_left,volume_right)
        self.channel2.set_volume(volume_left,volume_right)

        self.timer += dt
        pre_animation = self.actual_animation
        if (self.timer >= FRAME_TIME and self.state != "walk" and self.state != "attack" and self.state != "attack_base") or (self.state == "walk" and self.timer >= FRAME_TIME / self.speed) or ((self.state == "attack" or self.state == "attack_base") and self.timer >= FRAME_TIME / self.attack_speed):
            # update
            self.timer = 0
            if self.actual_frame < SOLDIERS_ANIMATIONS[self.type][self.actual_animation] - 1:
                self.actual_frame += 1
            else:
                self.actual_frame = 0

            if self.actual_health <= 0:
                self.state = "dead"
                self.actual_animation = "dead"
                if self.actual_frame == SOLDIERS_ANIMATIONS[self.type]["dead"] -1:
                    self.end = True
            else:

                if self.direction == "right":
                    # check can walk
                    can_walk = True
                    can_attack = False
                    if (soldiers[0] == self or self.type == "archer") and len(enemy_soldiers) > 0 and enemy_soldiers[0].left < self.right + self.range - SOLDIERS_OFFSET[enemy_soldiers[0].type][1]:
                        can_walk = False
                        can_attack = True
                    if can_walk:
                        if self.x >= BASE_POS[1] - self.range - self.width and len(enemy_soldiers) == 0:
                            can_walk = False
                    if can_walk:
                        if not soldiers[0] == self:
                            if soldiers[soldiers.index(self) - 1].x - self.x <= self.width - SOLDIERS_OFFSET[soldiers[soldiers.index(self) - 1].type][1] - SOLDIERS_OFFSET[self.type][0]:
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
                            if self.x >= BASE_POS[1] - self.range - self.width and len(enemy_soldiers) == 0:
                                self.state = "attack_base"
                            else:
                                self.state = "idle"

                    # set animation and dmg
                    if self.state == "walk":
                        self.x += SPEED
                        if self.type == "griffin" and self.special:
                            self.x += SPEED
                        self.actual_animation = "walk"
                        if self.actual_frame in SOLDIERS_SHOT_FRAMES[self.type]["walk"]:
                            self.channel.play(random.choice(sounds[self.type]["walk"]))
                    elif self.state == "attack":
                        self.actual_animation = "attack"
                        if self.actual_frame == SOLDIERS_SHOT_FRAMES[self.type]["attack"]:
                            if self.type == "archer":
                                projectiles.append(Arrow(self.x, "right"))
                                self.channel.play(random.choice(sounds[self.type]["shot"]))
                            else:
                                enemy_soldiers[0].actual_health -= self.dmg
                                self.channel.play(random.choice(sounds[self.type]["attack"]))
                                self.channel2.play(random.choice(sounds[enemy_soldiers[0].type]["block"]))
                                for i in range(30):
                                    particles.append(Particle("blood", enemy_soldiers[0].centerx , enemy_soldiers[0].centery))
                                if self.type == "mage":
                                    for i in range(30):
                                        particles.append(Particle("lightning", enemy_soldiers[0].centerx, enemy_soldiers[0].centery))
                                    if self.special and len(enemy_soldiers) > 1:
                                        if enemy_soldiers[1].left < self.right + self.range - SOLDIERS_OFFSET[enemy_soldiers[0].type][1] + enemy_soldiers[1].w + 30:
                                            enemy_soldiers[1].actual_health -= self.dmg
                                            for i in range(30):
                                                particles.append(Particle("blood", enemy_soldiers[1].centerx, enemy_soldiers[1].centery))
                                            for i in range(30):
                                                particles.append(Particle("lightning", enemy_soldiers[1].centerx, enemy_soldiers[1].centery))
                    elif self.state == "attack_base":
                        self.actual_animation = "attack"
                        if self.actual_frame == SOLDIERS_SHOT_FRAMES[self.type]["attack"]:
                            if self.type == "archer":
                                self.channel.play(random.choice(sounds[self.type]["shot"]))
                                projectiles.append(Arrow(self.x, "right"))
                            else:
                                self.channel.play(random.choice(sounds[self.type]["attack"]))
                                return self.dmg
                    else:
                        self.actual_animation = "idle"
                else:

                    # check can walk
                    can_walk = True
                    can_attack = False
                    if (enemy_soldiers[0] == self or self.type == "archer") and len(soldiers) > 0 and self.left < soldiers[0].right + self.range - SOLDIERS_OFFSET[soldiers[0].type][1]:
                        can_walk = False
                        can_attack = True
                    if can_walk:
                        if self.x <= BASE_POS[0] + self.range + 60 and len(soldiers) == 0:
                            can_walk = False
                    if can_walk:
                        if not enemy_soldiers[0] == self:
                            if self.x - enemy_soldiers[enemy_soldiers.index(self) - 1].x <= enemy_soldiers[enemy_soldiers.index(self) - 1].width - SOLDIERS_OFFSET[enemy_soldiers[enemy_soldiers.index(self) - 1].type][1] - SOLDIERS_OFFSET[self.type][0]:
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
                            if self.x <= BASE_POS[0] + self.range + 60 and len(soldiers) == 0:
                                self.state = "attack_base"
                            else:
                                self.state = "idle"

                    # set animation and dmg
                    if self.state == "walk":
                        self.x -= SPEED
                        self.actual_animation = "walk"
                        if self.actual_frame in SOLDIERS_SHOT_FRAMES[self.type]["walk"]:
                            self.channel.play(random.choice(sounds[self.type]["walk"]))
                    elif self.state == "attack":
                        self.actual_animation = "attack"
                        if self.actual_frame == SOLDIERS_SHOT_FRAMES[self.type]["attack"]:
                            if self.type == "archer":
                                projectiles.append(Arrow(self.x, "left"))
                                self.channel.play(random.choice(sounds[self.type]["shot"]))
                            else:
                                soldiers[0].actual_health -= self.dmg
                                self.channel.play(random.choice(sounds[self.type]["attack"]))
                                self.channel2.play(random.choice(sounds[soldiers[0].type]["block"]))
                                for i in range(30):
                                    particles.append(Particle("blood", soldiers[0].centerx , soldiers[0].centery))
                                if self.type == "mage":
                                    for i in range(30):
                                        particles.append(Particle("lightning", soldiers[0].centerx, soldiers[0].centery))

                    elif self.state == "attack_base":
                        self.actual_animation = "attack"
                        if self.actual_frame == SOLDIERS_SHOT_FRAMES[self.type]["attack"]:
                            if self.type == "archer":
                                self.channel.play(random.choice(sounds[self.type]["shot"]))
                                projectiles.append(Arrow(self.x, "left"))
                            else:
                                self.channel.play(random.choice(sounds[self.type]["attack"]))
                                return self.dmg
                    else:
                        self.actual_animation = "idle"

        if pre_animation != self.actual_animation:
            self.actual_frame = 0


        return 0

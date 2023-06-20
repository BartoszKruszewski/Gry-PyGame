from CONST import SCALE, MAP_SIZE, TROOP_TIMER, HITBOX_MARGIN, COLLECTING_GOLD_TIME, TROOPS_STATS, DANGER_TIME, UPGRADES
from game_object import GameObject

class Troop(GameObject):
    def __init__(self,pos,id,type,side):
        super().__init__(pos,id,type,"troop",side)
        self.direction = "up"
        self.flow_map_id = 0
        self.speed = 0.5
        self.state = "idle"
        self.timer = 0
        self.animation = "move"
        self.frame = 0
        self.target_reached = False
        self.dead_timer = 0

        self.stats = {}
        for stat in TROOPS_STATS[type].keys():
            self.stats[stat] = TROOPS_STATS[type][stat]

        self.focused_object = None
        self.focused_object_previous_pos = None
        self.danger_timer = 0
        self.chopped_tree = 0
        self.collected_gold = 0
        self.collecting_gold_timer = COLLECTING_GOLD_TIME
        self.visible = True
        self.actual_health = self.stats["health"]
        self.last_healtth = self.actual_health

    def update(self,dt,updates):
        if self.state != "idle":
            self.timer += dt
            if self.timer >= TROOP_TIMER:
                self.timer = 0
                self.frame += 1
                if self.frame >= 5:
                    self.frame = 0
        if self.actual_health <= 0:
            self.dead_timer += dt

        self.danger_timer -= dt
        self.danger_timer = max(self.danger_timer,0)

        if self.last_healtth > self.actual_health:
            self.danger_timer = DANGER_TIME
        self.last_healtth = self.actual_health

        self.update_upgrades(updates)

    def update_upgrades(self,updates):
        for update in updates:
            if self.type in UPGRADES[update][1]:
                self.stats[UPGRADES[update][0]] = TROOPS_STATS[self.type][UPGRADES[update][0]] + UPGRADES[update][2]

    def update_position(self,dt,colliders):
        def get_move_vector():
            move = [0,0]
            if self.direction == "up":
                move[1] = -1
            elif self.direction == "down":
                move[1] = 1
            elif self.direction == "right":
                move[0] = 1
            elif self.direction == "left":
                move[0] = -1
            return move

        move = get_move_vector()

        cast_box = self.hitbox.copy()
        cast_box.x += move[0] * self.speed * dt
        cast_box.y += move[1] * self.speed * dt

        can_move = True
        for collider in colliders:
            if cast_box.colliderect(collider):
                if self.direction == "up":
                    if collider.y < self.global_pos[1]:
                        can_move = False
                elif self.direction == "down":
                    if collider.y > self.global_pos[1]:
                        can_move = False
                elif self.direction == "left":
                    if collider.x < self.global_pos[0]:
                        can_move = False
                elif self.direction == "right":
                    if collider.x > self.global_pos[0]:
                        can_move = False
                if not can_move:
                    break

        if can_move:
            self.global_pos[0] += move[0] * self.speed * dt
            self.global_pos[1] += move[1] * self.speed * dt

            self.global_pos[0] = max(self.global_pos[0],0)
            self.global_pos[0] = min(self.global_pos[0],MAP_SIZE[0] * SCALE)
            self.global_pos[1] = max(self.global_pos[1], 0)
            self.global_pos[1] = min(self.global_pos[1], MAP_SIZE[1] * SCALE)

            self.hitbox.x = self.global_pos[0] + HITBOX_MARGIN + SCALE/2
            self.hitbox.y = self.global_pos[1] + HITBOX_MARGIN + SCALE/2
            self.clickbox.x = self.global_pos[0]
            self.clickbox.y = self.global_pos[1]

            self.pos[0] = int(self.global_pos[0] / SCALE) + 1
            self.pos[1] = int(self.global_pos[1] / SCALE) + 1

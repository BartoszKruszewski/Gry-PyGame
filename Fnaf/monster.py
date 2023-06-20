import random
from CONST import ROOMS_MAP, ROOM_PRIORITY, FAKE_ROOM_PRIORITY, MONSTER_WALK_SPEED, MONSTER_START_COOLDOWN, MONSTER_ATTACK_COOLDOWN

class Monster():
    def __init__(self,name,walk_type,start_room,level):
        self.name = name
        self.walk_type = walk_type
        self.actual_room = start_room
        self.level = level
        self.timer = MONSTER_START_COOLDOWN
        self.end_timer = MONSTER_ATTACK_COOLDOWN
        self.wait_timer = MONSTER_ATTACK_COOLDOWN
        self.active = False

    def move(self,walls,other_monsters_rooms,deceive):
        busy_rooms = []
        for room in other_monsters_rooms:
            if not room[0] == self.name:
                busy_rooms.append(room[1])

        avalible_rooms = []
        for room in ROOMS_MAP[self.actual_room]:
            if room[1] == "normal" or (room[1] == "vents" and self.walk_type == "all"):
                avalible_rooms.append(room[0])
            elif room[1][:-1] == "wall":
                if not walls[int(room[1][-1])]:
                    avalible_rooms.append(room[0])

        empty_choice = []
        for room in avalible_rooms:
            if room not in busy_rooms:
                empty_choice.append(room)

        if len(empty_choice) == 0:
            empty_choice = avalible_rooms.copy()

        best_choice = []
        highest_priority = 0
        if deceive and (self.name == "chica" or self.name == "mangle" or self.name == "ennard"):
            priority = FAKE_ROOM_PRIORITY
        else:
            priority = ROOM_PRIORITY[self.name]

        for room in empty_choice:
            if priority[room] == highest_priority:
                best_choice.append(room)
            elif priority[room] > highest_priority:
                best_choice.clear()
                highest_priority = priority[room]
                best_choice.append(room)

        self.actual_room = random.choice(best_choice)

    def update(self, delta_time,walls,mask_on,other_monsters_rooms, deceive):
        if self.actual_room != "main_room":
            self.timer -= delta_time
            if self.timer <= 0:
                self.timer = random.randint(MONSTER_WALK_SPEED[0],MONSTER_WALK_SPEED[1])
                self.move(walls,other_monsters_rooms, deceive)
        else:
            self.end_timer -= delta_time
            if mask_on:
                self.end_timer = max(self.end_timer,1)
            if self.end_timer == 1:
                self.wait_timer -= delta_time
                if self.wait_timer <= 0:
                    self.wait_timer = MONSTER_ATTACK_COOLDOWN
                    self.end_timer = MONSTER_ATTACK_COOLDOWN
                    self.move(walls,other_monsters_rooms, deceive)
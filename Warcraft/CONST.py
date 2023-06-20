SCALE = 16
MAP_SIZE = (32,32)
SCROLL_SPEED = 3
BUTTONS_SCROLLING_SPEED = 10
SCREEN_RESOLUTION = (1280,720)
GAME_RESOLUTION = (320,180)
CLICK_COOLDOWN = 30

FONTS = {
    "pixel":[8,32]
}
TROOPS_ANIMATIONS = {
    "swordsman":["move","attack"],
    "archer":["move",],
    "catapult":["attack","move"],
    "peasant":["move","wood","gold","use"],
    "knight":["move","attack"],
}

MINIMAP_COLORS = {
    "grass0":((16,52,8)),
    "grass1":((24,56,8)),
    "grass2":((36,64,4)),
    "path":((84,40,20)),
    "tree":((8,32,8)),
    "water":((36,52,128)),
}

BUILDING_TILES = {
    "townhall":9,
    "barrack":9,
    "farm":4,
    "lumbermill":9,
    "stables":9,
    "tower":4,
    "blacksmith":4,
    "goldmine":9
}

TROOPS_STATS = {
    "peasant":{"damage":1,"health":5,"speed":0.3,"armor":1,"penetration":1},
    "swordsman":{"damage":1,"health":10,"speed":0.3,"armor":1,"penetration":1},
    "archer":{"damage":1,"health":1,"speed":1,"armor":1,"penetration":1},
    "catapult":{"damage":1,"health":1,"speed":1,"armor":1,"penetration":1},
    "knight":{"damage":1,"health":1,"speed":1,"armor":1,"penetration":1},
}

BUILDING_STATS = {
    "townhall":{"health":100},
    "goldmine":{"health":1000},
    "farm":{"health":1000},
    "barrack":{"health":1000},
    "lumbermill":{"health":1000},
    "blacksmith":{"health":1000},
    "tower":{"health":1000},
    "stables":{"health":1000}
}

PRICES = {
    "peasant":(40,40),
    "swordsman":(40,40),
    "archer":(40,40),
    "catapult":(40,40),
    "knight":(40,40),
    "farm":(40,40),
    "barrack":(40,40),
    "lumbermill":(40,40),
    "blacksmith":(40,40),
    "stables":(40,40),
    "tower":(40,40),
    "armor1":(40,40),
    "armor2":(40,40),
    "armor3":(40,40),
    "bows1":(40,40),
    "bows2":(40,40),
    "bows3":(40,40),
    "fireballs":(40,40),
    "horses1":(40,40),
    "horses2":(40,40),
    "swords1":(40,40),
    "swords2":(40,40),
    "swords3":(40,40)
}

TROOP_FRAME_SIZE = (32,32)
TROOP_TIMER = 5
HITBOX_MARGIN = 5
CHUNK_SIZE = 4
COLLECTING_GOLD_TIME = 100
DEAD_VISIBLE_TIME = 300
DANGER_TIME = 200
FARM_CAPACITY = 4
WALK_POINT_TIME = 31

BUTTONS_VISIBLE = {
    "armor2":"armor1",
    "armor3":"armor2",
    "swords2":"swords1",
    "swords3":"swords2",
    "bows2":"bows1",
    "bows3":"bows2",
    "horses2":"horses1"
}

BUTTONS_BLOCKED = {
    "lumbermill":"barrack",
    "blacksmith":"lumbermill",
    "tower":"blacksmith",
    "stables":"blacksmith",
    "archer":"lumbermill",
    "catapult":"blacksmith",
    "knight":"stables"
}

UPGRADES = {
    "swords1":("damage",["knight","swordsman"],1),
    "swords2":("damage",["knight","swordsman"],2),
    "swords3":("damage",["knight","swordsman"],3),
    "bows1":("damage",["archer"],1),
    "bows2":("damage",["archer"],2),
    "bows3":("damage",["archer"],3),
    "horses1":("speed",["knight"],1),
    "horses2":("speed",["knight"],2),
    "armor1":("health",["knight","swordsman"],1),
    "armor2":("health",["knight","swordsman"],2),
    "armor3":("health",["knight","swordsman"],3),
    "fireballs":("damage",["catapult"],1)
}

REPAIRING_SPEED = 0.5
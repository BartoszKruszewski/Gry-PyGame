STATS = {}

KNIGHT = {}
KNIGHT["dmg"] = 20
KNIGHT["hp"] = 120
KNIGHT["speed"] = 1.2
KNIGHT["rate"] = 0.7
KNIGHT["range"] = 0
KNIGHT["time"] = 300
KNIGHT["lvl"] = 1

ARCHER = {}
ARCHER["dmg"] = 25
ARCHER["hp"] = 80
ARCHER["speed"] = 1.2
ARCHER["rate"] = 1.2
ARCHER["range"] = 170
ARCHER["time"] = 500
ARCHER["lvl"] = 2

PALADIN = {}
PALADIN["dmg"] = 60
PALADIN["hp"] = 500
PALADIN["speed"] = 1
PALADIN["rate"] = 1
PALADIN["range"] = 0
PALADIN["time"] = 800
PALADIN["lvl"] = 3

MAGE = {}
MAGE["dmg"] = 120
MAGE["hp"] = 250
MAGE["speed"] = 1.1
MAGE["rate"] = 0.8
MAGE["range"] = 10
MAGE["time"] = 1100
MAGE["lvl"] = 4

GRIFFIN = {}
GRIFFIN["dmg"] = 50
GRIFFIN["hp"] = 1000
GRIFFIN["speed"] = 1.4
GRIFFIN["rate"] = 1.3
GRIFFIN["range"] = 0
GRIFFIN["time"] = 1500
GRIFFIN["lvl"] = 5

STATS["knight"] = KNIGHT
STATS["archer"] = ARCHER
STATS["paladin"] = PALADIN
STATS["mage"] = MAGE
STATS["griffin"] = GRIFFIN

PRICES = {}

PRICES["knight"] = (80,0)
PRICES["archer"] = (180,30)
PRICES["paladin"] = (300,50)
PRICES["mage"] = (300,80)
PRICES["griffin"] = (700,250)
PRICES["archery"] = (0,200)
PRICES["blacksmith"] = (0,400)
PRICES["mage_tower"] = (0,600)
PRICES["griffin_rampart"] = (0,1500)
PRICES["plows"] = (120,120)
PRICES["flock"] = (250,250)
PRICES["cattle"] = (500,500)
PRICES["granary"] = (750,750)
PRICES["windmill"] = (1200,1200)
PRICES["range"] = (150,300)
PRICES["fire_arrows"] = (150,300)
PRICES["sharpshooters"] = (250,500)
PRICES["swords"] = (150,300)
PRICES["armor"] = (200,400)
PRICES["shields"] = (200,400)
PRICES["fencing"] = (150,300)
PRICES["lightning"] = (250,500)
PRICES["frenzy"] = (500,1000)
PRICES["tower1"] = (0,250)
PRICES["tower2"] = (0,500)
PRICES["tower3"] = (0,1000)
PRICES["tools"] = (100,200)
PRICES["learning"] = (150,300)
PRICES["fortifications"] = (200,400)
PRICES["finances"] = (400,800)

ENEMY_SPAWN = (
    (20,0,0,0,0),
    (17,3,0,0,0),
    (14,4,2,0,0),
    (10,5,3,2,0),
    (5,5,5,3,2)
)

ENEMY_SPAWN_RATE = (
    (6000,8000),
    (5000,6500),
    (4500,6000),
    (4000,5500),
    (3500,5000)
)

PHASE_CHANGE_TIME = (80000,110000,150000,160000)

START_SPAWN_DELAY = 18000

BASE_HP = 1000
FOOD_ADD = 10
START_GOLD = 0
START_FOOD = 0

UPGRADES = {}
UPGRADES["armor"] = 1.2
UPGRADES["swords"] = 1.2
UPGRADES["range"] = 1.3
UPGRADES["fire_arrows"] = 1.3
UPGRADES["lightning"] = 1.2
UPGRADES["frenzy"] = (0.7,1.2)
UPGRADES["sharpshooters"] = (-0.3,2.2)
UPGRADES["shields"] = 0.8
UPGRADES["fencing"] = 30
UPGRADES["plows"] = 5
UPGRADES["flock"] = 5
UPGRADES["cattle"] = 5
UPGRADES["granary"] = 5
UPGRADES["windmill"] = 5
UPGRADES["tools"] = 1.5
UPGRADES["learning"] = 2
UPGRADES["fortifications"] = 500
UPGRADES["finances"] = 1.5


GOLD_DROP_MULT = 0.3

TOWER_RANGE = (200,200,250)
TOWER_DMG = (25,35,70)
TOWER_ATTACK_SPEED = (250,250,200)

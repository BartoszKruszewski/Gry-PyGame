from STATS import *

SOLDIERS_IMG = {}
SOLDIERS_IMG["knight"] = (85,50)
SOLDIERS_IMG["paladin"] = (153,133)
SOLDIERS_IMG["archer"] = (54,55)
SOLDIERS_IMG["griffin"] = (133,115)
SOLDIERS_IMG["mage"] = (80,63)

SOLDIERS_ANIMATIONS = {}
SOLDIERS_ANIMATIONS["knight"] = {"idle":8,"walk":10,"dead":10,"attack":7}
SOLDIERS_ANIMATIONS["paladin"] = {"idle":4,"walk":11,"dead":10,"attack":15}
SOLDIERS_ANIMATIONS["archer"] = {"idle":7,"walk":10,"dead":11,"attack":16}
SOLDIERS_ANIMATIONS["griffin"] = {"idle":11,"walk":7,"dead":11,"attack":13}
SOLDIERS_ANIMATIONS["mage"] = {"idle":5,"walk":10,"dead":12,"attack":13}

SOLDIERS_OFFSET = {}
SOLDIERS_OFFSET["knight"] = (6,35)
SOLDIERS_OFFSET["archer"] = (2,14)
SOLDIERS_OFFSET["paladin"] = (27,57)
SOLDIERS_OFFSET["mage"] = (6,38)
SOLDIERS_OFFSET["griffin"] = (16,28)

SOLDIERS_SHOT_FRAMES = {}
SOLDIERS_SHOT_FRAMES["knight"] = {"walk":(4,9),"dead":7,"attack":2}
SOLDIERS_SHOT_FRAMES["archer"] = {"walk":(5,9),"dead":9,"attack":10}
SOLDIERS_SHOT_FRAMES["paladin"] = {"walk":(2,6),"dead":5,"attack":8}
SOLDIERS_SHOT_FRAMES["mage"] = {"walk":(5,0),"dead":9,"attack":4}
SOLDIERS_SHOT_FRAMES["griffin"] = {"walk":(1,4),"dead":7,"attack":7}

BASE_POS = (460,1160)

BUILDING_POS = {}
BUILDING_POS["farm"] = (105,240)
BUILDING_POS["town_hall"] = (0,187)
BUILDING_POS["archery"] = (210,213)
BUILDING_POS["blacksmith"] = (255,249)
BUILDING_POS["griffin_rampart"] = (65,52)
BUILDING_POS["mage_tower"] = (255,74)
BUILDING_POS["base"] = (440,193)
BUILDING_POS["guild"] = (329,189)

BUILDING_ORDER = ["griffin_rampart","town_hall","farm","mage_tower","archery","blacksmith","guild","base"]

PARTILCES = {}
PARTILCES["fire"] = ((1,2),(1,1),(0,0),1,[(86,1,11),(255,70,5),(255,215,41),(248,164,47),(250,121,0),(231,30,2)],(0,0),(False,False)) #size, random, moving, time, colors, acceleration, random direction
PARTILCES["blood"] = ((1,2),(10,10),(0.5,0.5),0.4,[(166,21,8)],(0.005,-0.005),(True,False))
PARTILCES["lightning"] = ((1,2),(10,10),(0.5,0.5),0.4,[(253,255,255),(0,255,240)],(0.005,-0.005),(True,True))

FRAMERATE = 144

INFO_BUTTON = {}
INFO_BUTTON["knight"] = "Basic infantry unit"
INFO_BUTTON["archer"] = "Shooting unit"
INFO_BUTTON["paladin"] = "Heavy unit"
INFO_BUTTON["mage"] = "Great damage unit"
INFO_BUTTON["griffin"] = "Powerfull unit"
INFO_BUTTON["archery"] = "Unlocks archers and updates"
INFO_BUTTON["blacksmith"] = "Unlocks Paladins and updates"
INFO_BUTTON["mage_tower"] = "Unlocks Mages"
INFO_BUTTON["griffin_rampart"] = "Unlocks Griffins"
INFO_BUTTON["tower1"] = "Builds a basic tower"
INFO_BUTTON["tower2"] = "Builds a double tower"
INFO_BUTTON["tower3"] = "Upgrades towers"
INFO_BUTTON["swords"] = "Increses hand-to-hand damage"
INFO_BUTTON["armor"] = "Increses health"
INFO_BUTTON["fencing"] = "Increses hand-to-hand attack range"
INFO_BUTTON["shields"] = "Protects knights and paladin from arrows"
INFO_BUTTON["fire_arrows"] = "Increses arrows damage"
INFO_BUTTON["range"] = "Increases archers and towers range"
INFO_BUTTON["sharpshooters"] = "Makes archers shooting slower but with more damage"
INFO_BUTTON["lightning"] = "Let mages attack 2 units being close to each other"
INFO_BUTTON["frenzy"] = "Increses griffin speed and attack speed"
INFO_BUTTON["flock"] = "Gives you " + str(UPGRADES["flock"]) + " food per second"
INFO_BUTTON["cattle"] = "Gives you " + str(UPGRADES["cattle"]) + " food per second"
INFO_BUTTON["plows"] = "Gives you " + str(UPGRADES["plows"]) + " food per second"
INFO_BUTTON["windmill"] = "Gives you " + str(UPGRADES["windmill"]) + " food per second"
INFO_BUTTON["granary"] = "Gives you " + str(UPGRADES["granary"]) + " food per second"
INFO_BUTTON["tools"] = "Repairs your base over time"
INFO_BUTTON["learning"] = "Speeds up training process"
INFO_BUTTON["fortifications"] = "Increses base resistance"
INFO_BUTTON["burials"] = "Gives you some gold from your dead troops"
INFO_BUTTON["finances"] = "Increses gold amount you get from dead enemies"

INFO_BUILDING = {}
INFO_BUILDING["base"] = "Here you can train more troops"
INFO_BUILDING["town_hall"] = "Here you can build more buildings"
INFO_BUILDING["farm"] = "Here you can upgrade your food production"
INFO_BUILDING["archery"] = "Here you can upgrade your archers and towers"
INFO_BUILDING["blacksmith"] = "Here you can upgrade your troops"
INFO_BUILDING["mage_tower"] = "Here you can upgrade your mages"
INFO_BUILDING["griffin_rampart"] = "Here you can upgrade your griffins"
INFO_BUILDING["guild"] = "Here you can buy special upgrades"

INFO_POS = (537,64,537,80,13)

BASE_BAR_SIZE = (42,6)
HEALTH_BAR_SIZE = (22,6)

GROUND_LVL = 327

COLORS = {"knight":[((44,62,95),(25,25,25)),((150, 41, 3), (65, 65, 65)),((103, 29, 5), (100, 100, 100))],
        "archer":[((28, 67, 96), (65, 65, 65)),((14, 52, 86), (100, 100, 100))],
        "paladin":[((24,8,61),(25,25,25)),((29, 48, 137), (65, 65, 65)),((33, 83, 170), (100, 100, 100))],
        "mage":[((24,8,61),(25,25,25)),((4, 38, 86), (65, 65, 65)),((0, 67, 123), (100, 100, 100))]
          }
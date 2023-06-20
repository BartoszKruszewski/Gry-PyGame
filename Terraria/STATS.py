CHUNK_SIZE = 8
TEXTURE_RESOLUTION = 16
GRAVITY = 0.04
AIR_RESISTANCE = 0.9
FRAMERATE = 144
DYNAMIC_TREES = True

MOBS = {}

WRAITH = {}
WRAITH["width"] = 32
WRAITH["height"] = 32
WRAITH["attitude"] = ["monster"]
WRAITH["health"] = 10
WRAITH["shift"] = 0
WRAITH["max_speed"] = 0.2
WRAITH["drop"] = "fur"
WRAITH["biom"] = "swamp"
WRAITH["exp"] = 3

WOLF = {}
WOLF["width"] = 32
WOLF["height"] = 14
WOLF["attitude"] = ["neutral","neutral","neutral","agressive"]
WOLF["health"] = 5
WOLF["shift"] = 16
WOLF["max_speed"] = 0.45
WOLF["drop"] = "fur"
WOLF["biom"] = "woodland"
WOLF["exp"] = 2

BEAR = {}
BEAR["width"] = 32
BEAR["height"] = 23
BEAR["attitude"] = ["neutral","neutral","neutral","agressive"]
BEAR["health"] = 7
BEAR["shift"] = 9
BEAR["max_speed"] = 0.3
BEAR["drop"] = "fur"
BEAR["biom"] = "snow_land"
BEAR["exp"] = 2

POLAR_BEAR = {}
POLAR_BEAR["width"] = 32
POLAR_BEAR["height"] = 23
POLAR_BEAR["attitude"] = ["neutral","neutral","neutral","agressive"]
POLAR_BEAR["health"] = 7
POLAR_BEAR["shift"] = 9
POLAR_BEAR["max_speed"] = 0.3
POLAR_BEAR["drop"] = "fur"
POLAR_BEAR["biom"] = "mountains"
POLAR_BEAR["exp"] = 2

SNOW_WOLF = {}
SNOW_WOLF["width"] = 32
SNOW_WOLF["height"] = 14
SNOW_WOLF["attitude"] = ["neutral","neutral","neutral","agressive"]
SNOW_WOLF["health"] = 5
SNOW_WOLF["shift"] = 16
SNOW_WOLF["max_speed"] = 0.45
SNOW_WOLF["drop"] = "fur"
SNOW_WOLF["biom"] = "snow_hills"
SNOW_WOLF["exp"] = 2

COW = {}
COW["width"] = 32
COW["height"] = 16
COW["attitude"] = ["passive"]
COW["health"] = 5
COW["shift"] = 0
COW["max_speed"] = 0.2
COW["drop"] = "beef"
COW["biom"] = "grass_hills"
COW["exp"] = 1

CROCODILE = {}
CROCODILE["width"] = 32
CROCODILE["height"] = 13
CROCODILE["attitude"] = ["neutral","neutral","neutral","agressive"]
CROCODILE["health"] = 8
CROCODILE["shift"] = 19
CROCODILE["max_speed"] = 0.1
CROCODILE["drop"] = "beef"
CROCODILE["biom"] = "jungle"
CROCODILE["exp"] = 2

GOLEM = {}
GOLEM["width"] = 32
GOLEM["height"] = 48
GOLEM["attitude"] = ["monster"]
GOLEM["health"] = 40
GOLEM["shift"] = 0
GOLEM["max_speed"] = 0.2
GOLEM["drop"] = "obsydian_ingot"
GOLEM["biom"] = "dark_land"
GOLEM["exp"] = 10

KING = {}
KING["width"] = 80
KING["height"] = 128
KING["attitude"] = ["monster"]
KING["health"] = 300
KING["shift"] = 0
KING["max_speed"] = 0.3
KING["drop"] = "dark_heart"
KING["biom"] = "dark_land"
KING["exp"] = 0

SHEEP = {}
SHEEP["width"] = 32
SHEEP["height"] = 16
SHEEP["attitude"] = ["passive"]
SHEEP["health"] = 5
SHEEP["shift"] = 16
SHEEP["max_speed"] = 0.2
SHEEP["drop"] = "wool_white"
SHEEP["biom"] = "grass_hills"
SHEEP["exp"] = 1

DINGO = {}
DINGO["width"] = 32
DINGO["height"] = 17
DINGO["attitude"] = ["neutral","neutral","neutral","agressive"]
DINGO["health"] = 3
DINGO["shift"] = 15
DINGO["max_speed"] = 0.5
DINGO["drop"] = "fur"
DINGO["biom"] = "desert"
DINGO["exp"] = 1

MOBS["wolf"] = WOLF
MOBS["snow_wolf"] = SNOW_WOLF
MOBS["cow"] = COW
MOBS["sheep"] = SHEEP
MOBS["wraith"] = WRAITH
MOBS["bear"] = BEAR
MOBS["polar_bear"] = POLAR_BEAR
MOBS["dingo"] = DINGO
MOBS["crocodile"] = CROCODILE
MOBS["golem"] = GOLEM
MOBS["king"] = KING

BIOMS = {}

NONE = {}
NONE["upper_layer"] = None
NONE["main_block"] = None
NONE["decos"] = []
NONE["max_height"] = 8

DESERT = {}
DESERT["upper_layer"] = "sand"
DESERT["main_block"] = "sandstone"
DESERT["decos"] = ["skull","deadbush","rock","deadbush","deadbush","deadbush","cactus"]
DESERT["max_height"] = 2

DARK_LAND = {}
DARK_LAND["upper_layer"] = "obsydian"
DARK_LAND["main_block"] = "obsydian"
DARK_LAND["decos"] = []
DARK_LAND["max_height"] = 2

WOODLAND = {}
WOODLAND["upper_layer"] = "grass"
WOODLAND["main_block"] = "dirt"
WOODLAND["decos"] = ["oak_tree","birch_tree","spruce_tree","bush"]
WOODLAND["max_height"] = 2

GRASS_HILLS = {}
GRASS_HILLS["upper_layer"] = "grass"
GRASS_HILLS["main_block"] = "dirt"
GRASS_HILLS["decos"] = ["plant","wheat_plant","flower_blue","flower_white","flower_red","flower_yellow"]
GRASS_HILLS["max_height"] = 4

SWAMP = {}
SWAMP["upper_layer"] = "swamp"
SWAMP["main_block"] = "dirt"
SWAMP["decos"] = ["deadbush","rock","dead_tree","fern","big_fern"]
SWAMP["max_height"] = 2

JUNGLE = {}
JUNGLE["upper_layer"] = "thicket"
JUNGLE["main_block"] = "dirt"
JUNGLE["decos"] = ["jungle_tree","sugar_cane"]
JUNGLE["max_height"] = 4

SNOW_LAND = {}
SNOW_LAND["upper_layer"] = "snow"
SNOW_LAND["main_block"] = "dirt"
SNOW_LAND["decos"] = ["snow_tree","rock"]
SNOW_LAND["max_height"] = 2

ICE_LAKE = {}
ICE_LAKE["upper_layer"] = "ice"
ICE_LAKE["main_block"] = "ice"
ICE_LAKE["decos"] = []
ICE_LAKE["max_height"] = 2

SNOW_HILLS = {}
SNOW_HILLS["upper_layer"] = "snow"
SNOW_HILLS["main_block"] = "dirt"
SNOW_HILLS["decos"] = []
SNOW_HILLS["max_height"] = 4

MOUNTAINS = {}
MOUNTAINS["upper_layer"] = "snow"
MOUNTAINS["main_block"] = "dirt"
MOUNTAINS["decos"] = ["rock"]
MOUNTAINS["max_height"] = 7

DARK_UNDERGROUND = {}
DARK_UNDERGROUND["upper_layer"] = "obsydian"
DARK_UNDERGROUND["main_block"] = "obsydian"
DARK_UNDERGROUND["decos"] = []
DARK_UNDERGROUND["max_height"] = -1

UNDERGROUND = {}
UNDERGROUND["upper_layer"] = "stone"
UNDERGROUND["main_block"] = "stone"
UNDERGROUND["decos"] = []
UNDERGROUND["max_height"] = -1

MINES = [
    ("coal_ore",250,0.1),
    ("iron_ore",400,0.1),
    ("diamond_ore",600,0.1),
    ("obsydian",1000,0.1),
    ("magma",800,0.2),
    ("gravel",0,0.3),
    ("marble",180,0.2),
    ("basalt",180,0.2)
]

CAVE = {}
CAVE["upper_layer"] = "stone"
CAVE["main_block"] = "stone"
CAVE["decos"] = ["web"]
CAVE["max_height"] = -1

BIOMS["none"] = NONE
BIOMS["desert"] = DESERT
BIOMS["woodland"] = WOODLAND
BIOMS["grass_hills"] = GRASS_HILLS
BIOMS["swamp"] = SWAMP
BIOMS["snow_land"] = SNOW_LAND
BIOMS["snow_hills"] = SNOW_HILLS
BIOMS["ice_lake"] = ICE_LAKE
BIOMS["mountains"] = MOUNTAINS
BIOMS["underground"] = UNDERGROUND
BIOMS["cave"] = CAVE
BIOMS["jungle"] = JUNGLE
BIOMS["dark_land"] = DARK_LAND
BIOMS["dark_underground"] = DARK_LAND

TILES = {}

BASALT = {}
BASALT["physics"] = "solid"
BASALT["hardness"] = 4
BASALT["resistance"] = 1
BASALT["sound"] = "stone"

BASALT_BRICKS = {}
BASALT_BRICKS["physics"] = "solid"
BASALT_BRICKS["hardness"] = 4
BASALT_BRICKS["resistance"] = 1
BASALT_BRICKS["sound"] = "stone"

BASALT_BRICKS_STAIRS = {}
BASALT_BRICKS_STAIRS["physics"] = "ramp"
BASALT_BRICKS_STAIRS["hardness"] = 4
BASALT_BRICKS_STAIRS["resistance"] = 1
BASALT_BRICKS_STAIRS["sound"] = "stone"

BIG_FERN = {}
BIG_FERN["physics"] = "deco"
BIG_FERN["hardness"] = 1
BIG_FERN["sound"] = "grass"

BIRCH_PLANKS = {}
BIRCH_PLANKS["physics"] = "solid"
BIRCH_PLANKS["hardness"] = 3
BIRCH_PLANKS["sound"] = "wood"

BIRCH_STAIRS = {}
BIRCH_STAIRS["physics"] = "ramp"
BIRCH_STAIRS["hardness"] = 3
BIRCH_STAIRS["sound"] = "wood"

BIRCH_TREE = {}
BIRCH_TREE["physics"] = "deco"
BIRCH_TREE["hardness"] = 5
BIRCH_TREE["drop"] = "birch_wood"
BIRCH_TREE["sound"] = "wood"

BIRCH_WINDOW = {}
BIRCH_WINDOW["physics"] = "solid"
BIRCH_WINDOW["hardness"] = 2
BIRCH_WINDOW["sound"] = "wood"

BIRCH_WOOD = {}
BIRCH_WOOD["physics"] = "solid"
BIRCH_WOOD["hardness"] = 3
BIRCH_WOOD["sound"] = "wood"

BRICKS = {}
BRICKS["physics"] = "solid"
BRICKS["hardness"] = 4
BRICKS["resistance"] = 1
BRICKS["sound"] = "stone"

BRICKS_STAIRS = {}
BRICKS_STAIRS["physics"] = "ramp"
BRICKS_STAIRS["hardness"] = 4
BRICKS_STAIRS["resistance"] = 1
BRICKS_STAIRS["sound"] = "stone"

BOOKSHELF = {}
BOOKSHELF["physics"] = "solid"
BOOKSHELF["hardness"] = 3
BOOKSHELF["sound"] = "wood"

BRAKE = {}
BRAKE["physics"] = "deco"
BRAKE["hardness"] = 1
BRAKE["animated"] = 10
BRAKE["drop"] = "none"
BRAKE["sound"] = "grass"

BONFIRE = {}
BONFIRE["physics"] = "deco"
BONFIRE["hardness"] = 5
BONFIRE["drop"] = "none"
BONFIRE["sound"] = "wood"

BUSH = {}
BUSH["physics"] = "deco"
BUSH["hardness"] = 1
BUSH["drop"] = "berries"
BUSH["sound"] = "grass"

CACTUS = {}
CACTUS["physics"] = "deco"
CACTUS["hardness"] = 1
CACTUS["sound"] = "grass"

COAL_ORE = {}
COAL_ORE["physics"] = "solid"
COAL_ORE["hardness"] = 4
COAL_ORE["drop"] = "coal"
COAL_ORE["resistance"] = 1
COAL_ORE["sound"] = "stone"

DARK_PLANT = {}
DARK_PLANT["physics"] = "deco"
DARK_PLANT["hardness"] = 1
DARK_PLANT["drop"] = "none"
DARK_PLANT["animated"] = 10
DARK_PLANT["sound"] = "grass"

DARK_PORTAL = {}
DARK_PORTAL["physics"] = "deco"
DARK_PORTAL["hardness"] = 1
DARK_PORTAL["resistance"] = 10
DARK_PORTAL["sound"] = "stone"

DEAD_PLANKS = {}
DEAD_PLANKS["physics"] = "solid"
DEAD_PLANKS["hardness"] = 3
DEAD_PLANKS["sound"] = "wood"

DEAD_STAIRS = {}
DEAD_STAIRS["physics"] = "ramp"
DEAD_STAIRS["hardness"] = 3
DEAD_STAIRS["sound"] = "wood"

DEAD_TREE = {}
DEAD_TREE["physics"] = "deco"
DEAD_TREE["hardness"] = 5
DEAD_TREE["drop"] = "dead_wood"
DEAD_TREE["sound"] = "wood"

DEAD_WINDOW = {}
DEAD_WINDOW["physics"] = "solid"
DEAD_WINDOW["hardness"] = 2
DEAD_WINDOW["sound"] = "wood"

DEAD_WOOD = {}
DEAD_WOOD["physics"] = "solid"
DEAD_WOOD["hardness"] = 3
DEAD_WOOD["sound"] = "wood"

DEADBUSH = {}
DEADBUSH["physics"] = "deco"
DEADBUSH["hardness"] = 1
DEADBUSH["drop"] = "stick"
DEADBUSH["sound"] = "grass"

DIAMOND_ORE = {}
DIAMOND_ORE["physics"] = "solid"
DIAMOND_ORE["hardness"] = 4
DIAMOND_ORE["drop"] = "diamond"
DIAMOND_ORE["resistance"] = 2
DIAMOND_ORE["sound"] = "stone"

DIAMOND_BLOCK = {}
DIAMOND_BLOCK["physics"] = "solid"
DIAMOND_BLOCK["hardness"] = 7
DIAMOND_BLOCK["resistance"] = 3
DIAMOND_BLOCK["sound"] = "stone"

DIRT = {}
DIRT["physics"] = "solid"
DIRT["hardness"] = 2
DIRT["sound"] = "grass"

DOOR_CLOSE = {}
DOOR_CLOSE["physics"] = "solid"
DOOR_CLOSE["hardness"] = 3
DOOR_CLOSE["sound"] = "wood"

DOOR_OPEN = {}
DOOR_OPEN["physics"] = "deco"
DOOR_OPEN["hardness"] = 3
DOOR_OPEN["drop"] = "door_close"
DOOR_OPEN["sound"] = "wood"

FERN = {}
FERN["physics"] = "deco"
FERN["hardness"] = 1
FERN["sound"] = "grass"

FLOWER_BLUE = {}
FLOWER_BLUE["physics"] = "deco"
FLOWER_BLUE["hardness"] = 1
FLOWER_BLUE["sound"] = "grass"

FLOWER_RED = {}
FLOWER_RED["physics"] = "deco"
FLOWER_RED["hardness"] = 1
FLOWER_RED["sound"] = "grass"

FLOWER_WHITE = {}
FLOWER_WHITE["physics"] = "deco"
FLOWER_WHITE["hardness"] = 1
FLOWER_WHITE["sound"] = "grass"

FLOWER_YELLOW = {}
FLOWER_YELLOW["physics"] = "deco"
FLOWER_YELLOW["hardness"] = 1
FLOWER_YELLOW["sound"] = "grass"

GLASS = {}
GLASS["physics"] = "solid"
GLASS["hardness"] = 1
GLASS["sound"] = "stone"

GRASS = {}
GRASS["physics"] = "solid"
GRASS["hardness"] = 1
GRASS["sound"] = "grass"

GRASS_RAMP = {}
GRASS_RAMP["physics"] = "ramp"
GRASS_RAMP["hardness"] = 1
GRASS_RAMP["drop"] = "plant"
GRASS_RAMP["sound"] = "grass"

GRAVEL = {}
GRAVEL["physics"] = "solid"
GRAVEL["hardness"] = 2
GRAVEL["sound"] = "grass"

ICE = {}
ICE["physics"] = "solid"
ICE["hardness"] = 4
ICE["sound"] = "stone"

ICE_RAMP = {}
ICE_RAMP["physics"] = "ramp"
ICE_RAMP["hardness"] = 4
ICE_RAMP["sound"] = "stone"

IRON_ORE = {}
IRON_ORE["physics"] = "solid"
IRON_ORE["hardness"] = 4
IRON_ORE["resistance"] = 1
IRON_ORE["sound"] = "stone"

IRON_BLOCK = {}
IRON_BLOCK["physics"] = "solid"
IRON_BLOCK["hardness"] = 5
IRON_BLOCK["resistance"] = 2
IRON_BLOCK["sound"] = "stone"

JUNGLE_TREE = {}
JUNGLE_TREE["physics"] = "deco"
JUNGLE_TREE["hardness"] = 5
JUNGLE_TREE["drop"] = "cocoa"
JUNGLE_TREE["sound"] = "wood"

WHEAT_PLANT = {}
WHEAT_PLANT["physics"] = "deco"
WHEAT_PLANT["hardness"] = 1
WHEAT_PLANT["drop"] = "wheat"
WHEAT_PLANT["animated"] = 10
WHEAT_PLANT["sound"] = "grass"

MAGMA = {}
MAGMA["physics"] = "solid"
MAGMA["hardness"] = 6
MAGMA["resistance"] = 2
MAGMA["sound"] = "stone"

MARBLE = {}
MARBLE["physics"] = "solid"
MARBLE["hardness"] = 4
MARBLE["resistance"] = 1
MARBLE["sound"] = "stone"

MARBLE_BRICKS = {}
MARBLE_BRICKS["physics"] = "solid"
MARBLE_BRICKS["hardness"] = 4
MARBLE_BRICKS["resistance"] = 1
MARBLE_BRICKS["sound"] = "stone"

MARBLE_BRICKS_STAIRS = {}
MARBLE_BRICKS_STAIRS["physics"] = "ramp"
MARBLE_BRICKS_STAIRS["hardness"] = 4
MARBLE_BRICKS_STAIRS["resistance"] = 1
MARBLE_BRICKS_STAIRS["sound"] = "stone"

MARSH = {}
MARSH["physics"] = "deco"
MARSH["hardness"] = 1
MARSH["drop"] = "none"
MARSH["animated"] = 10
MARSH["sound"] = "grass"

OAK_PLANKS = {}
OAK_PLANKS["physics"] = "solid"
OAK_PLANKS["hardness"] = 3
OAK_PLANKS["sound"] = "wood"

OAK_STAIRS = {}
OAK_STAIRS["physics"] = "ramp"
OAK_STAIRS["hardness"] = 3
OAK_STAIRS["sound"] = "wood"

OAK_TREE = {}
OAK_TREE["physics"] = "deco"
OAK_TREE["hardness"] = 5
OAK_TREE["drop"] = "oak_wood"
OAK_TREE["sound"] = "wood"

OAK_WINDOW = {}
OAK_WINDOW["physics"] = "solid"
OAK_WINDOW["hardness"] = 2
OAK_WINDOW["sound"] = "wood"

OAK_WOOD = {}
OAK_WOOD["physics"] = "solid"
OAK_WOOD["hardness"] = 3
OAK_WOOD["sound"] = "wood"

OBSYDIAN = {}
OBSYDIAN["physics"] = "solid"
OBSYDIAN["hardness"] = 10
OBSYDIAN["resistance"] = 4
OBSYDIAN["sound"] = "stone"

OBSYDIAN_BLOCK = {}
OBSYDIAN_BLOCK["physics"] = "solid"
OBSYDIAN_BLOCK["hardness"] = 20
OBSYDIAN_BLOCK["resistance"] = 4
OBSYDIAN_BLOCK["sound"] = "stone"

PAINT_BLUE = {}
PAINT_BLUE["physics"] = "deco"
PAINT_BLUE["hardness"] = 1
PAINT_BLUE["sound"] = "snow"

PAINT_GREEN = {}
PAINT_GREEN["physics"] = "deco"
PAINT_GREEN["hardness"] = 1
PAINT_GREEN["sound"] = "snow"

PAINT_RED = {}
PAINT_RED["physics"] = "deco"
PAINT_RED["hardness"] = 1
PAINT_RED["sound"] = "snow"

PAINT_WHITE = {}
PAINT_WHITE["physics"] = "deco"
PAINT_WHITE["hardness"] = 1
PAINT_WHITE["sound"] = "snow"

PAINT_YELLOW = {}
PAINT_YELLOW["physics"] = "deco"
PAINT_YELLOW["hardness"] = 1
PAINT_YELLOW["sound"] = "snow"

PLANT = {}
PLANT["physics"] = "deco"
PLANT["hardness"] = 1
PLANT["animated"] = 10
PLANT["drop"] = "none"
PLANT["sound"] = "grass"

ROCK = {}
ROCK["physics"] = "deco"
ROCK["hardness"] = 2
ROCK["drop"] = "stone"
ROCK["resistance"] = 1
ROCK["sound"] = "stone"

SAND = {}
SAND["physics"] = "solid"
SAND["hardness"] = 2
SAND["sound"] = "sand"

SAND_RAMP = {}
SAND_RAMP["physics"] = "ramp"
SAND_RAMP["hardness"] = 2
SAND_RAMP["drop"] = "sand"
SAND_RAMP["sound"] = "sand"

SANDSTONE = {}
SANDSTONE["physics"] = "solid"
SANDSTONE["hardness"] = 3
SANDSTONE["resistance"] = 1
SANDSTONE["sound"] = "stone"

SANDSTONE_BRICKS = {}
SANDSTONE_BRICKS["physics"] = "solid"
SANDSTONE_BRICKS["hardness"] = 3
SANDSTONE_BRICKS["resistance"] = 1
SANDSTONE_BRICKS["sound"] = "stone"

SANDSTONE_BRICKS_STAIRS = {}
SANDSTONE_BRICKS_STAIRS["physics"] = "ramp"
SANDSTONE_BRICKS_STAIRS["hardness"] = 3
SANDSTONE_BRICKS_STAIRS["resistance"] = 1
SANDSTONE_BRICKS_STAIRS["sound"] = "stone"

SKULL = {}
SKULL["physics"] = "deco"
SKULL["hardness"] = 1
SKULL["sound"] = "stone"

SMALL_PLANT = {}
SMALL_PLANT["physics"] = "deco"
SMALL_PLANT["hardness"] = 1
SMALL_PLANT["drop"] = "none"
SMALL_PLANT["animated"] = 10
SMALL_PLANT["sound"] = "grass"

SNOW = {}
SNOW["physics"] = "solid"
SNOW["hardness"] = 2
SNOW["sound"] = "snow"

SNOWDRIFT = {}
SNOWDRIFT["physics"] = "deco"
SNOWDRIFT["hardness"] = 1
SNOWDRIFT["drop"] = "none"
SNOWDRIFT["animated"] = 10
SNOWDRIFT["sound"] = "snow"

SNOW_RAMP = {}
SNOW_RAMP["physics"] = "ramp"
SNOW_RAMP["hardness"] = 2
SNOW_RAMP["drop"] = "snow"
SNOW_RAMP["sound"] = "snow"

SNOW_TREE = {}
SNOW_TREE["physics"] = "deco"
SNOW_TREE["hardness"] = 5
SNOW_TREE["drop"] = "spruce_wood"
SNOW_TREE["sound"] = "wood"

SPRUCE_PLANKS = {}
SPRUCE_PLANKS["physics"] = "solid"
SPRUCE_PLANKS["hardness"] = 3
SPRUCE_PLANKS["sound"] = "wood"

SPRUCE_STAIRS = {}
SPRUCE_STAIRS["physics"] = "ramp"
SPRUCE_STAIRS["hardness"] = 3
SPRUCE_STAIRS["sound"] = "wood"

SPRUCE_TREE = {}
SPRUCE_TREE["physics"] = "deco"
SPRUCE_TREE["hardness"] = 5
SPRUCE_TREE["drop"] = "spruce_wood"
SPRUCE_TREE["sound"] = "wood"

SPRUCE_WINDOW = {}
SPRUCE_WINDOW["physics"] = "solid"
SPRUCE_WINDOW["hardness"] = 2
SPRUCE_WINDOW["sound"] = "wood"

SPRUCE_WOOD = {}
SPRUCE_WOOD["physics"] = "solid"
SPRUCE_WOOD["hardness"] = 3
SPRUCE_WOOD["sound"] = "wood"

STONE = {}
STONE["physics"] = "solid"
STONE["hardness"] = 4
STONE["resistance"] = 1
STONE["sound"] = "stone"

STONE_BRICKS = {}
STONE_BRICKS["physics"] = "solid"
STONE_BRICKS["hardness"] = 4
STONE_BRICKS["resistance"] = 1
STONE_BRICKS["sound"] = "stone"

STONE_BRICKS_STAIRS = {}
STONE_BRICKS_STAIRS["physics"] = "ramp"
STONE_BRICKS_STAIRS["hardness"] = 4
STONE_BRICKS_STAIRS["resistance"] = 1
STONE_BRICKS_STAIRS["sound"] = "stone"

SUGAR_CANE = {}
SUGAR_CANE["physics"] = "deco"
SUGAR_CANE["hardness"] = 1
SUGAR_CANE["sound"] = "grass"

SWAMP = {}
SWAMP["physics"] = "solid"
SWAMP["hardness"] = 2
SWAMP["sound"] = "grass"

SWAMP_RAMP = {}
SWAMP_RAMP["physics"] = "ramp"
SWAMP_RAMP["hardness"] = 2
SWAMP_RAMP["drop"] = "swamp"
SWAMP_RAMP["sound"] = "grass"

THICKET = {}
THICKET["physics"] = "solid"
THICKET["hardness"] = 2
THICKET["sound"] = "grass"

THICKET_RAMP = {}
THICKET_RAMP["physics"] = "ramp"
THICKET_RAMP["hardness"] = 2
THICKET_RAMP["drop"] = "thicket"
THICKET_RAMP["sound"] = "grass"

TORCH = {}
TORCH["physics"] = "deco"
TORCH["hardness"] = 1
TORCH["sound"] = "wood"

UNDERGROUND = {}
UNDERGROUND["physics"] = "back"
UNDERGROUND["hardness"] = 1

WEB = {}
WEB["physics"] = "deco"
WEB["hardness"] = 1
WEB["sound"] = "snow"

WOOL_BLUE = {}
WOOL_BLUE["physics"] = "solid"
WOOL_BLUE["hardness"] = 2
WOOL_BLUE["sound"] = "snow"

WOOL_GREEN = {}
WOOL_GREEN["physics"] = "solid"
WOOL_GREEN["hardness"] = 2
WOOL_GREEN["sound"] = "snow"

WOOL_RED = {}
WOOL_RED["physics"] = "solid"
WOOL_RED["hardness"] = 2
WOOL_RED["sound"] = "snow"

WOOL_WHITE = {}
WOOL_WHITE["physics"] = "solid"
WOOL_WHITE["hardness"] = 2
WOOL_WHITE["sound"] = "snow"

WOOL_YELLOW = {}
WOOL_YELLOW["physics"] = "solid"
WOOL_YELLOW["hardness"] = 2
WOOL_YELLOW["sound"] = "snow"

TILES["basalt"] = BASALT
TILES["basalt_bricks"] = BASALT_BRICKS
TILES["basalt_bricks_stairs"] = BASALT_BRICKS_STAIRS
TILES["big_fern"] = BIG_FERN
TILES["birch_planks"] = BIRCH_PLANKS
TILES["birch_stairs"] = BIRCH_STAIRS
TILES["birch_tree"] = BIRCH_TREE
TILES["birch_window"] = BIRCH_WINDOW
TILES["birch_wood"] = BIRCH_WOOD
TILES["bricks"] = BRICKS
TILES["bricks_stairs"] = BRICKS_STAIRS
TILES["brake"] = BRAKE
TILES["bonfire"] = BONFIRE
TILES["bush"] = BUSH
TILES["bookshelf"] = BOOKSHELF
TILES["cactus"] = CACTUS
TILES["coal_ore"] = COAL_ORE
TILES["dark_plant"] = DARK_PLANT
TILES["dark_portal"] = DARK_PORTAL
TILES["dead_planks"] = DEAD_PLANKS
TILES["dead_stairs"] = DEAD_STAIRS
TILES["dead_tree"] = DEAD_TREE
TILES["dead_window"] = DEAD_WINDOW
TILES["dead_wood"] = DEAD_WOOD
TILES["deadbush"] = DEADBUSH
TILES["diamond_ore"] = DIAMOND_ORE
TILES["diamond_block"] = DIAMOND_BLOCK
TILES["dirt"] = DIRT
TILES["door_close"] = DOOR_CLOSE
TILES["door_open"] = DOOR_OPEN
TILES["fern"] = FERN
TILES["flower_blue"] = FLOWER_BLUE
TILES["flower_red"] = FLOWER_RED
TILES["flower_white"] = FLOWER_WHITE
TILES["flower_yellow"] = FLOWER_YELLOW
TILES["glass"] = GLASS
TILES["grass"] = GRASS
TILES["grass_ramp"] = GRASS_RAMP
TILES["gravel"] = GRAVEL
TILES["ice"] = ICE
TILES["ice_ramp"] = ICE_RAMP
TILES["iron_ore"] = IRON_ORE
TILES["iron_block"] = IRON_BLOCK
TILES["jungle_tree"] = JUNGLE_TREE
TILES["magma"] = MAGMA
TILES["marble"] = MARBLE
TILES["marble_bricks"] = MARBLE_BRICKS
TILES["marble_bricks_stairs"] = MARBLE_BRICKS_STAIRS
TILES["marsh"] = MARSH
TILES["oak_planks"] = OAK_PLANKS
TILES["oak_stairs"] = OAK_STAIRS
TILES["oak_tree"] = OAK_TREE
TILES["oak_window"] = OAK_WINDOW
TILES["oak_wood"] = OAK_WOOD
TILES["obsydian"] = OBSYDIAN
TILES["obsydian_block"] = OBSYDIAN_BLOCK
TILES["paint_blue"] = PAINT_BLUE
TILES["paint_green"] = PAINT_GREEN
TILES["paint_red"] = PAINT_RED
TILES["paint_white"] = PAINT_WHITE
TILES["paint_yellow"] = PAINT_YELLOW
TILES["plant"] = PLANT
TILES["rock"] = ROCK
TILES["sand"] = SAND
TILES["sand_ramp"] = SAND_RAMP
TILES["sandstone"] = SANDSTONE
TILES["sandstone_bricks"] = SANDSTONE_BRICKS
TILES["sandstone_bricks_stairs"] = SANDSTONE_BRICKS_STAIRS
TILES["skull"] = SKULL
TILES["small_plant"] = SMALL_PLANT
TILES["snow"] = SNOW
TILES["snowdrift"] = SNOWDRIFT
TILES["snow_ramp"] = SNOW_RAMP
TILES["snow_tree"] = SNOW_TREE
TILES["spruce_planks"] = SPRUCE_PLANKS
TILES["spruce_stairs"] = SPRUCE_STAIRS
TILES["spruce_tree"] = SPRUCE_TREE
TILES["spruce_window"] = SPRUCE_WINDOW
TILES["spruce_wood"] = SPRUCE_WOOD
TILES["stone"] = STONE
TILES["stone_bricks"] = STONE_BRICKS
TILES["stone_bricks_stairs"] = STONE_BRICKS_STAIRS
TILES["sugar_cane"] = SUGAR_CANE
TILES["swamp"] = SWAMP
TILES["swamp_ramp"] = SWAMP_RAMP
TILES["torch"] = TORCH
TILES["thicket"] = THICKET
TILES["thicket_ramp"] = THICKET_RAMP
TILES["underground"] = UNDERGROUND
TILES["web"] = WEB
TILES["wool_blue"] = WOOL_BLUE
TILES["wool_green"] = WOOL_GREEN
TILES["wool_red"] = WOOL_RED
TILES["wool_white"] = WOOL_WHITE
TILES["wool_yellow"] = WOOL_YELLOW
TILES["wheat_plant"] = WHEAT_PLANT

TOOLS = {}

WOODEN_PICKAXE = {}
WOODEN_PICKAXE["speed"] = 2
WOODEN_PICKAXE["power"] = 1

STONE_PICKAXE = {}
STONE_PICKAXE["speed"] = 3
STONE_PICKAXE["power"] = 2

IRON_PICKAXE = {}
IRON_PICKAXE["speed"] = 5
IRON_PICKAXE["power"] = 3

DIAMOND_PICKAXE = {}
DIAMOND_PICKAXE["speed"] = 8
DIAMOND_PICKAXE["power"] = 4

OBSYDIAN_PICKAXE = {}
OBSYDIAN_PICKAXE["speed"] = 15
OBSYDIAN_PICKAXE["power"] = 4

WOODEN_SWORD = {}
WOODEN_SWORD["speed"] = 0
WOODEN_SWORD["power"] = 1

STONE_SWORD = {}
STONE_SWORD["speed"] = 0
STONE_SWORD["power"] = 2

IRON_SWORD = {}
IRON_SWORD["speed"] = 0
IRON_SWORD["power"] = 4

DIAMOND_SWORD = {}
DIAMOND_SWORD["speed"] = 0
DIAMOND_SWORD["power"] = 6

OBSYDIAN_SWORD = {}
OBSYDIAN_SWORD["speed"] = 0
OBSYDIAN_SWORD["power"] = 10

WOODEN_BIG_SWORD = {}
WOODEN_BIG_SWORD["speed"] = 0
WOODEN_BIG_SWORD["power"] = 2

STONE_BIG_SWORD = {}
STONE_BIG_SWORD["speed"] = 0
STONE_BIG_SWORD["power"] = 4

IRON_BIG_SWORD = {}
IRON_BIG_SWORD["speed"] = 0
IRON_BIG_SWORD["power"] = 7

DIAMOND_BIG_SWORD = {}
DIAMOND_BIG_SWORD["speed"] = 0
DIAMOND_BIG_SWORD["power"] = 10

OBSYDIAN_BIG_SWORD = {}
OBSYDIAN_BIG_SWORD["speed"] = 0
OBSYDIAN_BIG_SWORD["power"] = 15

TOOLS["wooden_pickaxe"] = WOODEN_PICKAXE
TOOLS["stone_pickaxe"] = STONE_PICKAXE
TOOLS["iron_pickaxe"] = IRON_PICKAXE
TOOLS["diamond_pickaxe"] = DIAMOND_PICKAXE
TOOLS["obsydian_pickaxe"] = OBSYDIAN_PICKAXE
TOOLS["wooden_sword"] = WOODEN_SWORD
TOOLS["stone_sword"] = STONE_SWORD
TOOLS["iron_sword"] = IRON_SWORD
TOOLS["diamond_sword"] = DIAMOND_SWORD
TOOLS["obsydian_sword"] = OBSYDIAN_SWORD
TOOLS["wooden_big_sword"] = WOODEN_BIG_SWORD
TOOLS["stone_big_sword"] = STONE_BIG_SWORD
TOOLS["iron_big_sword"] = IRON_BIG_SWORD
TOOLS["diamond_big_sword"] = DIAMOND_BIG_SWORD
TOOLS["obsydian_big_sword"] = OBSYDIAN_BIG_SWORD

ITEMS = ["stick",
         "coal",
         "iron",
         "diamond",
         "fur",
         "dye_white",
         "dye_yellow",
         "dye_red",
         "dye_blue",
         "dye_green",
         "obsydian_ingot",
         "berries",
         "cocoa",
         "sugar",
         "wheat",
         "bread",
         "cake",
         "chocolate",
         "cookie",
         "beef",
         "steak",
         "book",
         "paper",
         "leather_armor",
         "iron_armor",
         "diamond_armor",
         "obsydian_armor",
         "dark_heart"
]

FOOD = [
    ("berries",0.5),
    ("bread",2),
    ("cake",2.5),
    ("steak",3.5),
    ("cookie",1.5),
    ("chocolate",2)
]

RECIPES = []
# other
RECIPES.append(["coal","stick","torch",1])
RECIPES.append(["torch","torch","bonfire",1])
RECIPES.append(["stone","stone","stone_bricks",2])
RECIPES.append(["sandstone","sandstone","sandstone_bricks",2])
RECIPES.append(["marble","marble","marble_bricks",2])
RECIPES.append(["basalt","basalt","basalt_bricks",2])
RECIPES.append(["sugar_cane","sugar_cane","paper",2])
RECIPES.append(["paper","paper","book",1])
RECIPES.append(["obsydian_block","obsydian_block","dark_portal",1,"dark_portal"])
# bookshelf
RECIPES.append(["book","oak_planks","bookshelf",1])
RECIPES.append(["book","birch_planks","bookshelf",1])
RECIPES.append(["book","spruce_planks","bookshelf",1])
RECIPES.append(["book","","dead_planks",1])
# melt
RECIPES.append(["sand","coal","glass",1])
RECIPES.append(["iron_ore","coal","iron",1])
RECIPES.append(["stone_bricks","coal","bricks",1])
RECIPES.append(["obsydian","magma","obsydian_ingot",1,"dark_forge"])
RECIPES.append(["beef","coal","steak",1])
# planks
RECIPES.append(["oak_wood","","oak_planks",4])
RECIPES.append(["dead_wood","","dead_planks",4])
RECIPES.append(["spruce_wood","","spruce_planks",4])
RECIPES.append(["birch_wood","","birch_planks",4])
# stairs
RECIPES.append(["oak_planks","oak_planks","oak_stairs",4])
RECIPES.append(["dead_planks","dead_planks","dead_stairs",4])
RECIPES.append(["birch_planks","birch_planks","birch_stairs",4])
RECIPES.append(["spruce_planks","spruce_planks","spruce_stairs",4])
RECIPES.append(["bricks","bricks","bricks_stairs",4])
RECIPES.append(["stone_bricks","stone_bricks","stone_bricks_stairs",4])
RECIPES.append(["sandstone_bricks","sandstone_bricks","sandstone_bricks_stairs",4])
RECIPES.append(["marble_bricks","marble_bricks","marble_bricks_stairs",4])
RECIPES.append(["basalt_bricks","basalt_bricks","basalt_bricks_stairs",4])
# blocks
RECIPES.append(["iron","iron","iron_block",1])
RECIPES.append(["diamond","diamond","diamond_block",1])
RECIPES.append(["obsydian_ingot","obsydian_ingot","obsydian_block",1])
# sticks
RECIPES.append(["oak_planks","","stick",2])
RECIPES.append(["dead_planks","","stick",2])
RECIPES.append(["birch_planks","","stick",2])
RECIPES.append(["spruce_planks","","stick",2])
# windows
RECIPES.append(["oak_planks","glass","oak_window",1])
RECIPES.append(["dead_planks","glass","dead_window",1])
RECIPES.append(["spruce_planks","glass","spruce_window",1])
RECIPES.append(["birch_planks","glass","birch_window",1])
# door
RECIPES.append(["oak_planks","oak_stairs","door_close",1])
RECIPES.append(["dead_planks","dead_stairs","door_close",1])
RECIPES.append(["birch_planks","birch_stairs","door_close",1])
RECIPES.append(["spruce_planks","spruce_stairs","door_close",1])
# dyes
RECIPES.append(["flower_blue","","dye_blue",4])
RECIPES.append(["flower_red","","dye_red",4])
RECIPES.append(["flower_yellow","","dye_yellow",4])
RECIPES.append(["flower_green","","dye_green",4])
RECIPES.append(["flower_white","","dye_white",4])
# wools
RECIPES.append(["wool_white","dye_blue","wool_blue",1])
RECIPES.append(["wool_white","dye_red","wool_red",1])
RECIPES.append(["wool_white","dye_green","wool_green",1])
RECIPES.append(["wool_white","dye_yellow","wool_yellow",1])
# wool white
RECIPES.append(["wool_blue","dye_white","wool_white",1])
RECIPES.append(["wool_red","dye_white","wool_white",1])
RECIPES.append(["wool_yellow","dye_white","wool_white",1])
RECIPES.append(["wool_green","dye_white","wool_white",1])
# paints
RECIPES.append(["wool_blue","stick","paint_blue",1])
RECIPES.append(["wool_red","stick","paint_red",1])
RECIPES.append(["wool_green","stick","paint_green",1])
RECIPES.append(["wool_yellow","stick","paint_yellow",1])
RECIPES.append(["wool_white","stick","paint_white",1])
# wooden tools
RECIPES.append(["oak_wood","stick","wooden_pickaxe",1])
RECIPES.append(["dead_wood","stick","wooden_pickaxe",1])
RECIPES.append(["spruce_wood","stick","wooden_pickaxe",1])
RECIPES.append(["birch_wood","stick","wooden_pickaxe",1])
RECIPES.append(["oak_wood","oak_planks","wooden_sword",1])
RECIPES.append(["dead_wood","dead_planks","wooden_sword",1])
RECIPES.append(["spruce_wood","spruce_planks","wooden_sword",1])
RECIPES.append(["birch_wood","birch_planks","wooden_sword",1])
# tools
RECIPES.append(["obsydian_ingot","stick","obsydian_pickaxe",1])
RECIPES.append(["diamond","stick","diamond_pickaxe",1])
RECIPES.append(["iron","stick","iron_pickaxe",1])
RECIPES.append(["stone","stick","stone_pickaxe",1])
RECIPES.append(["obsydian_ingot","oak_planks","obsydian_sword",1])
RECIPES.append(["obsydian_ingot","dead_planks","obsydian_sword",1])
RECIPES.append(["obsydian_ingot","birch_planks","obsydian_sword",1])
RECIPES.append(["obsydian_ingot","spruce_planks","obsydian_sword",1])
RECIPES.append(["diamond","oak_planks","diamond_sword",1])
RECIPES.append(["diamond","dead_planks","diamond_sword",1])
RECIPES.append(["diamond","birch_planks","diamond_sword",1])
RECIPES.append(["diamond","spruce_planks","diamond_sword",1])
RECIPES.append(["stone","oak_planks","stone_sword",1])
RECIPES.append(["stone","dead_planks","stone_sword",1])
RECIPES.append(["stone","birch_planks","stone_sword",1])
RECIPES.append(["stone","spruce_planks","stone_sword",1])
RECIPES.append(["iron","oak_planks","iron_sword",1])
RECIPES.append(["iron","dead_planks","iron_sword",1])
RECIPES.append(["iron","spruce_planks","iron_sword",1])
RECIPES.append(["iron","birch_planks","iron_sword",1])
# big swords
RECIPES.append(["wooden_sword","birch_wood","wooden_big_sword",1,"exp_forge"])
RECIPES.append(["wooden_sword","oak_wood","wooden_big_sword",1,"exp_forge"])
RECIPES.append(["wooden_sword","dead_wood","wooden_big_sword",1,"exp_forge"])
RECIPES.append(["wooden_sword","spruce_wood","wooden_big_sword",1,"exp_forge"])
RECIPES.append(["stone_sword","stone","stone_big_sword",1,"exp_forge"])
RECIPES.append(["diamond_sword","diamond","diamond_big_sword",1,"exp_forge"])
RECIPES.append(["iron_sword","iron","iron_big_sword",1,"exp_forge"])
RECIPES.append(["obsydian_sword","obsydian_ingot","obsydian_big_sword",1,"exp_forge"])
# food
RECIPES.append(["sugar_cane","","sugar",1])
RECIPES.append(["sugar","wheat","cake",1])
RECIPES.append(["sugar","cocoa","chocolate",1])
RECIPES.append(["wheat","wheat","bread",1])
RECIPES.append(["wheat","cocoa","cookie",1])
# armor
RECIPES.append(["fur","fur","leather_armor",1,"forge"])
RECIPES.append(["fur","iron","iron_armor",1,"forge"])
RECIPES.append(["fur","diamond","diamond_armor",1,"forge"])
RECIPES.append(["fur","obsydian","obsydian_armor",1,"forge"])
TOPS = {}

TOPS["grass"] = "small_plant"
TOPS["snow"] = "snowdrift"
TOPS["swamp"] = "marsh"
TOPS["thicket"] = "brake"
TOPS["ice"] = "snowdrift"
TOPS["obsydian"] = "dark_plant"

ARMOR = {}
ARMOR["leather_armor"] = (1,(219,182,103),(185,148,81))
ARMOR["iron_armor"] = (2,(216,216,216),(114,114,114))
ARMOR["diamond_armor"] = (3,(72,238,218),(21,146,155))
ARMOR["obsydian_armor"] = (5,(60,48,86),(30,24,43))

SKILLS = {}

SKILLS["blood_lust"] = None
SKILLS["regeneration"] = ["blood_lust"]
SKILLS["holy_aura"] = ["regeneration"]
SKILLS["shoes"] = None
SKILLS["double_jump"] = ["shoes"]
SKILLS["super_speed"] = ["double_jump"]
SKILLS["forge"] = None
SKILLS["exp_forge"] = ["forge"]
SKILLS["dark_forge"] = ["exp_forge"]
SKILLS["dark_portal"] = ["holy_aura","dark_forge","super_speed"]

INFO = {}
INFO["blood_lust"] = "Increases your strength by 1"
INFO["regeneration"] = "Makes your HP heals after some time"
INFO["holy_aura"] = "Allows your swords kill wraiths"
INFO["shoes"] = "Increases your speed by 20%"
INFO["double_jump"] = "Let you double jump"
INFO["super_speed"] = "Gives you huge speed when CRTL is on"
INFO["forge"] = "Allows you to build an armor"
INFO["exp_forge"] = "Allows you to build big swords"
INFO["dark_forge"] = "Allows you to melt obsydian"
INFO["dark_portal"] = "Allows you to build dark portal"

QUESTS = [
    ("The begining",["oak_wood","birch_wood","dead_wood","spruce_wood"],"Chop the tree,/ and collect wood."),
    ("The carpenter",["stick"],"Craft planks,/ and sticks."),
    ("Basic tool",["wooden_pickaxe"],"Use wood and stick/ to build a pickaxe."),
    ("Forewarned is forearmed",["wooden_sword"],"Use wood and planks/ to build a sword."),
    ("Let's go deeper",["stone"],"Gig a tunnel/ to the underground."),
    ("Stone age",["stone_pickaxe"],"Craft pickaxe/ using stone."),
    ("Novice miner",["iron_ore"],"Dig deeper/ to find iron ore."),
    ("Forge",["iron_ingot"],"Use coal to melt/ iron ingot."),
    ("Heavy equipment",["iron_pickaxe"],"Craft iron/ pickaxe."),
    ("Hunting",["fur"],"Craft iron sword and/ hunt a wild animal."),
    ("Time to eat!",["steak"],"Kill a cow and/ cook the steak."),
    ("Luxury food",["cake"],"Make cake from/ sugar and wheat. /( you can make sugar/ from sugar cane )"),
    ("Comfortable house",["marble_bricks"],"Mine marble/ and make marble bricks."),
    ("Jewellery",["diamond"],"Mine a diamond."),
    ("Improvements",["diamond_pickaxe"],"Craft a diamond/ pickaxe."),
    ("Dark rock",["obsydian"],"Mine an obsydian."),
    ("Dark technology",["dark_portal"],"Build a dark/ portal (10 lvl /requied)."),
    ("THE END",["dark_heart"],"Kill the dark/ king and collect/ dark heart.")
]

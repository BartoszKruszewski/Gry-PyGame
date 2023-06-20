LEVELS = 5
GAME_RESOLUTION = (320,180)
GAME_CAPTION = "FNAF FAN MADE"
FRAMERATE = 144
FULLSCREEN = True
BORDERS = (20, 300)
MONSTER_WALK_SPEED = (2000,4000)
MONSTER_START_COOLDOWN = 1000
BUTTON_COOLDOWN = 10
MONSTER_ATTACK_COOLDOWN = 180
MASK_COOLDOWN = 500
MENU_ANIMATION_TIMER = (100,400)
MASK_MAX_TIME = 600
MUSIC_BOX_OPEN_TIME = 10000
MUSIC_BOX_FILL_SPEED = 10

ANIMATIONS_LENGTH = {
    1:69,
    2:60,
    3:67,
    4:118,
    5:73
}

END_CAPTION = [
    "The police will look again at the infamous Fazbear pizzeria.",
    "New light on the case of three murders of children that took place in the premises was shed by the night watchman overseeing the restaurant.",
    "Another investigation was launched to determine whether there were any fatalities in the fire that hit the pizzeria a few years ago.",
    "Unofficial sources provide information about a father and daughter who disappeared on the day of the fire, being near the scene of the accident.",
    "We are waiting impatiently for the results of the investigators' work."
]

FONTS_SIZES = [
    ("small",12),
    ("normal",24),
    ("big",50)
]

BUTTONS = [
    ("console","main_room",(180,161,89,12),False),
    ("close_console","camera_panel",(200,161,89,12),False),
    ("corridor1","camera_panel",(217,95,12,36),False),
    ("corridor2","camera_panel",(273,95,12,36),False),
    ("kitchen","camera_panel",(241,95,20,12),False),
    ("party_room","camera_panel",(217,63,44,20),False),
    ("reception","camera_panel",(241,39,20,12),False),
    ("closet1","camera_panel",(193,67,12,12),False),
    ("closet2","camera_panel",(217,39,12,12),False),
    ("closet3","camera_panel",(273,39,12,12),False),
    ("music_box","camera_panel",(44,80,91,21),False),
    ("wall0","main_room",(11,98,19,27),True),
    ("wall1","main_room",(462,98,19,27),True),
    ("wall2","camera_panel",(201,95,4,4),False),
    ("wall3","camera_panel",(273,63,4,4),False),
    ("deceive","camera_panel",(201,47,4,4),False),
    ("light0","main_room",(11,138,19,27),True),
    ("light1","main_room",(462,138,19,27),True),
    ("camera_light","camera_panel",(10,10,160,160),False),
    ("mask_on","main_room",(51,161,89,12),False),
    ("new_game","menu",(55,55,105,25),False),
    ("continue","menu",(55,80,105,25),False)
]

MONSTERS = [
    (1,"chica","normal","closet1"),
    (2,"foxy","normal","reception"),
    (3,"puppet","normal","closet3"),
    (4,"mangle","all","closet1"),
    (5,"ennard","all","closet2"),
]

ROOMS_MAP = {
    "closet1":[("party_room","normal")],
    "closet2":[("reception","normal"),("vents4","vents")],
    "closet3":[("reception","normal")],
    "reception":[("closet2","normal"),("closet3","normal"),("party_room","wall3")],
    "party_room":[("reception","normal"),("closet1","normal"),("vents4","vents"),("corridor1","wall2"),("vents2","vents"),("kitchen","normal")],
    "kitchen":[("vents3","vents"),("corridor2","normal"),("party_room","normal")],
    "corridor1":[("main_room","wall0"),("party_room","normal"),("vents","vents")],
    "corridor2":[("main_room","wall1"),("vents2","vents"),("kitchen","normal"),("vents1","vents")],
    "main_room":[("corridor1","wall0"),("corridor2","wall1"),("vents1","vents")],
    "vents1":[("main_room","vents"),("corridor2","vents")],
    "vents2":[("party_room","vents"),("corridor2","vents")],
    "vents3":[("corridor1","vents"),("kitchen","vents")],
    "vents4":[("party_room","vents"),("closet2","vents")]
}

ROOM_PRIORITY = {
    "chica":{"closet1":1,"closet2":1,"closet3":1,"reception":1,"party_room":2,"kitchen":1,"corridor1":1,"corridor2":1,"main_room":2},
    "foxy":{"closet1":1,"closet2":1,"closet3":1,"reception":1,"party_room":2,"kitchen":1,"corridor1":2,"corridor2":2,"main_room":3},
    "puppet":{"closet1":0,"closet2":0,"closet3":0,"reception":0,"party_room":1,"kitchen":1,"corridor1":2,"corridor2":2,"main_room":3},
    "mangle":{"closet1":1,"closet2":1,"closet3":1,"reception":1,"party_room":2,"kitchen":2,"corridor1":2,"corridor2":2,"main_room":3,"vents1":3,"vents2":2,"vents3":2,"vents4":1},
    "ennard":{"closet1":1,"closet2":1,"closet3":1,"reception":1,"party_room":2,"kitchen":1,"corridor1":1,"corridor2":1,"main_room":2,"vents1":2,"vents2":2,"vents3":2,"vents4":1},
}

FAKE_ROOM_PRIORITY = {
    "closet1":0,
    "closet2":2,
    "closet3":0,
    "reception":3,
    "party_room":2,
    "kitchen":1,
    "corridor1":1,
    "corridor2":1,
    "main_room":0
}

POWER_USE = {
    "room_walls":0.01,
    "other_walls":0.005,
    "light":0.003,
    "cameras":0.001
}

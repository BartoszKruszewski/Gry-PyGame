from pygame import Vector2, Color, Rect

SCREEN_SIZE = Vector2(1280, 720)
DRAW_SCREEN_SIZE = Vector2(1280, 720)
STANDARD_FRAMERATE = 60
FRAMERATE = 120

EDITOR_POINT_SIZE = 10

EDITOR_DEFAULT_COLOR = Color(255, 255, 255)

EDITOR_QUEUE_FRAME_SIZE = Vector2(0.18, 0.8)
EDITOR_QUEUE_FIRST_FRAME_POS = Vector2(0.05, 0.1)
EDITOR_QUEUE_INTERLUDE = 0.05
EDITOR_QUEUE_COLOR = Color(200, 200, 200)

BUTTON_FRAME_SIZE = 5
BUTTON_LIGHTEN = 30

EDITOR_COLOR_NAMES = {
    "red": Color(255, 0, 0),
    "green": Color(0, 255, 0),
    "blue": Color(0, 0, 255),
    "yellow": Color(255, 255, 0)
}

EDITOR_COLORS = {
    "selected_point": Color(255, 255, 0, 255),
    "actual_point": Color(255, 0, 0, 200),
    "actual_relation": Color(255, 255, 255, 200),
    "previous_point": Color(200, 0, 255, 100),
    "previous_relation": Color(0, 50, 255, 100),
    "next_point": Color(255, 10, 200, 100),
    "next_relation": Color(200, 255, 100, 100),
}

WINDOWS = ["draw", "colors", "tools", "info", "queue"]

WINDOW_SIZES = {
    "draw": Vector2(0.7, 0.7),
    "colors": Vector2(0.3, 0.3),
    "tools": Vector2(0.3, 0.7),
    "info": Vector2(0.7, 0.1),
    "queue": Vector2(0.7, 0.2)
}

WINDOW_POSITIONS = {
    "draw": Vector2(0.0, 0.0),
    "colors": Vector2(0.7, 0.0),
    "tools": Vector2(0.7, 0.3),
    "info": Vector2(0.0, 0.9),
    "queue": Vector2(0.0, 0.7)
}

WINDOW_COLORS = {
    "draw": Color(20, 20, 20),
    "colors": Color(20, 20, 20),
    "tools": Color(20, 20, 20),
    "info": Color(20, 20, 20),
    "queue": Color(20, 20, 20)
}

WINDOW_BUTTONS = {
    "draw": [],
    "colors": ["red", "blue", "green", "yellow"],
    "tools": [
        "new_point", "add_relation", "remove_relation", "next_frame",
        "previous_frame"],
    "info": [],
    "queue": []
}

BUTTONS_SIZES = {
    "new_point": Vector2(0.2, 0.15),
    "add_relation": Vector2(0.2, 0.15),
    "remove_relation": Vector2(0.2, 0.15),
    "next_frame": Vector2(0.2, 0.15),
    "previous_frame": Vector2(0.2, 0.15),
    "red": Vector2(0.15, 0.3),
    "blue": Vector2(0.15, 0.3),
    "green": Vector2(0.15, 0.3),
    "yellow": Vector2(0.15, 0.3)
}

BUTTONS_POSITIONS = {
    "new_point": Vector2(0.05, 0.05),
    "add_relation": Vector2(0.05, 0.25),
    "remove_relation": Vector2(0.33, 0.25),
    "next_frame": Vector2(0.05, 0.45),
    "previous_frame": Vector2(0.33, 0.45),
    "red": Vector2(0.05, 0.15),
    "blue": Vector2(0.25, 0.15),
    "green": Vector2(0.45, 0.15),
    "yellow": Vector2(0.65, 0.15)
}

BUTTONS_COLORS = {
    "new_point": Color(100, 100, 100),
    "add_relation": Color(100, 100, 100),
    "remove_relation": Color(100, 100, 100),
    "next_frame": Color(100, 100, 100),
    "previous_frame": Color(100, 100, 100),
    "red": Color(255, 0, 0),
    "blue": Color(0, 0, 255),
    "green": Color(0, 255, 0),
    "yellow": Color(255, 255, 0)
}

BUTTONS_FUNCTIONS = {
    "new_point": "new_point",
    "add_relation": "add_relation",
    "remove_relation": "remove_relation",
    "next_frame": "next_frame",
    "previous_frame": "previous_frame",
    "red": "red",
    "green": "green",
    "blue": "blue",
    "yellow": "yellow",
}

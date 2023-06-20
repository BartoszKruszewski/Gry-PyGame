from point import Point
from point_map import PointMap
from relation import Relation
from animation import Animation
from mouse import Mouse
from pygame import *
from const import *
from draw import Draw
from window import Window
from frame_button import FrameButton


class Main:
    def __init__(self):
        self.screen = display.set_mode(SCREEN_SIZE)
        self.draw_screen = Surface(DRAW_SCREEN_SIZE)
        self.is_running = True
        self.dt = 1
        self.clock = time.Clock()
        self.mouse = Mouse()
        self.animation = Animation()
        self.selected_points = []
        self.frame_counter = 0
        self.actual_tool = None
        self.actual_color = EDITOR_DEFAULT_COLOR
        self.keys = {
            "shift": False,
            "ctrl": False,
            "alt": False,
        }
        self.windows = {name: Window(
            WINDOW_SIZES[name],
            WINDOW_POSITIONS[name],
            WINDOW_COLORS[name],
            WINDOW_BUTTONS[name])
            for name in WINDOWS}

        self.button_states = {}
        for window_name in WINDOWS:
            for button_name in WINDOW_BUTTONS[window_name]:
                self.button_states[button_name] = False

        self.animation.add_frame(0, PointMap())

        while self.is_running:
            self.check_events()
            self.check_keys()
            self.mouse.update()
            self.update()
            self.draw()
            self.display_update()

        self.animation.save("Animations/test5")

    def check_keys(self):
        keys = key.get_pressed()
        self.keys["shift"] = keys[K_LSHIFT]
        self.keys["ctrl"] = keys[K_LCTRL]
        self.keys["alt"] = keys[K_LALT]

    def check_events(self):
        for e in event.get():
            if e.type == WINDOWCLOSE:
                self.is_running = False

    def __get_next_point(self):
        return Point(
            f"punkt{len(self.animation.frames[self.frame_counter].points)}",
            Vector2(self.mouse.rect.x, self.mouse.rect.y))

    def __get_new_relation(self, points):
        relation = Relation([point.name for point in points])
        relation.properties["color"] = self.actual_color
        return relation

    def __change_selected_point(self, point):
        while point in self.selected_points:
            self.selected_points.remove(point)
        self.selected_points.append(point)

    def update_button_actions(self):
        if any(self.button_states.values()):
            for action_type in self.button_states:
                if action_type in WINDOW_BUTTONS["tools"]:
                    if self.button_states[action_type]:
                        self.actual_tool = action_type
                        self.button_states[action_type] = False
                elif action_type in WINDOW_BUTTONS["colors"]:
                    if self.button_states[action_type]:
                        self.actual_color = EDITOR_COLOR_NAMES[action_type]
                        self.button_states[action_type] = False
                elif action_type[:5] == "frame":
                    self.frame_counter = int(action_type[5:])
        else:
            if (not self.windows["draw"].hovered) and self.mouse.left_click:
                self.actual_tool = None
                self.selected_points = []

    def update(self):
        print(self.frame_counter)
        for window in self.windows.values():
            window.update(self.mouse, self.button_states)

        self.update_button_actions()

        if self.windows["draw"].hovered:
            hovered = None
            for point in self.animation.frames[self.frame_counter].points:
                if Vector2(self.mouse.rect.x, self.mouse.rect.y).distance_to(
                        point.pos) <\
                        EDITOR_POINT_SIZE * DRAW_SCREEN_SIZE.x / SCREEN_SIZE.x:
                    hovered = point
                    break

            match self.actual_tool:
                case "new_point":
                    if self.mouse.left_click:
                        if hovered is None:
                            self.__change_selected_point(
                                self.__get_next_point())
                            self.animation.frames[self.frame_counter].add_point(
                                self.selected_points[-1])
                case "add_relation":
                    if hovered is not None:
                        if self.mouse.left_click:
                            self.__change_selected_point(hovered)
                            if len(self.selected_points) >= 2:
                                self.animation.add_relation(
                                    self.__get_new_relation(
                                        self.selected_points[-2:]))
                case "remove_relation":
                    if hovered is not None:
                        if self.mouse.left_click:
                            self.__change_selected_point(hovered)
                            if len(self.selected_points) >= 2:
                                self.animation.remove_relations(
                                    self.selected_points[-2:])
                case default:
                    if self.mouse.left_switch:
                        if hovered is None:
                            if len(self.selected_points) > 0:
                                self.selected_points[-1].pos =\
                                    Vector2(
                                        self.mouse.rect.x, self.mouse.rect.y)
                        else:
                            self.__change_selected_point(hovered)

        match self.actual_tool:
            case "next_frame":
                self.frame_counter += 1
                if self.frame_counter >= len(self.animation.frames):
                    self.animation.add_frame(
                        self.frame_counter,
                        self.animation.get_point_map(self.frame_counter - 1))
                    self.windows["queue"].add_button(
                        Vector2(
                            EDITOR_QUEUE_FIRST_FRAME_POS.x +
                            (EDITOR_QUEUE_FRAME_SIZE.x +
                             EDITOR_QUEUE_INTERLUDE) * (self.frame_counter - 1),
                            EDITOR_QUEUE_FIRST_FRAME_POS.y
                        ),
                        EDITOR_QUEUE_FRAME_SIZE,
                        f"frame{self.frame_counter}",
                        EDITOR_QUEUE_COLOR,
                        FrameButton,
                        image = self.animation.get_frame(
                            self.frame_counter)
                    )
                self.selected_points = []
                self.actual_tool = None
            case "previous_frame":
                if self.frame_counter > 0:
                    self.frame_counter -= 1
                    self.selected_points = []
                self.actual_tool = None

    def display_update(self):
        self.dt = self.clock.tick(FRAMERATE) * STANDARD_FRAMERATE / 1000
        self.screen.blit(transform.scale(self.draw_screen, SCREEN_SIZE), (0, 0))
        display.update()

    def draw_relations(self, relations, point_map, draw_color = None):
        for relation in relations:
            relation_to_draw = relation.copy()
            if draw_color is not None:
                relation_to_draw.properties["color"] = draw_color
            Draw.draw_shape(self.draw_screen, relation_to_draw, point_map)

    def draw_point_map(self, point_map, draw_color):
        for point in point_map.points:
            draw.circle(
                self.draw_screen, draw_color, point.pos,
                EDITOR_POINT_SIZE * DRAW_SCREEN_SIZE.x / SCREEN_SIZE.x)

    def draw_animation(self):
        if self.frame_counter > 0:
            self.draw_relations(
                self.animation.relations,
                self.animation.get_point_map(self.frame_counter - 1),
                EDITOR_COLORS["previous_relation"])
            self.draw_point_map(
                self.animation.get_point_map(self.frame_counter - 1),
                EDITOR_COLORS["previous_point"])
        if self.frame_counter + 1 < len(self.animation.frames):
            self.draw_relations(
                self.animation.relations,
                self.animation.get_point_map(self.frame_counter + 1),
                EDITOR_COLORS["next_relation"])
            self.draw_point_map(
                self.animation.get_point_map(self.frame_counter + 1),
                EDITOR_COLORS["next_point"])
        self.draw_relations(
            self.animation.relations, self.animation.get_point_map(
                self.frame_counter))
        self.draw_point_map(
            self.animation.get_point_map(self.frame_counter),
            EDITOR_COLORS["actual_point"])
        if len(self.selected_points) > 0:
            draw.circle(
                self.draw_screen, EDITOR_COLORS["selected_point"],
                self.selected_points[-1].pos,
                EDITOR_POINT_SIZE * DRAW_SCREEN_SIZE.x / SCREEN_SIZE.x)

    def draw_windows(self):
        for window in self.windows.values():
            window.draw(self.draw_screen)

    def draw(self):
        self.draw_screen.fill((0, 0, 0))
        self.draw_windows()
        self.draw_animation()

    def load_point_map(self):
        pass


if __name__ == "__main__":
    Main()

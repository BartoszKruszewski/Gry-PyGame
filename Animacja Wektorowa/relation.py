from pygame import Color
from copy import deepcopy
from point_map import PointMap


class Relation:
    def __init__(self, point_names: list[str], properties = None):
        self.point_names = point_names
        if properties is None:
            self.properties = {
                "color": Color(255, 255, 255),
                "fill": False,
                "aa": False,
                "bezier": 0
            }
        else:
            self.properties = properties

    def load_properties(self, properties: dict):
        if "color" in properties:
            color_data = [int(x) for x in properties["color"][1:-1].split(
                ",")]
            self.properties["color"] = Color(
                color_data[0], color_data[1],
                color_data[2])
        if "fill" in properties:
            self.properties["fill"] = True if properties["fill"] == "True"\
                else False
        if "bezier" in properties:
            self.properties["bezier"] = int(properties["bezier"])
        if "aa" in properties:
            self.properties["aa"] = True if properties["aa"] == "True" else\
                False

    def is_drawable(self, point_map: PointMap) -> bool:
        point_names = [point.name for point in point_map.points]
        return all([(name in point_names) for name in self.point_names])

    def copy(self):
        return Relation(deepcopy(self.point_names), deepcopy(self.properties))

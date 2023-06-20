from pygame.gfxdraw import line, bezier, polygon, filled_polygon, aapolygon
from pygame import Vector2, Surface, Color
from relation import Relation
from point_map import PointMap


class Draw:
    @staticmethod
    def draw_shape(
            surf: Surface, relation: Relation, point_map: PointMap,
            shift = Vector2(0, 0)):

        if relation.is_drawable(point_map):
            points = [
                (int(p.x), int(p.y)) for p in
                (point.pos - shift for point in
                    (point_map[name] for name in relation.point_names))
            ]

            if relation.properties["bezier"] >= 2:
                bezier(
                    surf, points, relation.properties["bezier"],
                    relation.properties["color"])
            elif len(points) == 2:
                x1 = points[0][0]
                y1 = points[0][1]
                x2 = points[1][0]
                y2 = points[1][1]
                line(surf, x1, y1, x2, y2, relation.properties["color"])
            else:
                if relation.properties["fill"]:
                    filled_polygon(surf, points, relation.properties["color"])
                elif relation.properties["aa"]:
                    aapolygon(surf, points, relation.properties["color"])
                else:
                    polygon(surf, points, relation.properties["color"])

    @staticmethod
    def adjust_color(color: Color, amount: int):
        return Color(
            min(max(color.r + amount, 0), 255),
            min(max(color.g + amount, 0), 255),
            min(max(color.b + amount, 0), 255),
            color.a)

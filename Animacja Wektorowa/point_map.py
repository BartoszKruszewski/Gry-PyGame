from pygame import Vector2
import pygame.gfxdraw
from copy import deepcopy
from point import Point


class PointMap:
    def __init__(self, points = None):
        if points is None:
            points = []
        self.__points = points

    @property
    def points(self):
        return self.__points

    def add_point(self, point: Point):
        self.__points.append(point)

    def copy(self):
        return PointMap(deepcopy(self.__points))

    def scale_ip(self, value: float):
        for point in self.__points:
            point.pos *= value

    def scale(self, value: float):
        new_point_map = self.copy()
        new_point_map.scale_ip(value)
        return new_point_map

    def get_size(self) -> Vector2:
        if len(self.__points) > 0:
            x = max(self.__points, key = lambda point: point.pos.x).pos.x
            y = max(self.__points, key = lambda point: point.pos.y).pos.y
            return Vector2(x, y)
        return Vector2(0, 0)

    def get_coordinate_begin(self) -> Vector2:
        if len(self.__points) > 0:
            x = min(self.__points, key = lambda point: point.pos.x).pos.x
            y = min(self.__points, key = lambda point: point.pos.y).pos.y
            return Vector2(x, y)
        return Vector2(0, 0)

    def __getitem__(self, item) -> Point:
        for point in self.__points:
            if point.name == item:
                return point

    @staticmethod
    def load(file_name: str):
        data = [
            line.rstrip()
            for line in open(file_name, "r").readlines()
        ]

        points = []

        for line in data:
            name, pos = line.replace(" ", "").split(":")
            x, y = pos.split(",")
            points.append(Point(name, pygame.Vector2(float(x), float(y))))

        return PointMap(points)

    def save(self, filename: str):
        file = open(filename, "w")
        for point in self.__points:
            file.write(f"{point.name}: {point.pos.x}, {point.pos.y}\n")
        file.close()

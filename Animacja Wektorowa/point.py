from pygame import Vector2


class Point:
    def __init__(self, name: str, pos: Vector2):
        self.name = name
        self.pos = pos

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __str__(self) -> str:
        return f"<{self.name}:({self.pos.x}, {self.pos.y})>"

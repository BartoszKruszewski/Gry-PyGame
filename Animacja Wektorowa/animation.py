from pygame import Surface, Vector2
from point_map import PointMap
from relation import Relation
from os import listdir, mkdir, path
from draw import Draw


class Animation:
    def __init__(self, frames = None, relations = None):
        self.__frames = {} if frames is None else frames
        self.__relations = [] if relations is None else relations
        self.__rendered_frames = {}
        self.__coordinate_begin = self.__get_coordinate_begin()
        self.__size = self.__get_frame_size()
        self.length = self.__get_length()

    @property
    def frames(self):
        return self.__frames

    @property
    def relations(self):
        return self.__relations

    def __get_frame_size(self) -> Vector2:
        if len(self.__frames) > 0:
            sizes = [point_map.get_size() for point_map in self.__frames.values()]
            x = max(sizes, key = lambda size: size.x).x
            y = max(sizes, key = lambda size: size.y).y
            return Vector2(x, y) - self.__coordinate_begin
        return Vector2(0, 0)

    def __get_coordinate_begin(self) -> Vector2:
        if len(self.__frames) > 0:
            sizes = [
                point_map.get_coordinate_begin() for point_map in
                self.__frames.values()
            ]
            x = min(sizes, key = lambda size: size.x).x
            y = min(sizes, key = lambda size: size.y).y
            return Vector2(x, y)
        return Vector2(0, 0)

    def __get_length(self) -> int:
        if len(self.__frames) > 0:
            return max(self.__frames)
        return 0

    def __calculate_point_map(self, new_frame_id: int):
        previous_frame_id = 0
        next_frame_id = 0
        for frame_id in sorted(self.__frames):
            if frame_id < new_frame_id:
                previous_frame_id = frame_id
            else:
                next_frame_id = frame_id
                break

        scale = (new_frame_id - previous_frame_id) / (next_frame_id -
                                                      previous_frame_id)
        new_point_map = self.__frames[previous_frame_id].copy()

        for point in new_point_map.points:
            if self.__frames[next_frame_id][point.name] is None:
                continue
            dest_pos = self.__frames[next_frame_id][point.name].pos
            point.pos.move_towards_ip(
                dest_pos, point.pos.distance_to(
                    dest_pos) * scale)
        self.add_frame(new_frame_id, new_point_map)

    def render(self, frame_id: int):
        if frame_id not in self.__frames:
            self.__calculate_point_map(frame_id)
        point_map = self.__frames[frame_id]
        surf = Surface(self.__size)
        for relation in self.__relations:
            Draw.draw_shape(surf, relation, point_map, self.__coordinate_begin)
        self.__rendered_frames[frame_id] = surf

    def get_frame(self, frame_id: int) -> Surface:
        if frame_id not in self.__rendered_frames:
            self.render(frame_id)
        return self.__rendered_frames[frame_id]

    def get_point_map(self, frame_id: int) -> PointMap:
        if frame_id in self.__frames:
            return self.__frames[frame_id].copy()
        raise Exception("Frame index out of range!")

    def add_frame(self, frame_id, point_map):
        self.__frames[frame_id] = point_map
        self.__coordinate_begin = self.__get_coordinate_begin()
        self.__size = self.__get_frame_size()
        self.length = max(self.__frames)

    def add_relation(self, relation):
        self.__relations.append(relation)

    def remove_relations(self, points):
        for relation in self.__relations:
            if sorted(relation.point_names) ==\
                    sorted([point.name for point in points]):
                self.__relations.remove(relation)
                break

    @staticmethod
    def load(filename: str):
        keyframes = dict(
            map(
                lambda l: l.split(":"),
                open(f"{filename}/key_frames.txt", "r").readlines()))

        frames = {}
        for map_name in listdir(filename):
            if map_name not in ["key_frames.txt", "relations.txt"]:
                frames[int(keyframes[map_name[:-4]])] = PointMap.load(
                    f"{filename}/{map_name}")

        relations = []
        for line in open(f"{filename}/relations.txt", "r").readlines():
            names, properties = line.replace(" ", "").split("*")
            properties = dict((p.split("=") for p in properties.split(";")))
            relation = Relation(names.split(":"))
            relation.load_properties(properties)
            relations.append(relation)

        return Animation(frames, relations)

    def save(self, filename: str):
        if not path.exists(filename):
            mkdir(filename)
        file = open(f"{filename}/key_frames.txt", "w")
        for i, frame in enumerate(self.__frames):
            file.write(f"frame{i}:{frame}\n")
            self.__frames[frame].save(f"{filename}/frame{i}.txt")
        file.close()

        file = open(f"{filename}/relations.txt", "w")
        for relation in self.__relations:
            names = ""
            for name in relation.point_names:
                names += f"{name}:"
            file.write(f"{names[:-1]} * ")
            properties = ""
            for prop in relation.properties:
                properties += f"{prop} = {relation.properties[prop]}; "
            file.write(f"{properties[:-2]}\n")
        file.close()

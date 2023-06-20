import math, pygame
from CONST import MAP_SIZE, SCALE

def pos_to_string(pos):
    return str(pos[0]) + ":" + str(pos[1])

def pos_to_int(pos):
    new_pos = pos.split(":")
    new_pos[0] = int(new_pos[0])
    new_pos[1] = int(new_pos[1])
    return new_pos

def get_points_in_radius(pos, R):
    points_in_square = []
    for x in range(int(R * 2) + 2):
        for y in range(int(R * 2) + 2):
            points_in_square.append([x + pos[0] - int(R) - 1, y + pos[1] - int(R) - 1])
    points_in_radius = []
    global_pos = global_center_of(pos)
    for point in points_in_square:
        global_point = global_center_of(point)
        if distance(global_pos,global_point) <= R * SCALE:
            points_in_radius.append(point)
    return points_in_radius

def global_center_of(pos):
    return [pos[0] * SCALE + SCALE/2 , pos[1] * SCALE + SCALE/2]

def normalize_target(target,obstacles,troop_pos,R):
    if target not in obstacles:
        return target

    around = get_points_in_radius(target,R)
    posible_targets = []
    for point in around:
        if point not in target:
            posible_targets.append(point)

    return get_nearest(posible_targets,troop_pos)

def get_nearest(points,target):
    nearest = MAP_SIZE[0]
    new_target = None
    for point in points:
        dist = distance(point,target)
        if dist < nearest:
            nearest = dist
            new_target = point.copy()
    return new_target

def get_around_objects(objects,self_tiles,R):
    around = get_points_in_radius(get_center_tile(self_tiles),R)
    around_objects = []
    for game_object in objects:
        if game_object.pos in around:
            around_objects.append(game_object)
    return around_objects

def distance(point1,point2):
    return math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2))

def get_free_near_pos(self_tiles,obstacles,R):
    around = get_points_in_radius(get_center_tile(self_tiles),R)
    free_points = []
    for point in around:
        if point not in obstacles and point not in self_tiles:
            free_points.append(point)
    return free_points

def get_center_tile(tiles):
    if len(tiles) > 1:
        if len(tiles) == 4:
            return tiles[0]
        else:
            return tiles[4]
    else:
        return tiles[0]

def get_best_near_pos(self_tiles,obstacles,troop_pos,R):
    free_points = get_free_near_pos(self_tiles,obstacles,R)
    return get_nearest(free_points, troop_pos)

def liveBar(actual_state,size,color):
    surf = pygame.Surface(size)
    surf.fill((0,0,0))
    surf.fill((255,255,255),(1,1,size[0]-2,size[1]-2))
    surf.fill(color, (1, 1, min(int((size[0] - 2) * actual_state),size[0]-2), size[1] - 2))
    surf.set_colorkey((255,255,255))
    return surf

def get_direction(point1,point2):
    x = point1[0] - point2[0]
    y = point1[1] - point2[1]
    if abs(x) > abs(y):
        if x >= 0:
            return "left"
        else:
            return "right"
    else:
        if y >= 0:
            return "up"
        else:
            return "down"

def modify_surf(surf,func_name):
    def darken(color):
        DARKEN = 20
        return (max(color[0] - DARKEN, 0), max(color[1] - DARKEN, 0), max(color[2] - DARKEN, 0))

    new_surf = surf.copy()
    for x in range(surf.get_width()):
        for y in range(surf.get_height()):
            color = surf.get_at((x,y))
            new_color = eval(func_name + "(color)")
            new_surf.set_at((x,y),new_color)
    return new_surf
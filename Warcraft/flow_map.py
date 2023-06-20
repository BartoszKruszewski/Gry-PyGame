from FUNCTIONS import *
from CONST import MAP_SIZE

class FlowMap():
    def __init__(self):
        self.map = {}
        self.start = False

    def update(self,target,obstacles):
        def get_best_tile():
            minimum = INF + 1
            minimum_adress = ""
            for key in Q.keys():
                if Q[key] < minimum:
                    minimum = Q[key]
                    minimum_adress = key

            return pos_to_int(minimum_adress)

        # CREATE PATH MAP
        INF = 999
        Q = {}

        for y in range(MAP_SIZE[1]):
            for x in range(MAP_SIZE[0]):
                Q[pos_to_string([x,y])] = INF
        Q[pos_to_string(target)] = 0

        appointed = {}

        while len(Q) > 0:
            v_adress = get_best_tile()
            v_cost = Q[pos_to_string(v_adress)]
            Q.pop(pos_to_string(v_adress))

            around_tiles = [
                [v_adress[0] + 1,v_adress[1]],
                [v_adress[0],v_adress[1] + 1],
                [v_adress[0] - 1,v_adress[1]],
                [v_adress[0],v_adress[1] - 1]
            ]

            for tile in around_tiles:
                if tile[0] >= 0 and tile[1] >= 0 and tile[0] < MAP_SIZE[0] and tile[0] < MAP_SIZE[0]:
                    cost = v_cost + 1
                    if pos_to_string(tile) in Q.keys():
                        Q[pos_to_string(tile)] = cost
                    appointed[pos_to_string(tile)] = cost

        for key in appointed.keys():
            if pos_to_int(key) in obstacles:
                appointed[key] = INF


        # CREATE FLOW MAP
        self.map.clear()
        for tile_adress in appointed.keys():

            # get cost
            split = tile_adress.split(":")
            path_adress = [int(split[0]),int(split[1])]
            cost = appointed[tile_adress]

            # get around tiles
            around_tiles_adresses = []
            if not pos_to_string([path_adress[0] + 1,path_adress[1]]) in self.map.keys() or self.map[pos_to_string([path_adress[0] + 1,path_adress[1]])] != "left":
                around_tiles_adresses.append([path_adress[0] + 1,path_adress[1]])
            if not pos_to_string([path_adress[0] - 1,path_adress[1]]) in self.map.keys() or self.map[pos_to_string([path_adress[0] - 1,path_adress[1]])] != "right":
                around_tiles_adresses.append([path_adress[0] - 1,path_adress[1]])
            if not pos_to_string([path_adress[0],path_adress[1] + 1]) in self.map.keys() or self.map[pos_to_string([path_adress[0],path_adress[1] + 1])] != "up":
                around_tiles_adresses.append([path_adress[0],path_adress[1] + 1])
            if not pos_to_string([path_adress[0],path_adress[1] - 1]) in self.map.keys() or self.map[pos_to_string([path_adress[0],path_adress[1] - 1])] != "down":
                around_tiles_adresses.append([path_adress[0],path_adress[1] - 1])

            around_tiles = []
            for tile_adress in around_tiles_adresses:
                if tile_adress[0] >= 0 and tile_adress[1] >= 0 and tile_adress[0] < MAP_SIZE[0] and tile_adress[1] < MAP_SIZE[1]:
                    around_tiles.append((appointed[str(tile_adress[0]) + ":" + str(tile_adress[1])],tile_adress))


            # set lowest cost path
            if len(around_tiles) > 0:
                best_tiles = []
                minimum = around_tiles[0][0]

                for tile in around_tiles:
                    if tile[0] < minimum:
                        minimum = tile[0]
                        best_tiles.clear()
                        best_tiles.append(tile[1])
                    elif tile[0] == minimum:
                        best_tiles.append(tile[1])

                lowest = INF
                for tile in best_tiles:
                    dist = math.sqrt(math.pow(tile[0] - target[0],2) + math.pow(tile[1] - target[1],2))
                    if dist < lowest:
                        lowest = dist
                        minimum_adress = tile

            # set direction
            direction = ""
            if minimum_adress[1] < path_adress[1]:
                direction += "up"
            elif minimum_adress[1] > path_adress[1]:
                direction += "down"
            elif minimum_adress[0] > path_adress[0]:
                direction += "right"
            elif minimum_adress[0] < path_adress[0]:
                direction += "left"

            if path_adress == target:
                direction = "target"

            # add to flow_map
            self.map[pos_to_string(path_adress)] = direction
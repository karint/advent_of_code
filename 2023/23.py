import math
import os
import sys

from collections import defaultdict
from util import OPPOSITE_DIRECTIONS, Direction, get_cardinal_direction_coords, run
from termcolor import colored

COLORS = [
    # 'black',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    # 'white',
    # 'light_grey',
    # 'dark_grey',
    'light_red',
    'light_green',
    'light_yellow',
    'light_blue',
    'light_magenta',
    'light_cyan',
]


DIRECTION_MAP = {
    '>': [Direction.RIGHT],
    '<': [Direction.LEFT],
    '^': [Direction.UP],
    'v': [Direction.DOWN],
}


class Tunnel:
    def __init__(self, id_, path):
        self.id = id_
        self.path = path
        self.adjacent_connector_coords = set()

    @property
    def size(self):
        return len(self.path)

class Node:
    """
    A node that sits between tunnels and connects them.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.adjacent_tunnel_ids = set()


def is_adjacent(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return abs(x1 - x2) + abs(y1 - y2) == 1


class Solver:
    def __init__(self, grid):
        self.grid = grid
        self.min_x, self.max_x = 1, len(self.grid[0]) - 1
        self.min_y, self.max_y = 1, len(self.grid) - 1
        self.num_steps = 0
        self.start_coord = (1, 0)
        self.goal_coord = (self.max_x - 1, self.max_y)
        self.blocked = set()

        self.wall_coords = set()
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if char == '#':
                    self.wall_coords.add((x, y))

        self.tunnel_map = {}
        self.tunnel_connector_nodes = {}
        self.start_tunnel_id = None
        self.goal_tunnel_id = None

    def explore_tunnel(self, curr_tunnel, visited):
        curr_coord = curr_tunnel.path[-1]
        x, y = curr_coord
        visited.add(curr_coord)

        next_coords = get_cardinal_direction_coords(
            x, y,
            blocked=visited,
            grid=self.grid,
        )
        for _, nx, ny in next_coords:
            next_coord = (nx, ny)
            curr_tunnel.path.append(next_coord)
            symbol = self.grid[ny][nx]
            if symbol in DIRECTION_MAP or next_coord == self.goal_coord:
                visited.add(next_coord)
                return nx, ny
            return self.explore_tunnel(curr_tunnel, visited)
        return curr_coord

    def populate_tunnels(self):
        """
        The "maze" can be simplified to a graph of tunnels where a tunnel
        represents a single path between forks in the road. Hopefully by simplifying
        the space to fewer nodes, we can get a reasonable time for brute force.
        """
        tunnels = []
        tunnel_id = 0
        self.start_tunnel_id = tunnel_id
        visited = set(self.wall_coords)
        paths = [self.start_coord]

        while paths:
            new_paths = []
            for x, y in paths:
                curr_coord = (x, y)
                if curr_coord in visited:
                    continue

                symbol = self.grid[y][x]
                if symbol in DIRECTION_MAP or (x, y) == self.start_coord:
                    # New tunnel
                    curr_tunnel = Tunnel(tunnel_id, [curr_coord])
                    tunnels.append(curr_tunnel)
                    tunnel_id += 1

                    curr_coord = self.explore_tunnel(curr_tunnel, visited)
                    x, y = curr_coord
                    symbol = self.grid[y][x]
                else:
                    self.tunnel_connector_nodes[curr_coord] = Node(*curr_coord)
                    visited.add(curr_coord)

                next_coords = get_cardinal_direction_coords(
                    x, y,
                    # Respect directions as in Part 1 so this finishes efficiently
                    directions=DIRECTION_MAP.get(symbol),
                    blocked=visited,
                    grid=self.grid
                )
                viable_neighbors = []
                for _, nx, ny in next_coords:
                    next_coord = (nx, ny)
                    new_paths.append((
                        nx,
                        ny,
                    ))

            paths = new_paths

        self.tunnel_map = {t.id: t for t in tunnels}

        for tunnel_id, tunnel in self.tunnel_map.items():
            start_coord = tunnel.path[0]
            end_coord = tunnel.path[-1]

            # If adjacent to a connector, set as neighbor of that connector
            for connector_coord, node in self.tunnel_connector_nodes.items():
                if is_adjacent(start_coord, connector_coord):
                    node.adjacent_tunnel_ids.add(tunnel_id)
                    tunnel.adjacent_connector_coords.add(connector_coord)
                if is_adjacent(end_coord, connector_coord):
                    node.adjacent_tunnel_ids.add(tunnel_id)
                    tunnel.adjacent_connector_coords.add(connector_coord)

            if end_coord == self.goal_coord:
                self.goal_tunnel_id = tunnel_id

        # self.print_tunnels()
        # for coord, node in self.tunnel_connector_nodes.items():
        #     print(coord, node.adjacent_tunnel_ids)

    def print_tunnels(self, tunnel_ids=None):
        # Print the paths
        coord_to_tunnel_id = {
            (x, y): id_
            for id_, tunnel in self.tunnel_map.items()
            for (x, y) in tunnel.path
        }

        if tunnel_ids:
            coord_to_tunnel_id = {
                (x, y): id_
                for id_, tunnel in self.tunnel_map.items()
                for (x, y) in tunnel.path
                if id_ in tunnel_ids
            }
        else:
            coord_to_tunnel_id = {
                (x, y): id_
                for id_, tunnel in self.tunnel_map.items()
                for (x, y) in tunnel.path
            }

        for y, row in enumerate(self.grid):
            string = ''
            for x, char in enumerate(row):
                coord = (x, y)
                if coord in self.wall_coords:
                    string += '#'.rjust(2)
                elif coord in self.tunnel_connector_nodes:
                    string += '+'.rjust(2)
                elif coord in coord_to_tunnel_id:
                    tunnel_id = coord_to_tunnel_id[coord]
                    string += colored(str(tunnel_id).rjust(2), COLORS[tunnel_id % len(COLORS)])
                elif coord in self.blocked:
                    string += 'O'.rjust(2)
                else:
                    string += char.rjust(2)
            print(string)

    def simulate(self):
        self.populate_tunnels()
        return self.find_longest_path()

    def find_longest_path(self):
        return self.get_longest_path(self.start_tunnel_id, set(), set())

    def get_longest_path(self, curr_tunnel_id, visited_tunnel_ids, visited_connector_coords):
        curr_node = self.tunnel_map[curr_tunnel_id]
        visited_tunnel_ids.add(curr_tunnel_id)

        if curr_tunnel_id == self.goal_tunnel_id:
            longest_distance = (
                sum(self.tunnel_map[id_].size for id_ in visited_tunnel_ids) +
                len(visited_connector_coords)
            ) - 1  # Subtract one because the first step of the first tunnel is step 0
            self.print_tunnels(tunnel_ids = visited_tunnel_ids)
            print()
            return longest_distance

        viable_neighbors = set()
        for connector_coord in curr_node.adjacent_connector_coords:
            if connector_coord in visited_connector_coords:
                continue

            viable_neighbors |= set(
                (neighbor_tunnel_id, connector_coord)
                for neighbor_tunnel_id in (
                    self.tunnel_connector_nodes[connector_coord].adjacent_tunnel_ids -
                    visited_tunnel_ids
                )
            )

        if not viable_neighbors:
            return 0

        return max(
            self.get_longest_path(
                neighbor_tunnel_id,
                set(visited_tunnel_ids) | set([neighbor_tunnel_id]),
                set(visited_connector_coords) | set([connector_coord])
            ) for neighbor_tunnel_id, connector_coord in viable_neighbors
        )

def part_1(lines):
    grid = []
    for y, line in enumerate(lines):
        line = line.strip()
        grid.append(line)

    solver = Solver(grid)
    return solver.simulate()


def part_2(lines):
    grid = []
    for y, line in enumerate(lines):
        line = line.strip()
        grid.append(line)

    solver = Solver(grid)
    return solver.simulate()


if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)


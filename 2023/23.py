"""
Part 1: Find how many steps are on the longest hike, with directional slopes along the way.
Part 2: Same thing but no more directional slopes.
"""
import os

from util import (
    TERM_COLORS,
    Direction,
    color_string,
    get_cardinal_direction_coords,
    run
)

DIRECTION_MAP = {
    '>': [Direction.RIGHT],
    '<': [Direction.LEFT],
    '^': [Direction.UP],
    'v': [Direction.DOWN],
}

DIRECTION_DELTAS = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, -1),
    'v': (0, 1),
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
        self.valid_tunnel_ids = set()


class Solver:
    def __init__(self, lines, respect_slopes=True):
        self.grid = [line.strip() for line in lines]
        self.max_x = len(self.grid[0]) - 1
        self.max_y = len(self.grid) - 1
        self.start_coord = (1, 0)
        self.goal_coord = (self.max_x - 1, self.max_y)
        self.respect_slopes = respect_slopes

        self.wall_coords = set()
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if char == '#':
                    self.wall_coords.add((x, y))

        self.tunnel_map = {}
        self.tunnel_connector_nodes = {}
        self.start_tunnel_id = None
        self.goal_tunnel_id = None

        self.populate_tunnels()

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

    def is_connected(self, tunnel_endpoint, connector_coord):
        tunnel_x, tunnel_y = tunnel_endpoint
        connector_x,connector_y = connector_coord
        dx = tunnel_x - connector_x
        dy = tunnel_y - connector_y
        direction_correct = True

        # If we need to respect slopes, we need to check the symbol of the
        # tunnel endpoint. For the connector to be connected to it, it needs to
        # point away from the connector.
        if self.respect_slopes:
            symbol = self.grid[tunnel_y][tunnel_x]
            direction_correct = DIRECTION_DELTAS.get(symbol) == (dx, dy)

        return abs(dx) + abs(dy) == 1, direction_correct

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
                symbol = self.grid[connector_coord[1]][connector_coord[0]]

                for coord in (start_coord, end_coord):
                    is_adjacent, direction_correct = self.is_connected(coord, connector_coord)
                    if is_adjacent:
                        tunnel.adjacent_connector_coords.add(connector_coord)
                        if direction_correct:
                            node.valid_tunnel_ids.add(tunnel_id)

            if end_coord == self.goal_coord:
                self.goal_tunnel_id = tunnel_id

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
            return longest_distance

        viable_neighbors = set()
        for connector_coord in curr_node.adjacent_connector_coords:
            if connector_coord in visited_connector_coords:
                continue

            viable_neighbors |= set(
                (neighbor_tunnel_id, connector_coord)
                for neighbor_tunnel_id in (
                    self.tunnel_connector_nodes[connector_coord].valid_tunnel_ids -
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

    def print_tunnels(self, tunnel_ids=None):
        RJUST_SIZE = 2
        coord_to_tunnel_id = {
            (x, y): id_
            for id_, tunnel in self.tunnel_map.items()
            for (x, y) in tunnel.path
            if tunnel_ids is None or id_ in tunnel_ids
        }

        for y, row in enumerate(self.grid):
            string = ''
            for x, char in enumerate(row):
                coord = (x, y)
                if coord in self.wall_coords:
                    string += '#'.rjust(RJUST_SIZE)
                elif coord in self.tunnel_connector_nodes:
                    string += '+'.rjust(RJUST_SIZE)
                elif coord in coord_to_tunnel_id:
                    tunnel_id = coord_to_tunnel_id[coord]
                    string += color_string(
                        str(tunnel_id).rjust(RJUST_SIZE),
                        TERM_COLORS[tunnel_id % len(TERM_COLORS)]
                    )
                else:
                    string += char.rjust(RJUST_SIZE)
            print(string)


def part_1(lines):
    return Solver(lines, respect_slopes=True).find_longest_path()


def part_2(lines):
    return Solver(lines, respect_slopes=False).find_longest_path()


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)


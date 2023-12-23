import math
import os
import sys

from collections import defaultdict
from util import OPPOSITE_DIRECTIONS, Direction, get_cardinal_direction_coords, run

DIRECTION_MAP = {
    '>': [Direction.RIGHT],
    '<': [Direction.LEFT],
    '^': [Direction.UP],
    'v': [Direction.DOWN],
}


def extract_coord(dir_coord):
    return (dir_coord[1], dir_coord[2])


def flip_dir_coord(dir_coord):
    d, x, y = dir_coord
    return (OPPOSITE_DIRECTIONS[d], x, y)


class Slope:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction


class TunnelData:
    def __init__(self, path):
        self.path = path


class Solver:
    def __init__(self, grid, slopes):
        self.grid = grid
        self.slopes = slopes
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

        # Map of coordinate where if you step on it, you should teleport to the end of the path and add
        # num steps to your steps.
        self.tunnels = {}  # start_coord -> dest_coord, num_steps

    def get_longest_path(
        self,
        dir_curr_coord,
        num_steps,
        blocked,
        tunnel,
    ):
        d, x, y = dir_curr_coord

        new_blocked = set(blocked)
        new_blocked.add((x, y))

        if (x, y) == self.goal_coord:
            self.blocked = blocked
            return num_steps

        if tunnel:
            tunnel.path.append(dir_curr_coord)

        # We can jump!
        if self.grid[y][x] in DIRECTION_MAP and dir_curr_coord in self.tunnels:
            valid_tunnel = self.tunnels[dir_curr_coord]
            # print('Hopping from', dir_curr_coord, 'to', valid_tunnel.path[-1])
            # print('Steps from %s to %s' % (num_steps, num_steps + len(valid_tunnel.path)))
            new_blocked |= set((x, y) for _, x, y in valid_tunnel.path)
            return self.get_longest_path(
                valid_tunnel.path[-1],
                num_steps + len(valid_tunnel.path) - 1,
                set(new_blocked),
                None
            )

        if self.grid[y][x] in DIRECTION_MAP or (x, y) == self.start_coord:
            # Are we starting a new tunnel or finishing an existing one?
            if tunnel:  # Finishing a tunnel
                # print('Creating tunnel')
                # print('Path', tunnel.path)
                self.tunnels[tunnel.path[0]] = tunnel

                # Make the opposite tunnel too, flippinga all the directions
                tunnel_copy = TunnelData([flip_dir_coord(c) for c in tunnel.path[::-1]])
                self.tunnels[tunnel_copy.path[0]] = tunnel_copy

                tunnel = None
            else:  # Starting one
                # print('Starting tunnel')
                # print(dir_curr_coord, num_steps)
                tunnel = TunnelData([dir_curr_coord])

        next_coords = get_cardinal_direction_coords(
            x, y,
            blocked=blocked,
            grid=self.grid
        )
        num_steps += 1
        viable_neighbors = []
        for nd, nx, ny in next_coords:
            dir_next_coord = (nd, nx, ny)
            next_coord = (nx, ny)

            if nd == OPPOSITE_DIRECTIONS[d]:
                continue

            tunnel_copy = TunnelData([c for c in tunnel.path]) if tunnel else None

            viable_neighbors.append((
                dir_next_coord,
                num_steps,
                tunnel_copy
            ))

        if not viable_neighbors:
            return 0

        return max(
            self.get_longest_path(dir_neighbor_coord, steps, set(new_blocked), sc)
            for dir_neighbor_coord, steps, sc in viable_neighbors
        )

    def simulate(self):
        start_dir_coord =(Direction.DOWN, self.start_coord[0], self.start_coord[1])
        result = self.get_longest_path(
            start_dir_coord,
            0,
            self.wall_coords,
            None,
        )

        tunnel_starts = set(
            extract_coord(s.path[0]) for s in self.tunnels.values()
        )
        # print(tunnel_starts)
        for y, row in enumerate(self.grid):
            string = ''
            for x, char in enumerate(row):
                if (x, y) in self.wall_coords:
                    string += '#'
                elif (x, y) in tunnel_starts:
                    string += 'T'
                elif (x, y) in self.blocked:
                    string += 'O'
                else:
                    string += char
            print(string)

        return result


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbor_ids = set()
        self.dist_from_source = -math.inf

    @property
    def id(self):
        return (self.x, self.y)


class DAG:
    def __init__(self, lines):
        self.grid = []
        node_map = {}
        self.wall_coords = set()
        for y, line in enumerate(lines):
            line = line.strip()
            self.grid.append(line)
            for x, char in enumerate(line):
                if char == '#':
                    self.wall_coords.add((x, y))
                else:
                    node_map[(x, y)] = Node(x, y)

        self.min_x, self.max_x = 1, len(self.grid[0]) - 1
        self.min_y, self.max_y = 1, len(self.grid) - 1
        self.goal_coord = (self.max_x - 1, self.max_y)

        # Set neightbors to build graph
        node_batch = [(Direction.DOWN, 1, 0)]
        while node_batch:
            for d, x, y in node_batch:
                new_node_batch = []
                neighbor_coords = get_cardinal_direction_coords(
                    x, y, grid=self.grid
                )
                for nd, nx, ny in neighbor_coords:
                    if (nx, ny) in self.wall_coords:
                        continue
                    if nd == OPPOSITE_DIRECTIONS[d]:
                        continue
                    neighbor = node_map[(nx, ny)]
                    node_map[(x, y)].neighbor_ids.add(neighbor.id)
                    new_node_batch.append((nd, nx, ny))
                node_batch = new_node_batch

        # Topological sort
        visited = set()
        sorted_nodes = []

        def visit(node):
            if node.id not in visited:
                visited.add(node.id)
                for neighbor_id in node_map[node.id].neighbor_ids:
                    visit(node_map[neighbor_id])
                sorted_nodes.append(node)

        for node in node_map.values():
            visit(node)

        sorted_nodes.reverse()

        print([n.id for n in sorted_nodes])

        # Populate distances
        source_node = node_map[(1, 0)]
        source_node.dist_from_source = 0
        for node in sorted_nodes:
            for neighbor_id in node.neighbor_ids:
                neighbor = node_map[neighbor_id]
                neighbor.dist_from_source = max(
                    neighbor.dist_from_source,
                    node.dist_from_source + 1
                )

        dist_map = {
            node.id: node.dist_from_source for node in sorted_nodes
        }
        for y, row in enumerate(self.grid):
            curr_str = ''
            for x, char in enumerate(row):
                if (x, y) not in dist_map:
                    curr_str += char.rjust(4)
                else:
                    node = node_map[(x, y)]
                    curr_str += str(dist_map[(x, y)]).rjust(4)
            print(curr_str)

        self.max_steps = node_map[self.goal_coord].dist_from_source


def part_1(lines):
    grid = []
    slopes = []
    for y, line in enumerate(lines):
        line = line.strip()
        grid.append(line)
        for x, char in enumerate(line):
            if char in DIRECTION_MAP:
                slopes.append(Slope(x, y, char))

    solver = Solver(grid, slopes)
    return solver.simulate()


def part_2(lines):
    grid = []
    slopes = []
    for y, line in enumerate(lines):
        line = line.strip()
        grid.append(line)
        for x, char in enumerate(line):
            if char in DIRECTION_MAP:
                slopes.append(Slope(x, y, char))

    solver = Solver(grid, slopes)
    return solver.simulate()


if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)


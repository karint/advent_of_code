import math
import os
import sys

from collections import defaultdict
from util import OPPOSITE_DIRECTIONS, Direction, get_cardinal_direction_coords, run

DIRECTION_MAP = {
    '>': Direction.RIGHT,
    '<': Direction.LEFT,
    '^': Direction.UP,
    'v': Direction.DOWN,
}


class Slope:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction


class Solver:
    def __init__(self, grid, slopes):
        self.grid = grid
        self.slopes = slopes
        self.min_x, self.max_x = 1, len(self.grid[0]) - 1
        self.min_y, self.max_y = 1, len(self.grid) - 1
        self.num_steps = 0
        self.goal_coord = (self.max_x - 1, self.max_y)

        self.wall_coords = set()
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if char == '#':
                    self.wall_coords.add((x, y))

        self.x = 1
        self.y = 0

    def goal_unreachable(self, curr_x, curr_y, visited):
        # Goal is unreachable if there's either a col of walls + visited or
        # row of walls + visited between current coords and the goal
        blocked = self.wall_coords | visited
        goal_x, goal_y = self.goal_coord
        width = len(self.grid[0])
        height = len(self.grid)
        for x in range(curr_x + 1, goal_x):
            if all((x, y) in blocked for y in range(height)):
                return True

        for y in range(curr_y + 1, goal_y):
            if all((x, y) in blocked for x in range(width)):
                return True

        return False


    def simulate(self):
        cache = {}  # Mark all places where we could only go one direction and max steps
        paths = [(self.x, self.y, 0, set())]
        max_steps = 0
        best_path = None
        while paths:
            new_paths = defaultdict(list)
            for x, y, steps, visited in paths:
                # Prune any paths for which there's no path to the goal
                if self.goal_unreachable(x, y, visited):
                    continue

                visited.add((x, y))

                symbol = self.grid[y][x]
                next_coords = get_cardinal_direction_coords(
                    x, y,
                    # directions = DIRECTION_MAP.get(symbol),
                    grid=self.grid)
                steps += 1

                # If there's only one valid direction to go after arriving somewhere,
                # prune

                for d, nx, ny in next_coords:
                    if (nx, ny) in visited | self.wall_coords:
                        continue
                    if (nx, ny) == self.goal_coord:
                        if steps > max_steps:
                            max_steps = steps
                            best_path = visited
                            continue

                        new_paths[(nx, ny)].append((steps, set(visited)))



            paths = new_paths

        # path_coords = set(best_path)
        # for y, row in enumerate(self.grid):
        #     curr_str = ''
        #     for x, char in enumerate(row):
        #         if (x, y) in visited:
        #             curr_str += 'O'
        #         else:
        #             curr_str += char
        #     print(curr_str)
        return max_steps


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
    return DAG(lines).max_steps


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)


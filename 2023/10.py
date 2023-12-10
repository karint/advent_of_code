import os
import json
import re

from collections import defaultdict
from util import Direction, find_digits, get_adjacent_coords, run


CONNECTORS = {
    '|': set([Direction.UP, Direction.DOWN]),
    '-': set([Direction.LEFT, Direction.RIGHT]),
    'L': set([Direction.UP, Direction.RIGHT]),
    'J': set([Direction.LEFT, Direction.UP]),
    '7': set([Direction.LEFT, Direction.DOWN]),
    'F': set([Direction.RIGHT, Direction.DOWN]),
}


class Node:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def get_neighbors(self, grid):
        g = grid
        up = g[self.y - 1][self.x] if self.y > 0 else '.'
        down = g[self.y + 1][self.x] if self.y < len(g) - 1 else '.'
        left = g[self.y][self.x - 1] if self.x > 0 else '.'
        right = g[self.y][self.x + 1] if self.x < len(g[0]) - 1 else '.'

        neighbors = []
        if up != '.'  and Direction.DOWN in CONNECTORS[up] and Direction.UP in CONNECTORS[self.symbol]:
            neighbors.append((self.x, self.y - 1))
        if down != '.'  and Direction.UP in CONNECTORS[down] and Direction.DOWN in CONNECTORS[self.symbol]:
            neighbors.append((self.x, self.y + 1))
        if left != '.'  and Direction.RIGHT in CONNECTORS[left] and Direction.LEFT in CONNECTORS[self.symbol]:
            neighbors.append((self.x - 1, self.y))
        if right != '.'  and Direction.LEFT in CONNECTORS[right] and Direction.RIGHT in CONNECTORS[self.symbol]:
            neighbors.append((self.x + 1, self.y,))
        return neighbors


def part_1(lines):
    answer = 0
    grid = []
    nodes = {}
    start_x, start_y = None, None

    for y, line in enumerate(lines):
        row = list(line.strip())
        grid.append(row)
        for x, char in enumerate(row):
            if char == 'S':
                start_x, start_y = x, y
            elif char != '.':
                nodes[(x, y)] = Node(x, y, char)

    up = grid[start_y - 1][start_x] if start_y > 0 else '.'
    down = grid[start_y + 1][start_x] if start_y < len(grid) - 1 else '.'
    left = grid[start_y][start_x - 1] if start_x > 0 else '.'
    right = grid[start_y][start_x + 1] if start_x < len(grid[0]) - 1 else '.'

    connected_to = set()
    if up != '.' and Direction.DOWN in CONNECTORS[up]:
        connected_to.add(Direction.UP)
    if down != '.'  and Direction.UP in CONNECTORS[down]:
        connected_to.add(Direction.DOWN)
    if left != '.'  and Direction.RIGHT in CONNECTORS[left]:
        connected_to.add(Direction.LEFT)
    if right != '.'  and Direction.LEFT in CONNECTORS[right]:
        connected_to.add(Direction.RIGHT)

    start_symbol = None
    for sym, dirs in CONNECTORS.items():
        if len(dirs & connected_to) == 2:
            start_symbol = sym
    nodes[(start_x, start_y)] = Node(start_x, start_y, start_symbol)
    grid[start_y][start_x] = start_symbol

    visited_nodes = set()
    curr_nodes = set([(start_x, start_y)])
    steps = 0
    while curr_nodes:
        new_curr_nodes = set()
        for x, y in curr_nodes:
            visited_nodes.add((x, y))
            neighbors = nodes[(x, y)].get_neighbors(grid)
            for n_x, n_y in neighbors:
                if (n_x, n_y) not in visited_nodes:
                    new_curr_nodes.add((n_x, n_y))
        curr_nodes = new_curr_nodes
        steps += 1
        
    return steps - 1


def get_ground_neighbors(x, y, grid):
    neighbors = set()
    if x > 0:
        coords = (x - 1, y)
        if grid[coords[1]][coords[0]] == '.':
            neighbors.add(coords)
    if y > 0:
        coords = (x, y - 1)
        if grid[coords[1]][coords[0]] == '.':
            neighbors.add(coords)
    if x < len(grid[0]) - 1:
        coords = (x + 1, y)
        if grid[coords[1]][coords[0]] == '.':
            neighbors.add(coords)
    if y < len(grid) - 1:
        coords = (x, y + 1)
        if grid[coords[1]][coords[0]] == '.':
            neighbors.add(coords)

    return neighbors

def part_2(lines):
    answer = 0
    grid = []
    nodes = {}
    start_x, start_y = None, None

    # Create grid and find start
    for y, line in enumerate(lines):
        row = list(line.strip())
        grid.append(row)
        for x, char in enumerate(row):
            if char == 'S':
                start_x, start_y = x, y
            elif char != '.':
                nodes[(x, y)] = Node(x, y, char)

    # Figure out starting symbol
    up = grid[start_y - 1][start_x] if start_y > 0 else '.'
    down = grid[start_y + 1][start_x] if start_y < len(grid) - 1 else '.'
    left = grid[start_y][start_x - 1] if start_x > 0 else '.'
    right = grid[start_y][start_x + 1] if start_x < len(grid[0]) - 1 else '.'

    connected_to = set()
    if up != '.' and Direction.DOWN in CONNECTORS[up]:
        connected_to.add(Direction.UP)
    if down != '.'  and Direction.UP in CONNECTORS[down]:
        connected_to.add(Direction.DOWN)
    if left != '.'  and Direction.RIGHT in CONNECTORS[left]:
        connected_to.add(Direction.LEFT)
    if right != '.'  and Direction.LEFT in CONNECTORS[right]:
        connected_to.add(Direction.RIGHT)

    start_symbol = None
    for sym, dirs in CONNECTORS.items():
        if len(dirs & connected_to) == 2:
            start_symbol = sym
    nodes[(start_x, start_y)] = Node(start_x, start_y, start_symbol)
    grid[start_y][start_x] = start_symbol

    # Find out what pipes are in the loop
    visited_nodes = set()
    curr_nodes = set([(start_x, start_y)])
    steps = 0
    while curr_nodes:
        new_curr_nodes = set()
        for x, y in curr_nodes:
            visited_nodes.add((x, y))
            neighbors = nodes[(x, y)].get_neighbors(grid)
            for n_x, n_y in neighbors:
                if (n_x, n_y) not in visited_nodes:
                    new_curr_nodes.add((n_x, n_y))
        curr_nodes = new_curr_nodes

    # Replace all junk with ground
    all_edge_ground = set()
    all_ground = set()
    new_grid = []
    for y, row in enumerate(grid):
        new_row = []
        for x, char in enumerate(row):
            is_ground = char == '.'
            if char in CONNECTORS and (x, y) not in visited_nodes:
                new_row.append('.')
                is_ground = True
            else:
                new_row.append(char)
            if is_ground:
                if y == 0 or x == 0 or y == len(lines) - 1 or x == len(lines[0]) - 1:
                    all_edge_ground.add((x, y))
                all_ground.add((x, y))
        new_grid.append(new_row)
    grid = new_grid

    # As we traverse the loop, keep track of right/ left ground spots adjacent.
    pipe_nodes = set()
    curr_node = (start_x, start_y)
    steps = 0
    distances = {}
    right_ground = set()
    left_ground = set()
    last_pipe = (start_x, start_y + 1)
    while curr_node is not None:
        new_curr_nodes = set()
        x, y = curr_node
        g = grid
        symbol = g[y][x]
        pipe_nodes.add((x, y))
        next_node = None

        up = g[y - 1][x] if y > 0 else None
        down = g[y + 1][x] if y < len(g) - 1 else None
        left = g[y][x - 1] if x > 0 else None
        right = g[y][x + 1] if x < len(g[0]) - 1 else None

        if up:
            coords = (x, y - 1)
            if up == '.':
                if symbol == '7':
                    if last_pipe == (x, y + 1):
                        right_ground.add(coords)
                    else:
                        left_ground.add(coords)
                elif symbol == 'F':
                    if last_pipe == (x, y + 1):
                        left_ground.add(coords)
                    else:
                        right_ground.add(coords)
            elif Direction.DOWN in CONNECTORS[up] and Direction.UP in CONNECTORS[symbol] and coords not in pipe_nodes:
                next_node = coords

        if down:
            coords = (x, y + 1)
            if down == '.':
                if symbol == 'L':
                    if last_pipe == (x, y - 1):
                        right_ground.add(coords)
                    else:
                        left_ground.add(coords)
                elif symbol == 'J':
                    if last_pipe == (x, y - 1):
                        left_ground.add(coords)
                    else:
                        right_ground.add(coords)
            elif Direction.UP in CONNECTORS[down] and Direction.DOWN in CONNECTORS[symbol] and coords not in pipe_nodes:
                next_node = coords

        if left:
            coords = (x - 1, y)
            if left == '.':
                if symbol == 'F':
                    if last_pipe == (x + 1, y):
                        right_ground.add(coords)
                    else:
                        left_ground.add(coords)
                elif symbol == 'L':
                    if last_pipe == (x + 1, y):
                        left_ground.add(coords)
                    else:
                        right_ground.add(coords)
            elif Direction.RIGHT in CONNECTORS[left] and Direction.LEFT in CONNECTORS[symbol] and coords not in pipe_nodes:
                next_node = coords

        if right:
            coords = (x + 1, y)
            if right == '.':
                if symbol == 'J':
                    if last_pipe == (x - 1, y):
                        right_ground.add(coords)
                    else:
                        left_ground.add(coords)
                elif symbol == '7':
                    if last_pipe == (x - 1, y):
                        left_ground.add(coords)
                    else:
                        right_ground.add(coords)
            elif Direction.LEFT in CONNECTORS[right] and Direction.RIGHT in CONNECTORS[symbol] and coords not in pipe_nodes:
                next_node = coords

        last_pipe = curr_node
        curr_node = next_node

    # Find ground that touches the outside (without squeezing between pipes)
    outer_ground = set(all_edge_ground)
    for g_x, g_y in all_edge_ground:
        currs = set([(g_x, g_y)])
        while currs:
            new_currs = set()
            for x, y in currs:
                neighbors = get_ground_neighbors(x, y, grid)
                for n_x, n_y in neighbors:
                    if (n_x, n_y) not in outer_ground:
                        new_currs.add((n_x, n_y))
                outer_ground.update(neighbors)
            currs = new_currs

    # Figure out whether left or right grounds are inner or outer
    new_outer_grounds = None
    if len(left_ground & outer_ground):
        new_outer_grounds = left_ground
    else:
        new_outer_grounds = right_ground
    outer_ground |= new_outer_grounds

    # Now find everything left/right grounds touch
    for g_x, g_y in new_outer_grounds:
        currs = set([(g_x, g_y)])
        while currs:
            new_currs = set()
            for x, y in currs:
                neighbors = get_ground_neighbors(x, y, grid)
                for n_x, n_y in neighbors:
                    if (n_x, n_y) not in outer_ground:
                        new_currs.add((n_x, n_y))
                outer_ground.update(neighbors)
            currs = new_currs

    return len(all_ground) - len(outer_ground)



if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

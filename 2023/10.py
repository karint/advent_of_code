import os

from collections import defaultdict
from util import Direction, run


START_SYMBOL = 'S'

CONNECTORS = {
    '|': set([Direction.DOWN, Direction.UP]),
    '7': set([Direction.DOWN, Direction.LEFT]),
    'F': set([Direction.DOWN, Direction.RIGHT]),
    '-': set([Direction.LEFT, Direction.RIGHT]),
    'J': set([Direction.LEFT, Direction.UP]),
    'L': set([Direction.RIGHT, Direction.UP]),
}

OPPOSITES = {
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
    Direction.UP: Direction.DOWN,
}


def get_neighbors(x, y, grid, valid_symbols):
    """
    Returns a set of (direction, x, y) tuples of valid neighbors.
    Direction indicates what direction the neighbor is relative
    to the given coords.
    """
    symbol = grid[y][x]
    coords_to_check = [
        (Direction.UP, x, y - 1),
        (Direction.DOWN, x, y + 1),
        (Direction.LEFT, x - 1, y),
        (Direction.RIGHT, x + 1, y),
    ]

    neighbors = set()
    for direction, x, y in coords_to_check:
        try:
            neighbor_symbol = grid[y][x]
        except IndexError:
            continue

        if (
            neighbor_symbol in valid_symbols and
            OPPOSITES[direction] in CONNECTORS[neighbor_symbol]
        ):
            neighbors.add((direction, x, y))

    return neighbors


def part_1(lines):
    # Construct grid and find starting coords
    grid = []
    start_x, start_y = None, None
    for y, line in enumerate(lines):
        row = list(line.strip())
        if START_SYMBOL in row:
            start_x, start_y = row.index(START_SYMBOL), y
        grid.append(row)

    # Determine symbol of starting coord
    neighbors = get_neighbors(start_x, start_y, grid, CONNECTORS.keys())
    directions_of_neighbors = {n[0] for n in neighbors}
    for sym, dirs in CONNECTORS.items():
        if dirs == directions_of_neighbors:
            grid[start_y][start_x] = sym
            break

    # Traverse the loop
    steps = -1
    visited_coords = set()
    curr_coords = set([(start_x, start_y)])
    while curr_coords:
        steps += 1
        new_curr_coords = set()
        for x, y in curr_coords:
            visited_coords.add((x, y))
            neighbors = get_neighbors(x, y, grid, CONNECTORS.keys())
            neighbor_coords = {(n_x, n_y) for _, n_x, n_y in neighbors}
            new_curr_coords.update(neighbor_coords - visited_coords)
        curr_coords = new_curr_coords

    return steps


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
    start_x, start_y = None, None

    # Create grid and find start
    for y, line in enumerate(lines):
        row = list(line.strip())
        grid.append(row)
        for x, char in enumerate(row):
            if char == 'S':
                start_x, start_y = x, y

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
    grid[start_y][start_x] = start_symbol

    # Find out what pipes are in the loop
    visited_nodes = set()
    curr_nodes = set([(start_x, start_y)])
    steps = 0
    while curr_nodes:
        new_curr_nodes = set()
        for x, y in curr_nodes:
            visited_nodes.add((x, y))
            neighbors = get_neighbors(x, y, grid, CONNECTORS.keys())
            for _, n_x, n_y in neighbors:
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

    # As we traverse the loop, keep track of right/ left ground spots adjacent
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

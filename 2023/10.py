"""
Part 1: Find the farthest pipe from a starting point within a loop of pipes.
Part 2: Find the area enclosed by the pipe loop.
"""
import os

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

class NeighborType:
    GROUND = 'GROUND'
    PIPE = 'PIPE'

NEIGHBOR_TYPES = {
    NeighborType.GROUND: {'.'},
    NeighborType.PIPE: set(CONNECTORS.keys()),
}

# Honestly I can't even really explain what this is
LEFT_RIGHT_INFO = {
    Direction.UP: lambda x, y: (x, y + 1, '7', 'F'),
    Direction.DOWN: lambda x, y: (x, y - 1, 'L', 'J'),
    Direction.LEFT: lambda x, y: (x + 1, y, 'F', 'L'),
    Direction.RIGHT: lambda x, y: (x - 1, y, 'J', '7'),
}


def get_cardinal_coords(x, y):
    return [
        (Direction.UP, x, y - 1),
        (Direction.DOWN, x, y + 1),
        (Direction.LEFT, x - 1, y),
        (Direction.RIGHT, x + 1, y),
    ]


def initialize_grid(lines):
    # Initialize grid and find starting coords
    grid = []
    start_x, start_y = None, None
    for y, line in enumerate(lines):
        row = list(line.strip())
        if START_SYMBOL in row:
            start_x, start_y = row.index(START_SYMBOL), y
        grid.append(row)

    # Determine symbol of starting coord and replace it in the grid
    neighbors = get_neighbors(start_x, start_y, grid, NeighborType.PIPE)
    cardinal_map = {
        (x, y): direction for direction, x, y in get_cardinal_coords(start_x, start_y)
    }
    directions_of_neighbors = {
        cardinal_map[(x, y)] for x, y in neighbors
    }
    for sym, dirs in CONNECTORS.items():
        if dirs == directions_of_neighbors:
            grid[start_y][start_x] = sym
            break

    return start_x, start_y, grid


def get_neighbors(x, y, grid, neighbor_type):
    """
    Returns a set of (x, y) tuples of valid neighbors.
    """
    symbol = grid[y][x]
    neighbors = set()
    for direction, x, y in get_cardinal_coords(x, y):
        if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
            continue

        if (
            neighbor_type == NeighborType.PIPE and
            symbol in CONNECTORS and
            direction not in CONNECTORS[symbol]
        ):
            continue

        neighbor_symbol = grid[y][x]
        if (
            neighbor_symbol in NEIGHBOR_TYPES[neighbor_type] and
            (
                neighbor_type == NeighborType.GROUND or
                OPPOSITES[direction] in CONNECTORS[neighbor_symbol]
            )
        ):
            neighbors.add((x, y))

    return neighbors


def part_1(lines):
    start_x, start_y, grid = initialize_grid(lines)

    # Traverse the loop
    steps = -1
    visited_coords = set()
    curr_coords = set([(start_x, start_y)])
    while curr_coords:
        steps += 1
        new_curr_coords = set()
        for x, y in curr_coords:
            visited_coords.add((x, y))
            neighbors = get_neighbors(x, y, grid, NeighborType.PIPE)
            new_curr_coords.update(neighbors - visited_coords)
        curr_coords = new_curr_coords

    return steps


def part_2(lines):
    start_x, start_y, grid = initialize_grid(lines)

    # Traverse the loop, recording all the coords of loop pipes
    loop_pipe_coords = set()
    curr_coords = set([(start_x, start_y)])
    while curr_coords:
        new_curr_coords = set()
        for x, y in curr_coords:
            loop_pipe_coords.add((x, y))
            neighbors = get_neighbors(x, y, grid, NeighborType.PIPE)
            new_curr_coords.update(neighbors - loop_pipe_coords)
        curr_coords = new_curr_coords

    # Replace all junk (pipes not in the loop) with ground. Keep track also
    # of all ground coords and all ground coords on the outer edge.
    new_grid = []
    all_ground_coords = set()
    all_edge_ground_coords = set()
    for y, row in enumerate(grid):
        new_row = []
        for x, char in enumerate(row):
            if (x, y) not in loop_pipe_coords:
                new_row.append('.')
                if y == 0 or x == 0 or y == len(lines) - 1 or x == len(lines[0]) - 1:
                    all_edge_ground_coords.add((x, y))
                all_ground_coords.add((x, y))
            else:
                new_row.append(char)
        new_grid.append(new_row)
    grid = new_grid

    # As we traverse the loop, keep track of right / left ground spots adjacent
    # Note: This code is completely unreadable :)
    right_ground = set()
    left_ground = set()
    visited_coords = set()
    curr_pipe = (start_x, start_y)
    last_pipe = (start_x, start_y + 1)
    while curr_pipe is not None:
        visited_coords.add(curr_pipe)
        new_curr_pipes = set()
        x, y = curr_pipe
        symbol = grid[y][x]
        next_pipe = None

        cardinal_coords = get_cardinal_coords(x, y)
        left_right_tuples = {
            (direction, n_x, n_y, *LEFT_RIGHT_INFO[direction](x, y))
            for (direction, n_x, n_y) in cardinal_coords
        }

        for (direction, n_x, n_y, last_pipe_x, last_pipe_y, sym_1, sym_2) in left_right_tuples:
            if n_y < 0 or n_y >= len(grid) or n_x < 0 or n_x >= len(grid[0]):
                continue

            coords = (n_x, n_y)
            n_symbol = grid[n_y][n_x]
            if n_symbol == '.':
                if symbol == sym_1:
                    (right_ground if last_pipe == (last_pipe_x, last_pipe_y) else left_ground).add(coords)
                elif symbol == sym_2:
                    (left_ground if last_pipe == (last_pipe_x, last_pipe_y) else right_ground).add(coords)
            elif (
                OPPOSITES[direction] in CONNECTORS[n_symbol] and
                direction in CONNECTORS[symbol] and
                coords not in visited_coords
            ):
                next_pipe = coords

        last_pipe = curr_pipe
        curr_pipe = next_pipe

    # Find ground that touches the outside (without squeezing between pipes)
    outer_ground = set(all_edge_ground_coords)
    for g_x, g_y in all_edge_ground_coords:
        currs = set([(g_x, g_y)])
        while currs:
            new_currs = set()
            for x, y in currs:
                neighbors = get_neighbors(x, y, grid, NeighborType.GROUND)
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
                neighbors = get_neighbors(x, y, grid, NeighborType.GROUND)
                for n_x, n_y in neighbors:
                    if (n_x, n_y) not in outer_ground:
                        new_currs.add((n_x, n_y))
                outer_ground.update(neighbors)
            currs = new_currs

    # Finally return the diff of total ground tiles minus those that touch the outside
    return len(all_ground_coords) - len(outer_ground)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

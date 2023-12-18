"""
Part 1: Find energized cells in a grid that are hit by a light beam.
Part 2: Find the maximum of energized cells from any starting position.
"""
import os

from util import OPPOSITE_DIRECTIONS, Direction, get_cardinal_direction_coords, run


SLASH_REFLECT = {
    Direction.RIGHT: Direction.UP,
    Direction.LEFT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.UP: Direction.RIGHT,
}
BACKSLASH_REFLECT = {
    k: OPPOSITE_DIRECTIONS[v] for k, v in SLASH_REFLECT.items()
}


def is_valid(coord, grid):
    _, x, y = coord
    width = len(grid[0])
    height = len(grid)
    return (
        x >= 0 and y >= 0 and
        x < width and y < height
    )


def get_new_coords(x, y, symbol, direction, grid):
    directions = (direction,)

    if symbol == '|' and direction in (Direction.RIGHT, Direction.LEFT):
        directions = (Direction.UP, Direction.DOWN)
    elif symbol == '-' and direction in (Direction.UP, Direction.DOWN):
        directions = (Direction.LEFT, Direction.RIGHT)
    elif symbol == '/':
        directions = (SLASH_REFLECT[direction],)
    elif symbol == '\\':
        directions = (BACKSLASH_REFLECT[direction],)

    return set(get_cardinal_direction_coords(x, y, directions=directions, grid=grid))


def get_energized_coords(starting_coord, grid):
    energized = set([starting_coord])
    beam_coords = set(energized)
    while True:
        new_beam_coords = set()
        for direction, x, y in beam_coords:
            new_beam_coords |= get_new_coords(x, y, grid[y][x], direction, grid)

        new_beam_coords -= energized
        if not new_beam_coords:
            break

        beam_coords = new_beam_coords
        energized |= beam_coords

    energized_coords = set((x, y) for _, x, y in energized)
    return len(energized_coords)


def part_1(lines):
    grid = [list(line.strip()) for line in lines]
    return get_energized_coords((Direction.RIGHT, 0, 0), grid)


def part_2(lines):
    grid = [list(line.strip()) for line in lines]
    width = len(grid[0])
    height = len(grid)

    max_energized = 0
    for starting_direction in (Direction.RIGHT, Direction.LEFT):
        start_x = 0 if starting_direction == Direction.RIGHT else width - 1
        for y in range(height):
            max_energized = max(
                max_energized,
                get_energized_coords((starting_direction, start_x, y), grid)
            )

    for starting_direction in (Direction.UP, Direction.DOWN):
        start_y = 0 if starting_direction == Direction.DOWN else height - 1
        for x in range(width):
            max_energized = max(
                max_energized,
                get_energized_coords((starting_direction, x, start_y), grid)
            )

    return max_energized


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

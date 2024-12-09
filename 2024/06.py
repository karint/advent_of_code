"""
Start: Dec 8 at 10:56pm ET.
Part 1:
Part 2:
"""
import os

from util import Direction, run

DIRECTION_ORDER = [
    Direction.UP,
    Direction.RIGHT,
    Direction.DOWN,
    Direction.LEFT,
]

def _print_grid(lines, coords_touched):
    for y, row in enumerate(lines):
        row = row.strip()
        print(''.join(['X' if (x, y) in coords_touched else '.' for x, char in enumerate(row)]))


def part_1(lines):
    height = len(lines)
    width = len(lines[0].strip())

    curr_dir_index = 0
    coords_touched = set()
    obstacles = set()

    curr_x, curr_y = None, None
    for y, row in enumerate(lines):
        row = row.strip()
        for x, char in enumerate(row):
            if char == '^':
                curr_x, curr_y = x, y
                coords_touched.add((curr_x, curr_y))
            elif char == '#':
                obstacles.add((x, y))

    while True:
        curr_dir = DIRECTION_ORDER[curr_dir_index]
        match curr_dir:
            case Direction.UP:
                new_x = curr_x
                new_y = curr_y - 1
            case Direction.RIGHT:
                new_x = curr_x + 1
                new_y = curr_y
            case Direction.DOWN:
                new_x = curr_x
                new_y = curr_y + 1
            case Direction.LEFT:
                new_x = curr_x - 1
                new_y = curr_y

        if (
            new_x < 0 or
            new_y < 0 or
            new_x >= width or
            new_y >= height
        ):
            # Went off the grid
            break

        if (new_x, new_y) in obstacles:
            curr_dir_index = (curr_dir_index + 1) % len(DIRECTION_ORDER)
        else:
            curr_x, curr_y = new_x, new_y
            coords_touched.add((curr_x, curr_y))

    return len(coords_touched)


def part_2(lines):
    height = len(lines)
    width = len(lines[0].strip())

    loopy_obstacle_coords = set()
    obstacles = set()

    curr_x, curr_y = None, None
    for y, row in enumerate(lines):
        row = row.strip()
        for x, char in enumerate(row):
            if char == '^':
                curr_x, curr_y = x, y
            elif char == '#':
                obstacles.add((x, y))

    start_x, start_y = curr_x, curr_y

    for possible_obstacle_y, row in enumerate(lines):
        row = row.strip()
        for possible_obstacle_x, _ in enumerate(row):
            if possible_obstacle_x == start_x and possible_obstacle_y == start_y:
                continue

            # Rest all the things
            curr_x = start_x
            curr_y = start_y
            curr_dir_index = 0
            curr_dir = Direction.UP
            coord_dirs_touched = set([(curr_dir, curr_x, curr_y)])

            while True:
                match curr_dir:
                    case Direction.UP:
                        new_x = curr_x
                        new_y = curr_y - 1
                    case Direction.RIGHT:
                        new_x = curr_x + 1
                        new_y = curr_y
                    case Direction.DOWN:
                        new_x = curr_x
                        new_y = curr_y + 1
                    case Direction.LEFT:
                        new_x = curr_x - 1
                        new_y = curr_y

                if (
                    new_x < 0 or
                    new_y < 0 or
                    new_x >= width or
                    new_y >= height
                ):
                    # Went off the grid
                    break

                if (
                    (new_x, new_y) in obstacles or
                    (
                        possible_obstacle_x == new_x and
                        possible_obstacle_y == new_y
                    )
                ):
                    curr_dir_index = (curr_dir_index + 1) % len(DIRECTION_ORDER)
                    curr_dir = DIRECTION_ORDER[curr_dir_index]
                else:
                    curr_x, curr_y = new_x, new_y

                if (curr_dir, curr_x, curr_y) in coord_dirs_touched:
                    loopy_obstacle_coords.add((possible_obstacle_x, possible_obstacle_y))
                    break

                coord_dirs_touched.add((curr_dir, curr_x, curr_y))

    return len(loopy_obstacle_coords)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

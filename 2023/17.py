"""
Part 1:
Part 2:
"""
import os

from util import Direction, run

OPPOSITES ={
    Direction.RIGHT: Direction.LEFT,
    Direction.UP: Direction.DOWN,
    Direction.LEFT: Direction.RIGHT,
    Direction.DOWN: Direction.UP,
}

SYMBOL = {
    Direction.RIGHT: '>',
    Direction.UP: '^',
    Direction.LEFT: '<',
    Direction.DOWN: 'v',
}


class PathGrid(object):
    """
    Class that can find the shortest path from a starting char to ending char in a grid.

    Warning: Not very efficient :)
    """
    def __init__(
        self,
        lines
    ):
        self.grid = [list(map(int, l.strip())) for l in lines]

        self.width = len(self.grid[0])
        self.height = len(self.grid)

        (self.start_x, self.start_y) = (0, 0)
        self.ending_point = (self.width - 1, self.height - 1)

    def find_paths(self):
        min_heat = None
        min_path = []
        visited = {}
        viable_paths = [
            [(0, 0, Direction.RIGHT, 0, 0)],
            [(0, 0, Direction.DOWN, 0, 0)],
        ]
        while viable_paths:
            new_paths = []
            for path in viable_paths:
                (last_x, last_y, curr_dir, steps_so_far, heat_so_far) = path[-1]
                if (last_x, last_y) == self.ending_point:
                    if min_heat is None or heat_so_far < min_heat:
                        min_heat = heat_so_far
                        min_path = path
                        continue

                if min_heat is not None and heat_so_far >= min_heat:
                    continue

                if (last_x, last_y, curr_dir, steps_so_far) in visited:
                    if heat_so_far >= visited[(last_x, last_y, curr_dir, steps_so_far)]:
                        continue
                    else:
                        visited[(last_x, last_y, curr_dir, steps_so_far)] = heat_so_far
                else:
                    visited[(last_x, last_y, curr_dir, steps_so_far)] = heat_so_far

                right = (Direction.RIGHT, last_x + 1, last_y)
                left = (Direction.LEFT, last_x - 1, last_y)
                up = (Direction.UP, last_x, last_y - 1)
                down = (Direction.DOWN, last_x, last_y + 1)

                for direction, target_x, target_y in (right, left, up, down):
                    # Don't revisit past squares, go out of bounds, or go too far in one direction
                    if (
                        target_x < 0 or
                        target_x >= self.width or
                        target_y < 0 or
                        target_y >= self.height
                    ):
                        continue

                    if direction == curr_dir and steps_so_far >= 3:
                        continue

                    if direction == OPPOSITES[curr_dir]:
                        continue

                    new_step = (
                        target_x,
                        target_y,
                        direction,
                        steps_so_far + 1 if curr_dir == direction else 1,
                        heat_so_far + self.grid[target_y][target_x]
                    )
                    new_paths.append(path + [new_step])

            viable_paths = new_paths

        path_key = {
            (x, y): SYMBOL[d] for (x, y, d, _, _) in min_path
        }
        for y, row in enumerate(self.grid):
            line = ''
            for x, char in enumerate(row):
                line += path_key.get((x, y), str(char))
            print(line)

        return min_heat


def part_1(lines):
    grid = PathGrid(lines)
    min_heat = grid.find_paths()
    return min_heat


def part_2(lines):
    return part_1(lines)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

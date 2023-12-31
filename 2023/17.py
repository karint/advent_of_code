"""
Part 1: Move a crucible through a grid while minimizing heat loss.
Part 2: Move a bigger and needier crucible.
"""
import os

from util import OPPOSITE_DIRECTIONS, Direction, get_cardinal_direction_coords, run

class Grid(object):
    def __init__(
        self,
        lines,
        min_steps,
        max_steps,
    ):
        self.grid = [list(map(int, l.strip())) for l in lines]

        self.start_x, self.start_y = 0, 0
        self.end_x, self.end_y = len(self.grid[0]) - 1, len(self.grid) - 1

        self.min_steps = min_steps
        self.max_steps = max_steps

    def find_paths(self):
        min_heat = None
        visited = {}
        viable_paths = set([
            (0, 0, Direction.RIGHT, 0, 0),
            (0, 0, Direction.DOWN, 0, 0),
        ])
        while viable_paths:
            new_paths = set()
            for last_x, last_y, curr_dir, steps_so_far, heat_so_far in viable_paths:
                # If we meet ending conditions, store heat if it's min
                if (last_x, last_y) == (self.end_x, self.end_y) and steps_so_far >= self.min_steps:
                    if min_heat is None or heat_so_far < min_heat:
                        min_heat = heat_so_far
                        continue

                # If we're already too hot, no point in continuing
                if min_heat is not None and heat_so_far >= min_heat:
                    continue

                # If we took a path before that was not as hot, no point in continuing
                if (
                    (last_x, last_y, curr_dir, steps_so_far) in visited and
                    heat_so_far >= visited[(last_x, last_y, curr_dir, steps_so_far)]
                ):
                        continue
                else:
                    visited[(last_x, last_y, curr_dir, steps_so_far)] = heat_so_far

                for direction, target_x, target_y in get_cardinal_direction_coords(last_x, last_y, grid=self.grid):
                    if (
                        # Don't take too few steps
                        (direction != curr_dir and steps_so_far < self.min_steps) or
                        # Or take too many steps
                        (direction == curr_dir and steps_so_far >= self.max_steps) or
                        # Or go backwards
                        direction == OPPOSITE_DIRECTIONS[curr_dir]
                    ):
                        continue

                    new_step = (
                        target_x,
                        target_y,
                        direction,
                        steps_so_far + 1 if curr_dir == direction else 1,
                        heat_so_far + self.grid[target_y][target_x]
                    )
                    new_paths.add(new_step)

            viable_paths = new_paths

        return min_heat


def part_1(lines):
    return Grid(lines, 0, 3).find_paths()


def part_2(lines):
    return Grid(lines, 4, 10).find_paths()


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

"""
Part 1:
Part 2:
"""
import os
import time

from collections import defaultdict
from util import get_cardinal_direction_coords, run

ROCK = '#'
GARDEN = '.'


def part_1(lines):
    grid = []
    steps = 64
    start_x, start_y = None, None
    for y, line in enumerate(lines):
        line = line.strip()
        for x, char in enumerate(line):
            if char == 'S':
                start_x = x
                start_y = y
        grid.append(list(line))

    max_steps = 0

    num_steps = 0
    starts = [(start_x, start_y)]
    while num_steps < steps:
        new_starts = set()
        stepped = set()
        for x, y in starts:
            dir_coords = get_cardinal_direction_coords(x, y, grid=grid)
            for _, new_x, new_y in dir_coords:
                if grid[new_y][new_x] in (GARDEN, 'S'):
                    stepped.add((new_x, new_y))
                    new_starts.add((new_x, new_y))
        starts = new_starts
        num_steps += 1

    return len(new_starts)

TRAVERSIBLE = set([GARDEN, 'S'])


def part_2(lines):
    grid = []
    start_x, start_y = None, None
    for y, line in enumerate(lines):
        line = line.strip()
        for x, char in enumerate(line):
            if char == 'S':
                start_x = x
                start_y = y
        grid.append(list(line))

    num_steps = 0
    starts = [(start_x, start_y)]
    # Track when we first stepped on a coord, and when stepping on it again see how many steps it took. If num steps divisible by it, we can guarantee returning to it.
    cycles = defaultdict(list) # coord: num steps when reached
    guaranteed = set()

    steps = 5000
    # steps = 26501365
    start_time = time.perf_counter()
    while num_steps < steps:
        if num_steps % 1000 == 0:
            print('On step', num_steps, ',', time.perf_counter() - start_time)
        new_starts = set()
        num_steps += 1
        for x, y in starts:
            dir_coords = get_cardinal_direction_coords(x, y)
            for _, new_x, new_y in dir_coords:
                equiv_x = new_x % len(grid[0])
                equiv_y = new_y % len(grid)

                if (new_x, new_y) in guaranteed:
                    continue
                if grid[equiv_x][equiv_y] in TRAVERSIBLE:
                    new_starts.add((new_x, new_y))
                    for step_lengths in cycles[(new_x, new_y)]:
                        if (
                            num_steps > step_lengths and
                            (steps - num_steps) % (num_steps - step_lengths) == 0
                        ):
                            guaranteed.add((new_x, new_y))

                    if not cycles[(new_x, new_y)] or num_steps != cycles[(new_x, new_y)][-1]:
                        cycles[(new_x, new_y)].append(num_steps)

                # # If we arrive at an equivalent spot on a map copy as we've been before, and there
                # # are enough steps left, we can guarantee being able to travel to the equivalent on
                # # that map
                # steps_left = steps - num_steps
                # new_guaranteed_coords = set()
                # if (
                #     (equiv_x, equiv_y) != (new_x, new_y) and
                #     cycles[(equiv_x, equiv_y)]
                # ):
                #     for (gmult_x, gmult_y), gset in guaranteed.items():
                #         for (gx, gy) in gset:
                #             new_gx = gx + (mult_x - gmult_x) * len(grid[0])
                #             new_gy = gy + (mult_y - gmult_y) * len(grid)
                #             new_num_steps = cycles[(gx, gy)][0] - cycles[(equiv_x, equiv_y)][0] + num_steps
                #             cycles[(new_gx, new_gy)].append(new_num_steps)
                #             if new_num_steps <= steps:
                #                 # Enough steps left!
                #                 new_guaranteed_coords.add((new_gx, new_gy))

                # guaranteed[(mult_x, mult_y)] |= new_guaranteed_coords
                # new_starts -= guaranteed[(mult_x, mult_y)]

        starts = new_starts

    print('Total time:',  time.perf_counter() - start_time)
    return len(new_starts | guaranteed)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

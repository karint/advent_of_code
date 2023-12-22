"""
Part 1:
Part 2:
"""
import math
import os
import sys
import time

from collections import defaultdict
from util import get_cardinal_direction_coords, run

ROCK = '#'
GARDEN = '.'
START = 'S'
TRAVERSIBLE = {GARDEN, START}


def part_1(lines):
    grid = []
    steps = 64
    start_x, start_y = None, None
    for y, line in enumerate(lines):
        line = line.strip()
        for x, char in enumerate(line):
            if char == START:
                start_x = x
                start_y = y
        grid.append(list(line))

    num_steps = 0
    starts = [(start_x, start_y)]
    while num_steps < steps:
        new_starts = set()
        stepped = set()
        for x, y in starts:
            dir_coords = get_cardinal_direction_coords(x, y, grid=grid)
            for _, nx, ny in dir_coords:
                if grid[ny][nx] in TRAVERSIBLE:
                    stepped.add((nx, ny))
                    new_starts.add((nx, ny))
        starts = new_starts
        num_steps += 1

    return len(new_starts)


def get_equivalent_coord(x, y, width, height):
    # Handles negative x and y just fine for our purposes
    return (x % width, y % height)


def get_grid_coord(x, y, width, height):
    """
    Returns (0, 0) if original grid, (0, 1) if this grid is the copy below the original,
    (1, 0) if this grid is the copy to the right, etc.
    """
    return (
        int(x/width) if x >= 0 else int((x + 1)/width) - 1,
        int(y/height) if y >= 0 else int((y + 1)/height) - 1
    )


def part_2(lines):
    grid = []
    start_x, start_y = None, None
    for y, line in enumerate(lines):
        line = line.strip()
        for x, char in enumerate(line):
            if char == START:
                start_x = x
                start_y = y
        grid.append(list(line))

    width = len(grid[0])
    height = len(grid)

    # Keep track in initial starting grid which tiles are even and which are odd. Even tiles
    # can always be reached again and odds cannot.
    even = set()
    odd = set()
    num_steps = 0
    starts = [(start_x, start_y)]
    while num_steps < 66:
        new_starts = set()
        for x, y in starts:
            if (x, y) in even | odd:
                continue
            (even if num_steps % 2 == 0 else odd).add((x, y))
            dir_coords = get_cardinal_direction_coords(x, y, grid=grid)
            for _, nx, ny in dir_coords:
                if grid[ny][nx] in TRAVERSIBLE:
                    new_starts.add((nx, ny))

        num_steps += 1
        starts = new_starts

    # for y, row in enumerate(grid):
    #     line = ''
    #     for x, char in enumerate(row):
    #         if (x, y) in even:
    #             line += 'x'
    #         elif (x, y) in odd:
    #             line += 'o'
    #         else:
    #             line += char
    #     print(line)

    print('even', len(even))
    print('odd', len(odd))

    """
    We make a diamond that repeats in 66 steps from the origin. Since total number of steps is odd,
    all odd cells are viable in this first diamond. For this first diamond, counts are even 3637, odd 3699.

    With each additional 131 steps beyond that, we create additional diamonds. Each diamond adjacent to the origin
    diamond flips its even/odd parity. For 9 diamonds (197 steps), counts are even 33137, odd 32947. Taking out
    the middle diamond, we get even 29500 and odd 29248 across 8 diamonds.

    (26501365 - 65)/131 = 202300
    202300*2+1 = 404601
    404601^2 = 163701969201 diamonds total
    """

    # There are two types of diamonds -- ones that are the same as the original center diamond, and another
    # that is constructed from putting the four corners of the grid together. I grabbed counts of even/odd
    # for both types.
    ORIGIN_EVEN = 3637
    ORIGIN_ODD = 3699

    INTERCARD_ODD = 3583
    INTERCARD_EVEN = 3769

    """
    Since we have an odd number of steps, we want the total number of odd tiles. However, even and odd counts
    flip per adjacent diamond.
    """
    value = ORIGIN_ODD
    last_root = 1
    for step in range(202300 + 1):
        root = step * 2 + 1
        outer_blocks = math.pow(root, 2) - last_root
        value += outer_blocks//2 * (ORIGIN_ODD if step % 2 == 0 else ORIGIN_EVEN)
        if step > 0:
            num_intercards = outer_blocks//2
            value += num_intercards//2 * INTERCARD_ODD
            value += num_intercards//2 * INTERCARD_EVEN
        last_root = math.pow(root, 2)
        # print(step, value, key.get(step))

    return value


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

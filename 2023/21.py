"""
Part 1:
Part 2:
"""
import os
import sys
import time

from collections import defaultdict
from util import get_cardinal_direction_coords, run

ROCK = '#'
GARDEN = '.'
START = 'S'
TRAVERSIBLE = {GARDEN, START}

STEPS = None


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
    while starts:
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

    total_garden_tiles_per_grid = len(even | odd)

    # print('original grid')
    # for y, row in enumerate(grid):
    #     line = ''
    #     for x, char in enumerate(row):
    #         if (x, y) in even:
    #             line += 'E'
    #         elif (x, y) in odd:
    #             line += 'O'
    #         else:
    #             line += char
    #     print(line)
    # print()

    # For repeating grids, let (gx, gy) represent the grid's relative position
    # to the original grid, where the grid to the right is (1, 0), grid to the NW is (-1, -1),
    # and the original grid is (0, 0). We use floodfill to see if a whole grid has coverage,
    # and if not, we only need to analyze steps for those grids to determine partial coverage.
    grids_touched = defaultdict(set)
    grids_fully_traversed = set()
    is_flipped = {} # grid coords to whether it's flipped from original on even/odd

    # Use a flood fill from origin to explore how many repeated grids can be reached.
    # For each grid, determine when it was entered and how many steps were left when it was.
    num_steps = 0
    starts = [(start_x, start_y)]
    walked = defaultdict(set)
    while num_steps <= STEPS:
        new_starts = set()
        for x, y in starts:
            grid_coords = get_grid_coord(x, y, width, height)
            ex, ey = get_equivalent_coord(x, y, width, height)

            if grid_coords in grids_fully_traversed or (ex, ey) in walked[grid_coords]:
                continue
            walked[grid_coords].add((ex, ey))
            if len(walked[grid_coords]) == total_garden_tiles_per_grid:
                grids_fully_traversed.add(grid_coords)
                # Save some memory?
                walked[grid_coords] = set()

            if grid_coords not in grids_touched:
                # First time encountering this grid -- is the first step even or odd?
                is_flipped[grid_coords] = num_steps % 2 == 1

            grids_touched[grid_coords].add((ex, ey, num_steps))

            dir_coords = get_cardinal_direction_coords(x, y)
            for _, nx, ny in dir_coords:
                enx, eny = get_equivalent_coord(nx, ny, width, height)
                if grid[eny][enx] in TRAVERSIBLE:
                    new_starts.add((nx, ny))

        num_steps += 1
        starts = new_starts

    # First count up possible positions in all grids that were fully traversed. If
    # their first step into the grid was even and number of steps is even, the even
    # tiles are accessible, otherwise the odd tiles are accessible.
    total = 0
    even_is_good = STEPS % 2 == 0
    for grid_coords in grids_fully_traversed:
        flipped = is_flipped[grid_coords]
        if even_is_good:
            if is_flipped:
                total += len(odd)
            else:
                total += len(even)
        else:
            if is_flipped:
                total += len(even)
            else:
                total += len(odd)

    # print(grids_touched)
    # print(grids_fully_traversed)

    # Now for all grids that were only partially traversed, determine reachable
    # cells more manually
    for grid_coords, entry_points in grids_touched.items():
        # print(grid_coords)
        if grid_coords in grids_fully_traversed:
            continue

        grid_evens = set()
        grid_odds = set()

        for (ex, ey, num_steps) in entry_points:
            # print('(%d, %d): %d' % (ex, ey, num_steps))
            starts = [(ex, ey)]
            while num_steps <= STEPS:
                new_starts = set()
                for x, y in starts:
                    if (x, y) in grid_evens | grid_odds:
                        continue
                    (grid_evens if num_steps % 2 == 0 else grid_odds).add((x, y))
                    dir_coords = get_cardinal_direction_coords(x, y, grid=grid)
                    for _, nx, ny in dir_coords:
                        if grid[ny][nx] in TRAVERSIBLE:
                            new_starts.add((nx, ny))

                num_steps += 1
                starts = new_starts

        if even_is_good:
            total += len(grid_evens)
        else:
            total += len(grid_odds)

        # print('e: %d, o: %d' % (len(grid_evens), len(grid_odds)))

        # for y, row in enumerate(grid):
        #     line = ''
        #     for x, char in enumerate(row):
        #         if (x, y) in grid_evens:
        #             line += 'E'
        #         elif (x, y) in grid_odds:
        #             line += 'O'
        #         else:
        #             line += char
        #     print(line)
        # print()

    solution_key = {
        6: 16,
        10: 50,
        50: 1594,
        100: 6536,
        500: 167004,
        1000: 668697,
        5000: 16733044,
    }
    print('%d should be %d: %s' % (total, solution_key[STEPS], solution_key[STEPS] == total))

    return total


if __name__ == '__main__':
    STEPS = int(sys.argv[-1])
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

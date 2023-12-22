"""
Part 1: Determine how many possible ending spots an elf can end up in a grid after n steps.
Part 2: Do the same for a very high number of steps and an infinite repeating grid.
"""
import math
import os

from collections import defaultdict
from util import get_cardinal_direction_coords, run

ROCK = '#'
GARDEN = '.'
START = 'S'
TRAVERSIBLE = {GARDEN, START}

class DiamondType:
    INNER = 'inner'
    OUTER = 'outer'

class Parity:
    EVEN = 'even'
    ODD = 'odd'


def parse_grid(lines):
    grid = []
    start_x, start_y = None, None
    for y, line in enumerate(lines):
        line = line.strip()
        for x, char in enumerate(line):
            if char == START:
                start_x = x
                start_y = y
        grid.append(list(line))
    return grid, start_x, start_y


def part_1(lines):
    STEPS = 64
    grid, start_x, start_y = parse_grid(lines)

    num_steps = 0
    starts = [(start_x, start_y)]
    while num_steps < STEPS:
        visited, new_starts = set(), set()
        for x, y in starts:
            dir_coords = get_cardinal_direction_coords(x, y, grid=grid)
            for _, nx, ny in dir_coords:
                if grid[ny][nx] in TRAVERSIBLE:
                    visited.add((nx, ny))
                    new_starts.add((nx, ny))
        starts = new_starts
        num_steps += 1

    return len(new_starts)


def part_2(lines):
    """
    This solution is VERY specific to test input, which is a 131x131 square with S in the middle.
    The input also has straight garden lines from the middle to the outer edges and all along the
    edges of the grid. This means as we step out, we form a diamond pattern.
    """
    STEPS = 26501365
    grid, start_x, start_y = parse_grid(lines)
    width = len(grid)

    # Keep track in initial starting grid which tiles are even and which are odd. The odd tiles are
    # valid ending spots if # of steps is odd. If we take width / 2 steps, we fill the inner
    # diamond. While we're at it, find the total even/odd places of the space outside the diamond.
    walked = set()
    parity_sets = defaultdict(set)
    even = parity_sets[(DiamondType.INNER, Parity.EVEN)]
    odd = parity_sets[(DiamondType.INNER, Parity.ODD)]
    num_steps = 0
    starts = [(start_x, start_y)]
    while starts:
        new_starts = set()
        for x, y in starts:
            if (x, y) in walked:
                continue
            walked.add((x, y))
            (even if num_steps % 2 == 0 else odd).add((x, y))
            dir_coords = get_cardinal_direction_coords(x, y, grid=grid)
            for _, nx, ny in dir_coords:
                if grid[ny][nx] in TRAVERSIBLE:
                    new_starts.add((nx, ny))

        num_steps += 1
        if num_steps > width // 2:
            even = parity_sets[(DiamondType.OUTER, Parity.EVEN)]
            odd = parity_sets[(DiamondType.OUTER, Parity.ODD)]

        starts = new_starts

    parity_counts = {key: len(coords) for key, coords in parity_sets.items()}

    """
    With each additional `width` steps beyond the original starting point, we create additional
    diamonds. Each diamond adjacent to the inner diamond flips its even/odd parity. Outer diamonds always come in equal numbers of odd/even parities, so we don't worry about flipping them.

    For example, if we are taking 26501365 steps, after subtracting out the original 65 to get to
    the edge of the diamond, we get (26501365 - 65)/131 = 202300 expansions of the inner diamond.

    Now we just add the proper even or odd values as we expand out the diamond.
    """
    even_is_good = STEPS % 2 == 0
    expansions = (STEPS - (width - 1)//2) // width
    value = parity_counts[(DiamondType.INNER, Parity.ODD)]  # Initial diamond only
    last_root = 1
    for step in range(expansions + 1):
        step_is_even = step % 2 == 0

        # Square root of the number of diamonds
        root = step * 2 + 1

        # Get the outer blocks, which are the new values to add
        outer_blocks = math.pow(root, 2) - last_root

        # Add the copies of the inner diamond, which will be half of the outer blocks.
        # If we're on an even expansion, we'll want to add the count of the same parity
        # as the number of steps.
        value += outer_blocks // 2 * (
            parity_counts[(DiamondType.INNER, Parity.EVEN)] if even_is_good == step_is_even
            else parity_counts[(DiamondType.INNER, Parity.ODD)]
        )

        if step > 0:
            # Other half of the outer blocks are equal numbers of even and odd outer diamonds
            value += outer_blocks // 4 * (
                parity_counts[(DiamondType.OUTER, Parity.EVEN)] +
                parity_counts[(DiamondType.OUTER, Parity.ODD)]
            )
        last_root = math.pow(root, 2)

    return int(value)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

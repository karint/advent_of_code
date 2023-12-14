import os
import json
import re

from collections import defaultdict
from util import run


def part_1(lines):
    answer = 0
    grid = []
    rocks = set()
    for y, line in enumerate(lines):
        line = line.strip()
        grid.append(line)
        for x, char in enumerate(line):
            if char == 'O':
                rocks.add((x, y))

    shifted_grid = []

    for x in range(len(grid[0])):
        col = []
        banked_cells = []
        last_block = -1
        for y in range(len(grid)):
            cell = grid[y][x]
            if cell == '#':
                last_block = y
                col += list(sorted(banked_cells, reverse=True))
                banked_cells = []
                col += '#'
                continue
            elif cell == 'O':
                last_block = y
                banked_cells.append('O')
            elif cell == '.':
                banked_cells.append('.')

        col += list(sorted(banked_cells, reverse=True))
        col.reverse()
        print(col)

        answer += sum(
            i + 1 if char == 'O' else 0 for i, char in enumerate(col)
        )
        
    return answer


def part_2(lines):
    num_cycles = 1000000000

    MEMO = {}

    answer = 0
    orig_grid = []
    for y, line in enumerate(lines):
        line = line.strip()
        orig_grid.append(line)

    grid = orig_grid
    loop_starts = None
    loop_starts_again = None
    for cycle in range(num_cycles):
        total = 0
        key = ''
        for row in grid:
            key += ''.join(row)
        if not loop_starts and key in MEMO:
            # We've been here before
            loop_starts = MEMO[key]
            loop_starts_again = cycle
            print('loop is', loop_starts, loop_starts_again)
            break
        else:
            MEMO[key] = cycle

        for tilt in range(4):
            shifted_grid = []
            for x in range(len(grid[0])):
                col = []
                banked_cells = []
                last_block = -1
                for y in range(len(grid)):
                    cell = grid[y][x]
                    if cell == '#':
                        last_block = y
                        col += list(sorted(banked_cells, reverse=True))
                        banked_cells = []
                        col += '#'
                        continue
                    elif cell == 'O':
                        last_block = y
                        banked_cells.append('O')
                    elif cell == '.':
                        banked_cells.append('.')

                col += list(sorted(banked_cells, reverse=True))
                col.reverse()
                shifted_grid.append(col)

            grid = shifted_grid

    loop_length = loop_starts_again - loop_starts
    loops_left = (num_cycles - loop_starts) % loop_length
    print(loop_length, loops_left)
    for cycle in range(loops_left):
        total = 0
        for tilt in range(4):
            shifted_grid = []
            for x in range(len(grid[0])):
                col = []
                banked_cells = []
                last_block = -1
                for y in range(len(grid)):
                    cell = grid[y][x]
                    if cell == '#':
                        last_block = y
                        col += list(sorted(banked_cells, reverse=True))
                        banked_cells = []
                        col += '#'
                        continue
                    elif cell == 'O':
                        last_block = y
                        banked_cells.append('O')
                    elif cell == '.':
                        banked_cells.append('.')

                col += list(sorted(banked_cells, reverse=True))
                col.reverse()
                shifted_grid.append(col)

            grid = shifted_grid

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == 'O':
                answer += len(grid) - y

    return answer


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)


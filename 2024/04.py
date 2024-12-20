"""
Part 1: Find all instances of XMAS in the word find.
Part 2: Find all instances of two crossing MAS in word find.
"""
import os

from util import rotate_45, rotate_90, run


def part_1(lines):
    total = 0

    grid = [l.strip() for l in lines]
    for _ in range(4):
        total += sum(line.count('XMAS') for line in grid)

        diag_grid = rotate_45(grid)
        total += sum(line.count('XMAS') for line in diag_grid)

        grid = rotate_90(grid)

    return total


def part_2(lines):
    total = 0

    grid = [l.strip() for l in lines]

    width = len(grid[0])
    height = len(grid)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if grid[i][j] != 'A':
                continue

            nw = grid[i - 1][j - 1]
            ne = grid[i - 1][j + 1]
            sw = grid[i + 1][j - 1]
            se = grid[i + 1][j + 1]

            if (nw, ne, sw, se) in (
                ('M', 'S', 'M', 'S'),
                ('M', 'M', 'S', 'S'),
                ('S', 'M', 'S', 'M'),
                ('S', 'S', 'M', 'M'),
            ):
                total += 1

    return total


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

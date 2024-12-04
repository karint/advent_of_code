"""
Part 1:
Part 2:
"""
import os

from util import run

WORD = 'XMAS'


def part_1(lines):
    total = 0

    grid = [l.strip() for l in lines]
    for _ in range(4):
        total += sum(line.count(WORD) for line in grid)

        width = len(grid[0])
        height = len(grid)

        # Rotate original grid 45º
        diag_grid = []
        for i in range(height):
            temp = []
            length_of_row = i + 1
            for j in range(length_of_row):
                temp.append(grid[length_of_row - j - 1][j])
            diag_grid.append(''.join(temp))
            # print(''.join(temp))

            if i == height - 1:
                continue

            temp = []
            for j in range(length_of_row):
                temp.append(grid[height - (length_of_row - j - 1) - 1][width - j - 1])
            temp.reverse()
            diag_grid.append(''.join(temp))
            # print(''.join(temp))

        total += sum(line.count(WORD) for line in diag_grid)

        # Rotate original grid 90º
        new_grid = []
        for j in range(height):
            temp = []
            for i in range(width):
                temp.append(grid[i][width - j - 1])
            new_grid.append(''.join(temp))
            # print(''.join(temp))

        grid = new_grid

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

            if (
                (nw == 'M' and ne == 'S' and sw == 'M' and se == 'S') or
                (nw == 'M' and ne == 'M' and sw == 'S' and se == 'S') or
                (nw == 'S' and ne == 'M' and sw == 'S' and se == 'M') or
                (nw == 'S' and ne == 'S' and sw == 'M' and se == 'M')
            ):
                total += 1

    return total


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

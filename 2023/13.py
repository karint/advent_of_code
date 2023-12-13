import os
import json
import re

from collections import defaultdict
from util import run


def get_reflection_line(grid):
    width = len(grid[0])
    height = len(grid)

    for row_to_try in range(1, height):
        # Try rows
        grid_a = grid[0:row_to_try]
        grid_b = grid[row_to_try:2*row_to_try]
        grid_b.reverse()

        if len(grid_a) == len(grid_b):
            if all(grid_a[i] == grid_b[i] for i in range(len(grid_a))):
                return (row_to_try, None)

        grid_a = grid_a[-len(grid_b):]
        if all(grid_a[i] == grid_b[i] for i in range(len(grid_b))):
            return (row_to_try, None)

    transposed_grid = []
    for x in range(width):
        transposed_grid.append([])

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            transposed_grid[x].append(char)

    width = len(transposed_grid[0])
    height = len(transposed_grid)

    for row_to_try in range(1, height):
        # Try rows
        grid_a = transposed_grid[0:row_to_try]
        grid_b = transposed_grid[row_to_try:2*row_to_try]
        grid_b.reverse()

        if len(grid_a) == len(grid_b):
            if all(grid_a[i] == grid_b[i] for i in range(len(grid_a))):
                return (None, row_to_try)

        grid_a = grid_a[-len(grid_b):]
        if all(grid_a[i] == grid_b[i] for i in range(len(grid_b))):
            return (None, row_to_try)

    print('NO LINE')
    for row in grid:
        print(row)


def get_reflection_line_2(grid):
    width = len(grid[0])
    height = len(grid)

    for row_to_try in range(1, height):
        diff = 0

        # Try rows
        grid_a = grid[0:row_to_try]
        grid_b = grid[row_to_try:2*row_to_try]
        grid_b.reverse()

        if len(grid_a) == len(grid_b):
            for i in range(len(grid_a)):
                for j in range(width):
                    if grid_a[i][j] != grid_b[i][j]:
                        diff += 1
            if diff == 1:
                return (row_to_try, None)
        else:
            grid_a = grid_a[-len(grid_b):]
            for i in range(len(grid_b)):
                for j in range(width):
                    if grid_a[i][j] != grid_b[i][j]:
                        diff += 1
            if diff == 1:
                return (row_to_try, None)

    transposed_grid = []
    for x in range(width):
        transposed_grid.append([])

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            transposed_grid[x].append(char)

    width = len(transposed_grid[0])
    height = len(transposed_grid)

    for row_to_try in range(1, height):
        diff = 0

        # Try rows
        grid_a = transposed_grid[0:row_to_try]
        grid_b = transposed_grid[row_to_try:2*row_to_try]
        grid_b.reverse()

        if len(grid_a) == len(grid_b):
            for i in range(len(grid_a)):
                for j in range(width):
                    if grid_a[i][j] != grid_b[i][j]:
                        diff += 1
            if diff == 1:
                return (None, row_to_try)
        else:
            grid_a = grid_a[-len(grid_b):]
            for i in range(len(grid_b)):
                for j in range(width):
                    if grid_a[i][j] != grid_b[i][j]:
                        diff += 1
            if diff == 1:
                return (None, row_to_try)

    print('NO LINE')
    for row in grid:
        print(row)


def part_1(lines):
    answer = 0
    grid = []
    for line in lines:
        line = line.strip()

        # New grid
        if not line:
            (row, col) = get_reflection_line(grid)
            if row:
                print('row', row)
                answer += 100 * (row)
            elif col:
                print('col', col)
                answer += col
            grid = []
            continue

        grid.append(line)

    (row, col) = get_reflection_line(grid)
    if row:
        print('row', row)
        answer += 100 * (row)
    elif col:
        print('col', col)
        answer += col

    return answer


def part_2(lines):
    answer = 0
    grid = []
    for line in lines:
        line = line.strip()

        # New grid
        if not line:
            (row, col) = get_reflection_line_2(grid)
            if row:
                print('row', row)
                answer += 100 * (row)
            elif col:
                print('col', col)
                answer += col
            grid = []
            continue

        grid.append(line)

    (row, col) = get_reflection_line_2(grid)
    if row:
        print('row', row)
        answer += 100 * row
    elif col:
        print('col', col)
        answer += col

    return answer


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

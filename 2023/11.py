import os
import json
import re

from collections import defaultdict
from itertools import combinations
from util import run


def part_1(lines):
    grid = []
    width = len(lines[0].strip())
    height = len(lines)
    rows_with_gal = set()
    cols_with_gal = set()
    for y, line in enumerate(lines):
        line = line.strip()
        row = []
        for x, char in enumerate(line):
            if char == '#':
                rows_with_gal.add(y)
                cols_with_gal.add(x)
            row.append(char)
        grid.append(row)

    diff = 0
    for row_index in range(height):
        if row_index in rows_with_gal:
            continue

        grid.insert(row_index + diff, ['.'] * width)
        diff += 1


    diff = 0
    for col_index in range(width):
        if col_index in cols_with_gal:
            continue

        for row in grid:
            row.insert(col_index + diff, '.')
        diff += 1


    num_gal = 0
    galaxies = {}
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == '#':
                galaxies[num_gal] = (x, y)
                num_gal += 1

    pairs = combinations(range(num_gal), 2)

    answer = 0
    for i, (start, end) in enumerate(pairs):
        start_x, start_y = galaxies[start]
        end_x, end_y = galaxies[end]

        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)
        answer += dx + dy

    return answer


def part_2(lines):
    multiple = 1000000 - 1

    grid = []
    width = len(lines[0].strip())
    height = len(lines)
    rows_with_gal = set()
    cols_with_gal = set()
    num_gal = 0
    galaxies = {}
    for y, line in enumerate(lines):
        line = line.strip()
        row = []
        for x, char in enumerate(line):
            if char == '#':
                rows_with_gal.add(y)
                cols_with_gal.add(x)
                galaxies[num_gal] = (x, y)
                num_gal += 1
            row.append(char)
        grid.append(row)

    pairs = combinations(range(num_gal), 2)

    answer = 0

    for i, (start, end) in enumerate(pairs):
        start_x, start_y = galaxies[start]
        end_x, end_y = galaxies[end]

        # How many expansions are between x's
        span = range(start_x, end_x) if start_x < end_x else range(end_x, start_x)
        num_x_expansions = 0
        for x in span:
            if x not in cols_with_gal:
                num_x_expansions += 1
        dx = abs(start_x - end_x) + num_x_expansions * multiple

        # How many expansions are between y's
        span = range(start_y, end_y) if start_y < end_y else range(end_y, start_y)
        num_y_expansions = 0
        for y in span:
            if y not in rows_with_gal:
                num_y_expansions += 1
        dy = abs(start_y - end_y) + num_y_expansions * multiple

        answer += dx + dy

    return answer


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

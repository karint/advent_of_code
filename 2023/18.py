"""
Part 1: Dig a trench and find the area.
Part 2: The trench is really big.
"""
import math
import os
import sys

from util import Direction, run

DIR_MAP = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
}

def move(direction, x, y, steps=1):
    if direction == 'R':
        return (x + steps, y)
    if direction == 'D':
        return (x, y + steps)
    if direction == 'L':
        return (x - steps, y)
    if direction == 'U':
        return (x, y - steps)


def shoelace(vertices):
    # The Shoelace Algorithm - www.101computing.net/the-shoelace-algorithm
    total = 0
    for i, (x, y) in enumerate(vertices):
        if i == len(vertices) - 1:
            continue
        next_vertex = vertices[i + 1]
        total += x * next_vertex[1] - y * next_vertex[0]

    total += vertices[-1][0] * vertices[0][1] - vertices[-1][1] * vertices[0][0]
    return abs(total) / 2


def find_trench_area(lines, parse_ln_fn):
    trench_lines = []
    perimeter = 0
    curr_x, curr_y = 0, 0
    for line in lines:
        line = line.strip()
        direction, num_steps = parse_ln_fn(line)
        perimeter += num_steps
        curr_x, curr_y = move(direction, curr_x, curr_y, steps=num_steps)
        trench_lines.append((curr_x, curr_y))
    return int(shoelace(trench_lines) + perimeter/2 + 1)


def part_1(lines):
    def parse(line):
        direction, num_steps, _ = line.split(' ')
        return direction, int(num_steps)
    return find_trench_area(lines, parse)


def part_2(lines):
    def parse(line):
        _, _, hex_code = line.split(' ')
        hex_code = hex_code[2:-1]
        return DIR_MAP[hex_code[-1]], int(hex_code[:5], 16)
    return find_trench_area(lines, parse)


if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

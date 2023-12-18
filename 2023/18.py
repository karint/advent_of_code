"""
Part 1: 
Part 2:
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


def flood_fill(visited, curr_x, curr_y, grid):
    all_directions = [
        (curr_x + 1, curr_y),
        (curr_x, curr_y + 1),
        (curr_x - 1, curr_y),
        (curr_x, curr_y - 1),
    ]
    new_visited = set()
    for x, y in all_directions:
        if (x, y) in visited:
            continue
        if x >= 0 and y >=0 and x < len(grid[0]) and y < len(grid):
            if grid[y][x] == '.':
                new_visited.add((x, y))

    visited |= new_visited

    for x, y in new_visited:
        flood_fill(visited, x, y, grid)


def part_1(lines):
    answer = 0
    plan = []
    for line in lines:
        line = line.strip()
        direction, num_steps, hex_code = line.split(' ')
        plan.append((direction, num_steps))

    curr_x, curr_y = 0, 0
    trench_lines = set()
    for direction, num_steps in plan:
        num_steps = int(num_steps)
        for _ in range(num_steps):
            curr_x, curr_y = move(direction, curr_x, curr_y, steps=1)
            trench_lines.add((curr_x, curr_y))

    min_x = min(x for x, _ in trench_lines)
    min_y = min(y for _, y in trench_lines)

    trench_lines = set((x - min_x, y - min_y) for x, y in trench_lines)

    width = max(x for x, _ in trench_lines) + 1
    height = max(y for _, y in trench_lines) + 1

    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append('.' if (x, y) not in trench_lines else '#')
        grid.append(row)

    # Flood fill
    interior = set()
    flood_fill(interior, 20, 34, grid)

    # for y in range(height):
    #     line = ''
    #     for x in range(width):
    #         if (x, y) in trench_lines:
    #             line += '#'
    #         elif (x, y) in interior:
    #             line += 'o'
    #         else:
    #             line += '.'
    #     print(line)

    return len(interior | trench_lines)


# The Shoelace Algorithm - www.101computing.net/the-shoelace-algorithm
def shoelace(vertices):
    total = 0
    num_vertices = len(vertices)

    for i, (x, y) in enumerate(vertices):
        if i == len(vertices) - 1:
            continue

        next_vertex = vertices[i + 1]
        total += x * next_vertex[1] - y * next_vertex[0]

    last_vertex = vertices[-1]
    first_vertex = vertices[0]
    total += last_vertex[0] * first_vertex[1] - last_vertex[1] * first_vertex[0]
    area = abs(total) / 2
    return int(area)


def part_2(lines):
    answer = 0
    plan = []
    for line in lines:
        line = line.strip()
        _, _, hex_code = line.split(' ')
        hex_code = hex_code[2:-1]
        direction = DIR_MAP[hex_code[-1]]
        num_steps = int(hex_code[:5], 16)
        print(direction, num_steps)
        plan.append((direction, num_steps))

    curr_x, curr_y = 0, 0
    trench_lines = []
    perimeter = 0
    for direction, num_steps in plan:
        num_steps = int(num_steps)
        perimeter += num_steps
        curr_x, curr_y = move(direction, curr_x, curr_y, steps=num_steps)
        trench_lines.append((curr_x, curr_y))

    return shoelace(trench_lines) + perimeter/2 + 1


if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

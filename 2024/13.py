"""
Part 1:
Part 2:
"""
import os

from math import isclose
from util import run

COST_A = 3
COST_B = 1
MAX_PER_BUTTON = 100


def part_1(lines):
    tokens = 0
    for i in range(len(lines) // 4 + 1):
        index = i * 4
        a = lines[index].strip().split(': ')[1]
        b = lines[index + 1].strip().split(': ')[1]
        x = lines[index + 2].strip().split(': ')[1]

        x_str, y_str = a.split(', ')
        ax = int(x_str.split('+')[1])
        ay = int(y_str.split('+')[1])

        x_str, y_str = b.split(', ')
        bx = int(x_str.split('+')[1])
        by = int(y_str.split('+')[1])

        x_str, y_str = x.split(', ')
        x = int(x_str.split('=')[1])
        y = int(y_str.split('=')[1])

        min_cost = None
        for a_pressed in range(MAX_PER_BUTTON + 1):
            for b_pressed in range(MAX_PER_BUTTON + 1):
                if (
                    (a_pressed * ax + b_pressed * bx) == x and
                    (a_pressed * ay + b_pressed * by) == y
                ):
                    cost = COST_A * a_pressed + COST_B * b_pressed
                    if min_cost is None or min_cost > cost:
                        min_cost = cost

        if min_cost is not None:
            tokens += min_cost

    return tokens


def part_2(lines):
    tokens = 0
    for i in range(len(lines) // 4 + 1):
        index = i * 4
        a = lines[index].strip().split(': ')[1]
        b = lines[index + 1].strip().split(': ')[1]
        x = lines[index + 2].strip().split(': ')[1]

        x_str, y_str = a.split(', ')
        ax = int(x_str.split('+')[1])
        ay = int(y_str.split('+')[1])

        x_str, y_str = b.split(', ')
        bx = int(x_str.split('+')[1])
        by = int(y_str.split('+')[1])

        x_str, y_str = x.split(', ')
        x = int(x_str.split('=')[1]) + 10000000000000
        y = int(y_str.split('=')[1]) + 10000000000000

        # y = mx + b
        a_slope = float(ay)/ax
        b_slope = float(by)/bx
        ya = y - a_slope * x
        yb = y - b_slope * x

        # Now find intersection of the b-line that goes through the dest point
        # and the a-line that starts from (0, 0).
        x_intersect = yb/(a_slope - b_slope)

        num_a = round(x_intersect / ax)
        num_b = round((x - x_intersect) / bx)

        if not (
            num_a * ax + num_b * bx == x and
            num_a * ay + num_b * by == y
        ):
            continue

        if yb == 0:
            tokens += x / bx * COST_B
        elif ya == 0:
            tokens += x / ax * COST_A
        elif num_a >= 0 and num_b >= 0:
            tokens += num_a * COST_A + num_b * COST_B
        else:
            print('Unsolvable:', i + 1)

    return tokens


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

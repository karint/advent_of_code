"""
Part 1: Find highest integer formed by 2 digits of a string.
Part 2: Find highest integer formed by 12 digits of a string.
"""
import os

from util import run

DIGIT_DESC_ORDER = '9876543210'


def max_joltage(line, digits_left=12):
    if digits_left == 1:
        return max(d for d in line)

    line_length = len(line)
    for digit in DIGIT_DESC_ORDER:
        try:
            num_index = line.index(digit)
            if num_index <= line_length - digits_left:
                return line[num_index] + max_joltage(line[num_index + 1:], digits_left=digits_left-1)
        except ValueError:
            continue

    return line


def part_1(lines):
    return sum(int(max_joltage(line.strip(), digits_left=2)) for line in lines)


def part_2(lines):
    return sum(int(max_joltage(line.strip(), digits_left=12)) for line in lines)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

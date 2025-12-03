"""
Part 1: Find highest integer formed by 2 digits of a string.
Part 2: Find highest integer formed by 12 digits of a string.
"""
import os

from collections import Counter
from util import find_digits, run

DIGITS = '9876543210'


def max_joltage(line, digits=12):
    if digits == 1:
        return max(int(d) for d in line)

    curr_max = 0
    for digit in DIGITS:
        try:
            num_index = line.index(digit)

            if 0 <= num_index <= len(line) - digits:
                rest = max_joltage(line[num_index + 1:], digits=digits-1)
                curr_max = max(curr_max, int(line[num_index] + str(rest)))
                return curr_max

        except ValueError:
            continue

    return int(line)


def part_1(lines):
    return sum(max_joltage(line.strip(), digits=2) for line in lines)


def part_2(lines):
    return sum(max_joltage(line.strip(), digits=12) for line in lines)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

"""
Part 1: Find highest integer formed by 2 digits of a string.
Part 2: Find highest integer formed by 12 digits of a string.
"""
import os

from collections import Counter
from util import find_digits, run

DIGITS = '9876543210'


def max_joltage(line):
    curr_max = None
    num_index, second_num_index = None, None
    for i, digit in enumerate(DIGITS):
        try:
            num_index = line.index(digit)

            if num_index is not None and num_index >= 0 and num_index < len(line) - 1:
                second_num = max(int(line[j]) for j in range(num_index + 1, len(line)))

                new_max = int(line[num_index] + str(second_num))
                if curr_max is None:
                    curr_max = new_max
                else:
                    curr_max = max(curr_max, new_max)

        except ValueError:
            continue
    return curr_max


def max_joltage_2(line, remaining_digits=12):
    if remaining_digits == 1:
        return max(int(d) for d in line)

    curr_max = None
    num_indices = [None] * remaining_digits

    for i, digit in enumerate(DIGITS):
        try:
            num_index = line.index(digit)

            if num_index is not None and num_index >= 0 and num_index <= len(line) - remaining_digits:
                rest = max_joltage_2(line[num_index + 1:], remaining_digits=remaining_digits-1)

                new_max = int(line[num_index] + str(rest))
                if curr_max is None:
                    curr_max = new_max
                else:
                    curr_max = max(curr_max, new_max)

        except ValueError:
            continue
                    
        if curr_max:
            return curr_max

    return curr_max


def part_1(lines):
    count = 0
    for line in lines:
        max_j = max_joltage(line.strip())
        count += max_j

    return count


def part_2(lines):
    count = 0
    for line in lines:
        max_j = max_joltage_2(line.strip())
        count += max_j

    return count


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

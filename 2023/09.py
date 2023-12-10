"""
Part 1: Predict the next number in a sequence of values.
Part 2: Predict the number before a sequence of values.
"""
import operator
import os

from util import find_digits, run


def get_totals(lines, reverse=False):
    total = 0
    for line in lines:
        sequences = [find_digits(line)]

        if reverse:
            sequences[0].reverse()

        while any(val != 0 for val in sequences[-1]):
            sequences.append([
                sequences[-1][i] - sequences[-1][i - 1]
                for i in range(1, len(sequences[-1]))
            ])

        sequences.reverse()
        sequences[0].append(0)
        for i in range(1, len(sequences)):
            sequences[i].append(sequences[i][-1] + sequences[i - 1][-1])
        total += sequences[i][-1]
    return total


def part_1(lines):
    return get_totals(lines)


def part_2(lines):
    return get_totals(lines, reverse=True)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

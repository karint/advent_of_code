"""
Part 1: Find the sum of differences between two ordered lists.
Part 2: Find the similarity score between two lists.
"""
import os

from collections import Counter
from util import run


def _create_lists(lines):
    first, second = [], []
    for line in lines:
        one, two = map(int, line.split('   '))
        first.append(one)
        second.append(two)
    return first, second


def part_1(lines):
    first, second = _create_lists(lines)
    first.sort()
    second.sort()
    return sum(abs(a - b) for a, b in zip(first, second))


def part_2(lines):
    first, second = _create_lists(lines)
    counts = Counter(second)
    return sum(a * counts.get(a, 0) for a in first)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

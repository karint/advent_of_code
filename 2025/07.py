"""
Part 1: Count how many times a beam of light splits into unique new beams.
Part 2: Count the number of possible paths through splitters.
"""
import os

from collections import defaultdict
from util import run


def part_1(lines):
    width = len(lines[0])
    height = len(lines)
    def is_in_grid(x, y):
        return 0 <= x < width and 0 <= y < height

    start = None
    splitters = set()
    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            if char == 'S':
                start = (x, y)
            elif char == '^':
                splitters.add((x, y))

    split_count = 0
    beams = set()
    beams.add(start)
    while beams:
        new_beams = set()
        for bx, by in beams:
            split = False
            down = (bx, by + 1)
            if down in splitters:
                left = (bx - 1, by + 1)
                right = (bx + 1, by + 1)
                if is_in_grid(*left):
                    new_beams.add(left)
                    split = True
                if is_in_grid(*right):
                    new_beams.add(right)
                    split = True
            elif is_in_grid(*down):
                new_beams.add(down)

            if split:
                split_count += 1
        beams = new_beams

    return split_count


def part_2(lines):
    width = len(lines[0])
    height = len(lines)
    def is_in_grid(x, y):
        return 0 <= x < width and 0 <= y < height

    start = None
    splitters = set()
    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            if char == 'S':
                start = (x, y)
            elif char == '^':
                splitters.add((x, y))

    beams = set()
    beams.add(start)
    beam_dimensions = defaultdict(int)
    beam_dimensions[start] += 1
    while beams:
        new_beams = set()
        for bx, by in beams:
            down = (bx, by + 1)
            if down in splitters:
                left = (bx - 1, by + 1)
                right = (bx + 1, by + 1)
                if is_in_grid(*left):
                    new_beams.add(left)
                    beam_dimensions[left] += beam_dimensions[(bx, by)]
                if is_in_grid(*right):
                    new_beams.add(right)
                    beam_dimensions[right] += beam_dimensions[(bx, by)]

            elif is_in_grid(*down):
                new_beams.add(down)
                beam_dimensions[down] += beam_dimensions[(bx, by)]

        beams = new_beams

    return sum(d for (x, y), d in beam_dimensions.items() if y == height - 1)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

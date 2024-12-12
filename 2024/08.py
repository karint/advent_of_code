"""
Part 1:
Part 2:
"""
import os

from collections import defaultdict
from itertools import combinations
from util import run


def get_an_coord(first_coord, second_coord):
    dx = first_coord[0] - second_coord[0]
    dy = first_coord[1] - second_coord[1]
    return (first_coord[0] + dx, first_coord[1] + dy)


def get_an_coords(first_coord, second_coord, width, height):
    coords = set()

    curr_x, curr_y = first_coord
    dx = first_coord[0] - second_coord[0]
    dy = first_coord[1] - second_coord[1]
    while (
        curr_x >= 0 and curr_x < width and
        curr_y >= 0 and curr_y < height
    ):
        coords.add((curr_x, curr_y))
        curr_x += dx
        curr_y += dy

    curr_x, curr_y = second_coord
    dx = second_coord[0] - first_coord[0]
    dy = second_coord[1] - first_coord[1]
    while (
        curr_x >= 0 and curr_x < width and
        curr_y >= 0 and curr_y < height
    ):
        coords.add((curr_x, curr_y))
        curr_x += dx
        curr_y += dy
    return coords


def part_1(lines):
    freq_to_coords = defaultdict(set)
    antinodes = set()
    height = len(lines)
    width = len(lines[0].strip())

    for y, line in enumerate(lines):
        line = line.strip()
        for x, char in enumerate(line):
            if char != '.':
                freq_to_coords[char].add((x, y))

    for coord_set in freq_to_coords.values():
        all_pairs = combinations(coord_set, 2)
        for first_coord, second_coord in all_pairs:
            an_x, an_y = get_an_coord(first_coord, second_coord)
            if (
                an_x >= 0 and
                an_y >= 0 and
                an_x < width and
                an_y < height
            ):
                antinodes.add((an_x, an_y))

            an_x, an_y = get_an_coord(second_coord, first_coord)
            if (
                an_x >= 0 and
                an_y >= 0 and
                an_x < width and
                an_y < height
            ):
                antinodes.add((an_x, an_y))

    return len(antinodes)


def part_2(lines):
    freq_to_coords = defaultdict(set)
    antinodes = set()
    height = len(lines)
    width = len(lines[0].strip())

    for y, line in enumerate(lines):
        line = line.strip()
        for x, char in enumerate(line):
            if char != '.':
                freq_to_coords[char].add((x, y))

    for coord_set in freq_to_coords.values():
        all_pairs = combinations(coord_set, 2)
        for first_coord, second_coord in all_pairs:
            an_coords = get_an_coords(
                first_coord, second_coord, width, height
            )
            for an_x, an_y in an_coords:
                if (
                    an_x >= 0 and
                    an_y >= 0 and
                    an_x < width and
                    an_y < height
                ):
                    antinodes.add((an_x, an_y))

    return len(antinodes)



if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

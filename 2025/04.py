"""
Part 1: Find how many rolls of paper have fewer than 4 adjacent rolls of paper.
Part 2: Find how many rolls of paper you can remove if you iteratively remove all
        paper with fewer than 4 adjacent rolls.
"""
import os

from util import get_adjacent_coords, run

PAPER_CHAR = '@'
MOVABLE_MAX_ADJ_ROLLS = 4


def _print_grid(lines, paper_coords):
    for y, row in enumerate(lines):
        s = ''
        for x, char in enumerate(row):
            s += PAPER_CHAR if (x, y) in paper_coords else '.'
        print(s)


def _get_paper_coords(lines):
    return {
        (x, y)
        for y, row in enumerate(lines)
        for x, char in enumerate(row)
        if char == PAPER_CHAR
    }


def part_1(lines):
    paper_coords = _get_paper_coords(lines)

    count = 0
    for x, y in paper_coords:
        adjacent_coords = get_adjacent_coords(x, y)
        if sum(1 if (adj_x, adj_y) in paper_coords else 0 for adj_x, adj_y in adjacent_coords) < MOVABLE_MAX_ADJ_ROLLS:
            count += 1

    return count


def part_2(lines):
    paper_coords = _get_paper_coords(lines)

    count = 0
    while True:
        new_paper_coords = set()
        for x, y in paper_coords:
            adjacent_coords = get_adjacent_coords(x, y)
            if sum(1 if (adj_x, adj_y) in paper_coords else 0 for adj_x, adj_y in adjacent_coords) < MOVABLE_MAX_ADJ_ROLLS:
                count += 1
            else:
                new_paper_coords.add((x, y))
        if len(new_paper_coords) == len(paper_coords):
            break

        paper_coords = new_paper_coords

    return count


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

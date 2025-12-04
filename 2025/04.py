"""
Part 1: 
Part 2: 
"""
import os

from util import run, get_adjacent_coords


def part_1(lines):
    grid = []
    papers = set()
    empty = set()
    for y, row in enumerate(lines):
        grid.append(row)
        for x, char in enumerate(row):
            if char == '@':
                papers.add((x, y))
            else:
                empty.add((x, y))

    count = 0
    good = set()
    for y, row in enumerate(lines):
        s = ''
        for x, char in enumerate(row):
            if char == '@':
                adj = get_adjacent_coords(x, y)
                if (
                    sum(1 if (x2, y2) in papers else 0 for x2, y2 in adj) < 4
                ):
                    count += 1
                    s += 'x'
                else:
                    s += '@'
            else:
                s += '.'

    return count


def part_2(lines):
    grid = []
    empty = set()
    papers = set()
    for y, row in enumerate(lines):
        grid.append(row)
        for x, char in enumerate(row):
            if char == '@':
                papers.add((x, y))
            else:
                empty.add((x, y))

    count = 0
    removed = None
    while removed is None or removed:
        removed = False
        for y, row in enumerate(lines):
            s = ''
            for x, char in enumerate(row):
                if (x, y) in papers:
                    adj = get_adjacent_coords(x, y)
                    if (
                        sum(1 if (x2, y2) in papers else 0 for x2, y2 in adj) < 4
                    ):
                        count += 1
                        removed = True
                        papers.remove((x, y))
                        s += 'x'
                    else:
                        s += '@'
                else:
                    s += '.'
            print(s)


    return count


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

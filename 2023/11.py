import os

from itertools import combinations
from util import run


def solve(lines, galaxy_expansion):
    grid = []
    width = len(lines[0].strip())
    height = len(lines)

    num_galaxies = 0
    galaxy_id_to_coords = {}
    galaxy_rows, galaxy_cols = set(), set()
    for y, line in enumerate(lines):
        line = line.strip()
        for x, char in enumerate(line):
            if char == '#':
                galaxy_rows.add(y)
                galaxy_cols.add(x)
                galaxy_id_to_coords[num_galaxies] = (x, y)
                num_galaxies += 1
        grid.append(line)

    total = 0
    multiple = galaxy_expansion - 1
    all_galaxy_id_pairs = combinations(range(num_galaxies), 2)
    for start_id, end_id in all_galaxy_id_pairs:
        start_x, start_y = galaxy_id_to_coords[start_id]
        end_x, end_y = galaxy_id_to_coords[end_id]

        for start, end, exclusive_set in [
            (start_x, end_x, galaxy_cols),
            (start_y, end_y, galaxy_rows),
        ]:
            span = range(start, end) if start < end else range(end, start)
            num_expansions = sum(1 if i not in exclusive_set else 0 for i in span)
            total += abs(start - end) + num_expansions * multiple

    return total


def part_1(lines):
    return solve(lines, 2)


def part_2(lines):
    return solve(lines, 1000000)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

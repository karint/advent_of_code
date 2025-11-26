"""
Part 1:
Part 2:
"""
import os

from util import Direction, get_cardinal_direction_coords, run


def get_region(x, y, grid):
    char = grid[y][x]
    region = set([(x, y)])
    coords = set([(x, y)])

    while coords:
        new_coords = set()
        for curr_x, curr_y in coords:
            adj_coords = get_cardinal_direction_coords(curr_x, curr_y, grid=grid)
            for _, adj_x, adj_y in adj_coords:
                if grid[adj_y][adj_x] == char:
                    new_coords.add((adj_x, adj_y))
        coords = new_coords - region
        region |= new_coords

    return region


def get_perimeter(coords, grid):
    perimeter = 0
    width = len(grid[0])
    height = len(grid)
    for x, y in coords:
        adj_coords = get_cardinal_direction_coords(x, y)
        for _, adj_x, adj_y in adj_coords:
            if (
                (adj_x, adj_y) not in coords or
                adj_x < 0 or adj_y < 0 or
                adj_x >= width or adj_y >= height
            ):
                perimeter += 1
    return perimeter


def part_1(lines):
    counted = set()
    region_map = {}  # uppermost left coord of region -> all coords in region
    grid = [line.strip() for line in lines]

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if (x, y) in counted:
                continue

            region_coords = get_region(x, y, grid)
            region_map[(x, y)] = region_coords
            counted |= region_coords

    total_price = 0
    for region, coords_in_region in region_map.items():
        area = len(coords_in_region)
        perimeter = get_perimeter(coords_in_region, grid)
        price = area * perimeter
        total_price += price

    return total_price


def get_sides(coords, grid):
    perimeter_segments = set()  # (direction, x, y)
    width = len(grid[0])
    height = len(grid)
    perimeter = 0

    for x, y in coords:
        adj_coords = get_cardinal_direction_coords(x, y)
        for direction, adj_x, adj_y in adj_coords:
            if (
                (adj_x, adj_y) not in coords or
                adj_x < 0 or adj_y < 0 or
                adj_x >= width or adj_y >= height
            ):
                perimeter += 1
                perimeter_segments.add((
                    direction,
                    x,
                    y
                ))

    # Identify perimeter segments that share the same side
    sides = perimeter
    counted = set()
    for (d, x, y) in perimeter_segments:
        if (d, x, y) in counted:
            continue

        if d in (Direction.LEFT, Direction.RIGHT):
            # Adj coords with same x form same side
            if (d, x, y + 1) in perimeter_segments:
                if (d, x, y + 1) not in counted:
                    sides -= 1
            if (d, x, y - 1) in perimeter_segments:
                if (d, x, y - 1) not in counted:
                    sides -= 1
        else:
            # Adj coords with same dir and y form same side
            if (d, x + 1, y) in perimeter_segments:
                if (d, x + 1, y) not in counted:
                    sides -= 1
            if (d, x - 1, y) in perimeter_segments:
                if (d, x - 1, y) not in counted:
                    sides -= 1

        counted.add((d, x, y))

    return sides


def part_2(lines):
    counted = set()
    region_map = {}  # uppermost left coord of region -> all coords in region
    grid = [line.strip() for line in lines]

    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if (x, y) in counted:
                continue

            region_coords = get_region(x, y, grid)
            region_map[(x, y)] = region_coords
            counted |= region_coords

    total_price = 0
    for region, coords_in_region in region_map.items():
        area = len(coords_in_region)
        sides = get_sides(coords_in_region, grid)
        price = area * sides
        total_price += price

    return total_price


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

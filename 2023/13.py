"""
Part 1: Find the line of horizontal or vertical reflection in a pattern.
Part 2: Find the new line of reflection assuming one cell is different.
"""
import os

from util import run


def get_grid_diff(grid_a, grid_b):
    width = len(grid_a[0])
    return sum(
        1 if grid_a[y][x] != grid_b[y][x] else 0
        for x in range(width)
        for y in range(min(len(grid_a), len(grid_b)))
    )


def get_reflection_line(grid, target_diff):
    width = len(grid[0])
    height = len(grid)

    # First, try all the rows as reflection lines
    for row_to_try in range(1, height):
        diff = 0

        grid_a = grid[0:row_to_try]

        # Create a reflection to compare against
        grid_b = grid[row_to_try:2 * row_to_try]
        grid_b.reverse()

        if len(grid_a) == len(grid_b):
            if get_grid_diff(grid_a, grid_b) == target_diff:
                return (row_to_try, None)
        else:
            # Only compare the relevant part of grid a
            # if grid b is smaller
            grid_a = grid_a[-len(grid_b):]
            if get_grid_diff(grid_a, grid_b) == target_diff:
                return (row_to_try, None)

    # If rows don't work, must be a column. Transpose and run again.
    transposed_grid = [[] for _ in range(width)]
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            transposed_grid[x].append(char)

    reflection_line = get_reflection_line(transposed_grid, target_diff)

    # Flip the result since rows became columns
    return reflection_line[1], reflection_line[0]


def process_grids(lines, target_diff):
    answer = 0
    grid = []

    def process_grid():
        row, col = get_reflection_line(grid, target_diff)
        if row:
            return 100 * row
        return col

    for line in lines:
        line = line.strip()

        if line:
            grid.append(line)
        else:
            # Process old grid and start a new one
            answer += process_grid()
            grid = []
            continue

    answer += process_grid()
    return answer


def part_1(lines):
    return process_grids(lines, target_diff=0)


def part_2(lines):
    return process_grids(lines, target_diff=1)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

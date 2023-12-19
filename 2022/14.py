import os
import sys


def create_grid(lines):
    max_row_index = 0
    min_col_index = None
    max_col_index = None
    paths = []  # List of paths, which are lists of tuple coords
    for line in lines:
        coords = line.strip().split(' -> ')
        path = []
        for coord in coords:
            col_index, row_index = map(int, coord.split(','))
            path.append((col_index, row_index))
            if row_index > max_row_index:
                max_row_index = row_index
            if min_col_index is None or col_index < min_col_index:
                min_col_index = col_index
            if max_col_index is None or col_index > max_col_index:
                max_col_index = col_index
        paths.append(path)

    width = max_col_index - min_col_index + 1

    # Map of row index -> [] with array containing True
    # if space is empty, otherwise False
    grid = {
        y: [True] * width for y in range(max_row_index + 1)
    }
    for path in paths:
        last_coord = None
        for x, y in path:
            x -= min_col_index
            grid[y][x] = False
            if last_coord is not None:
                last_x, last_y = last_coord
                if last_x != x:  # Line is horizontal
                    if last_x < x:
                        for index in range(last_x, x + 1):
                            grid[y][index ] = False
                    else:
                        for index in range(x, last_x):
                            grid[y][index ] = False
                elif last_y != y:  # Line is vertical
                    if last_y < y:
                        for index in range(last_y, y + 1):
                            grid[index][x] = False
                    else:
                        for index in range(y, last_y):
                            grid[index][x ] = False

            last_coord = (x, y)
    
    return grid, min_col_index


def simulate_sand(grid, min_col_index):
    resting_sand_count = 0
    height = len(grid)
    width = len(grid[0])
    sand_loc = (500 - min_col_index, 0)  # Starting location
    while True:
        # print_grid(grid)
        sand_x, sand_y = sand_loc

        if sand_y + 1 < height:
            if grid[sand_y + 1][sand_x]: # Try straight down
                sand_loc = (sand_x, sand_y + 1)
            elif sand_x > 0 and grid[sand_y + 1][sand_x - 1]: # Try down left
                sand_loc = (sand_x - 1, sand_y + 1)
            elif sand_x + 1 < width and grid[sand_y + 1][sand_x + 1]: # Try down right
                sand_loc = (sand_x + 1, sand_y + 1)
            elif sand_x == 0 and not grid[sand_y + 1][sand_x]:
                return resting_sand_count
            elif sand_x == width + 1 and not grid[sand_y + 1][sand_x]:
                return resting_sand_count
            else: # Sand is at rest at a wall
                resting_sand_count += 1
                grid[sand_y][sand_x] = False
                sand_loc = (500 - min_col_index, 0)  # New sad location
        else: # Sand fell off to the void
            return resting_sand_count


def create_grid2(lines):
    max_row_index = 0
    min_col_index = None
    max_col_index = None
    paths = []  # List of paths, which are lists of tuple coords
    for line in lines:
        coords = line.strip().split(' -> ')
        path = []
        for coord in coords:
            col_index, row_index = map(int, coord.split(','))
            path.append((col_index, row_index))
            if row_index > max_row_index:
                max_row_index = row_index
            if min_col_index is None or col_index < min_col_index:
                min_col_index = col_index
            if max_col_index is None or col_index > max_col_index:
                max_col_index = col_index
        paths.append(path)

    max_row_index += 2
    width = max_row_index * 2 + 1
    half_width = int((width - 1) / 2)
    min_col_index = 500 - half_width
    max_col_index = 500 + half_width + 1

    # Map of row index -> [] with array containing True
    # if space is empty, otherwise False
    grid = {
        y: [True] * width for y in range(max_row_index + 1)
    }
    grid[max_row_index] = [False] * width
    for path in paths:
        last_coord = None
        for x, y in path:
            x -= min_col_index
            grid[y][x] = False
            if last_coord is not None:
                last_x, last_y = last_coord
                if last_x != x:  # Line is horizontal
                    if last_x < x:
                        for index in range(last_x, x + 1):
                            grid[y][index ] = False
                    else:
                        for index in range(x, last_x):
                            grid[y][index ] = False
                elif last_y != y:  # Line is vertical
                    if last_y < y:
                        for index in range(last_y, y + 1):
                            grid[index][x] = False
                    else:
                        for index in range(y, last_y):
                            grid[index][x ] = False

            last_coord = (x, y)
    
    return grid, min_col_index


def simulate_sand2(grid, min_col_index):
    resting_sand_count = 0
    height = len(grid)
    width = len(grid[0])
    source_x = 500 - min_col_index

    sand_loc = (source_x, 0)  # Starting location
    while True:
        # print_grid(grid)
        sand_x, sand_y = sand_loc

        if sand_y + 1 < height:
            if grid[sand_y + 1][sand_x]: # Try straight down
                sand_loc = (sand_x, sand_y + 1)
            elif sand_x > 0 and grid[sand_y + 1][sand_x - 1]: # Try down left
                sand_loc = (sand_x - 1, sand_y + 1)
            elif sand_x + 1 < width and grid[sand_y + 1][sand_x + 1]: # Try down right
                sand_loc = (sand_x + 1, sand_y + 1)
            else: # Sand is at rest at a wall
                resting_sand_count += 1
                grid[sand_y][sand_x] = False

                if sand_x == source_x and sand_y == 0:
                    return resting_sand_count

                sand_loc = (source_x, 0)  # New sad location


def print_grid(grid):
    height = len(grid)
    for y in range(height):
        row = grid[y]
        print(''.join(['.' if cell else '#' for cell in row]))


def solution(lines):
    grid, min_col_index = create_grid(lines)
    resting_sand_count = simulate_sand(grid, min_col_index)
    return resting_sand_count
    

def solution2(lines):
    grid, min_col_index = create_grid2(lines)
    resting_sand_count = simulate_sand2(grid, min_col_index)
    return resting_sand_count


if __name__ == '__main__':
    args = sys.argv
    is_test = len(args) > 1 and args[1] == 't'
    part_2 = len(args) > 2 and args[2] == '2'

    day = os.path.basename(__file__).replace('.py', '')

    with open('%s%s.txt' % (day, '_test' if is_test else ''), 'r') as file:
        lines = file.readlines()

    if part_2:
        print(solution2(lines))
    else:
        print(solution(lines))
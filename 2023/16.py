"""
Part 1:
Part 2:
"""
import os

from util import run


def is_valid(x, y, grid):
    width = len(grid[0])
    height = len(grid)
    return (
        x >= 0 and y >= 0 and
        x < width and y < height
    )

def get_new_coords(x, y, symbol, direction, grid):
    next_coords = None
    match(symbol):
        case '|':
            match(direction):
                case 'R':
                    next_coords = [('U', x, y-1), ('D', x, y+1)]
                case 'L':
                    next_coords = [('U', x, y-1), ('D', x, y+1)]
                case 'D':
                    next_coords = [('D', x, y+1)]
                case 'U':
                    next_coords = [('U', x, y-1)]
        case '-':
            match(direction):
                case 'R':
                    next_coords = [('R', x+1, y)]
                case 'L':
                    next_coords = [('L', x-1, y)]
                case 'D':
                    next_coords = [('L', x-1, y), ('R', x+1, y)]
                case 'U':
                    next_coords = [('L', x-1, y), ('R', x+1, y)]
        case '/':
            match(direction):
                case 'R':
                    next_coords = [('U', x, y-1)]
                case 'L':
                    next_coords = [('D', x, y+1)]
                case 'D':
                    next_coords = [('L', x-1, y)]
                case 'U':
                    next_coords = [('R', x+1, y)]
        case '\\':
            match(direction):
                case 'R':
                    next_coords = [('D', x, y+1)]
                case 'L':
                    next_coords = [('U', x, y-1)]
                case 'D':
                    next_coords = [('R', x+1, y)]
                case 'U':
                    next_coords = [('L', x-1, y)]
    return set(coord for coord in next_coords if is_valid(coord[1], coord[2], grid))


def part_1(lines):
    grid = []
    for line in lines:
        line = line.strip()
        grid.append(list(line))
    beam_coords = set([('R', 0, 0)])
    energized = set(beam_coords)

    while True:
        new_beam_coords = set()
        for direction, x, y in beam_coords:
            symbol = grid[y][x]
            if symbol == '.':
                match(direction):
                    case 'R':
                        next_coord = (direction, x+1, y)
                    case 'L':
                        next_coord = (direction, x-1, y)
                    case 'D':
                        next_coord = (direction, x, y+1)
                    case 'U':
                        next_coord = (direction, x, y-1)

                if is_valid(next_coord[1], next_coord[2], grid):
                    new_beam_coords.add(next_coord)
            else:
                new_beam_coords |= get_new_coords(x, y, symbol, direction, grid)

        new_set = new_beam_coords | energized

        if len(new_set) == len(energized):
            break

        beam_coords = new_beam_coords
        energized = new_set

    energized_coords = set((coord[1], coord[2]) for coord in energized)

    for y, row in enumerate(grid):
        line = ''
        for x, char in enumerate(row):
            if (x, y) in energized_coords:
                line += '#'
            else:
                line += char
        print(line)

    return len(energized_coords)


def part_2(lines):
    grid = []
    for line in lines:
        line = line.strip()
        grid.append(list(line))

    max_energized = None
    max_starting = None
    width = len(grid[0])
    height = len(grid)

    for d in ('R', 'L'):
        start_x = 0 if d == 'R' else width - 1
        for y in range(height):
            beam_coords = set([(d, start_x, y)])
            energized = set(beam_coords)

            while True:
                new_beam_coords = set()
                for direction, x, y in beam_coords:
                    symbol = grid[y][x]
                    if symbol == '.':
                        match(direction):
                            case 'R':
                                next_coord = (direction, x+1, y)
                            case 'L':
                                next_coord = (direction, x-1, y)
                            case 'D':
                                next_coord = (direction, x, y+1)
                            case 'U':
                                next_coord = (direction, x, y-1)

                        if is_valid(next_coord[1], next_coord[2], grid):
                            new_beam_coords.add(next_coord)
                    else:
                        new_beam_coords |= get_new_coords(x, y, symbol, direction, grid)

                new_set = new_beam_coords | energized

                if len(new_set) == len(energized):
                    break

                beam_coords = new_beam_coords
                energized = new_set

            energized_coords = set((coord[1], coord[2]) for coord in energized)

            if max_energized is None or len(energized_coords) > max_energized:
                max_energized = len(energized_coords)
                max_starting = (direction, start_x, y)

    for d in ('U', 'D'):
        start_y = 0 if d == 'D' else height - 1
        for x in range(width):
            beam_coords = set([(d, x, start_y)])
            energized = set(beam_coords)

            while True:
                new_beam_coords = set()
                for direction, x, y in beam_coords:
                    symbol = grid[y][x]
                    if symbol == '.':
                        match(direction):
                            case 'R':
                                next_coord = (direction, x+1, y)
                            case 'L':
                                next_coord = (direction, x-1, y)
                            case 'D':
                                next_coord = (direction, x, y+1)
                            case 'U':
                                next_coord = (direction, x, y-1)

                        if is_valid(next_coord[1], next_coord[2], grid):
                            new_beam_coords.add(next_coord)
                    else:
                        new_beam_coords |= get_new_coords(x, y, symbol, direction, grid)

                new_set = new_beam_coords | energized

                if len(new_set) == len(energized):
                    break

                beam_coords = new_beam_coords
                energized = new_set

            energized_coords = set((coord[1], coord[2]) for coord in energized)
            if max_energized is None or len(energized_coords) > max_energized:
                max_energized = len(energized_coords)
                max_starting = (direction, x, start_y)

    print(max_energized, max_starting)
    return max_energized


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

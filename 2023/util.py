import os
import re
import requests
import sys
import time

ALPHABET_LOWER = 'abcdefghijklmnopqrstuvwxyz'
ALPHABET_UPPER = ALPHABET_LOWER.upper()


class Direction:
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'


OPPOSITE_DIRECTIONS ={
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
    Direction.UP: Direction.DOWN,
}


def move(direction, x, y):
    match(direction):
        case Direction.RIGHT:
            return (x + 1, y)
        case Direction.LEFT:
            return (x - 1, y)
        case Direction.DOWN:
            return (x, y + 1)
        case Direction.UP:
            return (x, y - 1)


def get_cardinal_directions(x, y, grid=None):
    """
    If grid is provided, only returns directions
    within bounds.
    """
    all_directions = [
        (Direction.RIGHT, x + 1, y),
        (Direction.DOWN, x, y + 1),
        (Direction.LEFT, x - 1, y),
        (Direction.UP, x, y - 1),
    ]

    if not grid:
        return all_directions

    return [
        (d, x, y) for (d, x, y) in all_directions if
        (x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid))
    ]


def get_adjacent_coords(x, y):
    """
    Given x and y, returns a list of tuples of the
    8 adjacent coordinates.
    """
    return [
        (x - 1, y - 1),
        (x - 1, y),
        (x - 1, y + 1),
        (x, y - 1),
        (x, y + 1),
        (x + 1, y - 1),
        (x + 1, y),
        (x + 1, y + 1),
    ]


def get_manhattan_distance(coord_1, coord_2):
    dx = abs(coord_1[0] - coord_2[0])
    dy = abs(coord_1[1] - coord_2[1])
    return dx + dy


def find_digits(line, cast_to=int):
    return list(map(cast_to, re.findall('(-?\d+)', line.strip())))


def run(day, part_1_fn, part_2_fn):
    """
    - Automatically pulls input data and saves it to <day>.txt
    - Runs part 1 and/or part 2 with test data and/or real data
      based on arguments provided in the command line
    """
    args = sys.argv
    test_only = 't' in args
    real_only = 'r' in args
    force_part_1 = '1' in args
    measure_time = 'time' in args

    year = os.getcwd().split('/')[-1]
    input_file_name = '%s.txt' % day

    if not os.path.isfile(input_file_name):
        with open('../aoc_session_cookie.txt', 'r') as cookie_file:
            cookie = cookie_file.read()

        url = 'https://adventofcode.com/{}/day/{}/input'.format(year, day.lstrip('0'))

        response = requests.get(
            url=url,
            cookies={'session': cookie},
            headers={'User-Agent': 'get_input_script'},
        )
        with open(input_file_name, 'w+') as output:
            print(response.text.rstrip(), end='', file=output)

    fn = part_1_fn if force_part_1 else part_2_fn

    if not real_only:
        with open('%s_test.txt' % day, 'r') as file:
            lines = file.readlines()
            print('---Test---\n', fn(lines))
        if not test_only:
            print()

    if not test_only:
        with open('%s.txt' % day, 'r') as file:
            lines = file.readlines()
            start = time.perf_counter()
            result = fn(lines)
            duration = time.perf_counter() - start
            print('---Real---\n', result)
            if measure_time:
                print('Time:', duration)

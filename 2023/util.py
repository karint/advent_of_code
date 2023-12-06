import os
import re
import requests
import sys

ALPHABET_LOWER = 'abcdefghijklmnopqrstuvwxyz'
ALPHABET_UPPER = ALPHABET_LOWER.upper()


class PathGrid(object):
    """
    Class that can find the shortest path from a starting char to ending char in a grid.

    Warning: Not very efficient :)
    """
    def __init__(
        self,
        lines,
        starting_char,
        ending_char,
        can_reach,
        replacement_map=None
    ):
        self.grid = []
        self.starting_points = set()
        self.ending_points = set()
        self.can_reach = can_reach

        if replacement_map is None:
            replacement_map = {}

        for y, row in enumerate(lines):
            new_row = []
            for x, char in enumerate(row.strip()):
                if char == starting_char:
                    self.starting_points.add((x, y))
                elif char == ending_char:
                    self.ending_points.add((x, y))
                new_row.append(replacement_map.get(char, char))
            self.grid.append(new_row)

        self.width = len(self.grid[0])
        self.height = len(self.grid)

        self.shortest_path_length = self.find_shortest_path_length()

    def find_shortest_path_length(self):
        # Map of last coord to # of steps to get there
        viable_paths = {
            point: 0 for point in self.starting_points
        }
        while True:
            new_paths = {}
            for (last_x, last_y), num_steps in viable_paths.items():
                if (last_x, last_y) in self.ending_points:
                    return num_steps

                right = (last_x + 1, last_y)
                left = (last_x - 1, last_y)
                up = (last_x, last_y + 1)
                down = (last_x, last_y - 1)

                for target_x, target_y in (right, left, up, down):
                    # Don't revisit past squares or go out of bounds
                    if (
                        target_x < 0 or
                        target_x >= self.width or
                        target_y < 0 or
                        target_y >= self.height
                    ):
                        continue

                    if self.can_reach(self.grid, last_x, last_y, target_x, target_y):
                        new_paths[(target_x, target_y)] = num_steps + 1

            viable_paths = new_paths


class Direction:
    RIGHT = 'RIGHT'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    UP = 'UP'


def find_ints(line):
    return re.findall('(\d+)', line)


def get_manhattan_distance(coord_1, coord_2):
    dx = abs(coord_1[0] - coord_2[0])
    dy = abs(coord_1[1] - coord_2[1])
    return dx + dy


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

    year = os.getcwd().split('/')[-1]
    input_file_name = '%s.txt' % day

    if not os.path.isfile(input_file_name):
        with open('../aoc_session_cookie.txt', 'r') as cookie_file:
            cookie = cookie_file.read()

        url = 'https://adventofcode.com/{}/day/{}/input'.format(year, day)

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
            print('---Real---\n', fn(lines))

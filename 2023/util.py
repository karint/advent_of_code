import os
import re
import requests
import sys


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

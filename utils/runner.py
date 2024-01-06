"""
Utility methods related to running Advent of Code solutions.
"""

import importlib
import os
import requests
import sys
import time


def test_all(correct_answers):
    args = sys.argv
    if len(args) == 2:
        specific_day = args[1]
    else:
        specific_day = None

    for day, part_1_solution, part_2_solution in correct_answers:
        if specific_day is not None and specific_day != day:
            continue
        solution_file = importlib.import_module(day)
        with open('%s.txt' % day, 'r') as file:
            print('Day %s:' % day)
            lines = file.readlines()

            start = time.perf_counter()
            part_1_output = solution_file.part_1(lines)
            duration = time.perf_counter() - start
            print('\tPart 1: %s (%.6fs)' % (
                'Pass' if part_1_output == part_1_solution
                else  'Fail: %s should be %s' % (part_1_output, part_1_solution),
                duration
            ))

            start = time.perf_counter()
            part_2_output = solution_file.part_2(lines)
            duration = time.perf_counter() - start
            print('\tPart 2: %s (%.6fs)' % (
                'Pass' if part_2_output == part_2_solution
                else 'Fail: %s should be %s' % (part_2_output, part_2_solution),
                duration
            ))


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

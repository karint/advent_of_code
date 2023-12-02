import os
import json
import requests
import sys

from collections import defaultdict

"""
Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes.
"""

SET ={
    'red': 12,
    'green': 13,
    'blue': 14,
}

TOTAL = 39 # 12+13+14


def part_1(lines):
    answer = 0
    maxes = {
        'red': 0,
        'green': 0,
        'blue': 0,
    }
    for line in lines:
        line = line.strip()
        [game_id, rest] = line.split(': ')
        game_id = int(game_id.split(' ')[-1])
        games = rest.split('; ')

        for game_str in games:
            color_strs = game_str.split(', ')
            for color_str in color_strs:
                num, color = color_str.split(' ')
                num = int(num)
                if maxes[color] < num:
                    maxes[color] = num


    for line in lines:
        impossible = False
        line = line.strip()
        [game_id, rest] = line.split(': ')
        game_id = int(game_id.split(' ')[-1])
        games = rest.split('; ')

        for game_str in games:
            color_strs = game_str.split(', ')
            for color_str in color_strs:
                num, color = color_str.split(' ')
                num = int(num)
                if num > SET[color]:
                    impossible = True

        if not impossible:
            answer += game_id

    return answer


"""
The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.

For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
"""

def part_2(lines):
    answer = 0
    for line in lines:
        maxes = {
            'red': 0,
            'green': 0,
            'blue': 0,
        }
        line = line.strip()
        [game_id, rest] = line.split(': ')
        game_id = int(game_id.split(' ')[-1])
        games = rest.split('; ')

        for game_str in games:
            color_strs = game_str.split(', ')
            for color_str in color_strs:
                num, color = color_str.split(' ')
                num = int(num)
                if maxes[color] < num:
                    maxes[color] = num
        answer += maxes['red'] * maxes['green'] * maxes['blue']

    return answer


if __name__ == '__main__':
    args = sys.argv
    test_only = 't' in args
    real_only = 'r' in args
    force_part_1 = '1' in args

    day = os.path.basename(__file__).replace('.py', '')
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

    fn = part_1 if force_part_1 else part_2

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

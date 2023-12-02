import os
import requests
import sys


COLOR_SET ={
    'red': 12,
    'green': 13,
    'blue': 14,
}


def parse_game(line):
    """
    Takes a game line and returns a tuple of (game_id, list of maps),
    where each map contains color counts from each subset of the game.
    """
    [game_id_str, subsets_str] = line.strip().split(': ')

    colors_per_subset = [{
        color_str.split(' ')[1]: int(color_str.split(' ')[0])
        for color_str in subset_str.split(', ')
    } for subset_str in subsets_str.split('; ')]

    return int(game_id_str.split(' ')[-1]), colors_per_subset


def part_1(lines):
    answer = 0

    for line in lines:
        game_id, colors_per_subset = parse_game(line)

        if all(
            count <= COLOR_SET[color]
            for color_counts in colors_per_subset
            for color, count in color_counts.items()
        ):
            answer += game_id

    return answer


def part_2(lines):
    answer = 0

    for line in lines:
        game_id, colors_per_subset = parse_game(line)

        power = 1
        for color in COLOR_SET.keys():
            power *= max(
                color_counts.get(color, 0)
                for color_counts in colors_per_subset
            )

        answer += power

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

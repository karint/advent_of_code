import os
import re
import requests
import sys


COLOR_SET ={
    'red': 12,
    'green': 13,
    'blue': 14,
}


def extract_color_counts(line):
    return re.findall('(\d+) (%s)' % '|'.join(COLOR_SET.keys()), line)


def part_1(lines):
    answer = 0

    for line in lines:
        game_id = int(line.split(':')[0].split(' ')[1])
        if all(int(count) <= COLOR_SET[color] for count, color in extract_color_counts(line)):
            answer += game_id

    return answer


def part_2(lines):
    answer = 0

    for line in lines:
        game_id = int(line.split(':')[0].split(' ')[1])
        matches = extract_color_counts(line)
        max_color_counts = {
            color: max(
                int(count) for count, color in matches if color == match_color
            ) for count, match_color in matches
        }
        answer += max_color_counts['red'] * max_color_counts['green'] * max_color_counts['blue']

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

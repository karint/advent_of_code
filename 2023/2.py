import os
import re

from util import run


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
            match_color: max(
                int(count) for count, color in matches if color == match_color
            ) for count, match_color in matches
        }
        answer += max_color_counts['red'] * max_color_counts['green'] * max_color_counts['blue']

    return answer


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

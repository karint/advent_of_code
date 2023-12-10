"""
Red, Green, and Blue cubes in a bag.
Part 1: Which games were possible with predefined counts?
Part 2: For each game, what was the fewest number of cubes per color?
"""
import math
import os
import re

from collections import defaultdict
from util import run


COLOR_SET = dict(red=12, green=13, blue=14)


def extract_color_counts(line):
    """
    Returns map of color -> list of ints representing counts from various subsets.
    """
    color_map = defaultdict(list)
    matches = re.findall('(\d+) (%s)' % '|'.join(COLOR_SET.keys()), line)
    for count_str, color in matches:
         color_map[color].append(int(count_str))
    return color_map


def part_1(lines):
    answer = 0
    for line in lines:
        game_id = int(line.split(':')[0].split(' ')[1])
        color_map = extract_color_counts(line)
        if all(
            count <= COLOR_SET[color]
            for color, counts in color_map.items()
            for count in counts
        ):
            answer += game_id
    return answer


def part_2(lines):
    answer = 0
    for line in lines:
        color_map = extract_color_counts(line)
        max_color_counts = {
            color: max(counts)
            for color, counts in color_map.items()
        }
        answer += math.prod(max_color_counts.values())
    return answer


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

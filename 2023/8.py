import os
import math
import re

from util import run


def parse_lines(lines):
    directions = None
    mapping = {}
    for i, line in enumerate(lines):
        line = line.strip()
        if i == 0:
            directions = line
        elif '=' in line:
            key, start, end = re.findall('(\w+)', line)
            mapping[key] = (start, end)
    return directions, mapping


def find_num_steps(curr, directions, mapping, is_end_fn):
    steps = 0
    while True:
        for direction in directions:
            index = 1 if direction == 'R' else 0
            steps += 1
            curr = mapping[curr][index]
            if is_end_fn(curr):
                return steps


def part_1(lines):
    directions, mapping = parse_lines(lines)
    return find_num_steps('AAA', directions, mapping, lambda curr: curr == 'ZZZ')


def part_2(lines):
    directions, mapping = parse_lines(lines)
    currs = {key for key in mapping.keys() if key[-1] == 'A'}
    loop_lengths = {
        curr: find_num_steps(curr, directions, mapping, lambda curr: curr[-1] == 'Z')
        for curr in currs
    }
    return math.lcm(*loop_lengths.values())


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

import os
import json
import re
import math

from collections import defaultdict
from util import find_digits, run


def part_1(lines):
    steps = 0
    directions = None
    mapping = {}
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        if i == 0:
            directions = line
        else:
            key, tup = line.split(' = ')
            tup = tup.replace('(', '').replace(')', '').split(', ')
            mapping[key] = tup

    curr = 'AAA'
    while True:
        for direction in directions:
            if direction == 'R':
                index = 1
            else:
                index = 0
            curr = mapping[curr][index]
            steps += 1
            if curr == 'ZZZ':
                return steps


def part_2(lines):
    directions = None
    mapping = {}
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        if i == 0:
            directions = line
        else:
            key, tup = line.split(' = ')
            tup = tup.replace('(', '').replace(')', '').split(', ')
            mapping[key] = tup

    currs = {
        key for key in mapping.keys() if key[-1] == 'A'
    }
    starting_num = len(currs)
    loop_lengths = {}
    for curr in currs:
        steps = 0
        while loop_lengths.get(curr) is None:
            for direction in directions:
                if direction == 'R':
                    index = 1
                else:
                    index = 0
                curr = mapping[curr][index]
                steps += 1
                if curr[-1] == 'Z':
                    loop_lengths[curr] = steps

    return math.lcm(*loop_lengths.values())


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

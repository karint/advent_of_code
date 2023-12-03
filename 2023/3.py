import os
import json
import re
import requests

from collections import defaultdict
from util import run

REGEX = '(\d+)'


def part_1(lines):
    answer = 0
    symbol_coords = {}
    num_coords = {}
    id_ = 0
    for y, line in enumerate(lines):
        line = line.strip()
        checked_x = set()
        for x, char in enumerate(line):
            if not char.isdigit() and char != '.':
                symbol_coords[(x, y)] = char
            elif x not in checked_x and char.isdigit():
                num = re.findall(REGEX, line[x:])[0]
                for z in range(len(num)):
                    num_coords[(x+z, y)] = (num, id_)
                    checked_x.add(x+z)
                id_ += 1

    dups = set()
    for sym_x, sym_y in symbol_coords:
        for (x, y) in (
            (sym_x+1, sym_y-1),
            (sym_x+1, sym_y),
            (sym_x+1, sym_y+1),
            (sym_x, sym_y-1),
            (sym_x, sym_y+1),
            (sym_x-1, sym_y-1),
            (sym_x-1, sym_y),
            (sym_x-1, sym_y+1),
        ):
            if (x, y) in num_coords:
                num, id_ = num_coords[(x, y)]
                if id_ not in dups:
                    answer += int(num)
                    dups.add(id_)

    return answer


def part_2(lines):
    answer = 0
    gear_coords = {}
    num_coords = {}
    id_ = 0
    for y, line in enumerate(lines):
        line = line.strip()
        checked_x = set()
        for x, char in enumerate(line):
            if char == '*':
                gear_coords[(x, y)] = char
            elif x not in checked_x and char.isdigit():
                num = re.findall(REGEX, line[x:])[0]
                for z in range(len(num)):
                    num_coords[(x+z, y)] = (num, id_)
                    checked_x.add(x+z)
                id_ += 1

    dups = set()
    gear_adj = defaultdict(list)
    for sym_x, sym_y in gear_coords:
        for (x, y) in (
            (sym_x+1, sym_y-1),
            (sym_x+1, sym_y),
            (sym_x+1, sym_y+1),
            (sym_x, sym_y-1),
            (sym_x, sym_y+1),
            (sym_x-1, sym_y-1),
            (sym_x-1, sym_y),
            (sym_x-1, sym_y+1),
        ):
            if (x, y) in num_coords:
                num, id_ = num_coords[(x, y)]
                if id_ not in dups:
                    gear_adj[(sym_x, sym_y)].append(num)
                    dups.add(id_)

    # print(gear_adj)
    for nums in gear_adj.values():
        if len(nums) == 2:
            answer += int(nums[0]) * int(nums[1])

    return answer


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

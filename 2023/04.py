import math
import os
import re

from collections import defaultdict
from util import run


def get_num_matches(line):
    num_strs = line.split(': ')[1]
    winning, card = num_strs.split(' | ')
    winning = set(re.findall('(\d+)', winning))
    card = set(re.findall('(\d+)', card))
    return len(winning & card)


def part_1(lines):
    answer = 0
    for line in lines:
        num_matches = get_num_matches(line)
        answer += (1 if num_matches else 0) * math.pow(2, num_matches - 1)
    return answer


def part_2(lines):
    answer = 0
    copy_counts = defaultdict(int)
    for i, line in enumerate(lines):
        num_matches = get_num_matches(line)
        for j in range(num_matches):
            copy_counts[i + j + 1] += 1 + copy_counts[i]
    return sum(copy_counts.values()) + len(lines)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

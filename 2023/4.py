import os
import json
import math
import re
import requests

from collections import Counter, defaultdict
from util import run


def parse_input(line, callback):
    num_strs = line.split(": ")[1]
    winning, card = num_strs.split(' | ')
    winning = set(re.findall('(\d+)', winning))
    card = set(re.findall('(\d+)', card))
    callback(winning, card)


def part_1(lines):
    answer = 0
    
    def callback(winning, card):
        overlap = len(winning & card)
        answer += (1 if overlap else 0) * math.pow(2, overlap - 1)

    for line in lines:
        parse_input(line, callback)
        
    return answer


def part_2(lines):
    answer = 0
    copy_counts = defaultdict(int)

    for i, line in enumerate(lines):
        def callback(winning, card):
            matching = len(winning & card)
            for j in range(matching):
                copy_counts[i + j + 1] += 1 + copy_counts[i]

        parse_input(line, callback)

    return sum(copy_counts.values()) + len(lines)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

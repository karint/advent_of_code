import os
import json
import re

from collections import defaultdict
from util import run


def part_1(lines):
    answer = 1
    speed = 0
    times = None
    dists = None
    for line in lines:
        line = line.strip()
        if line.startswith('Time'):
            times = map(int, re.findall('(\d+)', line))
        if line.startswith('Dist'):
            records = list(map(int, re.findall('(\d+)', line)))

    for i, time in enumerate(times):
        record = records[i]
        win = 0
        for j in range(time):
            speed = j
            dist = speed * (time - j)
            if dist > record:
                win += 1
        answer *= win

    return answer


def part_2(lines):
    answer = 1
    speed = 0
    times = None
    dists = None
    for line in lines:
        line = line.strip()
        if line.startswith('Time'):
            time = int(''.join(re.findall('(\d+)', line)))
        if line.startswith('Dist'):
            record = int(''.join(re.findall('(\d+)', line)))

    wins = 0
    for j in range(time):
        speed = j
        dist = speed * (time - j)
        if dist > record:
            wins += 1

    return wins




if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

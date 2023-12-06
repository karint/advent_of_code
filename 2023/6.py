import math
import os
import re

from util import find_ints, run


def get_wins(time, record):
    return sum(1 if speed * (time - speed) > record else 0 for speed in range(time))


def part_1(lines):
    times = map(int, find_ints(lines[0]))
    records = map(int, find_ints(lines[1]))
    return math.prod(get_wins(time, record) for time, record in zip(times, records))


def part_2(lines):
    time = int(''.join(find_ints(lines[0])))
    record = int(''.join(find_ints(lines[1])))
    return get_wins(time, record)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

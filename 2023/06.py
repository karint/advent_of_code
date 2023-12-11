"""
Part 1: Find number of ways you could win a boat race by trading off speed for time.
Part 2: Do it again, but for one big, long race.
"""
import math
import os

from util import find_digits, run


def get_wins(time, record):
    return sum(1 if speed * (time - speed) > record else 0 for speed in range(time))


def part_1(lines):
    times = find_digits(lines[0])
    records = find_digits(lines[1])
    return math.prod(get_wins(time, record) for time, record in zip(times, records))


def part_2(lines):
    time = int(''.join(find_digits(lines[0], cast_to=str)))
    record = int(''.join(find_digits(lines[1], cast_to=str)))
    return get_wins(time, record)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

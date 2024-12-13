"""
Part 1: Determine number of stones after 25 blinks.
Part 2: Determine number of stones after 75 blinks.
"""
import os
import functools

from util import run


@functools.cache
def num_future_stones(s, blinks_left):
    if blinks_left == 0:
        return 1

    blinks_left -= 1

    if s == 0:
        return num_future_stones(1, blinks_left)

    if len(str(s)) % 2 == 0:
        stone_str = str(s)
        half_size = len(stone_str)//2
        return (
            num_future_stones(int(stone_str[:half_size]), blinks_left) +
            num_future_stones(int(stone_str[half_size:]), blinks_left)
        )

    return num_future_stones(s * 2024, blinks_left)


def get_num_stones(lines, num_blinks):
    stones = [int(num) for num in lines[0].strip().split(' ')]
    return sum(num_future_stones(s, num_blinks) for s in stones)


def part_1(lines):
    return get_num_stones(lines, 25)


def part_2(lines):
    return get_num_stones(lines, 75)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

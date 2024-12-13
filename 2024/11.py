"""
Part 1:
Part 2:
"""
import os
import functools

from util import run

def part_1(lines):
    num_blinks = 25
    line = lines[0].strip()
    stones = [int(num) for num in line.split(' ')]

    for i in range(num_blinks):
        new_stones = []
        for s in stones:
            if s == 0:
                new_stones.append(1)
            elif len(str(s)) % 2 == 0:
                stone_str = str(s)
                half_size = len(stone_str)//2
                new_stones.append(int(stone_str[:half_size]))
                new_stones.append(int(stone_str[half_size:]))
            else:
                new_stones.append(s * 2024)
        stones = new_stones

    return len(stones)

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


def part_2(lines):
    num_blinks = 75
    line = lines[0].strip()
    stones = [int(num) for num in line.split(' ')]
    return sum(num_future_stones(s, num_blinks) for s in stones)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

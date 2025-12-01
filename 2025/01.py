"""
Part 1: 
Part 2: 
"""
import os

from collections import Counter
from util import find_digits, run

DIAL_START = 50
DIAL_TOTAL_NUMS = 100


def part_1(lines):
    dial = DIAL_START
    count = 0
    for line in lines:
        ticks = int(line[1:])
        if 'L' in line:
            ticks *= -1
        dial += ticks
        dial %= DIAL_TOTAL_NUMS
        if dial == 0:
            count += 1

    return count

def part_2(lines):
    dial = DIAL_START
    count = 0
    for line in lines:
        ticks = int(line[1:])
        for i in range(ticks):
            if 'L' in line:
                dial -= 1
            else:
                dial += 1
            dial %= DIAL_TOTAL_NUMS
            if dial == 0:
                count += 1

    return count



if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

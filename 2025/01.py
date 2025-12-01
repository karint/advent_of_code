"""
Part 1: 
Part 2: 
"""
import os

from collections import Counter
from util import find_digits, run


def part_1(lines):
    answer = 50
    total = 0
    for line in lines:
        steps = int(line[1:])
        steps = steps % 100
        if 'L' in line:
            answer -= steps
        else:
            answer += steps
        if answer < 0:
            answer = 100 + answer
        if answer > 99:
            answer %= 100
        if answer == 0:
            total += 1

    return total

def part_2(lines):
    answer = 50
    total = 0
    for line in lines:
        steps = int(line[1:])
        for i in range(steps):
            if 'L' in line:
                answer -= 1
            else:
                answer += 1
            if answer < 0:
                answer = 100 + answer
            if answer > 99:
                answer %= 100
            if answer == 0:
                total += 1

    return total



if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

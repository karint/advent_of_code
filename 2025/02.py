"""
Part 1: 
Part 2: 
"""
import os

from collections import Counter
from util import find_digits, run


def part_1(lines):
    count = 0
    for line in lines:
        line = line.strip()
        if not line:
            return
        parts = line.split(',')
        for part in parts:
            s = part.split('-')
            if len(s) < 2:
                continue
            start, end = int(s[0]), int(s[1])
            for i in range(start, end + 1):
                t = str(i)
                half = int(len(t)/2)
                if t[:half] == t[half:]:
                    count += i

    return count

def part_2(lines):
    count = 0
    for line in lines:
        line = line.strip()
        if not line:
            return
        parts = line.split(',')
        for part in parts:
            s = part.split('-')
            if len(s) < 2:
                continue
            start, end = int(s[0]), int(s[1])
            for i in range(start, end + 1):
                t = str(i)
                l = int(len(t)/2)
                while l > 0:
                    if len(t) % l > 0:
                        l -= 1
                        continue

                    if t[:l]*int(len(t)/l) == t:
                        count += i
                        break

                    l -= 1
    return count


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

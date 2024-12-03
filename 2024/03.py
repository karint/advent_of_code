"""
Started at 1:52am ET.

Part 1: Find all valid mul(x,y) commands and add their products.
Part 2: Consider do() and don't() commands that toggle enable/disable.
"""
import re
import os

from util import run

REGEX = r'mul\(([0-9]{1,3}),([0-9]{1,3})\)'


def part_1(lines):
    matches = re.findall(REGEX, ''.join(lines))
    return sum(int(match[0]) * int(match[1]) for match in matches)


def part_2(lines):
    between_dos = ''.join(lines).split('do()')

    answer = 0
    for command in between_dos:
        parts = command.split("don't()")
        # Part before "don't" is enabled (including if no "don't"), rest is not
        matches = re.findall(REGEX, parts[0])
        answer += sum(int(match[0]) * int(match[1]) for match in matches)

    return answer


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

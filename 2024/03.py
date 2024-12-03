"""
Started at 1:52am ET.

Part 1: Find all valid mul(x,y) commands and add their products.
Part 2: Consider do() and don't() commands that toggle enable/disable.
"""
import re
import os

from util import run

REGEX = r'mul\(([0-9][0-9]?[0-9]?),([0-9][0-9]?[0-9]?)\)'


def part_1(lines):
    command = ''.join(lines)
    matches = re.findall(REGEX, command)

    answer = 0
    for match in matches:
        answer += int(match[0])*int(match[1])
    return answer


def part_2(lines):
    answer = 0
    command = ''.join(lines)
    between_dos = command.split('do()')

    for substring in between_dos:
        parts = substring.split("don't()")
        enabled = parts[0]
        matches = re.findall(REGEX, enabled)

        for match in matches:
            answer += int(match[0])*int(match[1])

    return answer


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

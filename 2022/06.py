import os

from util import run


def part_1(lines):
    marker_length = 4
    line = lines[0]
    for i, char in enumerate(line):
        marker = line[i:i + marker_length]
        if len(set(marker)) == marker_length:
            return i + marker_length
    

def part_2(lines):
    marker_length = 14
    line = lines[0]
    for i, char in enumerate(line):
        marker = line[i:i + marker_length]
        if len(set(marker)) == marker_length:
            return i + marker_length


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

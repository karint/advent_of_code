import os
import sys


def solution(lines):
    marker_length = 4
    line = lines[0]
    for i, char in enumerate(line):
        marker = line[i:i + marker_length]
        print(marker)
        if len(set(marker)) == marker_length:
            print(set(marker))
            return i + marker_length
    

def solution2(lines):
    marker_length = 14
    line = lines[0]
    for i, char in enumerate(line):
        marker = line[i:i + marker_length]
        print(marker)
        if len(set(marker)) == marker_length:
            print(set(marker))
            return i + marker_length


if __name__ == '__main__':
    args = sys.argv
    is_test = len(args) > 1 and args[1] == 't'
    part_2 = len(args) > 2 and args[2] == '2'

    day = os.path.basename(__file__).replace('.py', '')

    with open('%s%s.txt' % (day, '_test' if is_test else ''), 'r') as file:
        lines = file.readlines()

    if part_2:
        print(solution2(lines))
    else:
        print(solution(lines))
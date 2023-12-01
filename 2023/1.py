import os
import requests
import sys


NUMBER_MAP = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

REVERSED_NUMBER_MAP = {
    ''.join(reversed(k)): v for k, v in NUMBER_MAP.items()
}


def solution(lines):
    sums = 0
    for line in lines:
        line = line.strip()
        ints = []
        for char in line:
            if char.isdigit():
                ints.append(char)
        sums += int(ints[0] + ints[-1])

    return sums


def solution2_orig(lines):
    """
    Original solution: Find first string to replace with a number, replace it,
    then find the last string to replace by reversing the string, and replace it.
    Concatenate the results of both of these in case something overlaps
    (e.g. "oneight") and run part 1 solution on that resulting string.
    """
    sums = 0
    for line in lines:
        orig_line = line.strip()
        new_line = ''

        found = False
        for i in range(len(orig_line)):
            if found:
                break
            for num, rep in NUMBER_MAP.items():
                if orig_line[i:].startswith(num):
                    new_line += orig_line.replace(num, rep, 1)
                    found = True
                    break

        flipped_line = ''.join(reversed(orig_line))

        found = False
        for i in range(len(flipped_line)):
            if found:
                break
            for num, rep in REVERSED_NUMBER_MAP.items():
                if flipped_line[i:].startswith(num):
                    flipped_line = flipped_line.replace(num, rep, 1)
                    found = True
                    break

        new_line += ''.join(reversed(flipped_line))
        line = new_line

        ints = []
        for char in line:
            if char.isdigit():
                ints.append(char)
        sums += int(ints[0] + ints[-1])

    return sums


def solution2(lines):
    """
    Simpler solution: Just step through the string and keep track of the
    digits that show up in digit or word form.
    """
    sums = 0

    for line in lines:
        line = line.strip()
        ints = []

        for i, char in enumerate(line):
            if char.isdigit():
                ints.append(char)
                continue

            for num, rep in NUMBER_MAP.items():
                if line[i:].startswith(num):
                    ints.append(rep)
        sums += int(ints[0] + ints[-1])

    return sums


if __name__ == '__main__':
    args = sys.argv
    is_test = len(args) > 1 and args[1] == 't'
    part_2 = len(args) > 2 and args[2] == '2'

    day = os.path.basename(__file__).replace('.py', '')
    year = os.getcwd().split('/')[-1]
    input_file_name = '%s.txt' % day

    if not os.path.isfile(input_file_name):
        with open('aoc_session_cookie.txt', 'r') as cookie_file:
            cookie = cookie_file.read()

        url = 'https://adventofcode.com/{}/day/{}/input'.format(year, day)

        response = requests.get(
            url=url,
            cookies={'session': cookie},
            headers={'User-Agent': 'get_input_script'},
        )
        with open(input_file_name, 'w+') as output:
            print(response.text.rstrip(), end='', file=output)


    with open('%s%s.txt' % (day, '_test' if is_test else ''), 'r') as file:
        lines = file.readlines()

    if part_2:
        print(solution2(lines))
    else:
        print(solution(lines))

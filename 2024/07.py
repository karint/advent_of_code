"""
Part 1:
Part 2:
"""
import os

from util import run


def is_possible_1(rest, result):
    if len(rest) == 2:
        return (
            rest[0] + rest[1] == result or
            rest[0] * rest[1] == result
        )

    factor = rest[0]
    remaining = rest[1:]

    if result % factor == 0:
        mult_possible = is_possible_1(remaining, result / factor)
    else:
        mult_possible = False

    return is_possible_1(remaining, result - factor) or mult_possible


def part_1(lines):
    total = 0
    for line in lines:
        line = line.strip()
        result, rest = line.split(': ')
        result = int(result)
        rest = [int(n) for n in rest.split()]

        # Work backwards to see what's possible
        rest.reverse()
        if is_possible_1(rest, result):
            total += result

    return total


def is_possible_2(rest, result):
    if len(rest) == 1:
        return rest[0] == result

    if len(rest) == 2:
        a = rest[0]
        b = rest[1]
        return (
            eval(str(a) + str(b)) == result or
            a + b == result or
            a * b == result
        )

    mult_possible = result % rest[-1] == 0 and is_possible_2(rest[:-1], result // rest[-1])

    add_possible = result > rest[-1] and is_possible_2(rest[:-1], result - rest[-1])

    if str(result).endswith(str(rest[-1])):
        last_num = str(rest[-1])
        new_result = str(result)[:-len(last_num)]
        concat_possible = len(new_result) and is_possible_2(rest[:-1], int(new_result))
    else:
        concat_possible = False

    return mult_possible or add_possible or concat_possible


def part_2(lines):
    total = 0
    for line in lines:
        line = line.strip()
        result, rest = line.split(': ')
        result = int(result)
        rest = [int(n) for n in rest.split()]

        is_possible = is_possible_2(rest, result)
        if is_possible:
            total += result

    return total


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

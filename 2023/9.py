import operator
import os

from util import find_digits, run


def get_totals(lines, index, operator_fn, list_fn):
    total = 0
    for line in lines:
        sequences = [find_digits(line)]
        while True:
            sequences.append([
                sequences[-1][i] - sequences[-1][i - 1]
                for i in range(1, len(sequences[-1]))
            ])
            if all(val == 0 for val in sequences[-1]):
                break
        sequences.reverse()

        for i in range(len(sequences)):
            list_fn(
                sequences[i],
                0 if i == 0
                else operator_fn(sequences[i][index], sequences[i - 1][index]),
            )
        total += sequences[i][index]
    return total


def part_1(lines):
    return get_totals(
        lines,
        -1,
        operator.add,
        lambda row, val: row.append(val)
    )


def part_2(lines):
    return get_totals(
        lines,
        0,
        operator.sub,
        lambda row, val: row.insert(0, val)
    )


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

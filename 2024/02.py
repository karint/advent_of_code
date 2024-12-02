"""
Part 1:
Part 2:
"""
import os

from util import run


def part_1(lines):
    total = 0

    # for report in lines:
    #     good = True
    #     levels = report.split(' ')
    #     asc = sorted(levels)
    #     desc = sorted(levels, reverse=True)
    #     lvl_str = ' '.join(levels)
    #     if not (' '.join(asc) == lvl_str or ' '.join(desc) == lvl_str):
    #         good = False
    #         continue

    #     levels = list(map(int, levels))
    #     for i in range(len(levels) - 1):
    #         diff = abs(levels[i] - levels[i + 1])
    #         if diff > 3 or diff < 1:
    #             good = False

    #     if good:
    #         total += 1

        # print(report, good)


    for report in lines:
        is_asc = None
        safe = True
        levels = report.split(' ')
        for i in range(len(levels) - 1):
            a = int(levels[i])
            b = int(levels[i + 1])
            if i == 0:
                is_asc = b > a
            else:
                if (is_asc and b <= a) or (not is_asc and a <= b):
                    safe = False
                    break

            if abs(a - b) > 3 or abs(a - b) < 1:
                safe = False
                break

        if safe:
            total += 1

    return total


def is_safe(levels):
    is_asc = None
    safe = True
    for i in range(len(levels) - 1):
        a = int(levels[i])
        b = int(levels[i + 1])
        if i == 0:
            is_asc = b > a
        else:
            if (is_asc and b <= a) or (not is_asc and a <= b):
                safe = False
                break

        if abs(a - b) > 3 or abs(a - b) < 1:
            safe = False
            break

    return safe


def part_2(lines):
    total = 0
    for report in lines:
        safe = False
        levels = report.strip().split(' ')
        # print(is_safe(levels), levels)
        if is_safe(levels):
            safe = True

        if not safe:
            for i in range(len(levels)):
                new_levels = levels[:i] + levels[i+1:]
                if is_safe(new_levels):
                    safe = True
                    break

        if safe:
            total += 1

    return total


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

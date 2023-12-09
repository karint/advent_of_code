import os
import json
import re

from collections import defaultdict
from util import find_digits, run


def part_1(lines):
    hists = []
    for line in lines:
        diffs = []
        line = line.strip()
        nums = list(find_digits(line))
        diffs.append(nums)
        while any(num != 0 for num in nums):
            diff_row = []
            for i, num in enumerate(nums):
                if i == len(nums) - 1:
                    continue
                diff_row.append(nums[i+1] - num)
            diffs.append(diff_row)
            nums = diff_row

        # Calc hist
        diffs.reverse()
        for i in range(len(diffs)):
            row = diffs[i]
            if i == 0:
                row += [0]
            else:
                row.append(diffs[i-1][-1] + row[-1])
        hists.append(diffs[-1][-1])

    return sum(hists)


def part_2(lines):
    hists = []
    for line in lines:
        diffs = []
        line = line.strip()
        nums = list(find_digits(line))
        diffs.append(nums)
        while any(num != 0 for num in nums):
            diff_row = []
            for i, num in enumerate(nums):
                if i == len(nums) - 1:
                    continue
                diff_row.append(nums[i+1] - num)
            diffs.append(diff_row)
            nums = diff_row

        # Calc hist
        diffs.reverse()
        last_row = None
        for i in range(len(diffs)):
            row = diffs[i]
            if i == 0:
                row = [0] + row
            else:
                row = [row[0] - last_row[0]] + row
            last_row = row
        hists.append(row[0])

    return sum(hists)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

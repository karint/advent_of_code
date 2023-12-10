import os
import re

from collections import defaultdict
from util import get_adjacent_coords, run


def process_adjacent_numbers(lines, is_symbol_fn, is_adjacent_callback):
    symbol_coords = set()
    num_coords = {}
    id_ = 0

    # Find all symbols and number coordinates. Assign an auto-incrementing
    # ID to numbers found so we don't double-count them later.
    for y, line in enumerate(lines):
        line = line.strip()
        matched_numbers = re.finditer('(\d+)', line)
        for match in matched_numbers:
            for x in range(match.start(), match.end()):
                num_coords[(x, y)] = (int(match.group()), id_)
            id_ += 1

        symbol_coords.update(
            (x, y) for x, char in enumerate(line)
            if is_symbol_fn(char)
        )

    # For any numbers adjacent to a symbol, call the callback
    added_num_ids = set()
    for symbol_x, symbol_y in symbol_coords:
        for x, y in get_adjacent_coords(symbol_x, symbol_y):
            if (x, y) in num_coords:
                num, id_ = num_coords[(x, y)]
                if id_ not in added_num_ids:
                    is_adjacent_callback(symbol_x, symbol_y, num)
                    added_num_ids.add(id_)


def part_1(lines):
    nums = []
    process_adjacent_numbers(
        lines,
        lambda c: not c.isdigit() and c != '.',
        lambda x, y, num: nums.append(num)
    )
    return sum(nums)


def part_2(lines):
    gear_adj_nums = defaultdict(list)
    process_adjacent_numbers(
        lines,
        lambda c: c == '*',
        lambda x, y, num: gear_adj_nums[(x, y)].append(num)
    )
    return sum(
        nums[0] * nums[1]
        for nums in gear_adj_nums.values()
        if len(nums) == 2
    )


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

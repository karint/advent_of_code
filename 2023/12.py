import os
import json
import re
import sys

from itertools import combinations_with_replacement, permutations
from collections import Counter, defaultdict
from util import run


def is_viable(line, path, nums, next_char, is_finished=False):
    """
    Return None if not viable, otherwise returns the number of
    groups covered so far.
    """
    # print('is viable?', path, nums, next_char)
    path_to_try = path + next_char
    # Only not viable if set of # doesn't match nums in order
    curr_group_len = 0
    num_index = 0
    for char in path_to_try:
        if char == '#':
            curr_group_len += 1
            if num_index >= len(nums) or curr_group_len > nums[num_index]:
                # print('no -- group len too long', num_index, curr_group_len)
                return False
        elif char == '.' and curr_group_len:
            if nums[num_index] != curr_group_len:
                # print('no -- wrong number of rocks', num_index, curr_group_len)
                return False
            curr_group_len = 0
            num_index += 1

    # print('yes', num_index, curr_group_len)
    # Also check that there's room for the groups needed ahead
    line_so_far = path_to_try + line[len(path_to_try):]

    # Check if too many groups
    if sum(1 if char == '#' else 0 for char in line_so_far) > sum(nums):
        return False

    # Check if there's enough remaining space to fit what we need to
    if num_index < len(nums):
        wiggle_room = len(line) - len(path_to_try) + curr_group_len
        if wiggle_room < sum(nums[num_index:]) + len(nums[num_index:]) - 1:
            return False

    return True


def get_num_groups(path, nums):
    """
    Return None if not viable, otherwise returns the number of
    groups covered so far.
    """
    curr_group_len = 0
    num_index = 0
    for char in path:
        if char == '#':
            curr_group_len += 1
        elif char == '.' and curr_group_len:
            curr_group_len = 0
            num_index += 1

    if char == '#' and curr_group_len == nums[num_index]:
        num_index += 1

    # print('num groups for', path, 'is', num_index)
    return num_index


def is_done(path, nums):
    return [len(group) for group in path.split('.') if group] == nums


MEMO = {}
def get_possible_ways(line, nums):
    num_str = ','.join(map(str, nums))
    if (line, num_str) in MEMO:
        return MEMO[(line, num_str)]

    # print('get_possible_ways', line, nums)
    if '?' not in line:
        return 1 if is_viable(line, line, nums, '', is_finished=True) else 0

    total = 0
    viable_paths = set([''])
    for i, char in enumerate(line):
        if char != '?':
            viable_paths = [path + char for path in viable_paths if is_viable(line, path, nums, char)]
        else:
            new_viable_paths = (
                set(path + '.' for path in viable_paths if is_viable(line, path, nums, '.')) |
                set(path + '#' for path in viable_paths if is_viable(line, path, nums, '#'))
            )
            viable_paths = new_viable_paths

        if i == len(line) - 1:
            return total + sum(
                1 if is_done(path, nums) else 0 for path in viable_paths
            )

        counts = defaultdict(int)
        pruned_viable_paths = set()
        for path in viable_paths:
            # If all paths hit a '.' at the same time and have the same number of
            # groups/partial groups covered already, we can just see how one path does
            # and multiply num ways by number of viable paths to get there
            if path[-1] == '.':
                num_groups = get_num_groups(path, nums)
                if num_groups:
                    counts[num_groups] += 1
                else:
                    pruned_viable_paths.add(path)
            else:
                pruned_viable_paths.add(path)

        # print('path map', path_map)
        # print('pruned', pruned_viable_paths)
        if counts:
            for num_groups, count in counts.items():
                other_ways = get_possible_ways(line[i + 1:], nums[num_groups:])
                MEMO[(line[i + 1:], ','.join(map(str, nums[num_groups:])))] = other_ways
                total += count * other_ways
                # print('num_groups', num_groups, 'count', count, 'other_ways', other_ways, 'total', total)

        viable_paths = pruned_viable_paths


    return total + sum(
        1 if is_done(path, nums) else 0 for path in viable_paths
    )


def part_1(lines):
    answer = 0
    for line in lines:
        line = line.strip()
        line, nums = line.split(' ')
        nums = list(map(int, nums.split(',')))

        ways = get_possible_ways(line, nums)
        print(line, ','.join(map(str, nums)), ways)

        answer += ways

    return answer


def part_2(lines):
    answer = 0
    for i, line in enumerate(lines):
        line, nums = line.split(' ')

        line = '?'.join([line] * 5)
        nums = ','.join([nums] * 5)
        nums = list(map(int, nums.split(',')))

        answer += get_possible_ways(line, nums)

        # print(line, ','.join(map(str, nums)), ways)

    return answer


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

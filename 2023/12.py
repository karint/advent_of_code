"""
Part 1: Find all possible arrangements of a list of group sizes within a string.
Part 2: Part 1, but both the string and list are repeated 5 times (string separated by wildcards).
"""
import os

from collections import defaultdict
from util import run

WILDCARD = '?'


def is_viable(line, path, nums, next_char):
    """
    Return None if not viable, otherwise returns the number of
    groups covered so far.
    """
    path_to_try = path + next_char

    # Only not viable if set of # doesn't match nums in order
    curr_group_len = 0
    num_index = 0
    for char in path_to_try:
        if char == '#':
            curr_group_len += 1
            if num_index >= len(nums) or curr_group_len > nums[num_index]:
                return False
        elif char == '.' and curr_group_len:
            if nums[num_index] != curr_group_len:
                return False
            curr_group_len = 0
            num_index += 1

    # Check if too many groups
    line_so_far = path_to_try + line[len(path_to_try):]
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

    # Check if the last group we were working on was covered
    if char == '#' and curr_group_len == nums[num_index]:
        num_index += 1

    return num_index


def is_correct(path, nums):
    """
    Checks if the path fully matches the number of groups required.
    """
    return [len(group) for group in path.split('.') if group] == nums


MEMO = {}
def get_memo_key(line, nums):
    return line, ','.join(map(str, nums))


def get_possible_ways(line, nums):
    key = get_memo_key(line, nums)
    if key in MEMO:
        return MEMO[key]

    if WILDCARD not in line:
        # No choices to make -- it's either correct or not :)
        return 1 if is_correct(line, nums) else 0

    total = 0
    viable_paths = set([''])
    for i, char in enumerate(line):
        if char != WILDCARD:
            viable_paths = set(path + char for path in viable_paths if is_viable(line, path, nums, char))
        else:
            # Split viable paths to cases where the wildcard is '#' and when it's '.'
            new_viable_paths = (
                set(path + '.' for path in viable_paths if is_viable(line, path, nums, '.')) |
                set(path + '#' for path in viable_paths if is_viable(line, path, nums, '#'))
            )
            viable_paths = new_viable_paths

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

        if counts:
            # Use recursion to find the possible ways going forward for each combo of
            # number of groups covered so far
            for num_groups, count in counts.items():
                other_ways = get_possible_ways(line[i + 1:], nums[num_groups:])
                total += count * other_ways

        viable_paths = pruned_viable_paths

    ways = total + sum(1 if is_correct(path, nums) else 0 for path in viable_paths)
    MEMO[get_memo_key(line, nums)] = ways
    return ways


def part_1(lines):
    answer = 0
    for line in lines:
        line = line.strip()
        line, nums = line.split(' ')
        nums = list(map(int, nums.split(',')))
        answer += get_possible_ways(line, nums)
    return answer


def part_2(lines):
    answer = 0
    for i, line in enumerate(lines):
        line, nums = line.split(' ')
        line = WILDCARD.join([line] * 5)
        nums = ','.join([nums] * 5)
        nums = list(map(int, nums.split(',')))
        answer += get_possible_ways(line, nums)
    return answer


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

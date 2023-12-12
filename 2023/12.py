import os
import json
import re

from itertools import combinations_with_replacement, permutations
from collections import Counter, defaultdict
from util import run


def matches(line, nums):
    return [len(string) for string in line.split('.') if string] == nums


def is_possible(line, nums):
    # Determines if the line is viable with the set of nums provided
    groups = ['#' * num for num in nums]
    regex = '[\\./\\?]+'.join(['[#/\\?]' * num for num in nums])
    regex = '[\\./\\?]*' + regex + '[\\./\\?]*'
    match = re.fullmatch(regex, line)

    # if match:
    #     print('match')
    # else:
    #     print('no match')
    # print(line, nums, groups)
    # print(regex)
    return match is not None


def get_possible_ways(line, nums, num_index, start_search_index):
    if not is_possible(line, nums):
        return set()

    if matches(line, nums):
        # We finished putting everything in place, or there's
        # nothing left to replace, or there's only one arrangement.
        return set([line])

    # Set position of first group, then determine possible ways for remaining
    # string and groups. Recurse.
    ways = set()

    for i in range(start_search_index, len(line) - nums[num_index] + 1):
        not_viable = False

        # The group to place in various positions
        group = '#' * nums[num_index]

        # The substring we'll replace with it
        substring = line[i:i + len(group)]
        # If there's always a set break there, we can't do it
        if '.' in substring:
            continue

        # If we have another group to place, add a necessary break after this one
        if num_index < len(nums) - 1:
            # If we can't place the break, it's not a viable place
            if i + len(group) < len(line) and line[i  + len(group)] == '#':
                not_viable = True
            if not_viable:
                continue
            group += '.'

        # Replace the substring at the designated place
        attempt = line[0:i] + group + line[i + len(group):len(line)]
        # print('attempt', attempt, group)

        # If the placement is viable, recurse to find all possible placements
        if is_possible(attempt, nums):
            # print('possible!', attempt, nums)
            # If all groups were placed, track viable attempts then return that
            if num_index + 1 == len(nums):
                ways.add(attempt.replace('?', '.'))
            else:
                # Get possible ways for this new string and all non-placed groups
                ways |= get_possible_ways(attempt, nums, num_index + 1, i + len(group))
    return ways


def part_1(lines):
    answer = 0
    for line in lines:
        line = line.strip()
        line, nums = line.split(' ')
        nums = list(map(int, nums.split(',')))

        ways = get_possible_ways(line, nums, 0, 0)
        print(line, ','.join(map(str, nums)), len(ways))

        errors = 0
        for way in ways:
            if not is_possible(way, nums):
                print('ERROR')
                errors += 1
            print(way)

        answer += len(ways) - errors

    return answer


def part_2(lines):
    return part_1(lines)

# low: 6774
# high: 6922

if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

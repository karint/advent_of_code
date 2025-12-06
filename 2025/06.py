"""
Part 1: Do math problems down each column separated by spaces.
Part 2: Do math problems right-to-left where each number is in a col.
"""
import os

from math import prod
from util import run


def part_1(lines):
	problems = []
	for line in lines:
		parts = line.strip().split()
		if not problems:
			problems = [[] for _ in range(len(parts))]

		for i, part in enumerate(parts):
			problems[i].append(part)

	count = 0
	for problem in problems:
		numbers = map(int, problem[:-1])
		op = sum if problem[len(problem) - 1] == '+' else prod
		count += op(numbers)

	return count


def part_2(lines):
	max_len = 0
	rows = []
	for line in lines:
		line = line.rstrip()
		max_len = max(max_len, len(line))
		rows.append(line)

	count = 0
	op = None
	nums = []
	for num_index in reversed(range(max_len)):
		num_str = ''

		# Check each row to see if there's a character in the given col,
		# starting from the right
		for row in rows:
			if len(row) > num_index:
				char = row[num_index]
				if char in ('+', '*'):
					op = sum if char == '+' else prod
				else:
					num_str += char

		num_str = num_str.strip()

		if num_str:
			nums.append(int(num_str))
		else:
			count += op(nums)
			nums.clear()

	count += op(nums)
	return count


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

"""
Part 1: Do math problems down each column separated by spaces.
Part 2: Do math problems right-to-left where each number is in a col.
"""
import os

from math import prod
from util import run


def part_1(lines):
	problems = [[] for _ in range(len(lines[0].split()))]
	for line in lines:
		parts = line.strip().split()
		for i, part in enumerate(parts):
			problems[i].append(part)

	total = 0
	for problem in problems:
		op = sum if problem[len(problem) - 1] == '+' else prod
		nums = map(int, problem[:-1])
		total += op(nums)
	return total


def part_2(lines):
	rows, max_len = [], 0
	for line in lines:
		line = line.rstrip()
		max_len = max(max_len, len(line))
		rows.append(line)

	total, op, nums = 0, None, []
	for num_index in reversed(range(max_len)):
		num_str = ''
		for row in rows:
			char = row[num_index] if len(row) > num_index else ''
			if char in ('+', '*'):
				op = sum if char == '+' else prod
			else:
				num_str += char

		if num_str.strip():
			nums.append(int(num_str))
		else: # Column of spaces; execute operation
			total += op(nums)
			nums.clear()
	
	return total + op(nums)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

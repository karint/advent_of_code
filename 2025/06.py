"""
Part 1: 
Part 2: 
"""
import os

from util import find_digits, run


def part_1(lines):
	count = 0
	problems = []
	len_ = None

	for line in lines:
		line = line.strip()
		parts = line.split()
		len_ = len(parts)
		problems.append(parts)

	for i in range(len_):
		op = problems[len(problems) - 1][i]
		if op == '+':
			count += sum(int(problems[j][i]) for j in range(len(problems) - 1))
		else:
			prod = 1
			for j in range(len(problems) - 1):
				prod *= int(problems[j][i])
			count += prod

	return count


def part_2(lines):
	count = 0
	max_len = 0
	cols = []
	ops = []

	for line in lines:
		line = line.rstrip()
		max_len = max(max_len, len(line))
		cols.append(line)

	op = None
	nums = []
	for i in range(max_len):
		num_index = max_len - i - 1
		num_str = ''
		for col in cols:
			if len(col) <= num_index:
				continue

			char = col[num_index]
			if char in ('+', '*'):
				op = char
			else:
				num_str += char

		num_str = num_str.strip()

		# If whole string is spaces, move to next problem
		if num_str:
			nums.append(int(num_str))
		else:
			if op == '+':
				count += sum(nums)
			else:
				prod = 1
				for num in nums:
					prod *= num
				count += prod

			nums = []
			op = None


	if op == '+':
		count += sum(nums)
	else:
		prod = 1
		for num in nums:
			prod *= num
		count += prod
	return count


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

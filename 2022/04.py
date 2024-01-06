import os

from util import run


def part_1(lines):
	count = 0
	for line in lines:
		line = line.strip()
		first, second = line.split(',')
		first_tuple = [int(x) for x in first.split('-')]
		second_tuple = [int(x) for x in second.split('-')]
		if first_tuple[0] <= second_tuple[0] and first_tuple[1] >= second_tuple[1]:
			count += 1
		elif first_tuple[0] >= second_tuple[0] and first_tuple[1] <= second_tuple[1]:
			count += 1

	return count


def part_2(lines):
	count = 0
	for line in lines:
		line = line.strip()
		first, second = line.split(',')
		first_tuple = [int(x) for x in first.split('-')]
		second_tuple = [int(x) for x in second.split('-')]
		nums = set()
		for x in range(first_tuple[0], first_tuple[1] + 1):
			nums.add(x)
		for y in range(second_tuple[0], second_tuple[1] + 1):
			if y in nums:
				count += 1
				break

	return count


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

import os

from util import ALPHABET_LOWER, ALPHABET_UPPER, run

POINTS = {
	letter: index + 1
	for index, letter in enumerate(ALPHABET_LOWER + ALPHABET_UPPER)
}


def part_1(lines):
	points = 0
	for line in lines:
		line = line.strip()
		size = int(len(line)/2)
		first = set(line[:size])
		second = set(line[size:])
		common = first.intersection(second).pop()
		points += POINTS[common]

	return points


def part_2(lines):
	points = 0
	curr_set = set()
	count = 0

	for line in lines:
		line = line.strip()
		if not curr_set:
			curr_set = set(line)
		else:
			curr_set &= set(line)

		count += 1
		if count == 3:
			common = curr_set.pop()
			points += POINTS[common]
			count = 0

	return points


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

"""
Started with 06:54:00 left to Day 6 (5:06pm ET).
Took break between Part 1 and Part 2 (daycare pickup and such!).

Part 1: Find how many available IDs fell within the given ranges.
Part 2: Find how many total numbers fell within the given ranges.
"""
import os

from util import run


def part_1(lines):
	count = 0
	fresh = set()

	for line in lines:
		line = line.strip()
		if '-' in line:
			start, end = line.split('-')
			fresh.add((int(start), int(end)))
		elif line:
			avail = int(line)
			if any(start <= avail <= end for start, end in fresh):
				count += 1

	return count


def part_2(lines):
	fresh_ranges = []
	for line in lines:
		line = line.strip()
		if not line:
			break

		start, end = line.split('-')
		fresh_ranges.append([int(start), int(end)])
	fresh_ranges.sort()

	for i, range_ in enumerate(fresh_ranges):
		start, end = range_
		if i + 1 == len(fresh_ranges):
			break

		next_start, next_end = fresh_ranges[i + 1]
		if end >= next_start:
			range_.clear()
			fresh_ranges[i + 1][0] = min(start, next_start)
			fresh_ranges[i + 1][1] = max(end, next_end)

	count = 0
	for range_ in fresh_ranges:
		if range_:
			start, end = range_
			count += end - start + 1

	return count



if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

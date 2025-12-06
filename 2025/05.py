"""
Started with 06:54:00 left to Day 6 (5:06pm ET).
Took break between Part 1 and Part 2 (daycare pickup and such!).

Part 1: 
Part 2: 
"""
import os

from util import run


def part_1(lines):
	count = 0
	fresh = set()

	is_fresh = True
	for line in lines:
		line = line.strip()

		if not line:
			is_fresh = False
			continue

		if is_fresh:
			start, end = line.split('-')
			fresh.add((int(start), int(end)))
		else:
			avail = int(line)
			if any(start <= avail <= end for start, end in fresh):
				count += 1

	return count


def part_2(lines):
	count = 0
	fresh_ranges = []

	for line in lines:
		line = line.strip()
		if not line:
			break

		start, end = line.split('-')
		start = int(start)
		end = int(end)
		fresh_ranges.append([start, end])

	fresh_ranges.sort()

	for i, range_ in enumerate(fresh_ranges):
		start, end = range_
		if i + 1 == len(fresh_ranges):
			break

		other_start, other_end = fresh_ranges[i + 1]

		# start should be <= other_start due to sorting
		if start == other_start:
			# Can delete this range since encapsulated by the next
			range_.clear()
		elif end < other_start:
			# Keep as-is -- no overlap
			pass
		elif end >= other_start:
			# Merge ranges
			range_.clear()
			fresh_ranges[i + 1][0] = min(start, other_start)
			fresh_ranges[i + 1][1] = max(end, other_end)
		else:
			print('This should not be possible!')

	for range_ in fresh_ranges:
		if range_:
			start, end = range_
			count += end - start + 1

	return count



if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

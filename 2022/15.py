import os
import re
import sys
import time

from collections import defaultdict

REGEX = 'Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)'


def get_manhattan_distance(coord_1, coord_2):
    dx = abs(coord_1[0] - coord_2[0])
    dy = abs(coord_1[1] - coord_2[1])
    return dx + dy


def mark(row, x):
    if row.get(x) is not None:
        return
    row[x] = '#'


def solution(lines):
    TARGET_ROW_INDEX = 2000000
    target_row = {}
    beacons = {}
    for line in lines:
        line = line.strip()
        matches = re.match(REGEX, line)
        sensor_x, sensor_y, beacon_x, beacon_y = map(int, [
            matches.group(1),
            matches.group(2),
            matches.group(3),
            matches.group(4),
        ])
        dist = get_manhattan_distance((sensor_x, sensor_y), (beacon_x, beacon_y))
        if sensor_y == TARGET_ROW_INDEX:
            target_row[sensor_x] = 'S'
        if beacon_y == TARGET_ROW_INDEX:
            target_row[beacon_x] = 'B'

        row_delta = dist - abs(sensor_y - TARGET_ROW_INDEX)
        if row_delta > 0:
            mark(target_row, sensor_x)
            for x in range(row_delta):
                mark(target_row, sensor_x - x)
                mark(target_row, sensor_x + x)

    return sum(1 if val == '#' else 0 for val in target_row.values())


def add_range(coverage, row_index, new_range):
    coverage[row_index].append(new_range)

def get_frequency(x, y):
    return x * 4000000 + y

def solution2(lines):
    MIN = 0
    # MAX = 20
    MAX = 4000000

    # Map of row to ranges that are not possible for a beacon to be
    coverage = defaultdict(list)

    beacons = {}
    for line in lines:
        line = line.strip()
        matches = re.match(REGEX, line)
        sensor_x, sensor_y, beacon_x, beacon_y = map(int, [
            matches.group(1),
            matches.group(2),
            matches.group(3),
            matches.group(4),
        ])
        dist = get_manhattan_distance((sensor_x, sensor_y), (beacon_x, beacon_y))
        if MIN <= sensor_y and sensor_y < MAX:
            add_range(coverage, sensor_y, (sensor_x, sensor_x))
        if MIN <= beacon_y and beacon_y < MAX:
            add_range(coverage, beacon_y, (beacon_x, beacon_x))

        rows_to_remove = set()
        min_y_range = max(sensor_y - dist, MIN)
        max_y_range = min(sensor_y + dist + 1, MAX)
        for y in range(min_y_range, max_y_range):
            row_delta = dist - abs(sensor_y - y)
            if row_delta < 0:
                continue

            min_x_range = max(sensor_x - row_delta, MIN)
            max_x_range = min(sensor_x + row_delta + 1, MAX)
            add_range(coverage, y, (min_x_range, max_x_range))

    for row_index, ranges in coverage.items():
        ranges.sort()

        # Is there anything missing?
        most_max = None
        for range_min, range_max in ranges:
            if most_max is not None and range_min > most_max:
                print(row_index, ranges)
                return get_frequency(most_max, row_index)

            if most_max is None or range_max > most_max:
                most_max = range_max

if __name__ == '__main__':
    args = sys.argv
    is_test = len(args) > 1 and args[1] == 't'
    part_2 = len(args) > 2 and args[2] == '2'

    day = os.path.basename(__file__).replace('.py', '')

    with open('%s%s.txt' % (day, '_test' if is_test else ''), 'r') as file:
        lines = file.readlines()

    if part_2:
        print(time.time())
        print(solution2(lines))
        print(time.time())
    else:
        print(solution(lines))

"""
Part 1:
Part 2:
"""
import os

from util import run


def part_1(lines):
    is_lock = None
    locks = []
    keys = []

    curr = []
    for line in lines:
        line = line.strip()
        if not line:
            if is_lock:
                locks.append(curr)
            else:
                keys.append(curr)
            curr = []
            is_lock = None
            continue

        if is_lock is None and all(c == '#' for c in line):
            is_lock = True

        if is_lock is None and all(c == '.' for c in line):
            is_lock = False

        curr.append(line)

    if is_lock:
        locks.append(curr)
    else:
        keys.append(curr)

    height = len(keys[0])
    width = len(keys[0][0])

    key_heights = []
    for key in keys:
        heights = [0] * width
        for col_index in range(width):
            for h in range(height):
                if key[height - 1 - h][col_index] == '.':
                    heights[col_index] = h - 1
                    break

        key_heights.append(heights)

    lock_heights = []
    for lock in locks:
        heights = [0] * width
        for col_index in range(width):
            for h in range(height):
                if lock[h][col_index] == '.':
                    heights[col_index] = h - 1
                    break

        lock_heights.append(heights)

    count = 0
    for key_height in key_heights:
        for lock_height in lock_heights:
            # print(key_height, lock_height)
            if all(
                key_height[i] + lock_height[i] < height - 1
                for i in range(width)
            ):
                count += 1

    return count


def part_2(lines):
    return


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

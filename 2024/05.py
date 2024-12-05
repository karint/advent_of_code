"""
Part 1:
Part 2:
"""
import os

from collections import defaultdict
from util import run


def part_1(lines):
    total = 0
    before_map = defaultdict(set)
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if ',' in line:
            test_order = line.split(',')
            is_good = True
            for after, before_set in before_map.items():
                for before in before_set:
                    if not (
                        after not in test_order or
                        before not in test_order or
                        test_order.index(after) > test_order.index(before)
                    ):
                        is_good = False
                        break
            if is_good:
                total += int(test_order[int((len(test_order) - 1)/2)])
        else:
            x, y = line.split('|')
            before_map[y].add(x)

    return total


def part_2(lines):
    total = 0
    before_map = defaultdict(set)
    to_test = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if ',' in line:
            test_order = line.split(',')
            to_test.append(test_order)
        else:
            x, y = line.split('|')
            before_map[y].add(x)

    for test_order in to_test:
        is_good = True
        for after, before_set in before_map.items():
            for before in before_set:
                if not (
                    after not in test_order or
                    before not in test_order or
                    test_order.index(after) > test_order.index(before)
                ):
                    is_good = False
                    break
        if not is_good:
            num_earlier_than_map = defaultdict(int)
            for a in test_order:
                # How many times does this number show up in the before set of others?
                num_earlier_than = 0
                for b in test_order:
                    if a == b:
                        continue
                    if a in before_map[b]:
                        num_earlier_than += 1
                num_earlier_than_map[a] = num_earlier_than

                new_order = sorted(test_order, key=lambda n: num_earlier_than_map[n], reverse=True)
                print(new_order)


            total += int(new_order[int((len(new_order) - 1)/2)])

    return total


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

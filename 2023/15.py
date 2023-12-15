import os
import json
import re

from collections import defaultdict
from util import run


def part_1(lines):
    answer = 0
    for line in lines:
        if not line:
            continue
        tests = line.strip().split(',')
        for test in tests:
            a = 0
            for char in test:
                a += ord(char)
                a = a * 17
                a = a % 256
            answer += a
            # print(test, a)

    return answer


def get_a(test):
    a = 0
    for char in test:
        a += ord(char)
        a = a * 17
        a = a % 256

    return a


def part_2(lines):
    boxes = defaultdict(list)
    line = lines[0].strip()
    tests = line.split(',')
    for test in tests:
        test = test.strip()
        if not test:
            continue
        if '-' in test:
            label = test[:-1]
            box_index = get_a(label)
            box = boxes[box_index]
            boxes[box_index] = [
                (l, focal) for (l, focal) in box if l != label
            ]
        else:
            label, focal = test.split('=')
            box_index = get_a(label)
            box = boxes[box_index]
            found = False
            for i, (lens_label, _) in enumerate(box):
                if lens_label == label:
                    box[i] = (label, focal)
                    found = True
            if not found:
                box.append((label, focal))

    answer = 0
    for box_num, box in boxes.items():
        if not box:
            continue

        for i, (label, focal) in enumerate(box):
            answer += (1 + box_num) * (i + 1) * int(focal)

    return answer


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

"""
Part 1: Follow instructions to determine the hash of a sequence.
Part 2: Follow instructions to put lenses in boxes.
"""
import os

from collections import defaultdict
from util import run


def get_hash(string):
    hash_ = 0
    for char in string:
        hash_+= ord(char)
        hash_*= 17
        hash_%= 256
    return hash_


def part_1(lines):
    steps = lines[0].strip().split(',')
    return sum(get_hash(step) for step in steps)


def part_2(lines):
    boxes = defaultdict(list)
    steps = lines[0].strip().split(',')
    for step in steps:
        if '-' in step:
            label = step[:-1]
            box_index = get_hash(label)
            box = boxes[box_index]
            boxes[box_index] = [(l, f) for (l, f) in box if l != label]
        else:
            label, focal = step.split('=')
            box = boxes[get_hash(label)]
            found = False
            for i, (lens_label, _) in enumerate(box):
                if lens_label == label:
                    box[i] = (label, focal)
                    found = True
            if not found:
                box.append((label, focal))

    return sum(
        (box_index + 1) * (slot_index + 1) * int(focal)
        for box_index, box in boxes.items()
        for slot_index, (label, focal) in enumerate(box)
    )


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

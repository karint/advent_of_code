import os
import json
import re

from collections import defaultdict
from util import run


def part_1(lines):
    answer = 0
    seeds = None
    names = []
    map_dicts = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        elif line.startswith('seeds'):
            seeds = map(int, line.split(': ')[1].split(' '))
            continue
        elif ':' in line:
            names.append(line.split(' ')[0])
            map_dicts.append({})
            continue

        dest_start, source_start, range_length = map(
            int, re.findall('(\d+)', line)
        )
        map_dicts[-1][(
            source_start,
            source_start + range_length
        )] = (
            dest_start,
            dest_start + range_length
        )

    min_location = None
    for seed in seeds:
        for name, mapping in zip(names, map_dicts):
            for (source_start, source_end), (dest_start, dest_end) in mapping.items():
                if source_start <= seed and seed < source_end:
                    seed = dest_start + seed - source_start
                    break

        if min_location is None or seed < min_location:
            min_location = seed

    return min_location


def part_2(lines):
    part_1(lines)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

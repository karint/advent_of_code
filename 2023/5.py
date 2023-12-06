import os
import re

from util import run


def part_1(lines):
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
            # Tracking names is mostly for debugging and not required in the solution
            names.append(line.split(' ')[0])
            map_dicts.append({})
            continue

        dest_start, source_start, range_length = map(
            int, re.findall('(\d+)', line)
        )
        map_dicts[-1][(
            source_start,
            source_start + range_length
        )] = dest_start

    min_location = None
    for seed in seeds:
        for name, mapping in zip(names, map_dicts):
            for (source_start, source_end), dest_start in mapping.items():
                if source_start <= seed and seed < source_end:
                    seed = dest_start + seed - source_start
                    break

        if min_location is None or seed < min_location:
            min_location = seed

    return min_location


def map_ranges_to_destination(ranges, mapping):
    """
    Takes source ranges and a source-to-destination mapping and returns
    the new set of ranges at the destination.
    """
    new_ranges = set()
    for start, end in ranges:
        covered_ranges = []
        for (source_start, source_end), dest_start in mapping.items():
            min_overlap = max(start, source_start)
            max_overlap = min(end, source_end)

            # There's overlap -- map the new segments to their destination
            if min_overlap < max_overlap:
                diff = dest_start - source_start
                new_range = (min_overlap + diff, max_overlap + diff)
                new_ranges.add(new_range)
                covered_ranges.append((min_overlap, max_overlap))

        if not covered_ranges:
            # No overlap in any mappings -- keep original range
            new_ranges.add((start, end))
        else:
            # Add what remains of the original range that wasn't covered by the mapping
            covered_ranges.sort()
            if start < covered_ranges[0][0]:
                new_ranges.add((start, covered_ranges[0][0]))
            for i, (covered_start, covered_end) in enumerate(covered_ranges):
                if i == len(covered_ranges) - 1:
                    break
                next_start, _ = covered_ranges[i + 1]
                if next_start > covered_end:
                    new_ranges.add((covered_end, next_start))
            if end > covered_ranges[-1][1]:
                new_ranges.add((covered_ranges[-1][1], end))
    return new_ranges


def part_2(lines):
    # Parse all the things!
    seed_ranges = []
    names = []
    map_dicts = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        elif line.startswith('seeds'):
            starts_and_ranges = re.findall('(\d+ \d+)', line.split(': ')[1])
            for string in starts_and_ranges:
                start, range_ = map(int, string.split(' '))
                seed_ranges.append((start, start + range_))
            continue
        elif ':' in line:
            # Tracking names is mostly for debugging and not required in the solution
            names.append(line.split(' ')[0])
            map_dicts.append({})
            continue

        dest_start, source_start, range_length = map(
            int, re.findall('(\d+)', line)
        )
        map_dicts[-1][(
            source_start,
            source_start + range_length
        )] = dest_start

    # Approach will be to track the spans still viable from initial seed ranges
    # at each source category. At the end, the lowest viable location span will
    # contain the minimum location as its range start.
    possible_span_value_ranges = set(seed_ranges)
    for name, curr_map in zip(names, map_dicts):
        new_ranges = map_ranges_to_destination(possible_span_value_ranges, curr_map)
        possible_span_value_ranges = new_ranges

    return sorted(possible_span_value_ranges)[0][0]


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

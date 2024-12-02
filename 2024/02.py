"""
Part 1: Count how many levels in a report are deemed "safe".
Part 2: Count how many levels in a report are safe if up to 1 level could be removed.
"""
import os

from util import run


def _parse_levels(report):
    return [int(l) for l in report.strip().split(' ')]


def _is_safe(levels):
    safe = True
    last_level = levels[0]
    last_diff = None
    for level in levels[1:]:
        diff = level - last_level

        if (
            abs(diff) < 1 or
            abs(diff) > 3 or
            (last_diff is not None and last_diff * diff < 0)
        ):
            safe = False
            break

        last_level = level
        last_diff = diff

    return safe


def part_1(lines):
    return sum(
        1 if _is_safe(_parse_levels(report)) else 0
        for report in lines
    )


def part_2(lines):
    total = 0

    for report in lines:
        levels = _parse_levels(report)
        if _is_safe(levels):
            total += 1
            continue

        for index_to_ignore in range(len(levels)):
            if _is_safe(levels[:index_to_ignore] + levels[index_to_ignore + 1:]):
                total += 1
                break

    return total


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

import os
import json
import re

from collections import Counter, defaultdict
from util import find_digits, run

WILDCARD = 'J'


def get_total_winnings(lines, get_strength_fns, order):
    ranks = defaultdict(list)
    for line in lines:
        line = line.strip()
        hand, bid = line.split(' ')
        counts = Counter(hand)
        strength_fns = get_strength_fns(counts)

        for i, fn in enumerate(strength_fns):
            if fn(counts):
                ranks[i].append((hand, int(bid)))
                break

    total = 0
    rank = len(lines)
    for i in range(max(ranks.keys()) + 1):
        all_hands_at_rank = ranks[i]

        if not all_hands_at_rank:
            continue

        # Break ties
        all_hands_at_rank.sort(key=lambda tup: [
            order.index(tup[0][i]) for i in range(len(tup[0]))
        ])

        for hand, bid in all_hands_at_rank:
            total += rank * bid
            rank -= 1

    return total


def part_1(lines):
    def get_strength_fns(counts):
        return [
            lambda counts: max(counts.values()) == 5,  # 5 of a kind
            lambda counts: max(counts.values()) == 4,  # 4 of a kind
            lambda counts: len(counts.values()) == 2,  # Full house
            lambda counts: max(counts.values()) == 3,  # 3 of a kind
            lambda counts: sorted(counts.values()) == [1, 2, 2],  # Two pair
            lambda counts: sorted(counts.values()) == [1, 1, 1, 2],  # One pair
            lambda counts: True,  # Nothing
        ]
    return get_total_winnings(lines, get_strength_fns, 'AKQJT98765432')


def part_2(lines):
    def get_strength_fns(counts):
        non_wild_counts = {k: v for k, v in counts.items() if k != WILDCARD}
        wild_count = counts.get(WILDCARD, 0)
        return [
            lambda counts: (  # 5 of a kind
                counts.get(WILDCARD) == 5 or
                max(non_wild_counts.values()) + wild_count == 5
            ),
            lambda counts: (  # 4 of a kind
                max(non_wild_counts.values()) + wild_count == 4
            ),
            lambda counts: (  # Full house
                sorted(counts.values()) == [2, 3] or
                (sorted(counts.values()) == [1, 2, 2] and wild_count >= 1)
            ),
            lambda counts: (  # 3 of a kind
                max(non_wild_counts.values()) + wild_count == 3
            ),
            lambda counts: (  # Two pair
                sorted(counts.values()) == [1, 2, 2] or
                (sorted(counts.values()) == [1, 1, 1, 2] and wild_count > 1)
            ),
            lambda counts: (  # One pair
                max(non_wild_counts.values()) == 2 or wild_count > 0
            ),
            lambda counts: (  # Nothing
                True,
            ),
        ]
    return get_total_winnings(lines, get_strength_fns, 'AKQT98765432J')


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

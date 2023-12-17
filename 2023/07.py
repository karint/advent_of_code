"""
Part 1: Given a list of poker hands and bids, calculate total winnings.
Part 2: Jokers are wildcards.
"""
import os

from collections import Counter, defaultdict
from util import run

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
        max_dups = max(counts.values())
        sorted_counts = sorted(counts.values())
        return [
            lambda counts: max_dups == 5,  # 5 of a kind
            lambda counts: max_dups == 4,  # 4 of a kind
            lambda counts: sorted_counts == [2, 3],  # Full house
            lambda counts: max_dups == 3,  # 3 of a kind
            lambda counts: sorted_counts == [1, 2, 2],  # Two pair
            lambda counts: sorted_counts == [1, 1, 1, 2],  # One pair
            lambda counts: True,  # Nothing
        ]
    return get_total_winnings(lines, get_strength_fns, 'AKQJT98765432')


def part_2(lines):
    def get_strength_fns(counts):
        max_dups = max((v for c, v in counts.items() if c != WILDCARD), default=0)
        sorted_counts = sorted(counts.values())
        wild_count = counts.get(WILDCARD, 0)
        return [
            lambda counts: (  # 5 of a kind
                max_dups + wild_count == 5
            ),
            lambda counts: (  # 4 of a kind
                max_dups + wild_count == 4
            ),
            lambda counts: (  # Full house
                sorted_counts == [2, 3] or
                (sorted_counts == [1, 2, 2] and wild_count >= 1)
            ),
            lambda counts: (  # 3 of a kind
                max_dups + wild_count == 3
            ),
            lambda counts: (  # Two pair
                sorted_counts == [1, 2, 2] or
                (sorted_counts == [1, 1, 1, 2] and wild_count > 1)
            ),
            lambda counts: (  # One pair
                max_dups == 2 or wild_count > 0
            ),
            lambda counts: (  # Nothing
                True,
            ),
        ]
    return get_total_winnings(lines, get_strength_fns, 'AKQT98765432J')


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

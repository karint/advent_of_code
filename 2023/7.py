import os
import json
import re

from collections import Counter, defaultdict
from util import find_digits, run

ORDER = 'AKQJT98765432'
ORDER = 'AKQT98765432J'


def part_1(lines):
    answer = 0
    ranks = defaultdict(list)
    for line in lines:
        line = line.strip()
        hand, bid = line.split(' ')
        counts = Counter(hand)

        if max(counts.values()) == 5:
            ranks[1].append((hand, int(bid)))
        elif max(counts.values()) == 4:
            ranks[2].append((hand, int(bid)))
        elif len(counts.values()) == 2:
            ranks[3].append((hand, int(bid)))
        elif max(counts.values()) == 3:
            ranks[4].append((hand, int(bid)))
        elif sorted(counts.values()) == [1, 2, 2]:
            ranks[5].append((hand, int(bid)))
        elif sorted(counts.values()) == [1, 1, 1, 2]:
            ranks[6].append((hand, int(bid)))
        else:
            ranks[7].append((hand, int(bid)))

    # Break ties
    total = 0
    rank = len(lines)
    for i in range(1, 8):
        all_hands = ranks[i]
        if not all_hands:
            continue

        def rank_hand(tup):
            return (
                ORDER.index(tup[0][0]),
                ORDER.index(tup[0][1]),
                ORDER.index(tup[0][2]),
                ORDER.index(tup[0][3]),
                ORDER.index(tup[0][4]),
            )


        all_hands.sort(key=rank_hand)

        for hand, bid in all_hands:
            print(rank, hand, bid)
            total += rank * bid
            rank -= 1

    return total


def part_2(lines):
    answer = 0
    ranks = defaultdict(list)
    for line in lines:
        line = line.strip()
        hand, bid = line.split(' ')
        counts = Counter(hand)
        non_j_dups = Counter(hand.replace('J', ''))
        num_wild = counts.get('J', 0)

        if hand == 'JJJJJ':
            ranks[1].append((hand, int(bid)))
        elif max(non_j_dups.values()) + num_wild == 5:
            ranks[1].append((hand, int(bid)))
        elif max(non_j_dups.values()) + num_wild == 4:
            ranks[2].append((hand, int(bid)))
        elif (
            sorted(counts.values()) == [2, 3] or
            (sorted(counts.values()) == [1, 2, 2] and num_wild >= 1)
        ):
            # Full house
            ranks[3].append((hand, int(bid)))
        elif max(non_j_dups.values()) + num_wild == 3:
            # 3 kind
            ranks[4].append((hand, int(bid)))
        elif (
            sorted(counts.values()) == [1, 2, 2] or
            (sorted(counts.values()) == [1, 1, 1, 2] and num_wild > 1)
        ):
            # Two pair
            ranks[5].append((hand, int(bid)))
        elif max(non_j_dups.values()) == 2 or 'J' in hand:
            # One pair
            ranks[6].append((hand, int(bid)))
        else:
            ranks[7].append((hand, int(bid)))

    # print(json.dumps(ranks, indent=2))

    # Break ties
    total = 0
    rank = len(lines)
    for i in range(1, 8):
        all_hands = ranks[i]
        if not all_hands:
            continue

        def rank_hand(tup):
            return (
                ORDER.index(tup[0][0]),
                ORDER.index(tup[0][1]),
                ORDER.index(tup[0][2]),
                ORDER.index(tup[0][3]),
                ORDER.index(tup[0][4]),
            )


        all_hands.sort(key=rank_hand)

        for hand, bid in all_hands:
            total += rank * bid
            rank -= 1

    return total



if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

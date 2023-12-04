import os
import json
import re
import requests

from collections import Counter, defaultdict
from util import run


def part_1(lines):
    answer = 0
    all_winning = set()
    for line in lines:
        line = line.strip()
        line = line.replace('  ', ' ')
        card, nums = line.split(": ")
        winning, mine = nums.split(' | ')
        winning = winning.split(' ')
        all_winning.update(winning)

    for line in lines:
        line = line.strip()
        line = line.replace('  ', ' ')
        card, nums = line.split(": ")
        winning, mine = nums.split(' | ')
        winning = winning.split(' ')
        mine = mine.split(' ')
        overlap = [num for num in mine if num in winning]
        x = 0
        if overlap:
            x = 1

        for i in range(len(overlap) - 1):
            x = x*2
        answer += x
        
    return answer


def part_2(lines):
    answer = 0
    cards = []
    winnings = []
    for line in lines:
        line = line.strip()
        line = line.replace('  ', ' ')
        card, nums = line.split(": ")
        winning, mine = nums.split(' | ')
        winnings.append(winning.split(' '))
        cards.append(mine.split(' '))

    count = 0
    copy_counts = defaultdict(int)

    for i, orig_card in enumerate(cards):
        matching = len([num for num in orig_card if num in winnings[i]])
        for j in range(matching):
            copy_counts[i+j+1] += 1 + copy_counts[i]

    return sum(copy_counts.values()) + len(cards)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

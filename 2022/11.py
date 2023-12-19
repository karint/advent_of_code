import os
import sys


class Monkey(object):
    def __init__(
        self,
        items,
        operation,
        divisor,
        target_if_true,
        target_if_false,
        common_divisor=1,
    ):
        self.items = items
        self.operation = operation
        self.divisor = divisor
        self.target_if_true = target_if_true
        self.target_if_false = target_if_false
        self.inspect_count = 0
        self.common_divisor = common_divisor

    def test(self, x):
        return x % self.divisor == 0

    def take_round(self):
        for item in self.items:
            worry_level = self.operation(item) % self.common_divisor
            # worry_level = int(worry_level/3.0)
            target_monkey = self.target_if_true if self.test(worry_level) else self.target_if_false
            self.inspect_count += 1
            self.toss(worry_level, monkeys[target_monkey])

    def toss(self, new_worry_level, target_monkey):
        self.items = self.items[1:]
        target_monkey.items.append(new_worry_level)



# Initialize monkeys
MONKEYS = [
    Monkey(  # 0
        [92, 73, 86, 83, 65, 51, 55, 93],
        lambda old: old * 5,
        11,
        3,
        4,
    ),
    Monkey(  # 1
        [99, 67, 62, 61, 59, 98],
        lambda old: old * old,
        2,
        6,
        7,
    ),
    Monkey(  # 2
        [81, 89, 56, 61, 99],
        lambda old: old * 7,
        5,
        1,
        5,
    ),
    Monkey(  # 3
        [97, 74, 68],
        lambda old: old + 1,
        17,
        2,
        5,
    ),
    Monkey(  # 4
        [78, 73],
        lambda old: old + 3,
        19,
        2,
        3,
    ),
    Monkey(  # 5
        [50],
        lambda old: old + 5,
        7,
        1,
        6,
    ),
    Monkey(  # 6
        [95, 88, 53, 75],
        lambda old: old + 8,
        3,
        0,
        7,
    ),
    Monkey(  # 7
        [50, 77, 98, 85, 94, 56, 89],
        lambda old: old + 2,
        13,
        4,
        0,
    ),
]


TEST_MONKEYS = [
    Monkey(  # 0
        [79, 98],
        lambda old: old * 19,
        23,
        2,
        3,
    ),
    Monkey(  # 1
        [54, 65, 75, 74],
        lambda old: old + 6,
        19,
        2,
        0,
    ),
    Monkey(  # 2
        [79, 60, 97],
        lambda old: old * old,
        13,
        1,
        3,
    ),
    Monkey(  # 3
        [74],
        lambda old: old + 3,
        17,
        0,
        1,
    ),
]

NUM_ROUNDS = 10000

monkeys = MONKEYS


def solution(lines):
    common_divisor = 1
    for monkey in monkeys:
        common_divisor *= monkey.divisor

    for monkey in monkeys:
        monkey.common_divisor = common_divisor

    for num_round in range(NUM_ROUNDS):
        if num_round % 1000 == 0:
            print('Round ', num_round)
        # print('\nRound', num_round)
        for monkey in monkeys:
            monkey.take_round()

    inspect_counts = sorted([monkey.inspect_count for monkey in monkeys], reverse=True)
    print(inspect_counts[0])
    print(inspect_counts[1])
    print(inspect_counts[0]*inspect_counts[1])
    

def solution2(lines):
    pass


if __name__ == '__main__':
    args = sys.argv
    is_test = len(args) > 1 and args[1] == 't'
    part_2 = len(args) > 2 and args[2] == '2'

    day = os.path.basename(__file__).replace('.py', '')

    with open('%s%s.txt' % (day, '_test' if is_test else ''), 'r') as file:
        lines = file.readlines()

    if part_2:
        print(solution2(lines))
    else:
        print(solution(lines))
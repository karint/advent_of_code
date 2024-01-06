import os

from collections import Counter
from util import run

class Node(object):
    def __init__(self, value, prev, next):
        self.value = value
        self.prev = None
        self.next = None

class MixList(object):
    def __init__(self, values):
        self.nodes = []
        self.zero_node = None

        prev_node = None
        all_values = []
        for value in values:
            all_values.append(value)
            node = Node(value, None, None)
            self.nodes.append(node)

            if prev_node is not None:
                prev_node.next = node
                node.prev = prev_node

            prev_node = node

            if value == 0:
                self.zero_node = node

        # Link last node with first
        self.nodes[0].prev = self.nodes[-1]
        self.nodes[-1].next = self.nodes[0]

        self.pre_mix_counts = Counter(all_values)

    def run(self):
        # print('Initial config:')
        # self.print()

        for node in self.nodes:
            # print('Moving node', node.value)
            self.move_node(node)
            # self.print()

            # curr_node = self.zero_node
            # all_values = []
            # for i in range(len(self.nodes)):
            #     all_values.append(curr_node.value)
            #     curr_node = curr_node.next

            # post_mix_counts = Counter(all_values)

            # for value, count in self.pre_mix_counts.items():
            #     if post_mix_counts[value] != count:
            #         print('Diff detected for %d: %d vs. %d' % (value, count, post_mix_counts[value]))

        # print('After config:')
        # self.print()

    def move_node(self, node):
        steps = abs(node.value) % (len(self.nodes) - 1)

        if steps == 0:
            return

        target_node = node

        # Remove node from previous spot
        node.prev.next = node.next
        node.next.prev = node.prev

        if node.value > 0:
            for _ in range(steps):
                target_node = target_node.next

            # Plop node after target node
            node.next = target_node.next
            node.next.prev = node
            target_node.next = node
            node.prev = target_node
        else:
            for _ in range(steps):
                target_node = target_node.prev

            # Plop node before target node
            node.prev = target_node.prev
            node.prev.next = node
            target_node.prev = node
            node.next = target_node

    def print(self):
        curr_node = self.nodes[0]
        node_values = []
        for _ in range(len(self.nodes)):
            node_values.append(str(curr_node.value))
            curr_node = curr_node.next
        
        print(' '.join(node_values))


CHECK_AT = [1000, 2000, 3000]

def part_1(lines):
    values = []
    for line in lines:
        line = line.strip()
        values.append(int(line))

    mix_list = MixList(values)
    mix_list.run()

    # Find 0
    total_sum = 0
    curr_node = mix_list.zero_node
    for i in range(max(CHECK_AT) + 1):
        if i in CHECK_AT:
            # print(i, ':', curr_node.value)
            total_sum += curr_node.value
        curr_node = curr_node.next

    return total_sum
    

DECRYPTION_KEY = 811589153
TIMES_TO_MIX = 10

def part_2(lines):
    values = []
    for line in lines:
        line = line.strip()
        values.append(int(line) * DECRYPTION_KEY)

    mix_list = MixList(values)
    for _ in range(TIMES_TO_MIX):
        mix_list.run()

    # Find 0
    total_sum = 0
    curr_node = mix_list.zero_node
    for i in range(max(CHECK_AT) + 1):
        if i in CHECK_AT:
            # print(i, ':', curr_node.value)
            total_sum += curr_node.value
        curr_node = curr_node.next

    return total_sum


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

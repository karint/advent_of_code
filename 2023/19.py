"""
Part 1: Follow workflow instructions to determine if a part is accepted or rejected.
Part 2: Find all possible accepted combinations within ranges.
"""
import math
import os
import re

from util import run

START = 'in'


def part_1(lines):
    workflow_map = {}
    rating_maps = []
    is_workflow = True
    for line in lines:
        line = line.strip()
        if not line:
            is_workflow = False
            continue
        if is_workflow:
            key, commands_str = line[:-1].split('{')
            workflow_map[key] = commands_str.split(',')
        else:
            rating_maps.append(dict(re.findall('(\w)=(\d+)', line)))

    accepted = 0
    for rating_map in rating_maps:
        key = START
        while True:
            if key == 'A':
                accepted += sum(map(int, rating_map.values()))
                break

            if key == 'R':
                break

            for command in workflow_map[key]:
                if ':' in command:
                    eval_str, if_true = command.split(':')
                    key = eval_str[0]
                    if eval(rating_map[key] + eval_str[1:]):
                        key = if_true
                        break
                else:
                    key = command
    return accepted


class Node:
    def __init__(self, key, eval_str):
        self.key = key
        self.eval_str = eval_str
        self.children = {True: [], False: []}
        self.parents = {True: [], False: []}

    def __repr__(self):
        return self.eval_str

    def add_child(self, child_node, condition):
        self.children[condition].append(child_node)

    def add_parent(self, parent_node, condition):
        self.parents[condition].append(parent_node)


def part_2(lines):
    min_val = 1
    max_val = 4000

    workflows = []
    ratings = []
    array = workflows
    for line in lines:
        line = line.strip()
        if not line:
            array = ratings
            continue
        array.append(line)

    key_nodes = {
        'A': Node('A', 'True', None),  # accept node
        'R': Node('R', 'False', None),  # reject node
    }
    all_nodes = []
    for workflow in workflows:
        key, rest = workflow[:-1].split('{')
        commands = rest.split(',')
        key_if_false = commands[-1]
        commands = commands[:-1]
        last_node = None

        for i, command in enumerate(commands):
            eval_str, if_true = command.split(':')
            node = Node(key if i == 0 else None, eval_str, if_true)
            all_nodes.append(node)
            if i == 0:
                key_nodes[key] = node

            if last_node:
                # If there was a command before this, it had to be false to get here
                node.parent_was_false(last_node)
            last_node = node
        last_node.set_if_false(key_if_false)

    for node in all_nodes:
        # Now populate all the relationships between nodes and their "if true" attr
        if node.if_true in key_nodes:
            node_if_true = key_nodes[node.if_true]
            node_if_true.parent_was_true(node)

        # Now populate all the relationships between nodes and their "if false" attr
        if node.if_false in key_nodes:
            node_if_false = key_nodes[node.if_false]
            node_if_false.parent_was_false(node)

        # Also now that we have a node map, populate any false parents
        new_parents = [
            key_nodes[false_parent] if isinstance(false_parent, str) else false_parent
            for false_parent in node.parents[False]
        ]
        node.parents[False] = new_parents

    # Now we have a full graph of nodes. Trace up from the A node to see what
    # conditions needed to be true to get there.
    start = key_nodes['A']
    condition_paths = []

    for condition, parents in start.parents.items():
        for parent in parents:
            path = [(condition, parent)]
            condition_paths.append(path)

    has_parents = True
    final_paths = []
    new_condition_paths = condition_paths
    while new_condition_paths:
        new_condition_paths = []
        for condition_path in condition_paths:
            _, last_node = condition_path[-1]
            has_parents = False

            if last_node.parents[True]:
                for parent in last_node.parents[True]:
                    new_condition_paths.append(condition_path + [(True, parent)])
                has_parents = True

            if last_node.parents[False]:
                for parent in last_node.parents[False]:
                    new_condition_paths.append(condition_path + [(False, parent)])
                has_parents = True

            if not has_parents:
                final_paths.append(condition_path)

            condition_paths = new_condition_paths

    total = 0
    for condition_path in final_paths:
        # Only count those with "in" key
        if not any(node.key == 'in' for (condition, node) in condition_path):
            continue

        possible_rating_values = {
            'x': set(range(min_val, max_val + 1)),
            'm': set(range(min_val, max_val + 1)),
            'a': set(range(min_val, max_val + 1)),
            's': set(range(min_val, max_val + 1)),
        }
        for (condition, node) in condition_path:
            rating_key = node.eval_str[0]
            operator = node.eval_str[1]
            value = int(node.eval_str.split(operator)[1])
            if operator == '>':
                if condition: # Want rating > value
                    possible_rating_values[rating_key] &= set(range(value + 1, max_val + 1))
                else: # Want rating <= value
                    possible_rating_values[rating_key] &= set(range(1, value + 1))

            elif operator == '<':
                if condition: # Want rating < value
                    possible_rating_values[rating_key] &= set(range(1, value))
                else: # Want rating >= value
                    possible_rating_values[rating_key] &= set(range(value, max_val + 1))

        print(','.join([
            '%s=%s' % (node.eval_str, condition)
            for (condition, node) in condition_path
        ]))
        total += math.prod(len(total_set) for total_set in possible_rating_values.values())

    return total


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

"""
Part 1: Follow workflow instructions to determine if a part is accepted or rejected.
Part 2: Find all possible accepted combinations within ranges.
"""
import math
import os
import re

from util import run


def parse(lines):
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
    return workflow_map, rating_maps


def part_1(lines):
    workflow_map, rating_maps = parse(lines)

    accepted = 0
    for rating_map in rating_maps:
        key = 'in'
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
    def __init__(self, eval_str):
        self.eval_str = eval_str
        self.parents = {True: [], False: []}

    def __repr__(self):
        return self.eval_str

    def add_parent(self, parent_node, condition):
        self.parents[condition].append(parent_node)


def part_2(lines):
    MIN_VAL = 1
    MAX_VAL = 4000

    workflow_map, _ = parse(lines)

    key_nodes = {
        'A': Node('True'),  # Accept node
        'R': Node('False'),  # Reject node
    }
    key_nodes.update({
        key: Node(commands[0].split(':')[0]) for key, commands in workflow_map.items()
    })

    # Make a graph!
    for key, commands in workflow_map.items():
        last_node = None
        key_if_all_false = None
        for i, command in enumerate(commands):
            if ':' not in command:
                key_if_all_false = command
                break

            eval_str, key_if_true = command.split(':')
            if i == 0 and key in key_nodes:
                node = key_nodes[key]
            else:
                node = Node(eval_str)
            key_nodes[key_if_true].add_parent(node, True)

            if last_node:
                # If there was a command before this, it had to be false to get here
                node.add_parent(last_node, False)
            last_node = node

        # After all the commands are done, the last node is a parent of the final destination
        key_nodes[key_if_all_false].add_parent(last_node, False)

    # Now we have a full graph of nodes. Trace up from the A node to see what
    # conditions needed to be true to get there.
    condition_paths = [
        [(condition, parent)]
        for condition, parents in key_nodes['A'].parents.items()
        for parent in parents
    ]
    final_paths = []
    new_condition_paths = True
    while new_condition_paths:
        new_condition_paths = []
        for condition_path in condition_paths:
            _, node = condition_path[-1]
            has_parents = False

            for condition in (True, False):
                parents = node.parents[condition] or []
                for parent in parents:
                    new_condition_paths.append(condition_path + [(condition, parent)])
                has_parents = has_parents or bool(parents)

            if not has_parents:
                final_paths.append(condition_path)

        condition_paths = new_condition_paths

    # Calculate all combos
    total = 0
    for condition_path in final_paths:
        possible_rating_values = {
            'x': set(range(MIN_VAL, MAX_VAL + 1)),
            'm': set(range(MIN_VAL, MAX_VAL + 1)),
            'a': set(range(MIN_VAL, MAX_VAL + 1)),
            's': set(range(MIN_VAL, MAX_VAL + 1)),
        }
        for (condition, node) in condition_path:
            rating_key, operator, value = re.findall('(\w)([<|>])(\d+)', node.eval_str)[0]
            value = int(value)
            if operator == '>':
                if condition: # Rating > value
                    possible_rating_values[rating_key] &= set(range(value + 1, MAX_VAL + 1))
                else: # Rating <= value
                    possible_rating_values[rating_key] &= set(range(1, value + 1))

            elif operator == '<':
                if condition: # Rating < value
                    possible_rating_values[rating_key] &= set(range(1, value))
                else: # Rating >= value
                    possible_rating_values[rating_key] &= set(range(value, MAX_VAL + 1))

        total += math.prod(len(total_set) for total_set in possible_rating_values.values())

    return total


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

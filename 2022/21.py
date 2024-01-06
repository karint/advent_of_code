import json
import os

from collections import defaultdict
from util import run


OPERATIONS = {
    '+', '-', '*', '/'
}


class Monkey(object):
    def __init__(self, id_, operation, depends_on_ids=None):
        self.id = id_

        # Operation will just be an integer if the monkey has no dependencies
        self.operation = operation

        # IDs in order of monkeys in cases like '/' and '-'
        self.depends_on_ids = depends_on_ids
        self.depends_on_values = [None, None]

        self.depended_on_by = []
        self.depends_on = []

        self.value = operation if depends_on_ids is None else None

    def set_dependencies(self, monkeys):
        if self.depends_on_ids is not None:
            self.depends_on = [
                monkeys[monkey_id] for monkey_id in self.depends_on_ids
            ]

        for monkey in monkeys.values():
            if not monkey.depends_on_ids:
                continue

            if self.id in monkey.depends_on_ids:
                self.depended_on_by.append(monkey)

    def store_value(self, other_monkey_id, value):
        for i in range(2):
            if self.depends_on_ids[i] == other_monkey_id:
                self.depends_on_values[i] = value

    def set_value(self, value):
        if self.value is not None:
            raise Exception('ERROR, value already set for ', self.id)

        self.value = value

    def populate_value(self):
        if self.value is not None:
            return self.value

        parent = self.depended_on_by[0]
        is_first = parent.depends_on[0].id == self.id
        other_dependency = parent.depends_on[1 if is_first else 0]

        match parent.operation:
            case '+':
                self.value = parent.value - other_dependency.value
            case '-':
                if is_first:
                    self.value = parent.value + other_dependency.value
                else:
                    self.value = other_dependency.value - parent.value
            case '*':
                self.value = parent.value / other_dependency.value
            case '/':
                if is_first:
                    self.value = parent.value * other_dependency.value
                else:
                    self.value = other_dependency.value / parent.value

        return self.value

    def yell(self):
        ''' Returns None if unable to yell yet. '''
        if self.value is not None:
            return self.value

        # Check that values have been populated
        if any(value is None for value in self.depends_on_values):
            return None

        match self.operation:
            case '+':
                self.value = self.depends_on_values[0] + self.depends_on_values[1]
            case '-':
                self.value = self.depends_on_values[0] - self.depends_on_values[1]
            case '*':
                self.value = self.depends_on_values[0] * self.depends_on_values[1]
            case '/':
                self.value = self.depends_on_values[0] / self.depends_on_values[1]

        return self.value

    def __repr__(self):
        if self.depends_on_ids is None:
            return 'Monkey %s: %d' % (self.id, self.operation)
        else:
            return 'Monkey %s: %s %s %s' % (
                self.id,
                self.depends_on_values[0] if self.depends_on_values[0] is not None else self.depends_on_ids[0],
                self.operation,
                self.depends_on_values[1] if self.depends_on_values[0] is not None else self.depends_on_ids[1],
            )

TARGET_MONKEY = 'root'

# Map of monkey to monkeys dependent on it
DEPENDENCIES = defaultdict(set)

MONKEYS = {}

def part_1(lines):
    for line in lines:
        line = line.strip()
        [monkey_id, operation_string] = line.split(': ')

        operation_components = operation_string.split(' ')
        if len(operation_components) == 1:
            # Single value, no dependencies
            MONKEYS[monkey_id] = Monkey(monkey_id, int(operation_components[0]))
        else:
            DEPENDENCIES[operation_components[0]].add(monkey_id)
            DEPENDENCIES[operation_components[2]].add(monkey_id)
            MONKEYS[monkey_id] = Monkey(
                monkey_id,
                operation_components[1],
                [
                    operation_components[0],
                    operation_components[2]
                ],
            )

    while True:
        for monkey in MONKEYS.values():
            value = monkey.yell()

            if value is None:
                continue

            if monkey.id == TARGET_MONKEY:
                return int(value)

            for other_monkey_id in DEPENDENCIES[monkey.id]:
                MONKEYS[other_monkey_id].store_value(monkey.id, value)
    
ME = 'humn'


def part_2(lines):
    for line in lines:
        line = line.strip()
        [monkey_id, operation_string] = line.split(': ')

        operation_components = operation_string.split(' ')
        if len(operation_components) == 1:
            # Single value, no dependencies
            value = int(operation_components[0]) if monkey_id != ME else None
            MONKEYS[monkey_id] = Monkey(monkey_id, value)
        else:
            MONKEYS[monkey_id] = Monkey(
                monkey_id,
                operation_components[1],
                [
                    operation_components[0],
                    operation_components[2]
                ],
            )

    for monkey in MONKEYS.values():
        monkey.set_dependencies(MONKEYS)

    # Create dependency tree, starting from root
    root = MONKEYS[TARGET_MONKEY]
    distance_from_root = {} # id -> steps from root

    # One of these doesn't have me. Solve for it.
    branch_1 = root.depends_on[0]
    branch_2 = root.depends_on[1]
    distance_from_root[branch_1.id] = 1
    distance_from_root[branch_2.id] = 1

    branch_1_ids = set([branch_1.id])
    counter = 1
    while True:
        counter += 1
        initial_length = len(branch_1_ids)
        new_set = set(branch_1_ids)
        for id_ in branch_1_ids:
            depends_on_ids = MONKEYS[id_].depends_on_ids or []
            for depends_on_id in depends_on_ids:
                new_set.add(depends_on_id)
                if depends_on_id not in distance_from_root:
                    distance_from_root[depends_on_id] = counter
        if initial_length == len(new_set):
            break
        branch_1_ids = new_set

    branch_2_ids = set([branch_2.id])
    counter = 1
    while True:
        counter += 1
        initial_length = len(branch_2_ids)
        new_set = set(branch_2_ids)
        for id_ in branch_2_ids:
            depends_on_ids = MONKEYS[id_].depends_on_ids or []
            for depends_on_id in depends_on_ids:
                new_set.add(depends_on_id)
                if depends_on_id not in distance_from_root:
                    distance_from_root[depends_on_id] = counter
        if initial_length == len(new_set):
            break
        branch_2_ids = new_set

    branch_to_solve = branch_2_ids if ME in branch_1_ids else branch_1_ids
    semi_root_id = branch_2.id if ME in branch_1_ids else branch_1.id

    branch_distances_from_root = [
        (v, k) for k, v in distance_from_root.items() if k in branch_to_solve
    ]
    branch_distances_from_root.sort(reverse=True)

    for _, id_ in branch_distances_from_root:
        monkey = MONKEYS[id_]
        value = monkey.yell()
        for other_monkey in monkey.depended_on_by:
            other_monkey.store_value(monkey.id, value)

    target_value = int(MONKEYS[semi_root_id].yell())
    # print('Target value', target_value)

    # Observe the branch I'm in
    my_branch_ids = branch_1_ids if ME in branch_1_ids else branch_2_ids
    my_branch_root_id = branch_1.id if ME in branch_1_ids else branch_2.id
    my_branch_distances_from_root = [
        (v, k) for k, v in distance_from_root.items() if k in my_branch_ids
    ]
    my_branch_distances_from_root.sort()

    # Find remaining nodes that are dependent on me
    dependent_on_me_ids = set([ME])
    while True:
        initial_length = len(dependent_on_me_ids)
        new_set = set(dependent_on_me_ids)
        for monkey_id in dependent_on_me_ids:
            for other_monkey in MONKEYS[monkey_id].depended_on_by:
                new_set.add(other_monkey.id)
        if len(new_set) == initial_length:
            break

        dependent_on_me_ids = new_set

    # Solve the other ones first
    solvable_ids = my_branch_ids - dependent_on_me_ids
    # print(solvable_ids)

    distances_map = [
        (v, k) for k, v in distance_from_root.items() if k in solvable_ids
    ]
    distances_map.sort(reverse=True)

    for _, id_ in distances_map:
        monkey = MONKEYS[id_]
        value = monkey.yell()
        for other_monkey in monkey.depended_on_by:
            other_monkey.store_value(monkey.id, value)

    # Time to work backwards from what's remaining!
    MONKEYS[my_branch_root_id].set_value(target_value)
    curr_set = [MONKEYS[my_branch_root_id]]
    while True:
        new_set = []
        for parent in curr_set:
            if not parent.depends_on_ids:
                continue

            for id_ in parent.depends_on_ids:
                monkey = MONKEYS[id_]
                monkey.populate_value()
                if monkey.id == ME:
                    return int(monkey.value)
                new_set.append(monkey)
        curr_set = new_set
        # print(curr_set)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

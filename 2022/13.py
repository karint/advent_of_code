import json
import os

from util import run


def compare_ints(left, right):
    # If the left integer is lower than the right integer, the inputs are in the right order.
    if left < right:
        return True

    # If the left integer is higher than the right integer, the inputs are not in the right order.
    if left > right:
        return False

    # Otherwise, the inputs are the same integer; continue checking the next part of the input.
    return None


def compare_lists(list_1, list_2):
    # Compare the first value of each list, then the second value, and so on.
    for i, left in enumerate(list_1):
        # If the right list runs out of items first, the inputs are not in the right order.
        if i >= len(list_2):
            return False

        right = list_2[i]

        # If both values are integers
        if isinstance(left, int) and isinstance(right, int):
            result = compare_ints(left, right)
            if result is not None:
                return result

        # If both values are lists
        elif isinstance(left, list) and isinstance(right, list):
            result = compare_lists(left, right)
            if result is not None:
                return result

        # If exactly one value is an integer, convert the integer to a list which contains that integer as its only value.
        else:
            if isinstance(left, int):
                left = [left]
            elif isinstance(right, int):
                right = [right]

            # Then retry the comparison
            result = compare_lists(left, right)
            if result is not None:
                return result

        # If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.
        continue

    # If the left list runs out of items first, the inputs are in the right order.
    if len(list_1) < len(list_2):
        return True

    return


def part_1(lines):
    pair_num = 0
    first_line, second_line = None, None
    right_pairs = []
    for i, line in enumerate(lines):
        line = line.strip()

        if i % 3 == 0:
            first_line = line
        elif i % 3 == 1:
            second_line = line
            pair_num += 1
            left = json.loads(first_line)
            right = json.loads(second_line)
            if compare_lists(left, right):
                right_pairs.append(pair_num)
        
    return sum(right_pairs)
    

def part_2(lines):
    order = []
    divider_1 = [[2]]
    divider_2 = [[6]]

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        new_item = json.loads(line)

        if i == 0:
            order.append(new_item)
            continue

        inserted = False
        for insert_index, ordered_item in enumerate(order):
            if compare_lists(new_item, ordered_item):
                order.insert(insert_index, new_item)
                inserted = True
                break

        if not inserted:
            order.append(new_item)

    # Now insert dividers
    inserted = False
    for insert_index, ordered_item in enumerate(order):
        if compare_lists(divider_1, ordered_item):
            order.insert(insert_index, divider_1)
            divider_index_1 = insert_index + 1
            inserted = True
            break

    if not inserted:
        order.append(divider_1)

    inserted = False
    for insert_index, ordered_item in enumerate(order):
        if compare_lists(divider_2, ordered_item):
            order.insert(insert_index, divider_2)
            divider_index_2 = insert_index + 1
            inserted = True
            break

    if not inserted:
        order.append(divider_2)

    return divider_index_1 * divider_index_2


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

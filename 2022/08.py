import os
import sys

"""
A tree is visible if all of the other trees between it and an edge of the grid
are shorter than it. Only consider trees in the same row or column; that is,
only look up, down, left, or right from any given tree.
"""


def solution(lines):
    forest = [
        [int(tree_str) for tree_str in line.strip()]
        for line in lines
    ]
    num_visible = 0
    for row_index, tree_row in enumerate(forest):
        for col_index, tree in enumerate(tree_row):
            if (
                row_index == 0 or
                row_index + 1 == len(forest) or
                col_index == 0 or
                col_index + 1 == len(tree_row) or 
                (all(tree_row[x] < tree for x in range(0, col_index))) or  # Left
                (all(tree_row[x] < tree for x in range(col_index + 1, len(tree_row)))) or  # Right
                (all(forest[x][col_index] < tree for x in range(0, row_index))) or  # Top
                (all(forest[x][col_index] < tree for x in range(row_index + 1, len(forest))))  # Bottom
            ):
                num_visible += 1
    return num_visible
    

def solution2(lines):
    forest = [
        [int(tree_str) for tree_str in line.strip()]
        for line in lines
    ]
    max_score = 0
    for row_index, tree_row in enumerate(forest):
        for col_index, tree in enumerate(tree_row):
            # Trees on the edge have a score of 0 and can be skipped
            if (
                row_index == 0 or
                row_index +1 == len(forest) or
                col_index == 0 or
                col_index + 1 == len(tree_row)
            ):
                continue

            left = 0
            for x in reversed(range(0, col_index)):
                if tree_row[x] <= tree:
                    left += 1
                
                if tree_row[x] >= tree:
                    break

            right = 0
            for x in range(col_index + 1, len(tree_row)):
                if tree_row[x] <= tree:
                    right += 1
                
                if tree_row[x] >= tree:
                    break

            top = 0
            for x in reversed(range(0, row_index)):
                if forest[x][col_index] <= tree:
                    top += 1
                
                if forest[x][col_index] >= tree:
                    break

            bottom = 0
            for x in range(row_index + 1, len(forest)):
                if forest[x][col_index] <= tree:
                    bottom += 1
                
                if forest[x][col_index] >= tree:
                    break

            score = top * bottom * right * left
            if score > max_score:
                max_score = score

    return max_score


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
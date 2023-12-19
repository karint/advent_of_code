import os
import sys

class PathGrid(object):
    def __init__(self, lines, starting_char, ending_char, can_reach, replacement_map=None):
        self.grid = []
        self.starting_points = set()
        self.ending_points = set()
        self.can_reach = can_reach

        if replacement_map is None:
            replacement_map = {}

        for y, row in enumerate(lines):
            new_row = []
            for x, char in enumerate(row.strip()):
                if char == starting_char:
                    self.starting_points.add((x, y))
                elif char == ending_char:
                    self.ending_points.add((x, y))
                new_row.append(replacement_map.get(char, char))
            self.grid.append(new_row)

        self.width = len(self.grid[0])
        self.height = len(self.grid)

        self.shortest_path_length = self.find_shortest_path_length()

    def find_shortest_path_length(self):
        # Map of last coord to # of steps to get there
        viable_paths = {
            point: 0 for point in self.starting_points
        }
        while True:
            new_paths = {}
            for (last_x, last_y), num_steps in viable_paths.items():
                if (last_x, last_y) in self.ending_points:
                    return num_steps

                right = (last_x + 1, last_y)
                left = (last_x - 1, last_y)
                up = (last_x, last_y + 1)
                down = (last_x, last_y - 1)

                for target_x, target_y in (right, left, up, down):
                    # Don't revisit past squares or go out of bounds
                    if (
                        target_x < 0 or
                        target_x >= self.width or
                        target_y < 0 or
                        target_y >= self.height
                    ):
                        continue

                    if self.can_reach(self.grid, last_x, last_y, target_x, target_y):
                        new_paths[(target_x, target_y)] = num_steps + 1

            viable_paths = new_paths

def solution(lines):
    can_reach = (
        lambda grid, curr_x, curr_y, target_x, target_y:
        grid[curr_y][curr_x] + 1 >= grid[target_y][target_x]
    )
    replacement_map = {
        c: ord(c) for c in 'abcdefghijklmnopqrstuvwxyz'
    }
    replacement_map['S'] = ord('a')
    replacement_map['E'] = ord('z')

    return PathGrid(
        lines,
        'S',
        'E',
        can_reach,
        replacement_map=replacement_map,
    ).find_shortest_path_length()


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

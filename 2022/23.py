import os
import sys

from collections import defaultdict

DIRECTIONS = ['N', 'S', 'W', 'E']


class Elf:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.proposal = None

    def propose_coord(self, occupied_coords, cardinal_prio):
        self.proposal = None

        # Check if any elves around
        coords_to_check = (
            (self.x + 1, self.y + 1),
            (self.x + 1, self.y - 1),
            (self.x + 1, self.y),
            (self.x - 1, self.y + 1),
            (self.x - 1, self.y - 1),
            (self.x - 1, self.y),
            (self.x, self.y + 1),
            (self.x, self.y - 1),
        )
        if all(coord not in occupied_coords for coord in coords_to_check):
            return self.proposal

        # Otherwise, propose a direction
        for direction in cardinal_prio:
            match direction:
                case 'N':
                    coords_to_check = (
                        (self.x - 1, self.y - 1),
                        (self.x, self.y - 1),
                        (self.x + 1, self.y - 1),
                    )
                    if all(coord not in occupied_coords for coord in coords_to_check):
                        self.proposal = (self.x, self.y - 1)
                        break
                case 'S':
                    coords_to_check = (
                        (self.x - 1, self.y + 1),
                        (self.x, self.y + 1),
                        (self.x + 1, self.y + 1),
                    )
                    if all(coord not in occupied_coords for coord in coords_to_check):
                        self.proposal = (self.x, self.y + 1)
                        break
                case 'W':
                    coords_to_check = (
                        (self.x - 1, self.y - 1),
                        (self.x - 1, self.y),
                        (self.x - 1, self.y + 1),
                    )
                    if all(coord not in occupied_coords for coord in coords_to_check):
                        self.proposal = (self.x - 1, self.y)
                        break
                case 'E':
                    coords_to_check = (
                        (self.x + 1, self.y - 1),
                        (self.x + 1, self.y),
                        (self.x + 1, self.y + 1),
                    )
                    if all(coord not in occupied_coords for coord in coords_to_check):
                        self.proposal = (self.x + 1, self.y)
                        break

        # print('Checking %s: %s...' % (direction, coords_to_check))
        # print('Elf at %s proposes %s' % ((self.x, self.y), self.proposal))
        return self.proposal

    def execute_proposal(self):
        self.x, self.y = self.proposal


class Solver:
    def __init__(self, elves):
        self.elves = elves
        self.round = 0
        self.is_done = False
        self.occupied_coords = set()
        self.recalculate()

    def get_size(self):
        return (self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1)

    def recalculate(self):
        self.min_x, self.max_x = None, None
        self.min_y, self.min_y = None, None

        new_occupied_coords = set()
        for elf in self.elves:
            new_occupied_coords.add((elf.x, elf.y))

            if self.min_x is None:
                self.min_x = elf.x
                self.max_x = elf.x
                self.min_y = elf.y
                self.max_y = elf.y
                continue

            if self.min_x > elf.x:
                self.min_x = elf.x
            if self.max_x < elf.x:
                self.max_x = elf.x
            if self.min_y > elf.y:
                self.min_y = elf.y
            if self.max_y < elf.y:
                self.max_y = elf.y

        if new_occupied_coords == self.occupied_coords:
            self.is_done = True

        self.occupied_coords = new_occupied_coords

    def conduct_round(self):
        proposed_coords_count = defaultdict(int)
        direction_index = self.round % len(DIRECTIONS)
        directions = DIRECTIONS[direction_index:] + DIRECTIONS[:direction_index]
        print(directions)

        for elf in self.elves:
            proposed = elf.propose_coord(self.occupied_coords, directions)
            if proposed is not None:
                proposed_coords_count[proposed] += 1

        for elf in self.elves:
            if elf.proposal is not None and proposed_coords_count[elf.proposal] == 1:
                elf.execute_proposal()

        self.recalculate()
        self.round += 1

    def print(self):
        for y in range(self.min_y, self.max_y + 1):
            curr_str = ''
            for x in range(self.min_x, self.max_x + 1):
                curr_str += '#' if (x, y) in self.occupied_coords else '.'
            print(curr_str)
        print('-' * (self.max_x - self.min_x + 1))


def solution(lines):
    elves = []
    for y, line in enumerate(lines):
        line = line.strip()
        for x, char in enumerate(line):
            if char == '#':
                elves.append(Elf(x, y))

    solver = Solver(elves)
    solver.print()

    for round_num in range(10):
        print('Round', round_num + 1)
        solver.conduct_round()
        solver.print()
        
    return solver.get_size() - len(solver.occupied_coords)
    

def solution2(lines):
    elves = []
    for y, line in enumerate(lines):
        line = line.strip()
        for x, char in enumerate(line):
            if char == '#':
                elves.append(Elf(x, y))

    solver = Solver(elves)

    while not solver.is_done:
        print('Round', solver.round + 1)
        solver.conduct_round()
        
    return solver.round


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
import os

from collections import defaultdict
from util import get_adjacent_coords, run

DIRECTION_ORDERS = [
    ['N', 'S', 'W', 'E'],
    ['S', 'W', 'E', 'N'],
    ['W', 'E', 'N', 'S'],
    ['E', 'N', 'S', 'W'],
]

class Elf:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.proposal = None
        self.is_done = False

    def propose_coord(self, occupied_coords, cardinal_prio):
        self.proposal = None

        # Check if any elves around
        adjacent_coords = get_adjacent_coords(self.x, self.y)
        if not (occupied_coords & adjacent_coords):
            return self.proposal

        # Otherwise, propose a direction
        for direction in cardinal_prio:
            match direction:
                case 'N':
                    coords_to_check = {
                        (self.x - 1, self.y - 1),
                        (self.x, self.y - 1),
                        (self.x + 1, self.y - 1),
                    }
                    if not coords_to_check & occupied_coords:
                        self.proposal = (self.x, self.y - 1)
                        return self.proposal
                case 'S':
                    coords_to_check = {
                        (self.x - 1, self.y + 1),
                        (self.x, self.y + 1),
                        (self.x + 1, self.y + 1),
                    }
                    if not coords_to_check & occupied_coords:
                        self.proposal = (self.x, self.y + 1)
                        return self.proposal
                case 'W':
                    coords_to_check = {
                        (self.x - 1, self.y - 1),
                        (self.x - 1, self.y),
                        (self.x - 1, self.y + 1),
                    }
                    if not coords_to_check & occupied_coords:
                        self.proposal = (self.x - 1, self.y)
                        return self.proposal
                case 'E':
                    coords_to_check = {
                        (self.x + 1, self.y - 1),
                        (self.x + 1, self.y),
                        (self.x + 1, self.y + 1),
                    }
                    if not coords_to_check & occupied_coords:
                        self.proposal = (self.x + 1, self.y)
                        return self.proposal

    def execute_proposal(self, occupied_coords):
        occupied_coords.remove((self.x, self.y))
        self.x, self.y = self.proposal
        occupied_coords.add(self.proposal)


class Solver:
    def __init__(self, elves, num_rounds=None):
        self.elves = elves
        self.round = 0
        self.is_done = False
        self.occupied_coords = {(elf.x, elf.y) for elf in self.elves}

    def get_size(self):
        self.min_x, self.min_y = None, None
        self.max_x, self.max_y = None, None

        for elf in self.elves:
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

        return (self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1)

    def conduct_round(self):
        proposed_coords = {}
        directions = DIRECTION_ORDERS[self.round % 4]

        hold_still = set([None])
        for elf in self.elves:
            proposed = elf.propose_coord(self.occupied_coords, directions)
            if proposed not in hold_still:
                if proposed_coords.get(proposed):
                    hold_still.add(proposed)
                    del proposed_coords[proposed]
                else:
                    proposed_coords[proposed] = elf

        self.is_done = True
        for proposed_coord, elf in proposed_coords.items():
            elf.execute_proposal(self.occupied_coords)
            self.is_done = False

        self.round += 1

    def print(self):
        for y in range(self.min_y, self.max_y + 1):
            curr_str = ''
            for x in range(self.min_x, self.max_x + 1):
                curr_str += '#' if (x, y) in self.occupied_coords else '.'
            print(curr_str)
        print('-' * (self.max_x - self.min_x + 1))


def parse_elves(lines):
    elves = []
    for y, line in enumerate(lines):
        line = line.strip()
        for x, char in enumerate(line):
            if char == '#':
                elves.append(Elf(x, y))
    return elves


def part_1(lines):
    solver = Solver(parse_elves(lines))
    for round_num in range(10):
        solver.conduct_round()
    return solver.get_size() - len(solver.occupied_coords)
    

def part_2(lines):
    solver = Solver(parse_elves(lines))
    while not solver.is_done:
        solver.conduct_round()
    return solver.round


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

import os
import sys

from collections import defaultdict
from util import run


class Direction:
    RIGHT = '>'
    LEFT = '<'
    UP = '^'
    DOWN = 'v'


DIRECTIONS = {
    Direction.RIGHT,
    Direction.LEFT,
    Direction.UP,
    Direction.DOWN,
}


class Blizzard:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def advance(self, min_x, max_x, min_y, max_y):
        if self.direction == Direction.RIGHT:
            self.x += 1
            if self.x >= max_x:
                self.x = min_x
        elif self.direction == Direction.LEFT:
            self.x -= 1
            if self.x < min_x:
                self.x = max_x - 1
        elif self.direction == Direction.DOWN:
            self.y += 1
            if self.y >= max_y:
                self.y = min_y
        elif self.direction == Direction.UP:
            self.y -= 1
            if self.y < min_y:
                self.y = max_y - 1


class Path:
    def __init__(self, coords_so_far):
        self.coords_so_far = [coord for coord in coords_so_far]


class Solver:
    def __init__(self, grid, blizzards):
        self.grid = grid
        self.blizzards = blizzards
        self.min_x, self.max_x = 1, len(self.grid[0]) - 1
        self.min_y, self.max_y = 1, len(self.grid) - 1
        self.num_minutes = 0
        self.goal_coord = (self.max_x - 1, self.max_y)
        self.goal_coords = [
            (self.max_x - 1, self.max_y),
            (1, 0),
            (self.max_x - 1, self.max_y),
        ]

        self.wall_coords = set()
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if char == '#':
                    self.wall_coords.add((x, y))

        self.x = 1
        self.y = 0

    def simulate(self):
        goals_reached = 0
        current_goal = self.goal_coords[goals_reached]
        possible_current_locations = set([(self.x, self.y)])
        while goals_reached < len(self.goal_coords):
            self.num_minutes += 1
            # print('\nMinute %d...' % self.num_minutes)

            current_goal = self.goal_coords[goals_reached]
            new_possible_current_locations = set(possible_current_locations)
            occupied_coords = set(self.wall_coords)
            for blizzard in self.blizzards:
                blizzard.advance(self.min_x, self.max_x, self.min_y, self.max_y)
                occupied_coords.add((blizzard.x, blizzard.y))

            # Add anywhere we could've moved
            for possible_x, possible_y in possible_current_locations:
                if (goals_reached == 0 or goals_reached == 2) and (possible_x, possible_y + 1) == current_goal:
                    goals_reached += 1
                    new_possible_current_locations = set([(possible_x, possible_y + 1)])
                    break
                    
                if goals_reached == 1 and (possible_x, possible_y - 1) == current_goal:
                    goals_reached += 1
                    new_possible_current_locations = set([(possible_x, possible_y - 1)])
                    break

                if possible_x < self.max_x - 1 and (possible_x + 1, possible_y) not in occupied_coords:
                    new_possible_current_locations.add((possible_x + 1, possible_y))

                if possible_y < self.max_y - 1 and (possible_x, possible_y + 1) not in occupied_coords:
                    new_possible_current_locations.add((possible_x, possible_y + 1))

                if possible_x > self.min_x and (possible_x - 1, possible_y) not in occupied_coords:
                    new_possible_current_locations.add((possible_x - 1, possible_y))

                if possible_y > self.min_y and (possible_x, possible_y - 1) not in occupied_coords:
                    new_possible_current_locations.add((possible_x, possible_y - 1))

            # Remove anywhere that we could not have stayed
            new_possible_current_locations -= occupied_coords
            possible_current_locations = new_possible_current_locations


    def print(self):
        blizzards_at_coords = defaultdict(list)
        for blizzard in self.blizzards:
            blizzards_at_coords[(blizzard.x, blizzard.y)].append(blizzard)

        for y, row in enumerate(self.grid):
            if y == 0:
                # print(row.replace('.', 'E' if self.y == 0 else '.'))
                continue

            curr_str = ''
            for x, char in enumerate(row):
                # Check if is self
                if self.x == x and self.y == y:
                    symbol = 'E'
                else:
                    blizzards_at_this_coord = blizzards_at_coords[(x, y)]
                    if blizzards_at_this_coord:
                        if len(blizzards_at_this_coord) == 1:
                            symbol = blizzards_at_this_coord[0].direction
                        else:
                            symbol = str(len(blizzards_at_this_coord))
                    else:
                        symbol = '#' if char == '#' else '.'
                curr_str += symbol
            # print(curr_str)

    def solve(self):
        while ((self.x, self.y) != self.goal_coord):
            # self.print()
            self.num_minutes += 1
            occupied_coords = set(self.wall_coords)
            for blizzard in self.blizzards:
                blizzard.advance(self.min_x, self.max_x, self.min_y, self.max_y)
                occupied_coords.add((blizzard.x, blizzard.y))

            # print('Occupied', occupied_coords)

            # Determine whether to prio going down or right
            dx = self.goal_coord[0] - self.x
            dy = self.goal_coord[1] - self.y

            if dx > dy:
                good_prios = [Direction.RIGHT, Direction.DOWN]
                bad_prios = [Direction.UP, Direction.LEFT]
            else:
                good_prios = [Direction.DOWN, Direction.RIGHT]
                bad_prios = [Direction.LEFT, Direction.UP]

            already_moved = False
            for direction in good_prios:
                # Try moving a good direction first
                if direction == Direction.RIGHT:
                    if (
                        not already_moved and
                        self.x < self.max_x - 1 and
                        (self.x + 1, self.y) not in occupied_coords
                    ):
                        self.x += 1
                        already_moved = True
                elif direction == Direction.DOWN:
                    if (
                        not already_moved and
                        self.y < self.max_y - 1 and
                        (self.x, self.y + 1) not in occupied_coords
                    ):
                        self.y += 1
                        already_moved = True

            # Continue on if we already moved, or stay still if able
            if already_moved or (self.x, self.y) not in occupied_coords:
                continue

                # If we have to move, move by priority
            for direction in bad_prios:
                if direction == Direction.LEFT:
                    if (
                        not already_moved and
                        self.x > self.min_x and
                        (self.x - 1, self.y) not in occupied_coords
                    ):
                        self.x -= 1
                        already_moved = True
                elif direction == Direction.UP:
                    if (
                        not already_moved and
                        self.y > self.min_y and
                        (self.x, self.y - 1) not in occupied_coords
                    ):
                        self.y -= 1
                        already_moved = True

            if not already_moved:
                raise Exception("We got eaten by a blizzard!")

        self.print()


def part_1(lines):
    grid = []
    blizzards = []
    for y, line in enumerate(lines):
        line = line.strip()
        grid.append(line)
        for x, char in enumerate(line):
            if char in DIRECTIONS:
                blizzards.append(Blizzard(x, y, char))

    solver = Solver(grid, blizzards)
    solver.simulate()

    return solver.num_minutes


def part_2(lines):
    return part_1(lines)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

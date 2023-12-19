import math
import os
import sys

WIDTH = 7
UNITS_FROM_LEFT = 2
UNITS_FROM_HIGHEST_ROCK = 4
ROCK_SHAPES = ['HORIZONTAL', 'CROSS', 'L', 'VERTICAL', 'SQUARE']
MAX_SHAPE_HEIGHT = 4

'''
3  ####   .#.   ..#   #   ##
2         ###   ..#   #   ##
1         .#.   ###   #
0                     #
'''

class Simulation(object):
    def __init__(self, jetstream):
        self.jetstream = jetstream

        self.found_loop = False

        self.settled_rock_count = 0
        self.jet_count = 0
        self.highest_rock = -1

        # List of lists representing the chamber, where the first row is the row before
        # the floor, and subsequent rows represent going higher in the chamber. Every row
        # is 7 long. 'True' = rock at rest, 'False' = empty
        self.chamber = []

    def print_chamber(self, falling_rock_coords=None):
        printable_chamber = []
        for y, row in enumerate(self.chamber):
            new_row = []
            for x, is_blocked in enumerate(row):
                if falling_rock_coords and (x, y) in falling_rock_coords:
                    char = '@'
                else:
                    char = '#' if is_blocked else '.'
                new_row.append(char)
            printable_chamber.append(new_row)

        printable_chamber.reverse()
        for row in printable_chamber:
            print(''.join(row))

        print('-' * WIDTH)
        print('\n\n')

    def new_rock_fall(self):
        # Make chamber higher if needed
        if self.highest_rock + UNITS_FROM_HIGHEST_ROCK + MAX_SHAPE_HEIGHT > len(self.chamber):
            for _ in range(UNITS_FROM_HIGHEST_ROCK + MAX_SHAPE_HEIGHT):
                self.chamber.append([False] * WIDTH)

        shape = ROCK_SHAPES[self.settled_rock_count % len(ROCK_SHAPES)]
        lowest_y = self.highest_rock + UNITS_FROM_HIGHEST_ROCK

        match shape:
            case 'HORIZONTAL':
                coords_of_current_rock = [
                    (UNITS_FROM_LEFT, lowest_y),
                    (UNITS_FROM_LEFT + 1, lowest_y),
                    (UNITS_FROM_LEFT + 2, lowest_y),
                    (UNITS_FROM_LEFT + 3, lowest_y),
                ]
            case 'CROSS':
                coords_of_current_rock = [
                    (UNITS_FROM_LEFT + 1, lowest_y),     # top
                    (UNITS_FROM_LEFT, lowest_y + 1),     # left
                    (UNITS_FROM_LEFT + 1, lowest_y + 1), # middle
                    (UNITS_FROM_LEFT + 2, lowest_y + 1), # right
                    (UNITS_FROM_LEFT + 1, lowest_y + 2), # bottom
                ]
            case 'L':
                coords_of_current_rock = [
                    (UNITS_FROM_LEFT, lowest_y),         # left base
                    (UNITS_FROM_LEFT + 1, lowest_y),     # middle base
                    (UNITS_FROM_LEFT + 2, lowest_y),     # right base
                    (UNITS_FROM_LEFT + 2, lowest_y + 1), # middle row
                    (UNITS_FROM_LEFT + 2, lowest_y + 2), # top row
                ]
            case 'VERTICAL':
                coords_of_current_rock = [
                    (UNITS_FROM_LEFT, lowest_y),
                    (UNITS_FROM_LEFT, lowest_y + 1),
                    (UNITS_FROM_LEFT, lowest_y + 2),
                    (UNITS_FROM_LEFT, lowest_y + 3),
                ]
            case 'SQUARE':
                coords_of_current_rock = [
                    (UNITS_FROM_LEFT, lowest_y),
                    (UNITS_FROM_LEFT, lowest_y + 1),
                    (UNITS_FROM_LEFT + 1, lowest_y),
                    (UNITS_FROM_LEFT + 1, lowest_y + 1),
                ]

        self.simulate_rock_fall(shape, coords_of_current_rock)

    def simulate_rock_fall(self, shape, rock_coords):
        while True:
            # self.print_chamber(rock_coords)

            # Simulate jet burst
            jetstream_index = self.jet_count % len(self.jetstream)
            dx = 1 if self.jetstream[jetstream_index] == '>' else -1
            self.jet_count += 1
            try:
                # Shift rock based on jet if we can
                if all(y >= 0 and x + dx >= 0 and not self.chamber[y][x + dx] for x, y in rock_coords):
                    rock_coords = [(x + dx, y) for x, y in rock_coords]
            except IndexError: # Rock was going to go out of bounds, so don't move it
                pass

            # Simulate falling

            # Come to rest if we hit the floor or another rock
            if any(y == 0 or self.chamber[y - 1][x] for x, y in rock_coords):
                for x, y in rock_coords:
                    self.chamber[y][x] = True
                    if y > self.highest_rock:
                        self.highest_rock = y
                self.settled_rock_count += 1
                # print(jetstream_index)
                return

            # Otherwise move rock down
            rock_coords = [(x, y - 1) for x, y in rock_coords]


def solution(lines):
    resting_rocks = 2022
    jetstream = lines[0].strip()
    sim = Simulation(jetstream)

    while (sim.settled_rock_count < resting_rocks):
        sim.new_rock_fall()
        # sim.print_chamber()
        
    return sim.highest_rock + 1
    

def solution2(lines):
    resting_rocks = 1000000000000
    # rocks_per_loop = 35
    # rocks_before_loop = 14
    rocks_per_loop = 1745
    rocks_before_loop = 1748

    # Need to calculate
    height_before_loop = None
    height_after_first_loop = None
    height_after_second_loop = None
    height_after_third_loop = None

    jetstream = lines[0].strip() # len = 10091
    sim = Simulation(jetstream)

    while (sim.settled_rock_count < resting_rocks):
        if sim.settled_rock_count == rocks_before_loop:
            height_before_loop = sim.highest_rock
        elif sim.settled_rock_count == rocks_before_loop + rocks_per_loop:
            height_after_first_loop = sim.highest_rock
        elif sim.settled_rock_count == rocks_before_loop + rocks_per_loop * 2:
            height_after_second_loop = sim.highest_rock
        elif sim.settled_rock_count == rocks_before_loop + rocks_per_loop * 3:
            height_after_third_loop = sim.highest_rock
            break

        sim.new_rock_fall()
        # sim.print_chamber()

    print('height_before_loop', height_before_loop)
    print('height_after_first_loop', height_after_first_loop)
    print('height_after_second_loop', height_after_second_loop)
    print('height_after_third_loop', height_after_third_loop)

    # How high the structure was before we started looping, minus the latest row
    height_per_loop = height_after_third_loop - height_after_second_loop
    print('height_per_loop', height_per_loop)

    num_loops = math.floor((resting_rocks - rocks_before_loop) / rocks_per_loop)
    print('num_loops', num_loops)
    remainder = (resting_rocks - rocks_before_loop) % rocks_per_loop
    print('remainder', remainder)

    remainder_sim = Simulation(jetstream)
    while (remainder_sim.settled_rock_count < rocks_before_loop + rocks_per_loop + remainder):
        remainder_sim.new_rock_fall()
        # sim.print_chamber()

    return remainder_sim.highest_rock + (num_loops - 1) * height_per_loop + 1
   

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
"""
Part 1:
Part 2:
"""
import math
import os

from util import OPPOSITE_DIRECTIONS, Direction, run


ALL_DIRECTIONS = {
    Direction.RIGHT,
    Direction.LEFT,
    Direction.UP,
    Direction.DOWN,
}


class Step(object):
    def __init__(self, d, x, y):
        self.d = d
        self.x = x
        self.y = y
        self.distance = math.inf

    def set_distance_if_lower(self, distance):
        if self.distance > distance:
            self.distance = distance


HEIGHT = 71
WIDTH = 71

def part_1(lines):
    grid = []
    wall_coords = []
    for i, line in enumerate(lines):
        line = line.strip()
        x, y = map(int, line.split(','))
        wall_coords.append((x, y))

    start, end = (0, 0), (70, 70)
    num_fallen = 1024

    unvisited = {}
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) not in wall_coords[:num_fallen]:
                unvisited[(x, y)] = Step(None, x, y)
    unvisited[start].set_distance_if_lower(0)

    visited = set()

    while True:
        curr_step = sorted(unvisited.values(), key=lambda s: s.distance)[0]

        if (curr_step.x, curr_step.y) == end:
            return curr_step.distance

        if curr_step.distance == math.inf:
            break

        visited.add((curr_step.x, curr_step.y))

        dir_to_coords = {
            Direction.LEFT: (curr_step.x - 1, curr_step.y),
            Direction.RIGHT: (curr_step.x + 1, curr_step.y),
            Direction.UP: (curr_step.x, curr_step.y - 1),
            Direction.DOWN: (curr_step.x, curr_step.y + 1),
        }
        for (x, y) in dir_to_coords.values():
            if (x, y) in unvisited:
                neighbor = unvisited[(x, y)]
                neighbor.set_distance_if_lower(curr_step.distance + 1)
        del(unvisited[(curr_step.x, curr_step.y)])


def part_2(lines):
    grid = []
    wall_coords = []
    for i, line in enumerate(lines):
        line = line.strip()
        x, y = map(int, line.split(','))
        wall_coords.append((x, y))

    start, end = (0, 0), (70, 70)

    min_bytes = 1023
    max_bytes = len(wall_coords)
    while True:
        # binary search
        num_fallen = min_bytes + max(1, (max_bytes - min_bytes) // 2)
        unvisited = {}
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (x, y) not in wall_coords[:num_fallen]:
                    unvisited[(x, y)] = Step(None, x, y)
        unvisited[start].set_distance_if_lower(0)

        visited = set()

        while True:
            curr_step = sorted(unvisited.values(), key=lambda s: s.distance)[0]

            if (curr_step.x, curr_step.y) == end:
                # print('Too low', num_fallen)
                min_bytes = num_fallen
                break

            if curr_step.distance == math.inf:
                max_bytes = num_fallen
                if max_bytes - min_bytes <= 1:
                    return ','.join(map(str, wall_coords[num_fallen - 1]))
                else:
                    # print('Too high', num_fallen)
                    break

            visited.add((curr_step.x, curr_step.y))

            dir_to_coords = {
                Direction.LEFT: (curr_step.x - 1, curr_step.y),
                Direction.RIGHT: (curr_step.x + 1, curr_step.y),
                Direction.UP: (curr_step.x, curr_step.y - 1),
                Direction.DOWN: (curr_step.x, curr_step.y + 1),
            }
            for (x, y) in dir_to_coords.values():
                if (x, y) in unvisited:
                    neighbor = unvisited[(x, y)]
                    neighbor.set_distance_if_lower(curr_step.distance + 1)
            del(unvisited[(curr_step.x, curr_step.y)])


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

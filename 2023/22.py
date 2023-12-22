"""
Part 1:
Part 2:
"""
import os

from collections import defaultdict
from util import find_digits, run

FREE = '.'


class Brick:
    def __init__(self, id_, x1, y1, z1, x2, y2, z2):
        self.id = id_
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.depends_on = set()
        self.depended_on_by = set()

    def __repr__(self):
        return '(%s, %s, %s)~(%s, %s, %s)' % (
            self.x1,
            self.y1,
            self.z1,
            self.x2,
            self.y2,
            self.z2,
        )

    def fall(self, cube):
        # Move brick down z-axis until it can't
        while True:
            if self.z1 == 1:
                # Already at rest
                break

            # Check z layer below for any collisions
            for z in range(self.z1 - 1, self.z2):
                for y in range(self.y1, self.y2 + 1):
                    for x in range(self.x1, self.x2 + 1):
                        if cube[z][y][x] not in (FREE, self.id):
                            self.depends_on.add(cube[z][y][x])
            if self.depends_on:
                break
            else:
                self.z1 -= 1
                self.z2 -= 1

    def place(self, cube, replace=True):
        if replace:
            for z in range(len(cube)):
                for y in range(len(cube[0])):
                    for x in range(len(cube[0][0])):
                        if cube[z][y][x] == self.id:
                            cube[z][y][x] = FREE

        # Place brick in cube
        for z in range(self.z1, self.z2 + 1):
            for y in range(self.y1, self.y2 + 1):
                for x in range(self.x1, self.x2 + 1):
                    cube[z][y][x] = self.id


def part_1(lines):
    brick_map = {}
    max_x, max_y, max_z = -1, -1, -1
    for i, line in enumerate(lines):
        line = line.strip()
        one, two = line.split('~')
        x1, y1, z1 = map(int, one.split(','))
        x2, y2, z2 = map(int, two.split(','))
        brick = Brick(str(i), x1, y1, z1, x2, y2, z2)
        brick_map[str(i)] = brick

        if x2 > max_x:
            max_x = x2
        if y2 > max_y:
            max_y = y2
        if z2 > max_z:
            max_z = z2

        if x1 > x2 or y1 > y2 or z1 > z2:
            assert(False)

    # Make our 3d cube
    cube = []
    for _ in range(max_z + 1):
        grid = []
        for _ in range(max_y + 1):
            row = []
            for _ in range(max_x + 1):
                row.append(FREE)
            grid.append(row)
        cube.append(grid)

    # First add all bricks into the cube
    for id_, brick in brick_map.items():
        brick.place(cube, replace=False)

    # Order bricks by z axis
    ordered_bricks = sorted(brick_map.values(), key=lambda b: b.z1)
    for brick in ordered_bricks:
        brick.fall(cube)
        brick.place(cube, replace=True)

    for z, grid in enumerate(cube):
        line = ''
        for y, row in enumerate(grid):
            line += row[0]

    candidates = set(brick_map.keys())
    for brick in ordered_bricks:
        if len(brick.depends_on) == 1:
            candidates.discard(next(iter(brick.depends_on)))
    # print(candidates)
    # print(set(brick_map.keys()) - set(dependents.keys()))

    return len(candidates)


def part_2(lines):
    brick_map = {}
    max_x, max_y, max_z = -1, -1, -1
    for i, line in enumerate(lines):
        line = line.strip()
        one, two = line.split('~')
        x1, y1, z1 = map(int, one.split(','))
        x2, y2, z2 = map(int, two.split(','))
        brick = Brick(str(i), x1, y1, z1, x2, y2, z2)
        brick_map[str(i)] = brick

        if x2 > max_x:
            max_x = x2
        if y2 > max_y:
            max_y = y2
        if z2 > max_z:
            max_z = z2

        if x1 > x2 or y1 > y2 or z1 > z2:
            assert(False)

    # Make our 3d cube
    cube = []
    for _ in range(max_z + 1):
        grid = []
        for _ in range(max_y + 1):
            row = []
            for _ in range(max_x + 1):
                row.append(FREE)
            grid.append(row)
        cube.append(grid)

    # First add all bricks into the cube
    for id_, brick in brick_map.items():
        brick.place(cube, replace=False)

    # Order bricks by z axis
    ordered_bricks = sorted(brick_map.values(), key=lambda b: b.z1)
    for brick in ordered_bricks:
        brick.fall(cube)
        brick.place(cube, replace=True)

    for z, grid in enumerate(cube):
        line = ''
        for y, row in enumerate(grid):
            line += row[0]

    dependencies = defaultdict(set)
    for brick in ordered_bricks:
        for depended_on in brick.depends_on:
            supporting_brick = brick_map[depended_on]
            supporting_brick.depended_on_by.add(brick.id)
            dependencies[brick.id].add(supporting_brick.id)

    total_falling = 0
    for brick in ordered_bricks:
        dependency_copy = {k: set(v) for k, v in dependencies.items()}
        bricks_to_fall_ids = set([brick.id])
        while bricks_to_fall_ids:
            new_bricks_to_fall_ids = set()
            for falling_brick_id in bricks_to_fall_ids:
                for id_ in brick_map[falling_brick_id].depended_on_by:
                    if not dependency_copy[id_]:
                        continue
                    dependency_copy[id_].discard(falling_brick_id)
                    if not dependency_copy[id_]:
                        new_bricks_to_fall_ids.add(id_)
                        total_falling += 1
            bricks_to_fall_ids = new_bricks_to_fall_ids

    return total_falling


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

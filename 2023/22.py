"""
Part 1: Determine what bricks are safe to demolish once they are at rest in a cube.
Part 2: Determine the total falling bricks when demonlishing each brick.
"""
import os

from collections import defaultdict
from util import run

FREE = '.'


class Brick:
    def __init__(self, id_, x1, y1, z1, x2, y2, z2):
        self.id = id_
        self.x1, self.y1, self.z1 = x1, y1, z1
        self.x2, self.y2, self.z2 = x2, y2, z2
        self.depends_on = set()
        self.depended_on_by = set()

    def __repr__(self):
        return '(%s, %s, %s)~(%s, %s, %s)' % (
            self.x1, self.y1, self.z1,
            self.x2, self.y2, self.z2,
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

        self.place(cube, replace=True)

    def place(self, cube, replace=False):
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


def iniitalize(lines):
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

    # Add all bricks into the cube
    for id_, brick in brick_map.items():
        brick.place(cube)

    # Order bricks by z-axis and place them
    ordered_bricks = sorted(brick_map.values(), key=lambda b: b.z1)
    for brick in ordered_bricks:
        brick.fall(cube)

    return brick_map, cube


def part_1(lines):
    brick_map, cube = iniitalize(lines)
    return len(
        set(brick_map.keys()) -
        set.union(*(
            brick.depends_on for brick in brick_map.values()
            if len(brick.depends_on) == 1
        ))
    )


def part_2(lines):
    brick_map, cube = iniitalize(lines)

    dependency_map = defaultdict(set)
    for brick in brick_map.values():
        for depended_on_id in brick.depends_on:
            brick_map[depended_on_id].depended_on_by.add(brick.id)
            dependency_map[brick.id].add(depended_on_id)

    total_falling = 0
    for brick_to_disintegrate in brick_map.values():
        # Map of brick ID -> bricks it depends on
        dependency_map_copy = {k: set(v) for k, v in dependency_map.items()}
        bricks_to_fall_ids = set([brick_to_disintegrate.id])
        while bricks_to_fall_ids:
            new_bricks_to_fall_ids = set()
            for falling_brick_id in bricks_to_fall_ids:
                # Check all dependents of this falling brick
                for dependent_id in brick_map[falling_brick_id].depended_on_by:
                    # Check if dependent already fell
                    if not dependency_map_copy[dependent_id]:
                        continue

                    # Remove the eliminated brick from being depended on
                    dependency_map_copy[dependent_id].discard(falling_brick_id)

                    # If we no longer have any bricks to depend on, we fall
                    if not dependency_map_copy[dependent_id]:
                        new_bricks_to_fall_ids.add(dependent_id)
                        total_falling += 1
            bricks_to_fall_ids = new_bricks_to_fall_ids
    return total_falling


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

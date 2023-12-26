"""
Part 1: Find how many hailstone collisions will happen within a given area.
Part 2: Determine initial position of a rock to throw that will hit all hailstones.
"""
import os

from itertools import combinations
from util import run
from z3 import Int, Solver


class Hailstone:
    def __init__(self, id_, x, y, z, dx, dy, dz):
        self.id = id_
        self.x, self.y, self.z = x, y, z
        self.dx, self.dy, self.dz = dx, dy, dz

        self.xy_slope = self.dy/self.dx
        self.xy_intercept = self.y - self.xy_slope * self.x

    def __repr__(self):
        return '%s: %d %d %d @ %d %d %d' % (
            self.id,
            self.x, self.y, self.z,
            self.dx, self.dy, self.dz,
        )

    def get_xy_intersection_point(self, other):
        if self.xy_slope == other.xy_slope:
            return None

        ix = (other.xy_intercept - self.xy_intercept) / (self.xy_slope - other.xy_slope)
        iy = self.xy_slope * ix + self.xy_intercept

        # Check if these were past or future
        to_check = [
            (ix, self.x, self.dx),
            (ix, other.x, other.dx),
            (iy, self.y, self.dy),
            (iy, other.y, other.dy),
        ]
        for intercept, pos, velocity in to_check:
            if not (
                (intercept > pos and velocity > 0) or
                (intercept < pos and velocity < 0) or
                (intercept == pos and velocity == 0)
            ):
                return None

        return ix, iy


def parse_hailstones(lines):
    hailstones = {}
    for i, line in enumerate(lines):
        line = line.strip()
        segments = line.split('@')
        x, y, z = map(int, segments[0].split(', '))
        dx, dy, dz = map(int, segments[1].split(', '))
        hailstones[i] = Hailstone(i, x, y, z, dx, dy, dz)
    return hailstones


def part_1(lines):
    MIN = 200000000000000
    MAX = 400000000000000
    hailstones = parse_hailstones(lines)

    collisions = 0
    for a, b in combinations(hailstones.values(), 2):
        intersection_point = a.get_xy_intersection_point(b)
        if intersection_point:
            x, y = intersection_point
            if x >= MIN and x <= MAX and y >= MIN and y <= MAX:
                collisions += 1
        
    return collisions


def part_2(lines):
    # We need 5 hailstones to create a system of equations
    NEEDED_HAILSTONES = 5
    hailstones = parse_hailstones(lines)
    sample_hailstones = list(hailstones.values())[:NEEDED_HAILSTONES]

    x, y, z = Int('x'), Int('y'), Int('z')
    dx, dy, dz = Int('dx'), Int('dy'), Int('dz')
    times = [Int('t%s' % i) for i in range(len(sample_hailstones))]

    equations = []
    for i, h in enumerate(sample_hailstones):
        equations.append(dx*times[i] + x == h.dx*times[i] + h.x)
        equations.append(dy*times[i] + y == h.dy*times[i] + h.y)
        equations.append(dz*times[i] + z == h.dz*times[i] + h.z)

    s = Solver()
    s.add(*equations)
    s.check()
    m = s.model()
    x = m.evaluate(x).as_long()
    y = m.evaluate(y).as_long()
    z = m.evaluate(z).as_long()
    return x + y + z


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

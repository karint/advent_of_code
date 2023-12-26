"""
Part 1: 
Part 2:
"""
import math
import matplotlib.pyplot as plt
import os

from itertools import combinations
from util import run
from z3 import *

MIN = 200000000000000
MAX = 400000000000000
# MIN = 7
# MAX = 27


class Hailstone:
    def __init__(self, id_, x, y, z, dx, dy, dz):
        self.id = id_
        self.x0, self.y0, self.z0 = x, y, z
        self.x, self.y, self.z = x, y, z
        self.dx, self.dy, self.dz = dx, dy, dz

        self.xy_slope = self.dy/self.dx
        self.xy_intercept = self.y - self.xy_slope * self.x


        self.t = 0  # We are at time 0
        self.dt = 1  # Delta time is 1

    def __repr__(self):
        return '%s: %d %d %d @ %d %d %d' % (
            self.id,
            self.x, self.y, self.z,
            self.dx, self.dy, self.dz,
        )

    def get_position_at_time(self, time):
        return (
            self.x0 + time * self.dx,
            self.y0 + time * self.dy,
            self.z0 + time * self.dz,
        )

    def get_distance(self, other, time=0):
        # √[(x₂ - x₁)² + (y₂ - y₁)² +(z₂ - z₁)²]
        x0, y0, z0 = self.get_position_at_time(time)
        x1, y1, z1 = other.get_position_at_time(time)
        return math.sqrt(
            math.pow(x0 - x1, 2) +
            math.pow(y0 - y1, 2) +
            math.pow(z0 - z1, 2)
        )

    def get_xy_intersection_point(self, other):
        if self.xy_slope == other.xy_slope:
            return None

        ix = (other.xy_intercept - self.xy_intercept) / (self.xy_slope - other.xy_slope)
        iy = self.xy_slope * ix + self.xy_intercept

        # Check if these were past or future
        ix_good = (
            (ix > self.x and self.dx > 0) or
            (ix < self.x and self.dx < 0) or
            (ix == self.x and self.dx == 0)
        ) and (
            (ix > other.x and other.dx > 0) or
            (ix < other.x and other.dx < 0) or
            (ix == other.x and other.dx == 0)
        )
        iy_good = (
            (iy > self.y and self.dy > 0) or
            (iy < self.y and self.dy < 0) or
            (iy == self.y and self.dy == 0)
        ) and  (
            (iy > other.y and other.dy > 0) or
            (iy < other.y and other.dy < 0) or
            (iy == other.y and other.dy == 0)
        )

        if ix_good and iy_good:
            return ix, iy

        return None


class RockPath:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.c = None  # The mythical third hailstone to hit

        # With just two points, there are still infinite speeds
        # we can have to be able to hit them both along their
        # trajectories. We need to wait for a third point
        # before determining trajectory.
        self.dx, self.dy, self.dz = None, None, None

    def extend(self, hailstones):
        """
        Try to extend the existing path to hit the next hailstone.
        """
        for hailstone in hailstones.values():
            if hailstone.id in self.path:
                continue

            velocities = self.test_third_stone(hailstone)
            if velocities:
                self.dx, self.dy, self.dz = velocities
                return True

        return False

    def test_third_stone(self, c):
        # Try a bunch of velocities
        for dx in range(MIN_VELOCITY, MAX_VELOCITY):
            for dy in range(MIN_VELOCITY, MAX_VELOCITY):
                for dz in range(MIN_VELOCITY, MAX_VELOCITY):
                    if self.velocity_works(c, dx, dy, dz):
                        return True
        return False

    def test_velocity(self, c, dx, dy, dz):
        """
        Test if c is hittable with a rock that starts at a and goes through b
        at the given dx, dy, and dz.
        """
        # Assume we start at a at t0

    def get_original_coords(self):
        """
        Calculate the original coordinates of the rock that goes through
        the path.
        """
        if any(d is None for d in (self.dx, self.dy, self.dz)):
            raise Exception('Asked for original coords before we could determine them!')


def part_1(lines):
    hailstones = {}
    for i, line in enumerate(lines):
        line = line.strip()
        segments = line.split('@')
        x, y, z = map(int, segments[0].split(', '))
        dx, dy, dz = map(int, segments[1].split(', '))
        hailstones[i] = Hailstone(i, x, y, z, dx, dy, dz)

    collisions = 0
    for a, b in combinations(hailstones.values(), 2):
        intersection_point = a.get_xy_intersection_point(b)
        if intersection_point:
            x, y = intersection_point
            if x >= MIN and x <= MAX and y >= MIN and y <= MAX:
                collisions += 1
        
    return collisions


def part_2(lines):
    hailstones = {}
    for i, line in enumerate(lines):
        line = line.strip()
        segments = line.split('@')
        x, y, z = map(int, segments[0].split(', '))
        dx, dy, dz = map(int, segments[1].split(', '))
        hailstones[i] = Hailstone(i, x, y, z, dx, dy, dz)

    x0, y0, z0 = Int('x0'), Int('y0'), Int('z0')
    dx, dy, dz = Int('dx'), Int('dy'), Int('dz')

    sample_hailstones = list(hailstones.values())[:5]
    times = [Int('t%s' % i) for i in range(len(sample_hailstones))]

    equations = []
    for i, h in enumerate(sample_hailstones):
        equations.append(dx*times[i] + x0 == h.dx*times[i] + h.x0)
        equations.append(dy*times[i] + y0 == h.dy*times[i] + h.y0)
        equations.append(dz*times[i] + z0 == h.dz*times[i] + h.z0)

    s = Solver()
    s.add(*equations)
    s.check()
    m = s.model()
    x = m.evaluate(x0).as_long()
    y = m.evaluate(y0).as_long()
    z = m.evaluate(z0).as_long()
    print('x0:', x)
    print('y0:', y)
    print('z0:', z)
    return x + y + z


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

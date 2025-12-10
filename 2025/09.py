"""
Part 1: Started 9:16am ET. Find biggest rectangle that can be formed between two coords.
Part 2: Find biggest rectangle that can be found between two coords within the polygon
        formed by all the points.
"""
import math
import os

from util import run


def part_1(lines):
    count = 0
    coords = set()
    for line in lines:
        line = line.strip()
        a, b = line.split(',')
        (x, y) = int(a), int(b)
        coords.add((x, y))

    max_area = 0
    for x1, y1 in coords:
        for x2, y2 in coords:
            area = (abs(x1 - x2) + 1)*(abs(y1 - y2) + 1)
            max_area = max(area, max_area)

    return max_area


def rectangle_in_shape(vertices, sx1, sy1, sx2, sy2):
    # Returns True if all lines of the rectangle are within the
    # shape made by the vertices

    # No segment should intersect any side
    for i, (x1, y1) in enumerate(vertices):
        x2, y2 = vertices[(i + 1) % len(vertices)]

        # If perimeter segment is horizontal, make sure it doesn't stick
        # out of the middle of a vertical side of the rectangle into the
        # rectangle
        if y1 == y2:
            # (sx1, sy1), (sx1, sy2)
            # (sx2, sy1), (sx2, sy2)
            if sy1 < y1 < sy2 or sy2 < y1 < sy1:
                if (
                    # If they intersect, it's definitely bad
                    x1 < sx1 < x2 or 
                    x2 < sx1 < x1 or
                    x1 < sx2 < x2 or 
                    x2 < sx2 < x1
                ):  
                    return False

                if (
                    # If one endpoint touches, only bad if it's sticking
                    # into the rectangle
                    (x1 in (sx1, sx2) and (sx1 < x2 < sx2 or sx1 > x2 > sx2)) or
                    (x2 in (sx1, sx2) and (sx1 < x1 < sx2 or sx1 > x1 > sx2))
                ):
                    return False

        # If perimeter segment is vertical, make sure it doesn't stick
        # out of the middle of a horizontal side of the rectangle into the
        # rectangle
        elif x1 == x2:
            # (sx1, sy1), (sx2, sy1)
            # (sx1, sy2), (sx2, sy2)
            if sx1 < x1 < sx2 or sx2 < x1 < sx1:
                if (
                    # If they intersect, it's definitely bad
                    y1 < sy1 < y2 or 
                    y2 < sy1 < y1 or
                    y1 < sy2 < y2 or 
                    y2 < sy2 < y1
                ):
                    return False

                if (
                    # If one endpoint touches, only bad if it's sticking
                    # into the rectangle
                    (y1 in (sy1, sy2) and (sy1 < y2 < sy2 or sy1 > y2 > sy2)) or
                    (y2 in (sy1, sy2) and (sy1 < y1 < sy2 or sy1 > y1 > sy2))
                ):
                    return False

    return True


def is_inside_blocky_polygon(vertices, x, y):
    """
    Uses ray casting at a 45º angle to determine if the given point
    is within the polygon whose perimeter is defined by the given list of
    vertices (connected in order). Only works for polygons for which lines are
    straight on the x or y axis (hence casting at 45º never goes along an edge).
    """
    # Cast a ray at a -45º angle to the point. This means slope is -1 if
    # we want to be able to maintain (0, 0) coming from the top left.

    # Using y = mx + b -> y = -x + b, we can find b with y + x,
    intercept = y + x
    is_inside = False

    for i, (x1, y1) in enumerate(vertices):
        x2, y2 = vertices[(i + 1) % len(vertices)]

        # If the point is a vertex, it's inside
        if (x, y) in ((x1, y1), (x2, y2)):
            return True

        is_horizontal = None
        goes_through_end = False

        # If y's are equal, find the x at which the line defined
        # by this segment intersects the ray
        if y1 == y2:
            is_horizontal = True
            x_interception = intercept - y1
            if y > y1 or x_interception > x:
                continue
            elif x1 < x_interception < x2 or x2 < x_interception < x1:
                is_inside = not is_inside
            elif x_interception == x2:
                goes_through_end = True

        # If x's are equal, find the y at which the line defined
        # by this segment intersects the ray
        elif x1 == x2:
            is_horizontal = False
            y_interception = intercept - x1
            if x < x1 or y_interception < y:
                continue
            elif y1 < y_interception < y2 or y2 < y_interception < y1:
                is_inside = not is_inside
            elif y_interception == y2:
                goes_through_end = True
        else:
            raise('This is not a blocky polygon, or the vertices are not in order!')

        # If the intersection goes through the end of the segment, we need the
        # next point to determine if it's a cross into or out of the polygon or just
        # a glance on the perimeter. We only check the end so that we don't
        # double count as we step through all segments.
        if goes_through_end:
            x3, y3 = vertices[(i + 2) % len(vertices)]
            if is_horizontal:
                if (
                    # Cross if next point continues the straight line
                    y2 == y3 or
                    # Cross if coming from the left and next segment is going up
                    (x1 < x2 and y2 < y3) or
                    # Cross if coming from the right and next segment is going down
                    (x1 > x2 and y2 > y3)
                ):
                    is_inside = not is_inside
            else:
                if (
                    # Cross if next point continues the straight line
                    x2 == x3 or
                    # Cross if coming from the top and next segment is going to the left
                    (y1 > y2 and x2 > x3) or
                    # Cross if coming from the bottom and next segment is going right
                    (y1 < y2 and x2 < x3)
                ):
                    is_inside = not is_inside

    return is_inside


def part_2(lines):
    red_coords = []

    for line in lines:
        line = line.strip()
        a, b = line.split(',')
        (x, y) = int(a), -int(b) # We have to flip y to be consistent with 0, 0 being top left
        red_coords.append((x, y))

    max_area = 0
    num_vertices = len(red_coords)
    total_to_test = num_vertices * num_vertices
    tested = 0
    for x1, y1 in red_coords:
        for x2, y2 in red_coords:
            # Only measure if the other points are within the polygon
            if (
                is_inside_blocky_polygon(red_coords, x1, y2) and
                is_inside_blocky_polygon(red_coords, x2, y1) and
                rectangle_in_shape(red_coords, x1, y1, x2, y2)
            ):
                area = (abs(x1 - x2) + 1)*(abs(y1 - y2) + 1)
                max_area = max(area, max_area)

            # tested += 1
            # if tested % 10000 == 0:
            #     print('Testing %d/%d' % (tested, total_to_test))

    return max_area


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

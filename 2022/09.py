import os
import sys

class Coord(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction):
        match direction:
            case 'R':
                self.x += 1
            case 'L':
                self.x -= 1
            case 'U':
                self.y += 1
            case 'D':
                self.y -= 1

    def follow(self, coord):
        dx, dy = (coord.x - self.x, coord.y - self.y)

        if abs(dx) <= 1 and abs(dy) <= 1:
            # Adjacent, no movement
            return

        if dx > 0:
            self.x += 1
        elif dx < 0:
            self.x -= 1

        if dy > 0:
            self.y += 1
        elif dy < 0:
            self.y -= 1

    def to_tuple(self):
        return (self.x, self.y)
    

def solution(lines):
    visited = set()  # Set of visited coordinates (x, y)
    head_coord = Coord(0 , 0)
    tail_coord = Coord(0 , 0)
    visited.add(tail_coord.to_tuple())

    for line in lines:
        line = line.strip()
        direction, spaces = line.split(' ')
        spaces = int(spaces)

        for step in range(spaces):
            head_coord.move(direction)
            tail_coord.follow(head_coord)
            visited.add(tail_coord.to_tuple())

    return len(visited)
    

def solution2(lines):
    NUM_KNOTS = 10
    visited = set()  # Set of visited coordinates (x, y)
    coords = [  # Array of 10 knot coords
        Coord(0, 0) for coord in range(NUM_KNOTS)
    ]
    visited.add(coords[-1].to_tuple())

    for line in lines:
        line = line.strip()
        direction, spaces = line.split(' ')
        spaces = int(spaces)

        for step in range(spaces):
            for i, knot in enumerate(coords):
                if i == 0:
                    knot.move(direction)
                else:
                    knot.follow(coords[i - 1])
            visited.add(coords[-1].to_tuple())

    return len(visited)


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
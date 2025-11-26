"""
Part 1:
Part 2:
"""
import os

from util import run


class Robot(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction, wall_coords, other_moveables, dry=False):
        """
        Returns True if movement was successful, otherwise False.
        """
        moveable_map = {
            (m.x, m.y): m for m in other_moveables
        }
        moveable_map.update({
            (m.x + 1, m.y): m for m in other_moveables
        })


        if direction == '<':
            new_x = self.x - 1
            new_y = self.y

            if (new_x, new_y) in wall_coords:
                return False

            if (new_x, new_y) in moveable_map:
                if moveable_map[(new_x, new_y)].move(direction, wall_coords, other_moveables):
                    if not dry:
                        self.x = new_x
                        self.y = new_y
                    return True
                else:
                    return False

            if not dry:
                self.x = new_x
                self.y = new_y
            return True


        elif direction == '>':
            new_x = self.x + 1
            new_y = self.y

            if (new_x, new_y) in wall_coords:
                return False

            if (new_x, new_y) in moveable_map:
                if moveable_map[(new_x, new_y)].move(direction, wall_coords, other_moveables):
                    if not dry:
                        self.x = new_x
                        self.y = new_y
                    return True
                else:
                    return False

            if not dry:
                self.x = new_x
                self.y = new_y
            return True

        elif direction == '^':
            new_x = self.x
            new_y = self.y - 1

            if (new_x, new_y) in wall_coords:
                return False

            if (new_x, new_y) in moveable_map:
                if moveable_map[(new_x, new_y)].move(direction, wall_coords, other_moveables):
                    if not dry:
                        self.x = new_x
                        self.y = new_y
                    return True
                else:
                    return False

            if not dry:
                self.x = new_x
                self.y = new_y
            return True

        elif direction == 'v':
            new_x = self.x
            new_y = self.y + 1

            if (new_x, new_y) in wall_coords:
                return False

            if (new_x, new_y) in moveable_map:
                if moveable_map[(new_x, new_y)].move(direction, wall_coords, other_moveables):
                    if not dry:
                        self.x = new_x
                        self.y = new_y
                    return True
                else:
                    return False

            if not dry:
                self.x = new_x
                self.y = new_y
            return True

        return False


class WideMoveable(object):
    def __init__(self, id_, x, y):
        self.id = id_
        self.x = x  # Leftmost
        self.y = y

    def is_movable(self, direction, wall_coords, other_moveables):
        return self.move(direction, wall_coords, other_moveables, dry=True)

    def move(self, direction, wall_coords, other_moveables, dry=False):
        """
        Returns True if movement was successful, otherwise False.
        """
        moveable_map = {
            (m.x, m.y): m for m in other_moveables
        }
        moveable_map.update({
            (m.x + 1, m.y): m for m in other_moveables
        })

        if direction == '<':
            new_x = self.x - 1
            new_y = self.y

            if (new_x, new_y) in wall_coords:
                return False

            if (new_x, new_y) in moveable_map:
                if moveable_map[(new_x, new_y)].move(direction, wall_coords, other_moveables, dry=dry):
                    if not dry:
                        self.x = new_x
                        self.y = new_y
                    return True
                else:
                    return False

            if not dry:
                self.x = new_x
                self.y = new_y
            return True


        elif direction == '>':
            new_x = self.x + 1
            new_y = self.y

            if (new_x + 1, new_y) in wall_coords:
                return False

            if (new_x + 1, new_y) in moveable_map:
                if moveable_map[(new_x + 1, new_y)].move(direction, wall_coords, other_moveables, dry=dry):
                    if not dry:
                        self.x = new_x
                        self.y = new_y
                    return True
                else:
                    return False

            if not dry:
                self.x = new_x
                self.y = new_y
            return True

        elif direction == '^':
            new_x = self.x
            new_y = self.y - 1

            if (new_x, new_y) in wall_coords:
                return False
            elif (new_x + 1, new_y) in wall_coords:
                return False

            to_move = []
            if (new_x, new_y) in moveable_map:
                to_move.append(moveable_map[(new_x, new_y)])
            if (new_x + 1, new_y) in moveable_map:
                if not to_move or moveable_map[(new_x, new_y)].id != moveable_map[(new_x + 1, new_y)].id:
                    to_move.append(moveable_map[(new_x + 1, new_y)])

            if any(not m.is_movable(direction, wall_coords, other_moveables) for m in to_move):
                return False
            else:
                for moveable in to_move:
                    moveable.move(direction, wall_coords, other_moveables, dry=dry)
                if not dry:
                    self.x = new_x
                    self.y = new_y
                return True

            if not dry:
                self.x = new_x
                self.y = new_y
            return True

        elif direction == 'v':
            new_x = self.x
            new_y = self.y + 1

            if (new_x, new_y) in wall_coords:
                return False
            elif (new_x + 1, new_y) in wall_coords:
                return False

            to_move = []
            if (new_x, new_y) in moveable_map:
                to_move.append(moveable_map[(new_x, new_y)])
            if (new_x + 1, new_y) in moveable_map:
                if not to_move or moveable_map[(new_x, new_y)].id != moveable_map[(new_x + 1, new_y)].id:
                    to_move.append(moveable_map[(new_x + 1, new_y)])

            if any(not m.is_movable(direction, wall_coords, other_moveables) for m in to_move):
                return False
            else:
                for moveable in to_move:
                    moveable.move(direction, wall_coords, other_moveables, dry=dry)
                if not dry:
                    self.x = new_x
                    self.y = new_y
                return True

            if not dry:
                self.x = new_x
                self.y = new_y
            return True

        return False


class Moveable(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction, wall_coords, other_moveables):
        """
        Returns True if movement was successful, otherwise False.
        """
        moveable_map = {
            (m.x, m.y): m for m in other_moveables
        }

        if direction == '<':
            new_x = self.x - 1
            new_y = self.y
            if (new_x, new_y) in moveable_map:
                if moveable_map[(new_x, new_y)].move(direction, wall_coords, other_moveables):
                    self.x = new_x
                    self.y = new_y
                    return True
                else:
                    return False

            if (new_x, new_y) in wall_coords:
                return False
            else:
                self.x = new_x
                self.y = new_y
                return True


        elif direction == '>':
            new_x = self.x + 1
            new_y = self.y
            if (new_x, new_y) in moveable_map:
                if moveable_map[(new_x, new_y)].move(direction, wall_coords, other_moveables):
                    self.x = new_x
                    self.y = new_y
                    return True
                else:
                    return False

            if (new_x, new_y) in wall_coords:
                return False
            else:
                self.x = new_x
                self.y = new_y
                return True

        elif direction == '^':
            new_x = self.x
            new_y = self.y - 1
            if (new_x, new_y) in moveable_map:
                if moveable_map[(new_x, new_y)].move(direction, wall_coords, other_moveables):
                    self.x = new_x
                    self.y = new_y
                    return True
                else:
                    return False

            if (new_x, new_y) in wall_coords:
                return False
            else:
                self.x = new_x
                self.y = new_y
                return True

        elif direction == 'v':
            new_x = self.x
            new_y = self.y + 1
            if (new_x, new_y) in moveable_map:
                if moveable_map[(new_x, new_y)].move(direction, wall_coords, other_moveables):
                    self.x = new_x
                    self.y = new_y
                    return True
                else:
                    return False

            if (new_x, new_y) in wall_coords:
                return False
            else:
                self.x = new_x
                self.y = new_y
                return True

        return False


def part_1(lines):
    grid = []
    robot = None
    wall_coords = set()
    boxes = []
    grid_done = False
    movements = ''
    for y, row in enumerate(lines):
        row = row.strip()

        if grid_done:
            movements += row
            continue

        if not row:
            grid_done = True
            continue

        grid.append(row)
        for x, char in enumerate(row):
            if char == '@':
                robot = Moveable(x, y)
            elif char == 'O':
                boxes.append(Moveable(x, y))
            elif char == '#':
                wall_coords.add((x, y))

    for movement in movements:
        robot.move(movement, wall_coords, boxes)


    box_coords = {(b.x, b.y) for b in boxes}
    for y, _ in enumerate(grid):
        temp_str = ''
        for x, _ in enumerate(row):
            char = '.'
            if (x, y) in box_coords:
                char = 'O'
            elif (x, y) == (robot.x, robot.y):
                char = '@'
            elif (x, y) in wall_coords:
                char = '#'
            temp_str += char

    return sum(b.x + b.y * 100 for b in boxes)


def print_grid(grid, robot, wall_coords, boxes):
    lbox_coords = {(b.x, b.y) for b in boxes}
    rbox_coords = {(b.x + 1, b.y) for b in boxes}
    for y, row in enumerate(grid):
        temp_str = ''
        for x, _ in enumerate(row):
            char = '.'
            if (x, y) in lbox_coords:
                char = '['
            elif (x, y) in rbox_coords:
                char = ']'
            elif (x, y) == (robot.x, robot.y):
                char = '@'
            elif (x, y) in wall_coords:
                char = '#'
            temp_str += char


def part_2(lines):
    grid = []
    robot = None
    wall_coords = set()
    boxes = []
    grid_done = False
    movements = ''
    for y, row in enumerate(lines):
        row = row.strip()

        if grid_done:
            movements += row
            continue

        if not row:
            grid_done = True
            continue

        wide_row = ''
        for x, char in enumerate(row):
            if char == '@':
                wide_row += '@.'
            elif char == 'O':
                wide_row += '[]'
            elif char == '#':
                wide_row += '##'
            else:
                wide_row += '..'

        grid.append(wide_row)

        for x, char in enumerate(wide_row):
            if char == '@':
                robot = Robot(x, y)
            elif char == '[':
                boxes.append(WideMoveable(len(boxes), x, y))
            elif char == '#':
                wall_coords.add((x, y))


    for movement in movements:
        # print('Moving', movement)
        robot.move(movement, wall_coords, boxes)

    print_grid(grid, robot, wall_coords, boxes)

    return sum(b.x + b.y * 100 for b in boxes)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

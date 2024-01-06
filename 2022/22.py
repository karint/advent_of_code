import os

from collections import defaultdict
from util import run


class Direction:
    RIGHT = 'RIGHT'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    UP = 'UP'

ROTATIONS = {
    'R': {
        Direction.RIGHT: Direction.DOWN,
        Direction.DOWN: Direction.LEFT,
        Direction.LEFT: Direction.UP,
        Direction.UP: Direction.RIGHT,
    },
    'L': {
        Direction.RIGHT: Direction.UP,
        Direction.UP: Direction.LEFT,
        Direction.LEFT: Direction.DOWN,
        Direction.DOWN: Direction.RIGHT,
    }
}

# For each cube section, x range tuple and y range tuple
TEST_CUBE_SECTIONS = {
    1: [(8, 12), (0, 4)],
    2: [(0, 4), (4, 8)],
    3: [(4, 8), (4, 8)],
    4: [(8, 12), (4, 8)],
    5: [(8, 12), (8, 12)],
    6: [(12, 16), (8, 12)],
}

# Maps a section to direction of travel to tuple of next section and
# what direction you end up facing once you enter the section
TEST_SECTION_MAPPINGS = {
    1: {
        Direction.DOWN: (4, Direction.DOWN),
        Direction.LEFT: (3, Direction.DOWN),
        Direction.RIGHT: (6, Direction.LEFT),
        Direction.UP: (2, Direction.DOWN),
    },
    2: {
        Direction.DOWN: (5, Direction.UP),
        Direction.LEFT: (6, Direction.UP),
        Direction.RIGHT: (3, Direction.RIGHT),
        Direction.UP: (1, Direction.DOWN),
    },
    3: {
        Direction.DOWN: (5, Direction.RIGHT),
        Direction.LEFT: (2, Direction.LEFT),
        Direction.RIGHT: (4, Direction.RIGHT),
        Direction.UP: (1, Direction.RIGHT),
    },
    4: {
        Direction.DOWN: (5, Direction.DOWN),
        Direction.LEFT: (3, Direction.LEFT),
        Direction.RIGHT: (6, Direction.DOWN),
        Direction.UP: (1, Direction.UP),
    },
    5: {
        Direction.DOWN: (2, Direction.UP),
        Direction.LEFT: (3, Direction.UP),
        Direction.RIGHT: (6, Direction.RIGHT),
        Direction.UP: (4, Direction.UP),
    },
    6: {
        Direction.DOWN: (2, Direction.RIGHT),
        Direction.LEFT: (5, Direction.LEFT),
        Direction.RIGHT: (1, Direction.LEFT),
        Direction.UP: (4, Direction.LEFT),
    },
}

# For each cube section, x range tuple and y range tuple
CUBE_SECTIONS = {
    1: [(100, 150), (0, 50)],
    2: [(50, 100), (0, 50)],
    3: [(50, 100), (50, 100)],
    4: [(50, 100), (100, 150)],
    5: [(0, 50), (100, 150)],
    6: [(0, 50), (150, 200)],
}

# Maps a section to direction of travel to tuple of next section and
# what direction you end up facing once you enter the section
SECTION_MAPPINGS = {
    1: {
        Direction.DOWN: (3, Direction.LEFT),
        Direction.LEFT: (2, Direction.LEFT),
        Direction.RIGHT: (4, Direction.LEFT),
        Direction.UP: (6, Direction.UP),
    },
    2: {
        Direction.DOWN: (3, Direction.DOWN),
        Direction.LEFT: (5, Direction.RIGHT),
        Direction.RIGHT: (1, Direction.RIGHT),
        Direction.UP: (6, Direction.RIGHT),
    },
    3: {
        Direction.DOWN: (4, Direction.DOWN),
        Direction.LEFT: (5, Direction.DOWN),
        Direction.RIGHT: (1, Direction.UP),
        Direction.UP: (2, Direction.UP),
    },
    4: {
        Direction.DOWN: (6, Direction.LEFT),
        Direction.LEFT: (5, Direction.LEFT),
        Direction.RIGHT: (1, Direction.LEFT),
        Direction.UP: (3, Direction.UP),
    },
    5: {
        Direction.DOWN: (6, Direction.DOWN),
        Direction.LEFT: (2, Direction.RIGHT),
        Direction.RIGHT: (4, Direction.RIGHT),
        Direction.UP: (3, Direction.RIGHT),
    },
    6: {
        Direction.DOWN: (1, Direction.DOWN),
        Direction.LEFT: (2, Direction.DOWN),
        Direction.RIGHT: (4, Direction.UP),
        Direction.UP: (5, Direction.UP),
    },
}


class Solver:
    def __init__(self, grid, directions):
        self.grid = grid
        self.grid_width = len(self.grid[0])

        self.directions = directions

        self.facing = Direction.RIGHT
        self.curr_y = 0

        # Find first available x position
        for i, char in enumerate(self.grid[0]):
            if char == '.':
                self.curr_x = i
                break

        # self.init_wrap_map()

    def init_wrap_map(self):
        # Map of direction to off-grid coordinate to new coordinate. Will
        # map to self if rock is in the way.
        self.wrap_map = defaultdict(dict)
        for y, row in enumerate(self.grid):
            left_padding = self.grid_width - len(row.lstrip())
            right_padding = self.grid_width - len(row.rstrip())

            wrap_col = self.grid_width - right_padding - 1
            if self.grid[y][wrap_col] == '#':
                # Hit a wall, stay put
                self.wrap_map[Direction.LEFT][(y, left_padding - 1)] = (y, left_padding)
            else:
                self.wrap_map[Direction.LEFT][(y, left_padding - 1)] = (y, wrap_col)

            col = self.grid_width - right_padding
            wrap_col = left_padding
            if self.grid[y][wrap_col] == '#':
                # Hit a wall, stay put
                self.wrap_map[Direction.RIGHT][(y, col)] = (y, col - 1)
            else:
                self.wrap_map[Direction.RIGHT][(y, col)] = (y, wrap_col)

        for x in range(self.grid_width):
            top_padding = 0
            bottom_padding = 0
            is_still_top = True
            for row in self.grid:
                if row[x] == ' ':
                    if is_still_top:
                        top_padding += 1
                    else:
                        bottom_padding += 1
                else:
                    is_still_top = False

            wrap_row = len(self.grid) - bottom_padding - 1
            if self.grid[wrap_row][x] == '#':
                # Hit a wall, stay put
                self.wrap_map[Direction.UP][(top_padding - 1, x)] = (top_padding, x)
            else:
                self.wrap_map[Direction.UP][(top_padding - 1, x)] = (wrap_row, x)

            row = len(self.grid) - bottom_padding
            wrap_row = top_padding
            if self.grid[wrap_row][x] == '#':
                # Hit a wall, stay put
                self.wrap_map[Direction.DOWN][(row, x)] = (row - 1, x)
            else:
                self.wrap_map[Direction.DOWN][(row, x)] = (wrap_row, x)


    def solve(self, print_output=False):
        if print_output:
            self.print()
        for direction_or_steps in self.directions:
            if print_output:
                print(direction_or_steps)
            if isinstance(direction_or_steps, int):
                self.walk(direction_or_steps)
            else:
                self.rotate(direction_or_steps)
            if print_output:
                self.print()

    def walk(self, steps):
        dx_per_step, dy_per_step = 0, 0
        new_direction = self.facing

        for _ in range(steps):
            # self.print()
            # print()

            match self.facing:
                case Direction.RIGHT:
                    dx_per_step = 1
                    dy_per_step = 0
                case Direction.DOWN:
                    dx_per_step = 0
                    dy_per_step = 1
                case Direction.LEFT:
                    dx_per_step = -1
                    dy_per_step = 0
                case Direction.UP:
                    dx_per_step = 0
                    dy_per_step = -1

            new_x = self.curr_x + dx_per_step
            new_y = self.curr_y + dy_per_step
            
            if (
                new_x < 0 or
                new_y < 0 or
                new_x >= self.grid_width or
                new_y >= len(self.grid) or
                self.grid[new_y][new_x] == ' '
            ):
                # We stepped off the edge or into the abyss -- it's warping time!
                curr_section = None
                for section, [
                    (curr_min_x, curr_max_x),
                    (curr_min_y, curr_max_y)
                ] in CUBE_SECTIONS.items():
                    if (
                        self.curr_x >= curr_min_x and
                        self.curr_x < curr_max_x and
                        self.curr_y >= curr_min_y and
                        self.curr_y < curr_max_y
                    ):
                        curr_section = section
                        break

                (next_section, new_direction) = SECTION_MAPPINGS[curr_section][self.facing]
                [
                    (next_min_x, next_max_x),
                    (next_min_y, next_max_y)
                ] = CUBE_SECTIONS[next_section]

                if curr_section == next_section:
                    raise Exception('Stepped off an edge and stayed in the same section?')

                # Calculate new coordinate if we take this step
                old_direction = self.facing
                if new_direction == Direction.LEFT:
                    new_x = next_max_x - 1
                    if old_direction == Direction.UP:
                        new_y = next_min_y + curr_max_x - self.curr_x - 1
                    elif old_direction == Direction.DOWN:
                        new_y = next_min_y + self.curr_x - curr_min_x
                    elif old_direction == Direction.LEFT:
                        new_y = next_min_y + self.curr_y - curr_min_y
                    elif old_direction == Direction.RIGHT:
                        new_y = next_min_y + curr_max_y - self.curr_y - 1
                elif new_direction == Direction.RIGHT:
                    new_x = next_min_x
                    if old_direction == Direction.DOWN:
                        new_y = next_min_y + curr_max_x - self.curr_x - 1
                    elif old_direction == Direction.UP:
                        new_y = next_min_y + self.curr_x - curr_min_x
                    elif old_direction == Direction.RIGHT:
                        new_y = next_min_y + self.curr_y - curr_min_y
                    elif old_direction == Direction.LEFT:
                        new_y = next_min_y + curr_max_y - self.curr_y - 1
                elif new_direction == Direction.UP:
                    new_y = next_max_y - 1
                    if old_direction == Direction.LEFT:
                        new_x = next_min_x + curr_max_y - self.curr_y - 1
                    elif old_direction == Direction.RIGHT:
                        new_x = next_min_x + self.curr_y - curr_min_y
                    elif old_direction == Direction.UP:
                        new_x = next_min_x + self.curr_x - curr_min_x
                    elif old_direction == Direction.DOWN:
                        new_x = next_min_x + curr_max_x - self.curr_x - 1
                elif new_direction == Direction.DOWN:
                    new_y = next_min_y
                    if old_direction == Direction.RIGHT:
                        new_x = next_min_x + curr_max_y - self.curr_y - 1
                    elif old_direction == Direction.LEFT:
                        new_x = next_min_x + self.curr_y - curr_min_y
                    elif old_direction == Direction.DOWN:
                        new_x = next_min_x + self.curr_x - curr_min_x
                    elif old_direction == Direction.UP:
                        new_x = next_min_x + curr_max_x - self.curr_x - 1

            if self.grid[new_y][new_x] == '#':
                # We hit a wall, time to stop!
                return

            # Otherwise, just a normal step forward. Easy peasy.
            self.curr_x = new_x
            self.curr_y = new_y
            self.facing = new_direction

    def rotate(self, direction):
        self.facing = ROTATIONS[direction][self.facing]

    def get_password(self):
        '''
        Facing is 0 for right (>), 1 for down (v), 2 for left (<),
        and 3 for up (^). The final password is the sum of 1000
        times the row, 4 times the column, and the facing.
        '''
        match self.facing:
            case Direction.RIGHT:
                facing_value = 0
            case Direction.DOWN:
                facing_value = 1
            case Direction.LEFT:
                facing_value = 2
            case Direction.UP:
                facing_value = 3

        row = self.curr_y + 1
        column = self.curr_x + 1
        # print(row, column, facing_value)
        return 1000 * row + 4 * column + facing_value

    def get_facing_char(self):
        match self.facing:
            case Direction.RIGHT:
                return '>'
            case Direction.DOWN:
                return 'V'
            case Direction.LEFT:
                return '<'
            case Direction.UP:
                return '^'

    def print(self):
        for y, row in enumerate(self.grid):
            curr_str = ''
            for x, char in enumerate(row):
                if x == self.curr_x and y == self.curr_y:
                    curr_str += self.get_facing_char()
                    if char == ' ':
                        print(curr_str)
                        raise Exception('ERROR: In the middle of no where!')
                else:
                    curr_str += char
            print(curr_str)


def parse_direction(line):
    curr_str = ''
    directions = []
    for char in line:
        if char.isdigit():
            curr_str += char
        else:
            directions.append(int(curr_str))
            directions.append(char)
            curr_str = ''

    directions.append(int(curr_str))
    return directions


def part_1(lines):
    map_width = 0
    directions = None
    grid = []
    for i, line in enumerate(lines):
        line = line.rstrip()
        if not line:
            continue

        if i == len(lines) - 1:
            directions = parse_direction(line)
        else:
            if len(line) > map_width:
                map_width = len(line)
            grid.append(line)

    # Add right padding to prevent index errors
    for i, line in enumerate(grid):
        grid[i] = line.ljust(map_width, ' ')
        
    solver = Solver(grid, directions)
    solver.solve()
    return solver.get_password()
    

def part_2(lines):
    map_width = 0
    directions = None
    grid = []
    for i, line in enumerate(lines):
        line = line.rstrip()
        if not line:
            continue

        if i == len(lines) - 1:
            directions = parse_direction(line)
        else:
            if len(line) > map_width:
                map_width = len(line)
            grid.append(line)

    # Add right padding to prevent index errors
    for i, line in enumerate(grid):
        grid[i] = line.ljust(map_width, ' ')
        
    solver = Solver(grid, directions)
    solver.solve(print_output=False)
    return solver.get_password()


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

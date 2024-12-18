"""
Utility methods related to grids and traversing them.
"""

class Direction:
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'


OPPOSITE_DIRECTIONS = {
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
    Direction.UP: Direction.DOWN,
}


def get_cardinal_direction_coords(x, y, directions=None, grid=None, blocked=None):
    """
    If grid is provided, only returns directions
    within bounds.
    """
    all_directions = [
        (Direction.RIGHT, x + 1, y),
        (Direction.DOWN, x, y + 1),
        (Direction.LEFT, x - 1, y),
        (Direction.UP, x, y - 1),
    ]


    if directions is not None:
        all_directions = [
            (d, x, y) for (d, x, y) in all_directions if d in directions
        ]

    if blocked is not None:
        all_directions = [
            (d, x, y) for (d, x, y) in all_directions if (x, y) not in blocked
        ]

    if not grid:
        return all_directions

    return [
        (d, x, y) for (d, x, y) in all_directions if
        (x >= 0 and x < len(grid[0]) and y >= 0 and y < len(grid))
    ]


def get_adjacent_coords(x, y):
    """
    Given x and y, returns a set of tuples of the
    8 adjacent coordinates.
    """
    return {
        (x - 1, y - 1),
        (x - 1, y),
        (x - 1, y + 1),
        (x, y - 1),
        (x, y + 1),
        (x + 1, y - 1),
        (x + 1, y),
        (x + 1, y + 1),
    }


def get_manhattan_distance(coord_1, coord_2):
    dx = abs(coord_1[0] - coord_2[0])
    dy = abs(coord_1[1] - coord_2[1])
    return dx + dy


def rotate_45(grid):
    """
    Returns a grid representing the original grid rotated 45º clockwise.
    Only represents the content per row and does not preserve geometric integrity.
    Each row is a string, not a list.

    Example: rotate_45(['abc', 'def']) -> ['c', 'bf', 'ae', 'd']
    """
    width = len(grid[0])
    height = len(grid)

    diag_grid = []
    
    for i in range(height):
        length_of_row = i + 1
        diag_grid.append(''.join(
            grid[length_of_row - j - 1][j]
            for j in range(length_of_row)
        ))

    for i in range(height - 1):
        length_of_row = height - i - 1
        diag_grid.append(''.join(
            grid[height - (length_of_row - j - 1) - 1][width - j - 1]
            for j in reversed(range(length_of_row))
        ))

    return diag_grid


def rotate_90(grid):
    """
    Returns a grid of chars that is the original grid rotated 90º clockwise.
    Each row is a string, not a list.

    Example: rotate_90(['abc', 'def']) -> ['da', 'eb', 'fc']
    """
    width = len(grid[0])
    height = len(grid)

    return [
        ''.join(grid[height - i - 1][j] for i in range(height))
        for j in range(width)
    ]

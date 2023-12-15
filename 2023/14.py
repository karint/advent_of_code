"""
Part 1: Roll rocks north on a grid.
Part 2: Roll rocks north, east, south, and west in many cycles.
"""
import os

from util import run

TILTS_PER_CYCLE = 4


def tilt_and_rotate(grid):
    """
    Returns result of tilting grid up, then rotating clockwise.
    """
    shifted_grid = []
    for x in range(len(grid[0])):
        col = []
        ready_to_roll = []
        for y in range(len(grid)):
            cell = grid[y][x]
            match(cell):
                case '#':
                    col += ready_to_roll
                    ready_to_roll = []
                    col += '#'
                case 'O':
                    ready_to_roll.insert(0, cell)
                case '.':
                    ready_to_roll.append(cell)
        col += ready_to_roll
        col.reverse()
        shifted_grid.append(col)
    return shifted_grid


def part_1(lines):
    grid = tilt_and_rotate([line.strip() for line in lines])
    return sum(
        # Find distance from West, which is the new South
        sum(i + 1 if char == 'O' else 0 for i, char in enumerate(row))
        for row in grid
    )


def get_memo_key(grid):
    return ''.join([''.join(row) for row in grid])


def part_2(lines):
    MEMO = {}
    num_cycles = 1000000000
    grid = [line.strip() for line in lines]

    # Find the cycle that starts to repeat a pattern
    loop_starts = None
    loop_length = None
    for cycle in range(num_cycles):
        key = get_memo_key(grid)
        if key in MEMO:
            # We've been here before
            loop_starts = MEMO[key]
            loop_length = cycle - loop_starts
            break
        else:
            MEMO[key] = cycle

        for tilt in range(TILTS_PER_CYCLE):
            grid = tilt_and_rotate(grid)

    # Remove loops from remaining cycles
    loops_left = (num_cycles - loop_starts) % loop_length

    # Finish remaining cycles
    for cycle in range(loops_left):
        for tilt in range(TILTS_PER_CYCLE):
            grid = tilt_and_rotate(grid)

    # Find distance from South since we ended up still oriented North
    answer = 0
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == 'O':
                answer += len(grid) - y

    return answer


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)


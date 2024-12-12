"""
Start: 10:33pm ET

Part 1: 
Part 2:
"""
import os

from util import get_cardinal_direction_coords, run


def get_trailhead_score(starting_coords, trail_map):
    total_score = 0

    for starting_x, starting_y in starting_coords:
        trail_score = 0
        curr_height = 0
        curr_coords = set([(starting_x, starting_y)])
        dest_coords = set()
        while curr_height < 9:
            new_coords = []
            for curr_x, curr_y in curr_coords:
                adj_dir_coords = get_cardinal_direction_coords(
                    curr_x,
                    curr_y,
                    grid=trail_map,
                )
                for _, x, y in adj_dir_coords:
                    new_elevation = trail_map[y][x]
                    if new_elevation == curr_height + 1:
                        new_coords.append((x, y))
                        if new_elevation == 9:
                            dest_coords.add((x, y))
            curr_coords = new_coords
            curr_height += 1
        total_score += len(dest_coords)

        print(starting_x, starting_y, trail_score)
    return total_score


def get_trailhead_score_2(starting_coords, trail_map):
    total_score = 0

    for starting_x, starting_y in starting_coords:
        trail_score = 0
        curr_height = 0
        curr_coords = set([(starting_x, starting_y)])
        while curr_height < 9:
            new_coords = []
            for curr_x, curr_y in curr_coords:
                adj_dir_coords = get_cardinal_direction_coords(
                    curr_x,
                    curr_y,
                    grid=trail_map,
                )
                for _, x, y in adj_dir_coords:
                    new_elevation = trail_map[y][x]
                    if new_elevation == curr_height + 1:
                        new_coords.append((x, y))
                        if new_elevation == 9:
                            trail_score += 1
            curr_coords = new_coords
            curr_height += 1
        total_score += trail_score

        print(starting_x, starting_y, trail_score)
    return total_score


def part_1(lines):
    trailhead_coords = set()
    trail_map = []
    for y, line in enumerate(lines):
        line = line.strip()
        row = []
        for x, char in enumerate(line):
            if char == '0':
                trailhead_coords.add((x, y))
            row.append(int(char))
        trail_map.append(row)

    return get_trailhead_score(trailhead_coords, trail_map)


def part_2(lines):
    trailhead_coords = set()
    trail_map = []
    for y, line in enumerate(lines):
        line = line.strip()
        row = []
        for x, char in enumerate(line):
            if char == '0':
                trailhead_coords.add((x, y))
            row.append(int(char))
        trail_map.append(row)

    return get_trailhead_score_2(trailhead_coords, trail_map)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

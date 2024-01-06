import os

from util import run


def part_1(lines):
    all_cubes = set()
    for i, line in enumerate(lines):
        line = line.strip()
        x, y, z = map(int, line.split(','))
        all_cubes.add((x, y, z))

    num_surfaces = 0
    for x, y, z in all_cubes:
        if (x + 1, y, z) not in all_cubes:
            num_surfaces += 1
        if (x - 1, y, z) not in all_cubes:
            num_surfaces += 1
        if (x, y + 1, z) not in all_cubes:
            num_surfaces += 1
        if (x, y - 1, z) not in all_cubes:
            num_surfaces += 1
        if (x, y, z + 1) not in all_cubes:
            num_surfaces += 1
        if (x, y, z - 1) not in all_cubes:
            num_surfaces += 1

    return num_surfaces


def expand_air(all_lava_cubes, all_air_cubes, min_x, max_x, min_y, max_y, min_z, max_z):    
    while True:
        size_before = len(all_air_cubes)

        for (x, y, z) in all_air_cubes:
            new_set = set(all_air_cubes)
            if (x + 1, y, z) not in all_lava_cubes and x + 1 <= max_x:
                new_set.add((x + 1, y, z))
            if (x - 1, y, z) not in all_lava_cubes and x - 1 >= min_x:
                new_set.add((x - 1, y, z))
            if (x, y + 1, z) not in all_lava_cubes and y + 1 <= max_y:
                new_set.add((x, y + 1, z))
            if (x, y - 1, z) not in all_lava_cubes and y - 1 >= min_y:
                new_set.add((x, y - 1, z))
            if (x, y, z + 1) not in all_lava_cubes and z + 1 <= max_z:
                new_set.add((x, y, z + 1))
            if (x, y, z - 1) not in all_lava_cubes and z - 1 >= min_z:
                new_set.add((x, y, z - 1))
            all_air_cubes = new_set

        # Nothing was added -- done filling!
        if size_before == len(all_air_cubes):
            # print('num air cubes is', len(all_air_cubes))
            return all_air_cubes
    

def part_2(lines):
    all_lava_cubes = set()
    min_x, max_x, min_y, max_y, min_z, max_z = None, None, None, None, None, None
    for i, line in enumerate(lines):
        line = line.strip()
        x, y, z = map(int, line.split(','))

        if min_x is None:
            min_x = x
            max_x = x
        else:
            if min_x > x:
                min_x = x
            if max_x < x:
                max_x = x

        if min_y is None:
            min_y = y
            max_y = y
        else:
            if min_y > y:
                min_y = y
            if max_y < y:
                max_y = y

        if min_z is None:
            min_z = z
            max_z = z
        else:
            if min_z > z:
                min_z = z
            if max_z < z:
                max_z = z

        all_lava_cubes.add((x, y, z))

    # Expand box to one beyond the min and max lava cubes
    min_x -= 1
    max_x += 1
    min_y -= 1
    max_y += 1
    min_z -= 1
    max_z += 1

    # print(min_x, max_x)
    # print(min_y, max_y)
    # print(min_z, max_z)

    # Fill the box with air and find surface area of it
    all_air_cubes = set([(min_x, min_y, min_z)])
    all_air_cubes = expand_air(
        all_lava_cubes,
        all_air_cubes,
        min_x,
        max_x,
        min_y,
        max_y,
        min_z,
        max_z
    )

    # Get surface area of the air
    num_surfaces = 0
    for x, y, z in all_air_cubes:
        if (x + 1, y, z) not in all_air_cubes:
            num_surfaces += 1
        if (x - 1, y, z) not in all_air_cubes:
            num_surfaces += 1
        if (x, y + 1, z) not in all_air_cubes:
            num_surfaces += 1
        if (x, y - 1, z) not in all_air_cubes:
            num_surfaces += 1
        if (x, y, z + 1) not in all_air_cubes:
            num_surfaces += 1
        if (x, y, z - 1) not in all_air_cubes:
            num_surfaces += 1

    # Subtract outside of box surface area
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    depth = max_z - min_z + 1

    num_surfaces -= 2 * (width * height + height * depth + width * depth)
    return num_surfaces


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

"""
Part 1:
Part 2:
"""
import os

from util import run


def part_1(lines):
    # Make initial string
    disk_map = lines[0].strip()
    blocks = []
    index = 0
    curr_id = 0
    for i, num in enumerate(disk_map):
        if i % 2 == 0:
            blocks += [curr_id] * int(num)
            curr_id += 1
        else:
            blocks += ['.'] * int(num)
    print(''.join(map(str, blocks)))

    # Move files
    final_map = []
    take_from_index = len(blocks) - 1
    for i, char in enumerate(blocks):
        if take_from_index < i:
            break
        if char == '.':
            final_map.append(blocks[take_from_index])
            take_from_index -= 1
            while blocks[take_from_index] == '.':
                take_from_index -= 1
        else:
            final_map.append(char)

    print(''.join(map(str, final_map)))

    return sum(
        index * int(num) for index, num in enumerate(final_map)
    )


def part_2(lines):
    # Make initial string
    disk_map = lines[0].strip()
    blocks = []
    index = 0
    curr_id = 0
    blocks_by_size = []
    id_to_index = {}
    for i, num in enumerate(disk_map):
        if i % 2 == 0:
            blocks_by_size.append((curr_id, int(num)))
            id_to_index[curr_id] = len(blocks)
            blocks.append((curr_id, int(num)))
            curr_id += 1
        else:
            blocks.append(('.', int(num)))

    blocks_by_size = sorted(blocks_by_size, reverse=True)

    # Move files
    final_map = [b for b in blocks]

    for id_, size in blocks_by_size:
        for i, (char, length) in enumerate(final_map):
            if char == id_:
                break
            if char == '.':
                if length >= size:
                    final_map[i] = (id_, size)
                    if length > size:
                        final_map.insert(i + 1, ('.', length - size))
                        # Shift all indices by 1 that come after this
                        for id_to_shift, index in id_to_index.items():
                            if index > i:
                                id_to_index[id_to_shift] = index + 1
                    index_to_delete = id_to_index[id_]
                    char_to_delete, delete_length = final_map[index_to_delete]
                    final_map[index_to_delete] = ('.', delete_length)
                    break


    final_str = ''.join(str(char) * length for char, length in final_map).rstrip('.')
    print(final_str)

    # Wrong: 85630153184

    checksum = 0
    curr_index = 0
    for (char, length) in final_map:
        if char == '.':
            curr_index += length
            continue
        for i in range(length):
            checksum += curr_index * int(char)
            curr_index += 1
    return checksum


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

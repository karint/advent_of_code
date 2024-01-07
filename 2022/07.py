import os

from collections import defaultdict
from util import run

SIZE_MIN = 100000

def part_1(lines):
    directory_sizes = defaultdict(int)
    directory_children = defaultdict(set)

    dir_list = []
    in_directory = False
    for line in lines:
        line = line.strip()
        if line.startswith('$ cd ..'):
            dir_list.pop()
        elif line.startswith('$ cd '):
            curr_dir = '|'.join((dir_list + [line.split(' ')[2]]))
            if dir_list:
                directory_children[dir_list[-1]].add(curr_dir)
            dir_list.append(curr_dir)
        elif line.startswith('$ ls'):
            continue
        elif line.startswith('dir '):
            child_dir = '|'.join((dir_list + [line.split(' ')[1]]))
            directory_children[dir_list[-1]].add(child_dir)
        elif line:
            size = int(line.split(' ')[0])
            directory_sizes[dir_list[-1]] += size

    # Add children sizes to parents
    def get_size(directory):
        size = directory_sizes[directory]
        if directory in directory_children:
            for child in directory_children[directory]:
                size += get_size(child)
        return size
    
    total = 0
    for directory in set(directory_sizes.keys()) | set(directory_children.keys()):
        size = get_size(directory)
        if size <= SIZE_MIN:
            total += size
    return total
    
TOTAL_SPACE = 70000000
UNUSED_NEEDED = 30000000

def part_2(lines):
    directory_sizes = defaultdict(int)
    directory_children = defaultdict(set)
    
    dir_list = []
    in_directory = False
    for line in lines:
        line = line.strip()
        if line.startswith('$ cd ..'):
            dir_list.pop()
        elif line.startswith('$ cd '):
            curr_dir = '|'.join((dir_list + [line.split(' ')[2]]))
            if dir_list:
                directory_children[dir_list[-1]].add(curr_dir)
            dir_list.append(curr_dir)
        elif line.startswith('$ ls'):
            continue
        elif line.startswith('dir '):
            child_dir = '|'.join((dir_list + [line.split(' ')[1]]))
            directory_children[dir_list[-1]].add(child_dir)
        elif line:
            size = int(line.split(' ')[0])
            directory_sizes[dir_list[-1]] += size

    # Add children sizes to parents
    def get_size(directory):
        size = directory_sizes[directory]
        if directory in directory_children:
            for child in directory_children[directory]:
                size += get_size(child)
        return size
    
    needed_to_free = UNUSED_NEEDED + get_size('/') - TOTAL_SPACE
    all_directories = set(directory_sizes.keys()) | set(directory_children.keys())
    smallest = (None, 0)
    for directory in all_directories:
        size = get_size(directory)
        if size >= needed_to_free and (smallest[0] is None or size < smallest[1]):
            smallest = (directory, size)
    return smallest[1]


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

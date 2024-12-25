"""
Part 1:
Part 2:
"""
import os

from util import run


def part_1(lines):
    patterns = lines[0].strip().split(', ')
    designs = []

    for line in lines:
        line = line.strip()
        if ',' in line or not line:
            continue
        designs.append(line)

    possible = 0
    for design in designs:
        sequences = {}  # sequence so far: index in design
        done = False

        # Seed first sequences
        for pattern in patterns:
            if pattern == design:
                done = True
                break

            elif design.startswith(pattern):
                sequences[pattern] = len(pattern)
        while sequences and not done:
            new_sequences = {}
            for so_far, index in sequences.items():
                if done:
                    break
                remaining = design[index:]
                for pattern in patterns:
                    if remaining == pattern:
                        done = True
                        break

                    if remaining.startswith(pattern):
                        new_sequences[so_far + pattern] = index + len(pattern)

            sequences = new_sequences

        if done:
            possible += 1

    return possible


def part_2(lines):
    patterns = lines[0].strip().split(', ')
    designs = []

    for line in lines:
        line = line.strip()
        if ',' in line or not line:
            continue
        designs.append(line)

    total = 0
    for design in designs:
        found = False
        done_sequences = 0
        sequences = {}  # sequence so far: [sequences up to this point]

        # Seed first sequences
        for pattern in patterns:
            if pattern == design:
                done_sequences += 1

            elif design.startswith(pattern):
                sequences[pattern] = 1

        while sequences:
            new_sequences = {}
            for so_far, num_combos in sequences.items():
                remaining = design[len(so_far):]
                for pattern in patterns:
                    if remaining == pattern:
                        done_sequences += num_combos

                    elif remaining.startswith(pattern):
                        new_prog_point = so_far + pattern
                        if new_prog_point not in new_sequences:
                            new_sequences[new_prog_point] = num_combos
                        else:
                            new_sequences[new_prog_point] += num_combos

            sequences = new_sequences

        total += done_sequences

    return total



if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

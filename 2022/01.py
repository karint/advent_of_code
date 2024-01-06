import os

from util import run


def part_1(lines):
	elf_totals = []
	current_elf = 0
	for line in lines:
		line = line.strip()
		if line == "":
			elf_totals.append(current_elf)
			current_elf = 0
		else:
			current_elf += int(line)

	elf_totals.sort(reverse=True)
	return elf_totals[0] + elf_totals[1] + elf_totals[2]


def part_2(lines):
	return part_1(lines)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

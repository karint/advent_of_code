if __name__ == "__main__":
	with open("input.txt", "r") as file:
		lines = file.readlines()

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
	print(elf_totals[0] + elf_totals[1] + elf_totals[2])

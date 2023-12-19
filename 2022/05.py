DAY = 5
IS_TEST = False

if __name__ == '__main__':
	with open('%s%s.txt' % (DAY, '_test' if IS_TEST else ''), 'r') as file:
		lines = file.readlines()

	diagram_done = False 
	num_stacks = int((len(lines[0]) + 1)/4)

	# Front of array is top of stack
	stacks = {
		(i + 1): [] for i in range(num_stacks)
	}
	for line in lines:
		if '[' in line:
			cursor = 0
			for index in range(num_stacks):
				box = line[cursor:cursor + 3].replace('[', '').replace(']', '').strip()
				if box:
					stacks[index + 1].append(box)
				cursor += 4
			continue

		if 'move' not in line:
			continue

		line = line.strip()
		values = tuple(
			line
			.replace('move ', '')
			.replace(' from ', ',')
			.replace(' to ', ',')
			.split(',')
		)
		num_boxes, from_stack, to_stack = int(values[0]), int(values[1]), int(values[2])

		for i in range(num_boxes):
			box = stacks[from_stack].pop(0)
			stacks[to_stack].insert(0, box)

	final_string = ''
	for _, boxes in stacks.items():
		if boxes:
			final_string += boxes[0]

	print(final_string)

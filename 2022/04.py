DAY = 4
IS_TEST = True

if __name__ == '__main__':
	with open('%s%s.txt' % (DAY, '_test' if IS_TEST else ''), 'r') as file:
		lines = file.readlines()

	count = 0
	for line in lines:
		line = line.strip()
		first, second = line.split(',')
		first_tuple = [int(x) for x in first.split('-')]
		second_tuple = [int(x) for x in second.split('-')]
		if first_tuple[0] <= second_tuple[0] and first_tuple[1] >= second_tuple[1]:
			count += 1
		elif first_tuple[0] >= second_tuple[0] and first_tuple[1] <= second_tuple[1]:
			count += 1

	print(count)

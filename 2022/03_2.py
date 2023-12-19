DAY = 3
IS_TEST = False

ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
POINTS = {
	letter: index + 1 for index, letter in enumerate(ALPHABET)
}

if __name__ == '__main__':
	with open('%s%s.txt' % (DAY, '_test' if IS_TEST else ''), 'r') as file:
		lines = file.readlines()

	points = 0
	curr_set = set()
	count = 0

	for line in lines:
		line = line.strip()
		if not curr_set:
			curr_set = set(line)
		else:
			curr_set &= set(line)
		
		count += 1
		if count == 3:
			common = curr_set.pop()
			points += POINTS[common]
			count = 0


	print(points)

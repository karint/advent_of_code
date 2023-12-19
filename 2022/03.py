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
	for line in lines:
		line = line.strip()
		size = int(len(line)/2)
		first = set(line[:size])
		second = set(line[size:])
		common = first.intersection(second).pop()
		print(POINTS[common])
		points += POINTS[common]

	print(points)

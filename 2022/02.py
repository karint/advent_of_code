import os

from util import run

ROCK = 1  # A, X
PAPER = 2  # B, Y
SCISSORS = 3  # C, Z

LOSS = 0 # X
DRAW = 3 # Y
WIN = 6 # Z

MAPPING = {
	'X': LOSS,
	'Y': DRAW,
	'Z': WIN,
}

POINT_MAP = {
	'A': 1,
	'B': 2,
	'C': 3,
}

LOSS_COMBOS = { # if you play the key and opponent plays the value
	'A': 'C',
	'B': 'A',
	'C': 'B',
}
WIN_COMBOS = {
	you: opponent for opponent, you in LOSS_COMBOS.items()
}

def part_1(lines):
	points = 0
	for line in lines:
		opponent, result = line.strip().split(' ')

		points += MAPPING[result]

		if result == 'X':
			you = LOSS_COMBOS[opponent]
		elif result == 'Y':
			you = opponent
		else:
			you = WIN_COMBOS[opponent]

		points += POINT_MAP[you]

	return points


def part_2(lines):
	return part_1(lines)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

import os

from util import run

EQUIVALENT_MAPPING = {
	'X': 'A',
	'Y': 'B',
	'Z': 'C',
}

LOSS = 0 # X
DRAW = 3 # Y
WIN = 6 # Z

SCORE_MAPPING = {
	'X': LOSS,
	'Y': DRAW,
	'Z': WIN,
}

POINT_MAP = {
	'A': 1,
	'B': 2,
	'C': 3,
}

LOSS_COMBOS = { # if your opponent plays the key and you play the value
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
		opponent, you = line.strip().split(' ')
		you = EQUIVALENT_MAPPING[you]
		points += POINT_MAP[you]
		if (opponent, you) in LOSS_COMBOS.items():
			points += LOSS
		elif (opponent, you) in WIN_COMBOS.items():
			points += WIN
		else:
			points += DRAW

	return points


def part_2(lines):
	points = 0
	for line in lines:
		opponent, result = line.strip().split(' ')

		points += SCORE_MAPPING[result]

		if result == 'X':
			you = LOSS_COMBOS[opponent]
		elif result == 'Y':
			you = opponent
		else:
			you = WIN_COMBOS[opponent]

		points += POINT_MAP[you]

	return points


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

import os

from util import run


POWER = 5

DIGIT_MAPPING = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2,
}
SNAFU_VALUE_MAPPING = {
    v: k for k,v in DIGIT_MAPPING.items()
}

MULTIPLIERS = []


def convert_to_decimal(snafu):
    reverse_str = reversed(snafu)

    decimal = 0
    for i, char in enumerate(reverse_str):
        decimal += MULTIPLIERS[i] * DIGIT_MAPPING[char]

    return decimal


def convert_to_snafu(decimal):
    multipliers = list(MULTIPLIERS)
    while decimal > multipliers[-1]:
        new_multipliers = list(multipliers)
        new_multipliers.append(POWER**(len(multipliers)))
        multipliers = new_multipliers
    multipliers.reverse()

    remainder = decimal
    string_so_far = ''
    for multiplier in multipliers:
        candidates = {
            symbol: num * multiplier
            for num, symbol in SNAFU_VALUE_MAPPING.items()
        }

        min_diff = None
        winning_candidate = None
        winning_value = None
        for symbol, value in candidates.items():
            # Which candidate is closest to the remainder?
            diff = abs(remainder - value)
            if min_diff is None or diff < min_diff:
                min_diff = diff
                winning_candidate = symbol
                winning_value = value

        string_so_far += winning_candidate
        remainder -= winning_value

    return string_so_far.lstrip('0')


def part_1(lines):
    max_len = 0
    snafu_numbers = []

    for line in lines:
        line = line.strip()
        if len(line) > max_len:
            max_len = len(line)
        snafu_numbers.append(line)

    start = 1
    for i in range(max_len):
        MULTIPLIERS.append(POWER**i)

    decimal_sum = 0
    for snafu in snafu_numbers:
        decimal = convert_to_decimal(snafu)
        # print(snafu,' ->', decimal, '->', convert_to_snafu(decimal))
        decimal_sum += decimal

    return convert_to_snafu(decimal_sum)


def part_2(lines):
    return None


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

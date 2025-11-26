"""
Part 1: 
Part 2:
"""
import os

from collections import defaultdict
from util import run


def get_next_secret(secret):
    """
    Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number. Finally, prune the secret number.
    Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer. Then, mix this result into the secret number. Finally, prune the secret number.
    Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number. Finally, prune the secret number.
    """
    a = secret * 64
    secret = mix(secret, a)
    secret = prune(secret)

    b = secret // 32
    secret = mix(secret, b)
    secret = prune(secret)

    c = secret * 2048
    secret = mix(secret, c)
    secret = prune(secret)

    return secret


def mix(secret, num):
    """
    To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number. Then, the secret number becomes the result of that operation. (If the secret number is 42 and you were to mix 15 into the secret number, the secret number would become 37.)
    """
    return secret ^ num


def prune(secret):
    """
    To prune the secret number, calculate the value of the secret number modulo 16777216. Then, the secret number becomes the result of that operation. (If the secret number is 100000000 and you were to prune the secret number, the secret number would become 16113920.)
    """
    return secret % 16777216


def get_price(number):
    return int(str(number)[-1])


def part_1(lines):
    answer = 0
    for line in lines:
        line = line.strip()
        secret = int(line)
        for i in range(2000):
            secret = get_next_secret(int(secret))
        # print(line, secret)
        answer += secret
        
    return answer

def get_searchable_string(sequence):
    string = ''
    for num in sequence:
        if num >= 0:
            string += "+" + str(num)
        if num < 0:
            string += str(num)
    return string


def part_2(lines):
    possible_sequences = set()  # all tuples of 4 deltas that occur
    num_changes = 2000
    price_lists = []  # list of lists of prices; each item is a merchant
    delta_lists = []  # corresponding deltas to price lists
    for line in lines:
        delta = 'N/A'
        price_list = []
        delta_list = []
        line = line.strip()
        secret = int(line)
        for i in range(num_changes):
            price = get_price(secret)
            price_list.append(price)
            if i > 0:
                delta = price - price_list[i - 1]
                delta_list.append(delta)
            secret = get_next_secret(int(secret))

        price = get_price(secret)
        price_list.append(price)
        price_lists.append(price_list)

        delta_list.append(price - price_list[num_changes - 1])
        delta_lists.append(delta_list)

    sequence_to_delta_list_index = defaultdict(list)
    for j, delta_list in enumerate(delta_lists):
        for i in range(len(delta_list) - 3):
            sequence = (
                delta_list[i],
                delta_list[i + 1],
                delta_list[i + 2],
                delta_list[i + 3]
            )
            possible_sequences.add(sequence)
            sequence_to_delta_list_index[sequence].append((
                j, i, price_lists[j][i + 4]
            ))

    # Find best sequence
    most_bananas = None
    for possible_sequence in possible_sequences:
        num_bananas = 0
        merchants = set()
        for (j, _, price) in sequence_to_delta_list_index[possible_sequence]:
            if j not in merchants:
                num_bananas += price
                merchants.add(j)
        if most_bananas is None or num_bananas > most_bananas:
            most_bananas = num_bananas

    return most_bananas


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

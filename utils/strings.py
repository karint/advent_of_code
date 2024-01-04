"""
Utility methods related to strings and string manipulation.
"""

import re

from termcolor import colored

ALPHABET_LOWER = 'abcdefghijklmnopqrstuvwxyz'
ALPHABET_UPPER = ALPHABET_LOWER.upper()
TERM_COLORS = [
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'light_red',
    'light_green',
    'light_yellow',
    'light_blue',
    'light_magenta',
    'light_cyan',
]


def find_digits(line, cast_to=int):
    return list(map(cast_to, re.findall('(-?\d+)', line.strip())))


def color_string(string, color):
    return colored(string, color)

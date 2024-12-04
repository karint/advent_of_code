"""
File used to test and confirm that all answers are still correct.
Useful when refactoring utils that could impact multiple files.
"""
from util import test_all


CORRECT_ANSWERS = [
    ('01', 2970687, 23963899),
    ('02', 321, 386),
    ('03', 175015740, 112272912),
    ('04', 2639, 2005),
]


if __name__ == '__main__':
    test_all(CORRECT_ANSWERS)

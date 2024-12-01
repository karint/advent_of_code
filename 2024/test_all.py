"""
File used to test and confirm that all answers are still correct.
Useful when refactoring utils that could impact multiple files.
"""
from util import test_all


CORRECT_ANSWERS = [
    ('01', 2970687, 23963899),
]


if __name__ == '__main__':
    test_all(CORRECT_ANSWERS)

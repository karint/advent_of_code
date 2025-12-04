"""
File used to test and confirm that all answers are still correct.
Useful when refactoring utils that could impact multiple files.
"""
from util import test_all


CORRECT_ANSWERS = [
    ('01', 1023, 5899),
    ('02', 32976912643, 54446379122),
    ('03', 17193, 171297349921310),
    ('04', 1464, 8409),
]


if __name__ == '__main__':
    test_all(CORRECT_ANSWERS)

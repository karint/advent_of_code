"""
File used to test and confirm that all answers are still correct.
Useful when refactoring utils that could impact multiple files.
"""
import importlib
import time

from util import run


CORRECT_ANSWERS = [
    ('01', 56397, 55701),
    ('02', 2204, 71036),
    ('03', 532428, 84051670),
    ('04', 20829, 12648035),
    ('05', 600279879, 20191102),
    ('06', 2065338, 34934171),
    ('07', 251106089, 249620106),
    ('08', 16271, 14265111103729),
    ('09', 1789635132, 913),
    ('10', 6968, 413),
    ('11', 10154062, 553083047914),
    ('12', 6871, 2043098029844),
    ('13', 31265, 39359),
    ('14', 108792, 99118),
    ('15', 518107, 303404),
    ('16', 6994, 7488),
    ('17', 1001, 1197),
]

if __name__ == '__main__':
    for day, part_1_solution, part_2_solution in CORRECT_ANSWERS:
        solution_file = importlib.import_module(day)
        with open('%s.txt' % day, 'r') as file:
            print('Day %s:' % day)
            lines = file.readlines()

            start = time.perf_counter()
            part_1_output = solution_file.part_1(lines)
            duration = time.perf_counter() - start
            print('\tPart 1: %s (%.4fms)' % (
                'Pass' if part_1_output == part_1_solution
                else  'Fail: %s should be %s' % (part_1_output, part_1_solution),
                duration * 1000
            ))

            start = time.perf_counter()
            part_2_output = solution_file.part_2(lines)
            duration = time.perf_counter() - start
            print('\tPart 2: %s (%.4fms)' % (
                'Pass' if part_2_output == part_2_solution
                else 'Fail: %s should be %s' % (part_2_output, part_2_solution),
                duration * 1000
            ))

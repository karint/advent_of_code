"""
File used to test and confirm that all answers are still correct.
Useful when refactoring utils that could impact multiple files.
"""
import importlib
import sys
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
    ('18', 40745, 90111113594927),
    ('19', 472630, 116738260946855),
    ('20', 836127690, 240914003753369),
    ('21', 3637, 601113643448699),
    ('22', 475, 79144),
    ('23', 2294, 6418),
    ('24', 12015, 1016365642179116),
    ('25', 612945, None),
]

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2:
        specific_day = args[1]
    else:
        specific_day = None

    for day, part_1_solution, part_2_solution in CORRECT_ANSWERS:
        if specific_day is not None and specific_day != day:
            continue
        solution_file = importlib.import_module(day)
        with open('%s.txt' % day, 'r') as file:
            print('Day %s:' % day)
            lines = file.readlines()

            start = time.perf_counter()
            part_1_output = solution_file.part_1(lines)
            duration = time.perf_counter() - start
            print('\tPart 1: %s (%.6fs)' % (
                'Pass' if part_1_output == part_1_solution
                else  'Fail: %s should be %s' % (part_1_output, part_1_solution),
                duration
            ))

            start = time.perf_counter()
            part_2_output = solution_file.part_2(lines)
            duration = time.perf_counter() - start
            print('\tPart 2: %s (%.6fs)' % (
                'Pass' if part_2_output == part_2_solution
                else 'Fail: %s should be %s' % (part_2_output, part_2_solution),
                duration
            ))

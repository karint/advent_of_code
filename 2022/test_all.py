"""
File used to test and confirm that all answers are still correct.
Useful when refactoring utils that could impact multiple files.
"""
from util import test_all


CORRECT_ANSWERS = [
    ('01', 69626, 206780),
    ('02', 13675, 14184),
    ('03', 7821, 2752),
    ('04', 511, 821),
    ('05', 'HBTMTBSDC', 'PQTJRSHWS'),
    ('06', 1100, 2421),
    ('07', 1077191, 5649896),
    ('08', 1776, 234416),
    ('09', 5907, 2303),
    ('10', 11960, 'EJCFPGLH'),
    ('11', 120756, 39109444654),
    ('12', 528, 522),
    ('13', 5717, 25935),
    ('14', 665,  25434),
    ('15', 5403290, 10291582906626),
    ('16', 1906, 2548),
    ('17', 3188, 1591977077342),
    ('18', 3448, 2052),
    ('19', 1981, 10962),
    ('20', 4267, 6871725358451),
    ('21', 169525884255464, 3247317268284),
    ('22', 77318, 126017),
    ('23', 4138, 1010),
    ('24', 295, 851),
    ('25', '122-12==0-01=00-0=02', None),
]


if __name__ == '__main__':
    test_all(CORRECT_ANSWERS)

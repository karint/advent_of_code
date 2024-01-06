import os

from util import run


BREAKPOINTS = set([20, 60, 100, 140, 180, 220])
SCREEN_ROWS = set([40, 80, 120, 160, 200, 240])


def part_1(lines):
    signal_sum = 0
    register = 1
    cycle = 1
    for line in lines:
        instruction = line.strip()

        if instruction == 'noop':  # 1 cycle to complete
            cycle += 1
        else:  # addx; 2 cycles to complete
            _, value = instruction.split(' ')
            cycle += 1

            if cycle in BREAKPOINTS:
                signal_sum += cycle * register

            cycle += 1
            register += int(value)

        if cycle in BREAKPOINTS:
            signal_sum += cycle * register

    min_cycle = max(BREAKPOINTS)
    if cycle < min_cycle:
        signal_sum += min_cycle * register
        
    return signal_sum
    

class Solution(object):
    def __init__(self):
        self.sprite_pos = 1
        self.cycle = 0
        self.curr_line = ''
        self.cursor_pos = -1

    def proceed(self):
        self.cycle += 1
        self.cursor_pos += 1
        sprite_visible = abs(self.cursor_pos - self.sprite_pos) <= 1
        self.curr_line += '#' if sprite_visible else '.'

        if self.cycle in SCREEN_ROWS:
            # print(self.curr_line)
            self.curr_line = ''
            self.cursor_pos = -1

    def solve(self, lines):
        for line in lines:
            instruction = line.strip()
            self.proceed()  # Does same initial step whether noop or add

            if instruction != 'noop':  # If add, do an additional cycle
                _, value = instruction.split(' ')
                self.proceed()
                self.sprite_pos += int(value)
            
        return 'EJCFPGLH'  # Read manually in terminal


def part_2(lines):
    return Solution().solve(lines)


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

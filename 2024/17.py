"""
Part 1:
Part 2:
"""
import math
import os

from util import run


def process(a, b, c, program_str, match=None):
    program = program_str.split(',')
    outputs = []
    pointer_index = 0

    if match:
        target_outputs = list(match)

    while True:
        try:
            opcode = int(program[pointer_index])
            operand = int(program[pointer_index + 1])
        except IndexError:
            break

        comboed_values = {
            4: a,
            5: b,
            6: c,
        }

        match opcode:
            case 0:  # The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.
                assert(operand != 7)
                result = int(a // math.pow(2, comboed_values.get(operand, operand)))
                a = result
            case 1:  # bitwise XOR of register B and the instruction's literal operand, then stores the result in register B
                result = b ^ operand
                b = result
            case 2:  # calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register
                assert(operand != 7)
                result = comboed_values.get(operand, operand) % 8
                b = result
            case 3:  # nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
                if a == 0:
                    pointer_index += 2
                else:
                    pointer_index = operand
                continue
            case 4:  # calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
                result = b ^ c
                b = result
            case 5:  # calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)
                assert(operand != 7)
                result = comboed_values.get(operand, operand) % 8
                if match and result != target_outputs[len(outputs)]:
                    return False
                outputs.append(result)
            case 6:  # works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)
                result = int(a // math.pow(2, comboed_values.get(operand, operand)))
                b = result
            case 7:  # works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)
                result = int(a // math.pow(2, comboed_values.get(operand, operand)))
                c = result

        pointer_index += 2

    # print('Registers:', a, b ,c)
    return ','.join(map(str, map(int, outputs)))


def part_1(lines):
    a = int(lines[0].strip().split(': ')[1])
    b = int(lines[1].strip().split(': ')[1])
    c = int(lines[2].strip().split(': ')[1])
    program_str = lines[4].strip().split(': ')[1]

    # Tests
    # assert(process(729, 0, 0, '0,1,5,4,3,0') == '4,6,3,5,6,3,5,2,1,0')
    # assert(process(10, 0, 0, '5,0,5,1,5,4') == '0,1,2')
    # assert(process(2024, 0, 0, '0,1,5,4,3,0') == '4,2,5,6,7,7,7,7,3,1,0')

    return process(a, b, c, program_str)


def part_2(lines):
    b = int(lines[1].strip().split(': ')[1])
    c = int(lines[2].strip().split(': ')[1])
    program_str = lines[4].strip().split(': ')[1]
    outputs = list(map(int, program_str.split(',')))

    a = 0
    num_to_match = 1
    while True:
        output = process(a, b, c, program_str, match=outputs[-num_to_match:])

        if output == program_str:
            return a
        if output:
            a *= 8
            num_to_match += 1
        else:
             a += 1


if __name__ == '__main__':
    day = os.path.basename(__file__).replace('.py', '')
    run(day, part_1, part_2)

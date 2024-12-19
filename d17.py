import itertools
import re
from functools import partial
from collections import deque


def read_input(file):
    with open(file,"r") as f:
        s = f.readlines()
        s = map(str.strip, s)
        s = map(partial(str.split, sep=': '), s)
        s = list(s)
        print(s)
    arr = str.split(s[4][1], sep=',')
    print(f"{arr = }")
    program = [int(n) for n in arr]
    data = [int(s[0][1]),int(s[1][1]),int(s[2][1]),program]
    print(data)
    return data


A = 4
B = 5
C = 6
IP = 0
OUT = 1
PROGRAM = 2


def combo(c, value):
    if value < A:
        return value
    if value == A:
        return c[A]
    if value == B:
        return c[B]
    if value == C:
        return c[C]
    raise Exception(f"Expected 0 <= value <= 6, not {value}.")


# adv 0 A / 2 ^ combo -> truncated and written to A
def adv(data, operand):
    com = combo(data, operand)
    temp = data[A] // (2 ** com)
    data[A] = temp
    data[IP] += 2


# bxl 1 bitwise XOR of register B and literal -> B
def bxl(data, operand):
    data[B] = data[B] ^ operand
    data[IP] += 2


# bst 2 combo operand % 8 -> B
def bst(data, operand):
    data[B] = combo(data, operand) % 8
    data[IP] += 2


# jnz 3 if A!=0 then IP = literal operand
def jnz(data, operand):
    if data[A] == 0:
        data[IP] += 2
    else:
        data[IP] = operand


# bxc 4 bitwise B XOR C -> B (also reads operand and ignores)
def bxc(data, operand):
    data[B] = data[B] ^ data[C]
    data[IP] += 2


# out 5 combo operand % 8 and outputs value (separate w commas)
def out(data, operand):
    com = combo(data, operand)
    data[OUT].append(com % 8)
    last = len(data[OUT]) - 1
    if data[PROGRAM] and (data[OUT][last] != data[PROGRAM][last]):
        raise ValueError
    data[IP] += 2

# 6 not used


# cdv 7 adv except stored to C
def cdv(data, operand):
    com = combo(data, operand)
    temp = data[A] // (2 ** com)
    data[C] = temp
    data[IP] += 2


funcs = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    7: cdv
}


def loop(c, program):
    while c[IP] < len(program):
        func = program[c[IP]]
        operand = program[c[IP] + 1]
        funcs[func](c, operand)


def matches_end(output, program):
    start = -1
    for _ in range(len(output)):
        if output[start] != program[start]:
            return False
        start -= 1
    return True


def part2(program):
    deq = deque()
    index = 0
    power = 8
    # for a in range(8):
    #     deq.append((index, a))
    deq.append((index, 7))

    get_out = False
    while deq:
        index, prev_a = deq.popleft()

        for bits in range(8):
            a = bits + power * prev_a
            print(f"{a = } {prev_a = }")
            c = [0, [], None, None, a, 0, 0]
            loop(c, program)
            print(f"A={a} output={c[OUT]}")
            if matches_end(c[OUT], program):
                node = (index, a)
                if node not in deq:
                    deq.append(node)
                print(f"Appending {node}")
            if c[OUT] == program:
                print(f"Part 2 answer is {a}")  # Actual 266932601404433
                get_out = True
                break

        if get_out:
            break
        print(f"{deq = }")
        # cmd = input("Continue?")
        index += 1


def main():
    stuff = read_input("input17.txt")
    # stuff = read_input("input17_sample.txt")
    program = stuff[-1]
    print(f"{program = }")
    # c = [0, [], None, None, stuff[0],stuff[1],stuff[2]]
    # loop(c, program)
    # print(f"Part 1 {','.join([str(n) for n in c[OUT]])}")

    # thing = Thing(program)
    # start = 35_184_372_000_000  # out goes from 15 to 16 items within the next 1 million.
    # start = 35_184_600_000_000
    # end = start + 100_000_000_000
    # for i in range(start, end):
    #     c = [0, [], program, None, i, stuff[1], stuff[2]]
    #     try:
    #         loop(c, program)
    #     except ValueError:
    #         pass
    #     # cmd = input(f"{i} Continue?")
    #     if i % 1_000_000 == 0:
    #         print(f"{i = } {c[OUT] = }")
    #     if program == c[OUT]:
    #         print(f"identity value = {i}")
    #         break

    part2(program)
    print(f"Part 2")


if __name__ == "__main__":
    main()
    print(f"Day 17")


def test_matches_end__matching__returns_true():
    output = [6, 7, 8]
    program = [3, 4, 5, 6, 7, 8]
    assert matches_end(output, program)


def test_matches_end__not_matching__returns_false():
    output = [8]
    program = [3,4,5]
    assert not matches_end(output, program)

def test_different_but_equal_valued_arrays_test_equal():
    a = [7, 6, 5]
    b = [7, 6, 5]
    assert a == b

def test_c_9():
    c = [0, [], None, None, 0, 0, 9]
    program = [2,6]
    loop(c, program)
    assert c[B] == 1

def test_a_10():
    c = [0, [], None, None, 10, 0, 0]
    program = [5,0,5,1,5,4]
    loop(c, program)
    assert c[OUT] == [0, 1, 2]

def test_a_2024():
    c = [0, [], None, None, 2024, 0, 0]
    program = [0,1,5,4,3,0]
    loop(c, program)
    assert c[OUT] == [4,2,5,6,7,7,7,7,3,1,0]

def test_b_29():
    c = [0, [], None, None, 0, 29, 0]
    program = [1,7]
    loop(c, program)
    assert c[B] == 26

def test_b_2024_c_43690():
    c = [0, [], None, None, 0, 2024, 43690]
    program = [4,0]
    loop(c, program)
    assert c[B] == 44354


'''
If register C contains 9, the program 2,6 would set register B to 1.
If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
If register B contains 29, the program 1,7 would set register B to 26.
If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
'''

'''
The adv instruction (opcode 0) performs division. The numerator is the value in the A 
register. The denominator is found by raising 2 to the power of the 
instructions combo operand. (So, an operand of 2 would divide A by 4 (2^2); 
an operand of 5 would divide A by 2^B.) The result of the division operation is 
truncated to an integer and then written to the A register.

The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the 
instruction's literal operand, then stores the result in register B.

The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 
(thereby keeping only its lowest 3 bits), then writes that value to the B register.

The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the 
    A register is not zero, it jumps by setting the instruction pointer to the value 
    of its literal operand; if this instruction jumps, the instruction pointer is not 
    increased by 2 after this instruction.

The bxc instruction (opcode 4) calculates the bitwise XOR of register B and 
register C, then stores the result in register B. (For legacy reasons, this 
instruction reads an operand but ignores it.)

The out instruction (opcode 5) calculates the value of its combo operand modulo 8, 
then outputs that value. (If a program outputs multiple values, they are separated 
by commas.)

NOT USED
The bdv instruction (opcode 6) works exactly like the adv instruction except that 
the result is stored in the B register. (The numerator is still read from the A 
register.)

The cdv instruction (opcode 7) works exactly like the adv instruction except that
the result is stored in the C register. (The numerator is still read from the A 
register.)
'''

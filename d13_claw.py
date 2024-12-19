import itertools
import operator
import re
from functools import cache, partial


def read_input(file):
    with open(file, "r") as f:
        m = f.read().split("\n\n")
        m = map(partial(re.findall, r"\d+"), m)
        m = [[int(num) for num in mach] for mach in m]
        # m = list(m)
    return m


def solve(m):
    e1 = [m[0], m[2], m[4]]
    e2 = [m[1], m[3], m[5]]
    e1 = map(partial(operator.mul, m[1]), e1)
    e2 = map(partial(operator.mul, m[0]), e2)
    e1 = list(e1)
    e2 = list(e2)
    b = [e1[2] - e2[2], e1[1] - e2[1]]
    print(b)
    b_solve = b[0]/b[1]
    print(b_solve)
    print(list(e1))
    print(list(e2))
    a_solve = (m[4] - (m[2] * b_solve)) / m[0]
    print(a_solve)
    solvable = True
    if 0.0001 < abs(a_solve - round(a_solve)):
        solvable = False
    if 0.0001 < abs(b_solve - round(b_solve)):
        solvable = False
    return solvable, a_solve, b_solve


def main():
    m = read_input("input13.txt")
    # m = read_input("input13_sample.txt")
    print(m)
    for machine in m:
        machine = map(int, machine)
    print(m)
    # Assumption: there is only one possible way to get to the prize.
    #     Only if button A and B do different things.
    # Assumption: There is only one prize per machine.
    #    That's the way the data looks.
    # 94A + 22B = 8400
    # 34A + 67B = 5400
    s = solve(m[0])
    print(s)
    s = solve(m[1])
    print(s)
    s = solve(m[2])
    print(s)
    s = solve(m[3])
    print(s)
    tokens = 0
    for mach in m:
        mach[4] = mach[4] + 10000000000000
        mach[5] = mach[5] + 10000000000000

        s = solve(mach)
        if s[0]:
            tokens += 3 * s[1] + s[2]
    print(tokens)


if __name__ == "__main__":
    main()
    print(f"Day 13")

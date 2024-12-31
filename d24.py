import itertools
import re
from functools import cache, partial
from dataclasses import dataclass
from collections import deque
from queue import PriorityQueue
import copy


def read_input(file):
    with open(file,"r") as f:
        s = f.read().split("\n\n")
        starts = [wire.split(': ') for wire in s[0].split('\n')]
        gates = [gate.split() for gate in s[1].split('\n')]
    return starts, gates


def has_value(values, name):
    return name in values


def gen(values, g):
    a = values[g[0]]
    b = values[g[2]]
    if g[1] == 'AND':
        return a & b
    if g[1] == 'OR':
        return a | b
    if g[1] == 'XOR':
        return a ^ b
    raise ValueError(f"Expected AND, OR, or XOR, not {g[1]}")


def part1():
    starts, gates = read_input("input24.txt")
    # starts, gates = read_input("input24_tiny.txt")
    print(f"{starts = }")
    print()
    gates = deque(gates)
    print(f"{gates = }")
    values = {s[0]: int(s[1]) for s in starts}
    print(f"{values = }")
    done_gates = []
    while gates:
        g = gates.popleft()
        if g[0] in values and g[2] in values:
            values[g[4]] = gen(values, g)
            print(f" {g = }  {values[g[4]]}")
            done_gates.append(g)
        else:
            gates.append(g)
        print(f"  {gates = }")
    print("Wires")
    print(values)
    zs = []
    for k in values.keys():
        if 0 == k.find('z'):
            zs.append(k)
    zs = sorted(zs, reverse=True)
    output = 0
    for z in zs:
        output *= 2
        output += values[z]
    print(f"Part 1 output: {output}")


def get_value(values, ch):
    zs = []
    for k in values.keys():
        if 0 == k.find(ch):
            zs.append(k)
    zs = sorted(zs, reverse=True)
    output = 0
    for z in zs:
        output *= 2
        output += values[z]
    return output


def chug(start_gates, values, zs):
    changed = True
    unfinished = start_gates
    while changed:
        done_gates = []
        gates = deque(unfinished)
        unfinished = []
        changed = False
        while gates:
            g = gates.popleft()
            if g[0] in values and g[2] in values:
                val = gen(values, g)
                values[g[4]] = val
                changed = True
                if g[4] in zs and zs[g[4]] != val:
                    return False
                done_gates.append(g)
            else:
                unfinished.append(g)
    print(f"Chug return True")
    return True


def iter_four(lyst):
    yield [lyst[0],lyst[1]], [lyst[2],lyst[3]]
    yield [lyst[0],lyst[2]], [lyst[1],lyst[3]]
    yield [lyst[0],lyst[3]], [lyst[1],lyst[2]]


def swap_wires(pairs):
    # Swap the wires
    for p1, p2 in itertools.batched(pairs, 2):
        temp = p1[4]
        p1[4] = p2[4]
        p2[4] = temp


def get_zs(val):
    bits = []
    while val > 0:
        if val % 2 == 0:
            bits.append(0)
        else:
            bits.append(1)
        val = val // 2
    zs = {}
    for i, b in enumerate(bits):
        if i < 10:
            zs[f'z0{i}'] = b
        else:
            zs[f'z{i}'] = b
    return zs


def part2():
    start_values, start_gates = read_input("input24_sample.txt")
    print(f"{start_values = }")
    print()
    gates = deque(start_gates)
    print(f"{gates = }")
    start_values = {s[0]: int(s[1]) for s in start_values}
    x_val = get_value(start_values, 'x')
    y_val = get_value(start_values, 'y')
    z_val = x_val + y_val
    zs = get_zs(z_val)

    c_8s = 0
    for pairs in itertools.combinations(start_gates, 8):
        c_8s += 1
        if c_8s % 100_000 == 0:
            print(f"Tried={c_8s}")
        names = []
        for p in pairs:
            names.append(p[4])
        values = {}
        for k, v in start_values.items():
            values[k] = v

        swap_wires(pairs)

        success = chug(gates, values, zs)
        swap_wires(pairs)
        # if not success:
        #     continue
        output = get_value(values, 'z')
        # print(f"{x_val =}  {y_val=}  {output = }")
        # print(output)
        # print(x_val + y_val)
        if x_val + y_val == output:
            print('YAYYYYY!')
            print(f"Sorted names: {','.join(sorted(names))}")
            break

    print(f"Part 2 Done")


def main():
    # part1()
    part2()


if __name__ == "__main__":
    main()
    print(f"Day 24")


def test_stuff():
    assert False

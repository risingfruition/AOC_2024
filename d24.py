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
    values = {s[0]: int(s[1]) for s in starts}
    print(f"{values = }")
    output = add_xy(gates, values)
    print(f"Part 1 output: {output}")


def add_xy(gates: list[list[str]], values: dict[str, int]) -> int:
    # TODO: copy values so that when I change it below, the originals
    # are unchanged.
    gates = deque(gates)
    done_gates = []
    while gates:
        g = gates.popleft()
        if g[0] in values and g[2] in values:
            values[g[4]] = gen(values, g)
            done_gates.append(g)
        else:
            gates.append(g)
    output: int = wires_to_num(values)
    return output


def wires_to_num(values: dict[str, int]) -> int:
    zs = []
    for k in values.keys():
        if 0 == k.find('z'):
            zs.append(k)
    zs = sorted(zs, reverse=True)
    output: int = 0
    for z in zs:
        output *= 2
        output += values[z]
    return output


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


def swap_wires(pairs):
    # Swap the wires
    for p1, p2 in itertools.batched(pairs, 2):
        temp = p1[4]
        p1[4] = p2[4]
        p2[4] = temp


# Need something like this, but to set x and y wires
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
    start_values, start_gates = read_input("input24.txt")
    # start_values, start_gates = read_input("input24_sample.txt")
    print(f"{start_values = }")
    print()
    gates = deque(start_gates)
    print(f"{gates = }")
    start_values = {s[0]: int(s[1]) for s in start_values}
    x_val = get_value(start_values, 'x')
    y_val = get_value(start_values, 'y')
    z_val = x_val + y_val
    zs = get_zs(z_val)
    print()
    wire_to_gates = {'None': 'No gate'}
    unsorted_wires = set()
    input_wires_gates = {
        'None': ['No gate'],
        'z19': ['swapped'],
        'z00': ['special case for bit 0'],
        'z01': ['special case for bit 0']
    }
    output_wires_gates = {'None': ['No gate']}
    for g in gates:
        w = g[0]
        wire_to_gates[w] = wire_to_gates.get(w, []) + [g]
        unsorted_wires.add(w)
        input_wires_gates[w] = input_wires_gates.get(w, []) + [g]

        w = g[2]
        wire_to_gates[w] = wire_to_gates.get(w, []) + [g]
        unsorted_wires.add(w)
        input_wires_gates[w] = input_wires_gates.get(w, []) + [g]

        w = g[4]
        wire_to_gates[w] = wire_to_gates.get(w, []) + [g]
        unsorted_wires.add(w)
        output_wires_gates[w] = output_wires_gates.get(w, []) + [g]
        print(f"Wire:{w}  Gate:{g}")

    sorted_wires = sorted(list(unsorted_wires))
    # print(sorted_wires)
    # print(wire_to_gates)
    # print()
    # print(f"{input_wires_gates = }")
    #
    # print()
    # for w in sorted_wires:
    #     print(w)
    #     print(f"  {wire_to_gates[w]}")

    print()
    for n in range(46):
        print()
        nn = f"{n:02d}"
        z = 'z' + nn
        y = 'y' + nn
        x = 'x' + nn
        a, b, c = find_xy(wire_to_gates, x, y, 'AND')
        and_g = input_wires_gates[c]
        and_g_2 = []
        for g in and_g:
            and_g_2.append(input_wires_gates.get(g[4], "Not found"))
        print(f"{x} AND {y} --> {c}  {and_g}  {and_g_2}")
        a, b, c = find_xy(wire_to_gates, x, y, 'XOR')
        xor_g = input_wires_gates[c]
        xor_g_2 = []
        for g in xor_g:
            xor_g_2.append(input_wires_gates.get(g[4], "Not found"))
        print(f"{x} XOR {y} --> {c}  {xor_g}  {xor_g_2}")
    # print(f"{output_wires_gates = }")
    print(f"Part 2 Done")


def find_xy(wire_to_gates, x, y, cond):
    gates = wire_to_gates.get(x, None)
    if not gates:
        return 'None', 'None', 'None'
    for g in wire_to_gates[x]:
        if (g[0] == x and g[2] == y) or (g[2] == x and g[0] == y):
            if g[1] == cond:
                return g[0], g[2], g[4]
    return 'None', 'None', 'None'


def main():
    part1()  # Answer is 64755511006320
    part2()


if __name__ == "__main__":
    main()
    print(f"Day 24")


def test_stuff():
    assert False

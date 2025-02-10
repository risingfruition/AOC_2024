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


A = 0
OP = 1
B = 2
OUT = 4
OPS = {
    "AND": lambda a, b: a & b,
    "XOR": lambda a, b: a ^ b,
    "OR": lambda a, b: a | b
}


def wire_value(wire: str, gates, init: dict[str, int]) -> int:
    if wire in init:
        # print(f"{init[wire] = }")
        return init[wire]
    # print(wire)
    for g in gates:
        if g[OUT] == wire:
            # print(g)
            return OPS[g[OP]](wire_value(g[A], gates, init), wire_value(g[B], gates, init))


def to_num(lyst):
    num = 0
    for item in lyst:
        num = num * 2 + item
    return num


def calc_z(gates, init):
    zs = []
    for z in range(46):
        zs.append(wire_value(f"z{z:02}", gates, init))
    # print(zs)
    zs = zs[::-1]
    # print(zs)
    return to_num(zs)


def make_init(n):
    init = {}
    for num in range(45):
        init[f"x{num:02}"] = 0
        init[f"y{num:02}"] = 0
    for x in range(2):
        init[f"x{n:02}"] = x
        for y in range(2):
            init[f"y{n:02}"] = y
            for c in range(2):
                init[f"x{n-1:02}"] = c
                init[f"y{n-1:02}"] = c
                yield init, x + y + c


def part2():
    starts, gates = read_input("input24.txt")
    init = {s[0]: int(s[1]) for s in starts}
    print(f"{init = }")
    print(calc_z(gates, init))

    # for n in range(1, 46):
    #     for init, bit_sum in make_init(n):
    #         sum = bit_sum * (2 ** n)
    #         # print(f"{sum = }")
    #         calced = calc_z(gates, init)
    #         if sum == calced:
    #             # print(f"GOOD bit {n}  {sum=}  {calced=}")
    #             pass
    #         else:
    #             print(f"BAD bit {n}  {sum=}  {calced=}")
    #             break

    swaps = []
    swap_outs(gates, swaps, 'djg', 'z12')
    swap_outs(gates, swaps, 'sbg', 'z19')
    swap_outs(gates, swaps, 'mcq', 'hjm')
    swap_outs(gates, swaps, 'dsd', 'z37')
    # print(f"\nBit 10")
    # print(only_wires_for(gates, 10))
    # kerfuffle(gates, 10, only_wires_for(gates, 10))
    # print(f"\nBit 11")
    # print(only_wires_for(gates, 11))
    # kerfuffle(gates, 11, only_wires_for(gates, 11))
    bit_num = 12
    break_at = 999
    CarryOut = None
    while bit_num < 49:
        CarryOut = show_bit(gates, bit_num, CarryOut)
        if CarryOut is None:
            break_at = bit_num + 1
        if break_at == bit_num:
            break
        bit_num += 1

    print(f"Swaps: {swaps}")
    swaps = sorted(swaps)
    print(f"Swaps: {swaps}")
    print(",".join(swaps))


def show_bit(gates, bit_num, CarryOut) -> str | None:
    print(f"\nBit {bit_num}")
    print(only_wires_for(gates, bit_num))
    return kerfuffle(gates, bit_num, only_wires_for(gates, bit_num), CarryOut)


def wire_str(dd, xyz):
    return f"{xyz}{dd:02}"


def goober(wires, gates, wire):
    # find all gates with wire
    # for each wire coming into the gate (cuz we're starting
    # with the output wire) if it's not in set, add it and
    # find all gates with that as an output.
    wires.add(wire)
    for g in gates:
        if g[OUT] == wire:
            if g[A] not in wires:
                wires.add(g[A])
                goober(wires, gates, g[A])
            if g[B] not in wires:
                wires.add(g[B])
                goober(wires, gates, g[B])


def only_wires_for(gates, dd):
    """Find the set of wires involved in creating specifically
    output dd. So, it will be all the wires involved in dd,
    minus all the wires involved in dd-1."""
    wires_curr = set()
    wire = wire_str(dd, 'z')
    goober(wires_curr, gates, wire)

    wires_prev = set()
    if dd > 0:
        wire = wire_str(dd - 1, 'z')
        goober(wires_prev, gates, wire)
    return wires_curr - wires_prev


"""
I want to pattern match the gates I expect to have.
Find the first output that doesn't match. Then swap 
with some output gate and try again. There is only
one possible output wire that it could swap with, by
definition of the problem. So, I could just try them
all if I don't have a better plan. First I need to 
find a wire in the wrong place.
"""
'''
Each bit should have:
xdd XOR ydd -> DD_xor
xdd AND ydd -> DD_and
CarryPrev XOR DD_xor -> Zdd
CarryPrev AND DD_xor -> CarryIntermediate
DD_and OR  CarryIntermediate -> CarryDD
'''


def look_for(gates, a, b, op):
    for g in gates:
        if (a == g[A] or a == g[B]) and (b == g[A] or b == g[B]) and op == g[OP]:
            return g
    return None


def look_for_a_out(gates, a, out, op):
    for g in gates:
        if (a == g[A] or a == g[B]) and out == g[OUT] and op == g[OP]:
            return g
    return None


def look_for_input(gates, a, op):
    group = []
    for g in gates:
        if (a == g[A] or a == g[B]) and op == g[OP]:
            group.append(g)
    if len(group) == 1:
        return group[0]
    if len(group) > 1:  # Not expecting to encounter this but ???
        assert False
    return None


def snuffleufugus(gates, dd, CarryPrev = None):
    a = wire_str(dd, 'x')
    b = wire_str(dd, 'y')
    z = wire_str(dd, 'z')
    DD_and = None
    DD_xor = None
    CarryIntermediate = None
    CarryDD = None
    g = look_for(gates, a, b, 'XOR')
    DD_xor = g[OUT]
    g = look_for(gates, a, b, 'AND')
    DD_and = g[OUT]
    SUM = None

    changes = True
    while changes:
        changes = False
        if SUM is None:
            if CarryPrev:
                g = look_for(gates, CarryPrev, DD_xor, 'XOR')
                if g is None:
                    g = look_for_input(gates, CarryPrev, 'XOR')
                    if g:
                        SUM = g[OUT]
            else:
                g = look_for_input(gates, DD_xor, 'XOR')
                if g:
                    SUM = g[OUT]
    assert False == "Look for all the gates and return CarryDD if I find it"
    return None


def kerfuffle(gates, dd, try_wires, carry_dd) -> str | None:
    a = wire_str(dd, 'x')
    b = wire_str(dd, 'y')
    out = wire_str(dd, 'z')
    g = look_for(gates, a, b, 'XOR')
    if not g:
        print(f"Not found: xdd XOR ydd")
        return None
    DD_xor = g[OUT]
    print(f"xdd XOR ydd -> DD_xor = {DD_xor}")

    g = look_for(gates, a, b, 'AND')
    if not g:
        print(f"Not found: xdd AND ydd")
        return None
    DD_and = g[OUT]
    print(f"xdd XOR ydd -> DD_and = {DD_and}")

    g = look_for_a_out(gates, DD_xor, out, 'XOR')
    if g is None:
        print(f"Not found: CarryPrev XOR DD_xor({DD_xor}) -> {out} ")
        for w in try_wires:
            g = look_for(gates, DD_xor, w, 'XOR')
            if g is not None:
                break
        if g is None:
            return None
    CarryPrev = g[A] if g[B] == DD_xor else g[B]
    print(f"CarryPrev({CarryPrev}) XOR DD_xor({DD_xor}) -> {g[OUT]}")

    g = look_for(gates, CarryPrev, DD_xor, 'AND')
    if g is None:
        print(f"Not found: CarryPrev AND DD_xor")
        return None
    CarryIntermediate = g[OUT]
    print(f"CarryPrev({CarryPrev}) AND DD_xor({DD_xor}) -> CarryIntermediate({CarryIntermediate})")

    g = look_for(gates, CarryIntermediate, DD_and, 'OR')
    if g is None:
        print(f"Not found: CarryIntermediate({CarryIntermediate}) OR DD_and({DD_and})")
        return None
    CarryDD = g[OUT]
    print(f"{CarryIntermediate} OR {DD_and} -> CarryDD({CarryDD})")

    return CarryDD


def swap_outs(gates, swaps, a, b):
    for g in gates:
        if g[OUT] == a:
            swaps.append(a)
            g[OUT] = b
            continue
        if g[OUT] == b:
            swaps.append(b)
            g[OUT] = a
            continue


def main():
    part2()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
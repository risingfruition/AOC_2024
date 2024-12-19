import itertools
import re
from functools import cache, partial
from dataclasses import dataclass
from collections import deque
from queue import PriorityQueue


def read_input(file):
    with open(file,"r") as f:
        s = f.read().split("\n\n")
    return s


EMPTY = 0
WALL = 1
START = 2
END = 3

DOWN = 0
UP = 1
RIGHT = 2
LEFT = 3
NUM_DIRECTIONS = 4
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
move_dir = "v^><"
too_costly = 999_999_999
facing_next = {
    DOWN: [DOWN, RIGHT, LEFT],
    UP: [UP, RIGHT, LEFT],
    RIGHT: [RIGHT, DOWN, UP],
    LEFT: [LEFT, DOWN, UP]
}
facing_text = {
    DOWN: "DOWN",
    UP: "UP",
    RIGHT: "RIGHT",
    LEFT: "LEFT"
}


def is_matchable(design, patterns):
    # print(f"{design = }")
    if not design:
        return True
    for p in patterns:
        # print(f" pattern={p} {design=}")
        d = design[:]
        l = len(p)
        if len(d) < l:
            # print(f"  pattern bigger than design - won't match.")
            continue
        d = design[:l]
        if d == p:
            # print(f" Design starts with pattern={p} len={l} {d=} {design=}")
            if not is_matchable(design[l:], patterns):
                continue
            return True
        # print("returning")
        # return False
    return False


def part1():
    data = read_input("input19.txt")
    # data = read_input("input19_sample.txt")
    patterns = data[0].split(', ')
    designs = data[1].split('\n')
    print(patterns)
    print(designs)
    num_possible = 0
    # designs [4] and [7] are not possible. The others are possible.
    # print(f"{is_matchable(designs[0], patterns) = }")
    # print(f"{is_matchable(designs[1], patterns) = }")
    # print(f"{is_matchable(designs[2], patterns) = }")
    # print(f"{is_matchable(designs[3], patterns) = }")
    # print(f"{is_matchable(designs[4], patterns) = } False")
    # print(f"{is_matchable(designs[5], patterns) = }")
    # print(f"{is_matchable(designs[6], patterns) = }")
    # print(f"{is_matchable(designs[7], patterns) = } False")
    for design in designs:
        if is_matchable(design, patterns):
            num_possible += 1
    print(f"Part 1: {num_possible = }")


stuff = [0]


def fewer_strings_count_matchable(design, d_len, start, patt, max_patt_len):
    if start >= d_len:
        stuff[0] += 1
        if stuff[0] % 1_000_000 == 0:
            print(f"Count {stuff[0] // 1_000_000}")
        return 1
    # print(f"{design = }")
    count = 0
    remaining = d_len - start
    max_len = min(max_patt_len, remaining) + 1
    for i in range(1, max_len):
        d = design[start:start+i]
        if d in patt:
            count += fewer_strings_count_matchable(design, d_len, start+i, patt, max_patt_len)
    return count


patt = {}

@cache
def count_matchable(design, leng):
    # print(f"{design = }")
    if not design:
        # print("FOUND IT")
        return 1
    count = 0
    max_len = min(leng, len(design)) + 1
    for i in range(1, max_len):
        d = design[:i]
        if d in patt:
            count += count_matchable(design[i:], leng)
    return count


def part2():
    data = read_input("input19.txt")
    # data = read_input("input19_sample.txt")
    patterns = data[0].split(', ')
    designs = data[1].split('\n')
    print(patterns)
    print(designs)
    l = 0

    for p in patterns:
        patt[p] = p
        if l < len(p):
            l = len(p)

    num_possible = 0
    # designs [4] and [7] are not possible. The others are possible.
    # print(f"{count_matchable(designs[0], patterns) = }")
    # print(f"{count_matchable(designs[1], patterns) = }")
    # print(f"{count_matchable(designs[2], patterns) = }")
    # print(f"{count_matchable(designs[3], patterns) = }")
    # print(f"{count_matchable(designs[4], patterns) = } False")
    # print(f"{count_matchable(designs[5], patterns) = }")
    # print(f"{count_matchable(designs[6], patterns) = }")
    # print(f"{count_matchable(designs[7], patterns) = } False")
    total = 0

    for design in designs:
        print(f"Design: {design}")
        count = count_matchable(design, l)
        print(f" {count = }")
        if count > 0:
            total += count
        print(f" {total = }")
    print(f"Part 2 possible combos = {total}")


def main():
    # part1()
    part2()


if __name__ == "__main__":
    main()
    print(f"Day 19")


def test_stuff():
    assert False

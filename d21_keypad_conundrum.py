import itertools
import re
from functools import cache, partial
from dataclasses import dataclass
from collections import deque
from queue import PriorityQueue, SimpleQueue


def read_input(file):
    with open(file,"r") as f:
        s = f.readlines()
        s = [str.strip(l) for l in s]
    return s


'''
numeric keypad
789
456
123
 0A
 
directional keypad
 ^A
<v>
'''

numpad = {
    'A0': '<A',
    '02': '^A',
    '29': '^^>A',
    '9A': 'vvvA',
    'A9': '^^^A',
    '98': '<A',
    '80': 'vvvA',
    '0A': '>A',
    'A1': '^<<A',
    '17': '^^A',
    '79': '>>A',
    # '9A': 'dup',
    'A4': '^^<<A',
    '45': '>A',
    '56': '>A',
    '6A': 'vvA',
    'A3': '^A',
    '37': '^^<<A',
    # '79': 'dup',
    # '9A': 'dup',
    # '': '',
    # '': '',
    # '': '',
    # '': '',
}

dir_pad = {
    'A^': '<A',
    'A<': 'v<<A',
    'Av': 'v<A',
    'A>': 'vA',
    '^A': '>A',
    '<A': '>>^A',
    'vA': '>^A',
    '>A': '^A',
    '^<': 'v<A',
    '^v': 'vA',
    '^>': 'v>A',
    '^^': 'A',
    '<^': '>^A',
    '<<': 'A',
    '<v': '>A',
    '<>': '>>A',
    'v^': '^A',
    'v<': '<A',
    'vv': 'A',
    'v>': '>A',
    '>^': '<^A',
    '><': '<<A',
    '>v': '<A',
    '>>': 'A',
    'AA': 'A',

}

OFFSET = 4
EMPTY = 0 - OFFSET
WALL = 1 - OFFSET
START = 2 - OFFSET
END = 3 - OFFSET

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


'''
OP
<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
v<<A>>^A<A>AvA<^AA>A<vAAA>^A
<A^A>^^AvvvA
029A
ME: I got this one. The last one (379A) gave me trouble.
'''

'''
029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
'''


numpad_grid = [
    '#####',
    '#789#',
    '#456#',
    '#123#',
    '##0A#',
    '#####'
]
dir_pad_grid = [
    '#####',
    '##^A#',
    '#<v>#',
    '#####',
]


def part1():
    data = read_input("input21_sample.txt")
    print(data)
    total = 0
    for code in data:
        control_door_bot = ''
        print(f"{code = }")
        prev = 'A'
        for ch in code:
            move = prev + ch
            # print(f"{move = }")
            control_door_bot += numpad[move]
            prev = ch
        print(f"len(door_bot) = {len(control_door_bot)}  {control_door_bot = }")
        dir_pad_r = make_dir_pad(control_door_bot)
        print(f"{len(dir_pad_r) = }  {dir_pad_r}")
        dir_pad_d = make_dir_pad(dir_pad_r)
        print(f"{len(dir_pad_d) = }  {dir_pad_d}")
        print(f"Numeric part = {int(code[:3])}")

        total += len(dir_pad_d) * int(code[:3])
    print(f"Part 1 total = {total}")

    s = '^^^<<A'
    for i in range(3):
        print(s)
        s = make_dir_pad(s)
    print()
    s = '<<^^^A'
    for i in range(3):
        print(s)
        s = make_dir_pad(s)
    print()
    s = '^<^<^A'
    for i in range(3):
        print(s)
        s = make_dir_pad(s)
    print()
    s = '^^<^<A'
    for i in range(3):
        print(s)
        s = make_dir_pad(s)
    print()


def make_dir_pad(control_door_bot):
    dir_pad_bot = ''
    prev = 'A'
    for ch in control_door_bot:
        move = prev + ch
        stuff = dir_pad[move]
        # print(f"{move = }  {stuff = }")
        dir_pad_bot += stuff
        prev = ch
    return dir_pad_bot


def main():
    # Part 1 sample has 44 cheats that save time.
    part1()
    # part2()


if __name__ == "__main__":
    main()
    print(f"Day 20")


def test_stuff():
    assert False

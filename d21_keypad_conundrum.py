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

"""The direction codes to get from one key to another."""
# obsolete
numpad = {
    # 'A2': '<<^^^A',  # Illegal because it goes over the blank spot.
    'A0': '<A',
    'A1': '^<<A',
    'A3': '^A',
    'A4': '^^<<A',
    'A9': '^^^A',
    '0A': '>A',
    '02': '^A',
    '17': '^^A',
    '29': '^^>A',
    '37': '<<^^A',
    '45': '>A',
    '56': '>A',
    '6A': 'vvA',
    '79': '>>A',
    '80': 'vvvA',
    '9A': 'vvvA',
    '98': '<A',
# 780A
# 846A
# 965A
# 386A
# 638A
    'A6': '^^A',
    'A7': '^^^<<A',
    'A8': '<^^^A',
    '78': '>A',
    '84': '<vA',
    '46': '>>A',
    '96': 'vA',
    '65': '<A',
    '5A': 'vv>A',
    '38': '<^^A',
    '86': 'v>A',
    '63': 'vA',
    '8A': 'vvv>A',
    # '': '',
}

"""The direction codes to get from one dir_pad key to another."""
# obsolete
dir_pad = {
    'A^': '<A',
    'A<': 'v<<A',
    'Av': '<vA',
    'A>': 'vA',
    '^A': '>A',
    '<A': '>>^A',
    'vA': '^>A',
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

WALL = '#'


def find_stuff(data, thing):
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            if col == thing:
                return r, c
    raise Exception(f"Expected to find {thing} in data.")


DOWN = 0
UP = 1
RIGHT = 2
LEFT = 3
NUM_DIRECTIONS = 4
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
move_dir = "v^><"
too_costly = 999_999_999


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


num_pad_grid = [
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

num_pad_items = 'A0123456789'
dir_pad_items = 'A<>v^'

class Node:
    def __init__(self, cost: int, r: int, c: int, d: str, parent):
        self.cost = cost
        self.r = r
        self.c = c
        self.d = d
        self.parent = parent

    def __lt__(self, other):
        return self.cost < other.cost


def neighbors(data, r, c):
    for d in range(NUM_DIRECTIONS):
        dr, dc = directions[d]
        nr, nc = r + dr, c + dc
        if data[nr][nc] != WALL:
            yield nr, nc, d


def bfs(data, s, e):
    """Return all smallest paths from s to e."""
    sr, sc = s
    er, ec = e
    prev_cost = 0
    node = Node(prev_cost, sr, sc, None, None)
    if sr == er and sc == ec:
        return [node]

    for nr, nc, _d in neighbors(data, sr, sc):
        costs_rc = {
            (sr, sc, nr, nc): prev_cost
        }
    queue = deque()
    queue.append(node)
    least_cost = 999_999_999
    best = []
    while len(queue):
        node = queue.popleft()
        r, c = node.r, node.c
        # print(f'{r=} {c=}')
        for nr, nc, d in neighbors(data, r, c):
            # print(f'{nr=} {nc=}')
            n = Node(node.cost + 1, nr, nc, move_dir[d], node)
            if nr == er and nc == ec:
                # print(f"ENDPOINT found")
                if least_cost >= n.cost:
                    if least_cost > n.cost:
                        least_cost = n.cost
                        best = []
                        # print(f"New least cost found: clearing best.")
                    else:
                        # print(f"Another same cost found.")
                        pass
                    best.append(n)
                continue
            if (nr, nc, r, c) in costs_rc:
                prev_cost = costs_rc[(nr, nc, r, c)]
                if prev_cost > n.cost:
                    # print(f"New lower cost path found")
                    costs_rc[(nr, nc, r, c)] = n.cost
                elif prev_cost == n.cost:
                    # another path with equal value
                    # print(f"Another path with equal value.")
                    pass
                else:
                    # print(f"Expensive: Don't add this node to queue.")
                    continue
            else:
                costs_rc[(nr, nc, r, c)] = n.cost
            # print(f"Appending {nr} {nc}")
            queue.append(n)
        # input(f"{len(queue)}  ------- continue?")
    return best


def part1_b():
    # data = read_input("input21.txt")
    data = read_input("input21_sample.txt")
    print(data)
    total = 0
    for code in data:
        control_door_bot = ''
        print(f"{code = }")
        prev = 'A'  # Robot initially points to the 'A' button.
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
    # Too high 261714

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


@cache
def dfs(st, level) -> int:
    if level == 0:
        return len(st)
    n = 0
    for s in itertools.pairwise('A' + st):
        n += dfs(dir_pad[''.join(s)], level - 1)
    return n


def part2():
    data = read_input("input21.txt")
    # data = read_input("input21_sample.txt")
    print(data)
    total = 0
    for code in data:
        control_door_bot = ''
        print(f"{code = }")
        prev = 'A'  # Robot initially points to the 'A' button.
        for ch in code:
            move = prev + ch
            # print(f"{move = }")
            control_door_bot += numpad[move]
            prev = ch
        print(f"  len(door_bot) = {len(control_door_bot)}  {control_door_bot = }")

        count = dfs(control_door_bot, 25)
        print(f"len {count}")

        int_code = int(code[:3])
        total += count * int_code
        print(f"   Leng of string {count}")
        print(f"   Numeric part = {int_code}")
        print(f"   Total = {total}")
    print(f"Part 2 total = {total}")


@cache
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


def show_path(n):
    path = 'A'
    while n.parent:
        path = n.d + path
        n = n.parent
    return path


def find_paths(grid, start, end):
    s = find_stuff(grid, start)
    e = find_stuff(grid, end)
    result = bfs(grid, s, e)
    return result


def blurf(paths, s, i, st, out):
    if i == len(s):
        out.append(st)
        # print(f"       {st}")
        return
    # print(f"{i}  {s[i]}  {st}")
    for word in paths[s[i]]:
        blurf(paths, s, i+1, st + word, out)


def all_possible(paths, sequence):
    # print(f"all_possible({sequence})")
    out = []
    s = ["".join(pair) for pair in list(itertools.pairwise('A' + sequence))]
    # print(f"all_possible: {s}")
    i = 0
    blurf(paths, s, i, '', out)
    return out


def all_pad_expand(paths, sequence):
    out = []
    for seq in sequence:
        s = ["".join(pair) for pair in list(itertools.pairwise('A' + seq))]
        # print(f"all_pad_expand: {s}")
        i = 0
        blurf(paths, s, i, "", out)
    return out


def limit_blurf(paths, s, i, st, out, best):
    if len(st) > best[0]:
        return
    if i == len(s):  # Stop
        if len(st) < best[0]:
            best[0] = len(st)
            # print(f"New best[0] of {best[0]}")
            out.clear()
        out.append(st)
        return
    for word in paths[s[i]]:
        limit_blurf(paths, s, i+1, st + word, out, best)


def all_pad_expand_limit(paths, sequence, limit):
    out = []
    best = [limit]
    for seq in sequence:
        s = ["".join(pair) for pair in list(itertools.pairwise('A' + seq))]
        # print(f"all_pad_expand_limit: {s}")
        i = 0
        limit_blurf(paths, s, i, "", out, best)
    return out


def part1():
    data = read_input("input21.txt")
    # data = read_input("input21_sample.txt")
    print(data)

    num_pad_paths = {}
    for s, e in itertools.permutations(num_pad_items, 2):
        result = [show_path(n) for n in find_paths(num_pad_grid, s, e)]
        num_pad_paths[s+e] = result
        print(f" {s}-{e}:  {', '.join(result)}")

    dir_pad_paths = {}
    for s, e in itertools.product(dir_pad_items, repeat=2):
        result = [show_path(n) for n in find_paths(dir_pad_grid, s, e)]
        dir_pad_paths[s+e] = result
        print(f" {s}-{e}:  {', '.join(result)}")

    for k,v in numpad.items():
        if v not in num_pad_paths[k]:
            print(f"Value {v} not in num_pad_paths[{k}].")
    print()
    for k, v in dir_pad.items():
        if v not in dir_pad_paths[k]:
            print(f"Value {v} not in dir_pad_paths[{k}].")
    print()

# when from and to are the same, the only path should be 'A'.
    # That's not what happens here.
    # Num pad paths doesn't repeat items, maybe that's not a problem
    # due to the limitations of the input.
    # Dir pad paths DO have multiples, but the case where "I'm already
    # here" doesn't occur to the bfs and we get paths like '><A' instead
    # of just 'A'.
    print(f"{num_pad_paths}")
    print(f"{dir_pad_paths}")
    # exit()
    print()
    total = 0
    for door_code in data:
        print(f"DOOR CODE {door_code} --------------------------------------")
        pad_depressurized_robot = all_possible(num_pad_paths, door_code)
        print(f"{pad_depressurized_robot}")
        print(f"{len(pad_depressurized_robot)} items of length {len(pad_depressurized_robot[0])}")
        print(f"{len(pad_depressurized_robot)} items of length {len(pad_depressurized_robot[-1])}")
        print()

        pad_radiation_robot = all_pad_expand_limit(dir_pad_paths, pad_depressurized_robot, 10_000)
        # print(f"{pad_radiation_robot}")
        print(f"{len(pad_radiation_robot)} items of length {len(pad_radiation_robot[0])}")
        print(f"{len(pad_radiation_robot)} items of length {len(pad_radiation_robot[-1])}")
        print()

        # MAKE A NEW function that only saves one string, or none and only saves
        # the length.
        pad_cold_robot = all_pad_expand_limit(dir_pad_paths, pad_radiation_robot, 10_000)
        # print(f"{pad_cold_robot}")
        print(f"{len(pad_cold_robot)} items of length {len(pad_cold_robot[0])}")
        print(f"{len(pad_cold_robot)} items of length {len(pad_cold_robot[-1])}")
        print()
        print(f"For door code {door_code}")

        total += len(pad_cold_robot[0]) * int(door_code[:3])

    print(f"------------------------------------------------------")
    print(f"Part 1 total = {total}")


def main():
    # part1()
    part1_b()  # Sample value is 126384  # Correct value is 246990
    part2()


if __name__ == "__main__":
    main()
    print(f"Day 20")


def test_bfs__returns_multiple_paths():
    s = find_stuff(num_pad_grid, '7')
    e = find_stuff(num_pad_grid, '3')
    result = bfs(num_pad_grid, s, e)
    expect = []
    assert result == expect

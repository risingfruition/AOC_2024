import itertools
import re
from functools import partial

def list_int(lyst):
    return list(map(int, lyst))


def join_list(lyst):
    stuff = ""
    for i in lyst:
        stuff = stuff + i
    return stuff


def colon_blow(st):
    return str.split(st, ':')


def read_input(file):
    with open(file,"r") as f:
        s = f.readlines()
        s = map(str.rstrip, s)
        # s = map(colon_blow, s)
        # s = map(join_list, s)
        # s = map(str.split, s)
        # s = map(list_int, s)
        s = list(s)
    return s



class Node:
    def __init__(self, r, c):
        self.r = r
        self.c = c


frequencies = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def get_nodes(data):
    nodes = {}
    for r, line in enumerate(data):
        for c, frequency in enumerate(line):
            if frequency in frequencies:
                # print(frequency, nodes)
                if frequency in nodes:
                    current = nodes[frequency]
                    to_add = list((r,c))
                    # print(current, to_add)
                    nodes[frequency] = current + [(r, c)]
                else:
                    nodes[frequency] = [(r, c)]
                # print(frequency, nodes)
    return nodes


def get_antinodes(combo):
    dr = combo[0][0] - combo[1][0]
    dc = combo[0][1] - combo[1][1]
    antinodes = []
    antinodes.append((combo[0][0] + dr, combo[0][1] + dc))
    antinodes.append((combo[1][0] - dr, combo[1][1] - dc))
    return antinodes


def part1(data):
    print(data)
    solution = {}
    nodes = get_nodes(data)
    r_len = len(data)
    c_len = len(data[0])
    for frequency in nodes.keys():
        print(f"frequency {frequency}")
        for combo in itertools.combinations(nodes[frequency], 2):
            print(combo)
            antinodes = get_antinodes(combo)
            for a in antinodes:
                r = a[0]
                c = a[1]
                if r < 0 or c < 0 or r >= r_len or c >= c_len:
                    continue
                solution[a] = solution.get(a, 0) + 1
    result = len(solution.keys())
    return result


def get_antinodes_2(r_len, c_len, combo):
    dr = combo[0][0] - combo[1][0]
    dc = combo[0][1] - combo[1][1]
    antinodes = [combo[0], combo[1]]
    mult = 1
    while True:
        anti = (combo[0][0] + dr * mult, combo[0][1] + dc * mult)
        r = anti[0]
        c = anti[1]
        if r < 0 or c < 0 or r >= r_len or c >= c_len:
            break
        mult += 1
        antinodes.append(anti)

    mult = 1
    while True:
        anti = (combo[0][0] - dr * mult, combo[0][1] - dc * mult)
        r = anti[0]
        c = anti[1]
        if r < 0 or c < 0 or r >= r_len or c >= c_len:
            break
        mult += 1
        antinodes.append(anti)
    return antinodes


def part2(data):
    solution = {}
    nodes = get_nodes(data)
    r_len = len(data)
    c_len = len(data[0])
    for frequency in nodes.keys():
        print(f"frequency {frequency}")
        for combo in itertools.combinations(nodes[frequency], 2):
            print(combo)
            antinodes = get_antinodes_2(r_len, c_len, combo)
            for a in antinodes:
                solution[a] = solution.get(a, 0) + 1
    result = len(solution.keys())
    return result


def main():
    data = read_input("input08.txt")
    result = part1(data)
    print(f"Day 8 Part 1  Unique antinodes {result}")
    result = part2(data)
    print(f"Day 8 Part 2  Unique antinodes {result}")


if __name__ == "__main__":
    main()


def test_stuff():
    combo = [(2, 3), (4, 7)]
    expect1 = (0, -1)
    expect2 = (6, 11)
    antinodes = get_antinodes(combo)
    assert expect1 in antinodes
    assert expect2 in antinodes
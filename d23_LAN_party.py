import itertools
import re
from functools import cache, partial
from dataclasses import dataclass
from collections import deque
from queue import PriorityQueue


def read_input(file):
    with open(file,"r") as f:
        s = f.read().split("\n")
        s = [str.split(n, '-') for n in s]
    return s


def part1():
    data = read_input("input23.txt")
    # data = read_input("input23_sample.txt")
    print(data)
    net = {}
    for con in data:
        # print(f"{con[0] = }  {con[1] = }")
        links = net.get(con[0], list())
        links.append(con[1])
        net[con[0]] = links

        links = net.get(con[1], list())
        links.append(con[0])
        net[con[1]] = links

    s = set()
    for k in net.keys():
        for a, b in itertools.combinations(net[k], 2):
            if a in net[b]:
                t = tuple(sorted([a, b, k]))
                s.add(t)
    print()
    print(f"Count 3-node networks = {len(s)}")
    has_t = set()
    for i in s:
        for st in i:
            # print(f"{st=}")
            if st.find('t') == 0:
                has_t.add(i)
                break
    print(f"has_t contains {len(has_t)} items.")
    print(f"3-node networks in a 10-node network? {(10*9*8*7*6*5*4)}")
    print(f"3-node networks in a 9-node network? {(9*8*7*6*5*4)}")
    print(f"3-node networks in a 8-node network? {(8*7*6*5*4)}")
    print(f"3-node networks in a 7-node network? {(7*6*5*4)}")
    count = 40
    thing = itertools.combinations(range(count), 3)
    total = 0
    for _ in thing:
        total += 1
    print(f"{total = }")
    counts = []
    for i in net:
        counts.append(len(net[i]))
    counts.sort()
    print(f"counts {counts[:10]} ...... {counts[-10:]}")

    r = 14
    solutions = {}
    while True:
        for node in net:
            for sub in itertools.combinations(net[node], r-1):
                q = list(sub) + [node]
                fail = False
                for a, b in itertools.combinations(q, 2):
                    if a not in net[b]:
                        fail = True
                        break
                if fail:
                    continue
                solutions[tuple(sorted(q))] = True
                print(f"Solution {q}")
        print(f"{len(solutions)}")
        if len(solutions) > 0:
            break
        r -= 1
        solutions = {}
    print(f"biggest network is size {r}")
    print(f"there are {len(solutions)} networks that big.")
    for k in solutions.keys():
        print(k)
        print(f"Password is {','.join(sorted(k))}")
    print(f"Part 2 Done.")


def main():
    part1()
    # part2()


if __name__ == "__main__":
    main()


'''
1: 8685429
10: 4700978
100: 15273692
2024: 8667524

Total: 37327623
'''

import itertools
import re
from functools import cache, partial
from dataclasses import dataclass
from collections import deque
from queue import PriorityQueue


MOD = 16777216


def read_input(file):
    with open(file,"r") as f:
        s = f.read().split("\n")
        s = [int(n) for n in s]
    return s


def mix_prune(n, s):
    n = n ^ s
    n = n % MOD
    return n


def calc_new(s):
    s = mix_prune(s * 64, s)
    s = mix_prune(s // 32, s)
    s = mix_prune(s * 2048, s)
    # print(f"calc_new returning {s}")
    return s


def part1():
    data = read_input("input22.txt")
    # data = read_input("input22_sample.txt")
    print(data)

    s = {}
    total = 0
    for d in data:
        curr = d
        for i in range(2000):
            curr = calc_new(curr)
            # if curr in s:
            #     print(f"Curr in s {curr}")
            s[curr] = curr
            # print(f"{curr = }")
            # cmd = input("Continue?")
        total += curr
    print(f"{total = }")


def calc_new_2(s,diff,price):
    n = calc_new(s)
    p = n % 10
    price.append(p)
    d = p - s % 10
    diff.append(d)
    return n


def part2():
    data = read_input("input22.txt")
    count = 2000
    # data = read_input("input22_sample.txt")
    # data = read_input("input22_part2.txt")
    # count = 2000
    # print(data)

    s = {}
    for start in data:
        diff = []
        price = []
        nums = []
        curr = start
        local = {}
        for i in range(count+4):
            curr = calc_new_2(curr, diff, price)
            nums.append(curr)
        for i in range(count-3):
            t = tuple(diff[i:i+4])
            if t not in local:
                p = price[i+3]
                local[t] = p
        for k, v in local.items():
            s[k] = s.get(k, 0) + v

    m = 0
    mk = None
    for k, v in s.items():
        if v > m:
            m = v
            mk = k
    print(f"Max = {m}  max key = {mk}")
    print(f"{''.join(str(mk).split())}")
    # The right answer: 2058 Bananas!  max key = (-1, 1, -1, 2)


def main():
    # part1()
    part2()


if __name__ == "__main__":
    main()


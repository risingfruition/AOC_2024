import itertools
import re
from functools import cache, partial


def read_input(file):
    with open(file,"r") as f:
        s = f.read().rstrip().split()
        s = map(partial(int), s)
    return list(s)


@cache
def breaker2(d):
    s = str(d)
    s_len = len(s)
    if s_len % 2 == 1:
        return []
    breakpoint = s_len // 2
    return [int(s[:breakpoint]), int(s[breakpoint:])]


def breaker(s):
    breakpoint = len(s) // 2
    return [int(s[:breakpoint]), int(s[breakpoint:])]


def breaker_d(d):
    blunk = []
    s = str(d)
    s_len = len(s)
    if s_len % 2 == 0:
        # print(s)
        blunk = blunk + breaker(s)
        # blunk.append(int(s[:s_len // 2]))
        # blunk.append(int(s[s_len // 2:]))
    return blunk


def blink(data):
    blunk = []
    for d in data:
        if d == 0:
            blunk.append(1)
            continue

        broke = breaker2(d)
        # broke_d = breaker_d(d)
        # if broke != broke_d:
        #     print(d, broke, broke_d)
        #     exit(0)
        if broke:
            blunk.extend(broke)
            continue

        # if broke_d:
        #     blunk.extend(broke_d)
        #     continue

        # s = str(d)
        # s_len = len(s)
        # if s_len % 2 == 0:
        #     # print(s)
        #     blunk = blunk + breaker(s)
        #     # blunk.append(int(s[:s_len // 2]))
        #     # blunk.append(int(s[s_len // 2:]))
        #     continue

        blunk.append(d * 2024)
    return blunk


running_count = 0


def main():
    data = read_input("input11.txt")
    # data = read_input("input11_sample.txt")
    print(f"data = {data}")
    data = data.split()
    data = map(partial(int), data)
    print(f"data = {data}")
    data = list(data)
    print(f"data = {data}")
    test_data = [125, 17]
    for i in range(6):
        test_data = blink(test_data)
    print(test_data)
    test_data = [125, 17]
    for i in range(25):
        test_data = blink(test_data)
    print(f"Test data has {len(test_data)} stones after 25 blinks.")
    # for i in range(75):
    #     print(i)
    #     data = blink(data)
    # print(f"Part 1 data has {len(data)} stones after 25 blinks.")

    test_data = [125, 17]
    depth = 6
    count = 0
    for d in test_data:
        count += deep_blink(d, depth)
        print(f"Count after {d}")
    print(f"Test data has {count} stones after {depth} deep_blinks.")
    test_data = [125, 17]
    depth = 25
    count = 0
    for d in test_data:
        count += deep_blink(d, depth)
        print(f"Count after {d}")
    print(f"Test data has {count} stones after {depth} deep_blinks.")

    depth = 25
    count = 0
    for d in data:
        count += deep_blink(d, depth)
        print(f"Count after {d}")
    print(f"Part 1 data has {count} stones after {depth} deep_blinks.")

    depth = 75
    count = 0
    for d in data:
        count += deep_blink(d, depth)
        print(f"Count after {d}")
    print(f"Part 2. Data has {count} stones after {depth} deep_blinks.")


# @cache
def convert(d):
    return str(d)


# @ cache
def break_in_half(s):
    s_len = len(s)
    return [int(s[:s_len // 2]), int(s[s_len // 2:])]


@cache
def get_values(d):
    if d == 0:
        return [1]
    s = convert(d)
    s_len = len(s)
    if s_len % 2 == 0:
        return break_in_half(s)
    return [d * 2024]


def deep_blink(d, depth):
    global running_count
    if depth == 0:
        running_count += 1
        if running_count % 100_000_000 == 0:
            print(f"{running_count = }")
        return 1
    # if depth > 30 and depth % 10 == 0:
    #     print(depth)
    count = 0
    for v in get_values(d):
        count += deep_blink(v, depth - 1)
    return count

    # if d == 0:
    #     return deep_blink(1, depth - 1)
    # s = convert(d)
    # s_len = len(s)
    # if s_len % 2 == 0:
    #     broken = break_in_half(s)
    #     assert len(broken) == 2
    #     count = deep_blink(broken[0], depth - 1)
    #     count += deep_blink(broken[1], depth - 1)
    #     return count
    # return deep_blink(d * 2024, depth - 1)


def fast_blink(data):
    stones = {}
    for d, count in data.items():
        for x in get_values(d):
            stones[x] = stones.get(x, 0) + count
    return stones


def main_2():
    data = read_input("input11.txt")
    # data = read_input("input11_sample.txt")
    print(f"data = {data}")

    # data = {125: 1, 17: 1}
    temp = {}
    for k in data:
        temp[k] = 1
    data = temp

    for i in range(1075):
        data = fast_blink(data)
        print(f"{len(data.keys()) = }")
        print(f"fast_blink {i}")
    total = 0
    for k, count in data.items():
        total += count
    # print(f"{data = }")
    print(f"{total = }")


if __name__ == "__main__":
    main_2()
    print(f"Day 11")


def test_breaker__245030__gives_245_and_30():
    d = 245030
    broken = breaker(str(d))

    assert broken == [245, 30]


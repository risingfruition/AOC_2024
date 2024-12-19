import itertools
import re
from functools import partial


def read_input(file):
    with open(file,"r") as f:
        s = f.readlines()
        s = map(str.rstrip, s)
    return list(s)


directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def neighbors(r, c):
    for dr, dc in directions:
        rr = r + dr
        cc = c + dc
        yield rr, cc


def trailhead(data):
    for r, line in enumerate(data):
        for c, ch in enumerate(line):
            if ch == '0':
                yield r, c


tt = 0
positions = set()


def dfs(data, r, c, depth, trail):
    assert trail is not None
    global tt
    global positions
    # if data[r][c] == '9' and depth == 10:
    #     # if depth == 9:
    #     tt += 1
    #     return 1
    total = 0
    for nr, nc in neighbors(r, c):
        if nr < 0 or nc < 0 or nr >= len(data) or nc >= len(data[0]):
            continue
        ch = data[nr][nc]
        if ch != '.' and int(ch) == depth:
            t = trail[:] + [(nr, nc)]
            if depth == 9:
                tt += 1
                positions.add((nr, nc))

                total += 1
                print(f"Trail {t}")
            else:
                total += dfs(data, nr, nc, depth + 1, t)
    # print(f"Returning {total} from depth {depth}")
    return total


def main():
    data = read_input("input10.txt")
    # data = read_input("input10_sample.txt")
    # data = read_input("input10_my.txt")
    nc = len(data[0])
    for i, line in enumerate(data):
        data[i] = data[i] + '.'
    data.append('.' * len(data[0]))
    total = 0
    trailheads = 0
    global positions
    for tr, tc in trailhead(data):
        positions = set()
        trailheads += 1
        # print(f"trailhead at r {tr}, c {tc}")
        sub = dfs(data, tr, tc, 1, [(tr, tc)])
        print(f"trainhead {sub = }")
        print(len(positions))
        total += len(positions)
    print(data)
    print(f"{trailheads=}")
    print(f"{tt = }")
    print(f"total {total}")


if __name__ == "__main__":
    main()
    print(f"Day 10")


def test_thing():
    assert False

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


def find_stuff(data, thing):
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            if col == thing:
                return r, c
    raise Exception(f"Expected to find {thing} in data.")


def convert(data) -> list[list[int]]:
    return [[(".#SE".index(ch)) - OFFSET for ch in row] for row in data]


def print_grid(g):
    for row in g:
        print(row)


def neighbors(grid, r, c):
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if nr < 0 or nc < 0 or nr >= len(grid) or nc >= len(grid[0]):
            continue
        if grid[nr][nc] != WALL:
            yield nr, nc


def bfs(r, c, er, ec, grid, write=False):
    d = {(r, c): 0}
    if write:
        # print(f"grid ({r},{c}) = {dist}")
        grid[r][c] = 0
    open = SimpleQueue()
    dist = 0
    open.put((r, c, dist))
    found = False
    while not open.empty():
        r, c, dist = open.get()
        dist += 1
        for nr, nc in neighbors(grid, r, c):
            if nr == er and nc == ec:
                if write:
                    # print(f"grid ({nr},{nc}) = {dist}")
                    grid[nr][nc] = dist
                found = True
                return dist, found
            if (nr, nc) in d:
                prev_dist = d[(nr, nc)]
                if dist < prev_dist:
                    if write:
                        # print(f"grid ({nr},{nc}) = {dist}")
                        grid[nr][nc] = dist
                    # if dist + 2 != prev_dist:
                    #     print(f"Not expecting better distances. {nr},{nc} {dist=} < {prev_dist=}")
                    open.put((nr, nc, dist))
                    d[(nr, nc)] = dist
            else:
                if write:
                    # print(f"grid ({nr},{nc}) = {dist}")
                    grid[nr][nc] = dist
                # print(f"putting {nr} {nc}")
                d[(nr, nc)] = dist
                open.put((nr, nc, dist))
    return 0, found


def count_diags(G):
    diags = 0
    for r, row in enumerate(G):
        for c, col in enumerate(row):
            if G[r][c] == EMPTY:
                if G[r][c+1] == WALL and G[r+1][c] == WALL and G[r+1][c+1] != WALL:
                    diags += 1
                if G[r][c-1] == WALL and G[r+1][c] == WALL and G[r+1][c-1] != WALL:
                    diags += 1
    return diags


def gen_cheats(G):
    r_len = len(G)
    c_len = len(G[0])
    for r, row in enumerate(G):
        for c, col in enumerate(row):
            if G[r][c] != WALL:
                for dr, dc in directions:
                    r1, c1 = r + dr, c + dc
                    r2, c2 = r1 + dr, c1 + dc
                    if r2 < 0 or c2 < 0 or r2 >= r_len or c2 >= c_len:
                        continue
                    if G[r1][c1] == WALL and G[r2][c2] != WALL:
                        yield r1, c1, r2, c2


def smallest_around(r, c, G):
    r_len = len(G)
    c_len = len(G[0])
    x = too_costly
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if nr < 0 or nc < 0 or nr >= r_len or nc >= c_len:
            continue
        val = G[nr][nc]
        if val >= 0:
            if x > val:
                x = val
    return x


def calc_dist(c, from_start, from_end):
    r1, c1, r2, c2 = c
    val_fs = smallest_around(r1, c1, from_start)
    new_dist = val_fs + 2 + from_end[r2][c2]
    return new_dist


def part1():
    G = read_input("input20.txt")
    # G = read_input("input20_sample.txt")
    print_grid(G)
    from_start = convert(G)
    from_end = convert(G)
    G = convert(G)
    r, c = find_stuff(G, START)
    er, ec = find_stuff(G, END)
    print_grid(G)
    print(r, c, er, ec)
    leng_best, found = bfs(r, c, er, ec, G)
    print(f"{leng_best = }")
    bfs(r, c, er, ec, from_start, True)
    print()
    print("From Start")
    print_grid(from_start)
    bfs(er, ec, r, c, from_end, True)
    print()
    print(f"From End")
    print_grid(from_end)
    best = leng_best
    total_saves = 0
    saving = {}
    for c in gen_cheats(G):
        print(c)
        dist = calc_dist(c, from_start, from_end)
        if dist <= best - 100:
            saves = best - dist
            total_saves += 1
            saving[saves] = saving.get(saves, 0) + 1
        else:
            saves = 0
        print(f"{best = }  {dist = }  {saves = }")
    print(f"{total_saves = }")
    print(f"{saving = }")
    diags = count_diags(G)
    print(f"{diags = }")


def calc_dist_2(c, from_start, from_end):
    r1, c1, r2, c2 = c
    # val_fs = smallest_around(r1, c1, from_start)
    val_fs = from_start[r1][c1]
    separation = abs(r1 - r2) + abs(c1 - c2)
    new_dist = val_fs + separation + from_end[r2][c2]
    return new_dist


def gen_cheats_2(G):
    r_len = len(G)
    c_len = len(G[0])
    for r, row in enumerate(G):
        for c, col in enumerate(row):
            if G[r][c] != WALL:
                for er, erow in enumerate(G):
                    for ec, ecol in enumerate(erow):
                        if er < 0 or ec < 0 or er >= r_len or ec >= c_len:
                            continue
                        if G[er][ec] != WALL:
                            # do we need to have a WALL-only path??? NO.
                            dist = abs(r - er) + abs(c - ec)
                            if dist > 20:
                                continue
                            yield r, c, er, ec


def part2():
    G = read_input("input20.txt")
    cheat_by = 100
    # G = read_input("input20_sample.txt")
    # cheat_by = 50
    print_grid(G)
    from_start = convert(G)
    from_end = convert(G)
    G = convert(G)
    r, c = find_stuff(G, START)
    er, ec = find_stuff(G, END)
    print(r, c, er, ec)
    leng_best, found = bfs(r, c, er, ec, G)
    assert found
    print(f"{leng_best = }")
    bfs(r, c, er, ec, from_start, True)
    bfs(er, ec, r, c, from_end, True)
    best = leng_best
    total_saves = 0
    saving = {}
    for c in gen_cheats_2(G):
        # print(c)
        dist = calc_dist_2(c, from_start, from_end)
        if dist <= best - cheat_by:
            saves = best - dist
            total_saves += 1
            saving[saves] = saving.get(saves, 0) + 1
        else:
            saves = 0
        # print(f"{best = }  {dist = }  {saves = }")
    print(f"{total_saves = }")
    for i in range(50, 100):
        if i in saving:
            print(f"  - There are {saving[i]} cheats that save {i} picoseconds.")
    # print(f"{saving = }")


def main():
    # Part 1 sample has 44 cheats that save time.
    # part1()
    part2()


if __name__ == "__main__":
    main()
    print(f"Day 20")


def test_stuff():
    assert False

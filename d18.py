import itertools
import re
from functools import cache, partial
from dataclasses import dataclass
from collections import deque
from queue import PriorityQueue, LifoQueue, SimpleQueue

#     s = map(str.rstrip, s)
#     # s = map(colon_blow, s)
#     # s = map(join_list, s)
#     # s = map(str.split, s)
#     # s = map(list_int, s)
#     s = list(s.strip())
# with open(file, "r") as f:
#     rules, updates = tuple(f.read().strip().split("\n\n"))
#     rules = rules.split()
#     rules = map(str.strip, rules)
#     rules = map(goober, rules)
#     print(list(rules))
#     print("------")
#     updates = updates.split()
#     updates = [u.split(',') for u in updates]
#     updates = [list(map(int, u)) for u in updates]
#     print(list(updates))
# return rules, updates


def read_input(file):
    with open(file,"r") as f:
        s = f.read().split("\n")
        s = [str.split(line, ',') for line in s]
        print(s)
        s = [[int(n) for n in nums] for nums in s]
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
too_many = 999_999


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


def bfs(r, c, er, ec, grid):
    d = {(r, c): 0}
    open = SimpleQueue()
    dist = 0
    open.put((r, c, dist))
    found = False
    while not open.empty():
        r, c, dist = open.get()
        dist += 1
        for nr, nc in neighbors(grid, r, c):
            if nr == er and nc == ec:
                found = True
                return dist, found
            if (nr, nc) in d:
                prev_dist = d[(nr, nc)]
                if dist < prev_dist:
                    # if dist + 2 != prev_dist:
                    #     print(f"Not expecting better distances. {nr},{nc} {dist=} < {prev_dist=}")
                    open.put((nr, nc, dist))
                    d[(nr, nc)] = dist
            else:
                # print(f"putting {nr} {nc}")
                d[(nr, nc)] = dist
                open.put((nr, nc, dist))
    return 0, found

def main():
    # data = read_input("input18_sample.txt")
    # size = 7
    # end = size - 1
    # num_bytes = 12

    data = read_input("input18.txt")
    size = 71
    end = size - 1
    num_bytes = 1024
    num_bytes = len(data)  # 3450
    num_bytes = 2222  # Found
    num_bytes = 2822  # Found
    num_bytes = 3122  # Not found
    num_bytes = 2988  # Not found
    num_bytes = 2930  # Found
    num_bytes = 2960  # Found
    num_bytes = 2974  # Found
    num_bytes = 2981  # Not found
    num_bytes = 2978  # Not found
    # num_bytes = 2976  # Not found -- I do range(num_bytes) below, which goes until i=2975,
    # and which is line 2976 in the input file. OFF BY ONE ERRORS!!!!!!!!!!!!!
    num_bytes = 2975  # Found

    print(data)
    grid = [[0 for i in range(size)] for j in range(size)]
    for i in range(num_bytes):
        x, y = data[i]
        print(x,y)
        grid[y][x] = WALL

    dist, found = bfs(0, 0, end, end, grid)
    print_grid(grid)
    print(f"{dist = } {found = }")
    print(f"{len(grid) = } {len(grid[0]) = }")
    print(f"Size of data: {len(data)}")
    # Part 1: 646 is not right.
    # Part 1: 882 is not right.
    # Part 1: 276 is right.
    print(f"Day 18 Part 1")

    grid = [[0 for i in range(size)] for j in range(size)]
    for i in range(len(data)):
        x, y = data[i]
        # print(f"{data[i]}")
        grid[y][x] = WALL
        dist, found = bfs(0, 0, end, end, grid)
        if not found:
            print(f"This one cut it off: {i=}: {data[i][0]},{data[i][1]}")
            break

    print(f"Day 18 Part 2: 60,37")


if __name__ == "__main__":
    main()
    print(f"Day 18")


def test_node__less_than__implementation_works():
    assert False

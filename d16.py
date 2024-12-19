import itertools
import re
from functools import cache, partial
from dataclasses import dataclass
from collections import deque
from queue import PriorityQueue


def read_input(file):
    with open(file,"r") as f:
        s = f.read().split("\n")
    return s


def find(data, ch):
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            if col == ch:
                return r, c
    raise Exception(f"No character {ch} in data.")


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

class Node:
    def __init__(self, cost: int, est: int, r: int, c: int, facing: int, parent):
        self.cost = cost
        self.est = est
        self.r = r
        self.c = c
        self.facing = facing
        self.parent = parent

    def __lt__(self, other):
        return self.cost + self.est < other.cost + other.est


def is_wall_at(data, r, c, dir):
    dr, dc = directions[dir]
    if WALL == data[r + dr][c + dc]:
        return 1
    return 0


def is_dead_end(data, r, c):
    count = 0
    for dir in range(NUM_DIRECTIONS):
        count += is_wall_at(data, r, c, dir)
    return count == 3


def find_empty_around(data, r, c):
    for dr, dc in directions:
        thing = data[r + dr][c + dc]
        if thing == START or thing == END:
            return False, 0, 0
        if thing == EMPTY:
            return True, r + dr, c + dc
    raise Exception(f"Expected to find empty spot around {r}, {c}.")


def follow(data, r, c):
    more_dead = True
    while more_dead:
        more_dead = False
        found, er, ec = find_empty_around(data, r, c)
        if not found:
            return
        if is_dead_end(data, er, ec):
            print(f"Filling {er},{ec}")
            data[er][ec] = WALL
            r, c = er, ec
            more_dead = True


def fill_dead(data):
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            if col == EMPTY:
                if is_dead_end(data, r, c):
                    print(f"Dead end at {r},{c}")
                    data[r][c] = WALL
                    follow(data, r, c)


def convert(data) -> list[list[int]]:
    return [[".#SE".index(ch) for ch in row] for row in data]


def print_data(data):
    for r, row in enumerate(data):
        print(f"{r} {row}")


def find_stuff(data, thing):
    for r, row in enumerate(data):
        for c, col in enumerate(row):
            if col == thing:
                return r, c
    raise Exception(f"Expected to find {thing} in data.")


TURN_CHARGE = 1000
facing_charge = {
    DOWN: 2 * TURN_CHARGE,
    UP: TURN_CHARGE,
    RIGHT: TURN_CHARGE,
    LEFT: 2 * TURN_CHARGE
}


def heuristic(r, c, facing, er, ec):
    # End is up right (lowest r) and (highest c)
    # This does not yet take turns into consideration.
    if c == ec:
        return r - er
    if r == er:
        return ec - c
    return r - er + ec - c + facing_charge[facing]


def neighbors(data, r, c, facing):
    for new_facing in facing_next[facing]:
        dr, dc = directions[new_facing]
        if new_facing != facing:
            yield r, c, new_facing
        else:
            nr, nc = r + dr, c + dc
            if data[nr][nc] != WALL:
                yield nr, nc, new_facing


def solve(best, data: list[list[int]], r: int, c: int, facing: int, er: int, ec: int):
    closed = []
    open: PriorityQueue = PriorityQueue()
    cost = 0
    est = heuristic(r, c, facing, er, ec)
    parent = None
    node = Node(cost, est, r, c, facing, parent)
    open.put(node)
    best_node = None
    while not open.empty():
        node = open.get()
        closed.append(node)
        if node.r == er and node.c == ec:
            if not best_node:
                best_node = node
                print(f"First best_node cost={node.cost}")
            elif best_node.cost > node.cost:
                print(f"New best_node cost={node.cost} < {best_node.cost}")
                best_node = node
            else:
                pass  # No new best node

        print(f"Node cost={node.cost} est={node.est}  r={node.r}  c={node.c}  f={facing_text[node.facing]}")
        for nr, nc, nf in neighbors(data, node.r, node.c, node.facing):
            cost = node.cost
            if nf != node.facing:
                cost += TURN_CHARGE
            else:
                cost = node.cost + 1  # ALSO NEED THIS IF NR NC NOT EQUAL NODE R OR C
            est = heuristic(nr, nc, nf, er, ec)
            location = (nr, nc, nf)
            prev = best.get(location, too_costly)
            curr = cost + est
            print(f"     {cost=} {est=} {nr=} {nc=} nf={facing_text[nf]} {prev=} {curr=}")
            if prev == too_costly:
                # this is the first time adding this node.
                print(f"       Add first time.")
                best[location] = curr
                open.put(Node(cost, est, nr, nc, nf, node))
            elif prev > curr:
                # Current node is better than any previous one at this location.
                print(f"       Add better node.")
                best[location] = curr
                open.put(Node(cost, est, nr, nc, nf, node))
            else:
                # prev is still the best value.
                # Therefore: do not put this neighbor on the open list.
                print(f"  ----")
                pass
            # com = input("Continue?")
    small = too_costly
    end_facing = 0
    for facing in range(NUM_DIRECTIONS):
        stuff = best.get((er, ec, facing), -1)
        if 0 < stuff < small:
            small = stuff
            end_facing = facing
    print(f"Lowest cost = {small} facing {facing_text[facing]}.")
    for f in range(4):
        print(f"{best.get((er, ec, f), 0) = }")
    # Part 1 24036 is too low.
    path = []
    node = best_node
    while node:
        path.append((node.cost, node.r, node.c, facing_text[node.facing]))
        node = node.parent
    print()
    print("Path:")
    print(path)

def main():
    data = read_input("input16.txt")
    # data = read_input("input16_sample.txt")
    print(data)
    data = convert(data)
    print(data)
    fill_dead(data)
    print_data(data)
    sr, sc = find_stuff(data, START)
    er, ec = find_stuff(data, END)
    data[er][ec] = EMPTY
    data[sr][sc] = EMPTY
    facing: int = RIGHT
    best = {(sr, sc, facing): 0}
    solve(best, data, sr, sc, facing, er, ec)
    small = 9999999999999
    for facing in range(NUM_DIRECTIONS):
        stuff = best.get((er, ec, facing), -1)
        if 0 < stuff < small:
            small = stuff
    print(f"Part 1 Best cost is {small}")  # 85420


if __name__ == "__main__":
    main()
    print(f"Day 16")


def test_node__less_than__implementation_works():
    a = Node(10, 0, 0, 0, 0, None)
    b = Node(22, 0, 0, 0, 0, None)
    assert a < b

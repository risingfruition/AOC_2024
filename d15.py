import itertools
import re
from functools import cache, partial


def read_input(file):
    with open(file,"r") as f:
        s = f.read().rstrip().split("\n\n")
        warehouse = s[0].split()
        moves = s[1].split()
        moves = ''.join(moves)
    return warehouse, moves


EMPTY = 0
WALL = 1
BOX = 2
ROBOT = 3

DOWN = 0
UP = 1
RIGHT = 2
LEFT = 3
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
move_dir = "v^><"


def move(data, r, c, move_ch):
    print(f"Move {move_ch}")
    dr, dc = directions[move_dir.index(move_ch)]
    blocks = 1
    boxes = 0
    assert data[r][c] == ROBOT
    while True:
        nr = r + dr * blocks
        nc = c + dc * blocks
        ch = data[nr][nc]
        if ch == WALL:
            break
        if ch == BOX:
            boxes += 1
            blocks += 1
            continue
        if ch == EMPTY:
            while boxes > 0:
                data[nr][nc] = BOX
                boxes -= 1
                blocks -= 1
                nr = r + dr * blocks
                nc = c + dc * blocks

            data[r][c] = EMPTY
            data[nr][nc] = ROBOT
            r, c = nr, nc
            break
        raise Exception(f'unexpected input {ch}')
    return r, c


def gps_sum(data):
    gps = 0
    for r, row in enumerate(data):
        for c, stuff in enumerate(row):
            if stuff == BOX:
                gps += r * 100 + c
    return gps


def convert_warehouse(warehouse):
    return [[".#O@".index(ch) for ch in w] for w in warehouse]


def find_robot(data):
    for r, row in enumerate(data):
        for c, ch in enumerate(row):
            if ch == ROBOT:
                return r, c
    raise Exception(f"There is no robot")


def print_data(data):
    for row in data:
        print(row)


def main():
    warehouse, moves = read_input("input15.txt")
    # warehouse, moves = read_input("input15_sample.txt")
    # warehouse, moves = read_input("input15_tiny.txt")
    # warehouse, moves = read_input("input15_micro.txt")
    print(f"{warehouse = }")
    print(f"{moves = }")
    data = convert_warehouse(warehouse)

    r, c = find_robot(data)
    for ch in moves:
        r, c = move(data, r, c, ch)
    print_data(data)
    sum = gps_sum(data)
    print(f"{sum = }")


if __name__ == "__main__":
    main()
    print(f"Day 11")


def test_stuff():
    assert False

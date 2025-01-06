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

T_EMPTY = 0
T_WALL = 1
T_LEFT = 2
T_RIGHT = 3
T_ROBOT = 4

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


def find_robot_2(data):
    for r, row in enumerate(data):
        for c, ch in enumerate(row):
            if ch == T_ROBOT:
                return r, c
    raise Exception(f"There is no robot")


def print_data(data):
    for row in data:
        print(row)


def part_1():
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


ex = {".": "..", "#": "##", "O": "[]", "@": "@."}


def expand_warehouse_2(warehouse):
    w = [[ex[ch] for ch in row] for row in warehouse]
    t = []
    for line in w:
        t.append(''.join(line))
    return t


def convert_warehouse_2(warehouse):
    return [[".#[]@".index(ch) for ch in w] for w in warehouse]


def gps_sum_2(data):
    gps = 0
    for r, row in enumerate(data):
        for c, stuff in enumerate(row):
            if stuff == T_LEFT:
                gps += r * 100 + c
    return gps


def can_move_up(data, r, c, boxes):
    spot = data[r-1][c]
    if spot == T_EMPTY:
        return True
    if spot == T_WALL:
        return False
    if spot == T_LEFT:
        if (r-1, c) not in boxes:
            boxes.append((r-1, c))
        return can_move_up(data, r-1, c, boxes) and can_move_up(data, r-1, c+1, boxes)
    if spot == T_RIGHT:
        if (r-1, c-1) not in boxes:
            boxes.append((r-1, c-1))
        return can_move_up(data, r-1, c-1, boxes) and can_move_up(data, r-1, c, boxes)


def can_move_down(data, r, c, boxes):
    spot = data[r + 1][c]
    if spot == T_EMPTY:
        return True
    if spot == T_WALL:
        return False
    if spot == T_LEFT:
        if (r+1, c) not in boxes:
            boxes.append((r + 1, c))
        return can_move_down(data, r + 1, c, boxes) and can_move_down(data, r + 1, c + 1, boxes)
    if spot == T_RIGHT:
        if (r+1, c-1) not in boxes:
            boxes.append((r + 1, c - 1))
        return can_move_down(data, r + 1, c - 1, boxes) and can_move_down(data, r + 1, c, boxes)


def can_move_left(data, r, c, boxes):
    spot = data[r][c-1]
    if spot == T_EMPTY:
        return True
    if spot == T_WALL:
        return False
    if spot == T_RIGHT:
        if (r, c-2) in boxes:
            raise ValueError("can_move_left box already added")
        boxes.append((r, c-2))
        return can_move_left(data, r, c-2, boxes)
    if spot == T_LEFT:
        raise ValueError("Not possible to see T_LEFT when moving left.")


def can_move_right(data, r, c, boxes):
    spot = data[r][c+1]
    if spot == T_EMPTY:
        return True
    if spot == T_WALL:
        return False
    if spot == T_LEFT:
        if (r, c+1) in boxes:
            raise ValueError("can move right box already added")
        boxes.append((r, c+1))
        return can_move_right(data, r, c+2, boxes)
    if spot == T_RIGHT:
        raise ValueError("Not possible to see T_RIGHT when moving right.")


def move_up(data, r, c, boxes):
    boxes = sorted(boxes)
    # print(f"move_up {boxes=}")
    for box in boxes:
        br, bc = box
        assert data[br-1][bc] == T_EMPTY
        assert data[br-1][bc+1] == T_EMPTY
        data[br-1][bc] = T_LEFT
        data[br-1][bc+1] = T_RIGHT
        data[br][bc] = T_EMPTY
        data[br][bc+1] = T_EMPTY
    assert data[r][c] == T_ROBOT
    assert data[r-1][c] == T_EMPTY
    data[r][c] = T_EMPTY
    data[r-1][c] = T_ROBOT


def move_down(data, r, c, boxes):
    boxes = sorted(boxes, reverse=True)
    for box in boxes:
        br, bc = box
        assert data[br + 1][bc] == T_EMPTY
        assert data[br + 1][bc + 1] == T_EMPTY
        data[br + 1][bc] = T_LEFT
        data[br + 1][bc + 1] = T_RIGHT
        data[br][bc] = T_EMPTY
        data[br][bc + 1] = T_EMPTY
    assert data[r][c] == T_ROBOT
    assert data[r+1][c] == T_EMPTY
    data[r][c] = T_EMPTY
    data[r+1][c] = T_ROBOT


def move_right(data, r, c, boxes):
    for box in reversed(boxes):
        br, bc = box
        assert data[br][bc] == T_LEFT
        assert data[br][bc+2] == T_EMPTY
        data[br][bc] = T_EMPTY
        data[br][bc+1] = T_LEFT
        data[br][bc+2] = T_RIGHT
    assert data[r][c] == T_ROBOT
    assert data[r][c+1] == T_EMPTY
    data[r][c+1] = T_ROBOT
    data[r][c] = T_EMPTY


def move_left(data, r, c, boxes):
    for box in reversed(boxes):
        br, bc = box
        assert data[br][bc-1] == T_EMPTY
        assert data[br][bc+1] == T_RIGHT
        data[br][bc-1] = T_LEFT
        data[br][bc] = T_RIGHT
        data[br][bc+1] = T_EMPTY
    assert data[r][c] == T_ROBOT
    assert data[r][c-1] == T_EMPTY
    data[r][c-1] = T_ROBOT
    data[r][c] = T_EMPTY


str_dir = ["DOWN", "UP", "RIGHT", "LEFT"]


def inform(boxes):
    return boxes and len(boxes) > 1


def move_2(data, r, c, dir):
    # print(f"Move {str_dir[dir]}")
    dr, dc = directions[dir]
    nr = r + dr
    nc = c + dc
    assert data[r][c] == T_ROBOT
    boxes = []
    if dir == UP:
        if can_move_up(data, r, c, boxes):
            if inform(boxes):
                print(f"Move {str_dir[dir]}  boxes={boxes}")
                before = make_text_data(data)
            move_up(data, r, c, boxes)
            if inform(boxes):
                after = make_text_data(data)
                for b,a in zip(before, after):
                    print(f"{b}   {a}")
            return nr, nc
    elif dir == DOWN:
        if can_move_down(data, r, c, boxes):
            move_down(data, r, c, boxes)
            return nr, nc
    elif dir == RIGHT:
        if can_move_right(data, r, c, boxes):
            move_right(data, r, c, boxes)
            return nr, nc
    elif dir == LEFT:
        if can_move_left(data, r, c, boxes):
            move_left(data, r, c, boxes)
            return nr, nc
    return r, c


def make_text_data(data):
    grid = []
    for row in data:
        s = "".join(['.#[]@'[r] for r in row])
        grid.append(s)
    return grid


def text_data(data):
    for row in make_text_data(data):
        print(row)


def part_2():
    warehouse, moves = read_input("input15.txt")
    # warehouse, moves = read_input("input15_sample.txt")
    # warehouse, moves = read_input("input15_tiny.txt")
    # warehouse, moves = read_input("input15_micro.txt")
    print(f"{warehouse = }")
    print(f"{moves = }")
    print(warehouse)
    print(f"Original up above")
    warehouse = expand_warehouse_2(warehouse)
    print(warehouse)
    data = convert_warehouse_2(warehouse)
    r, c = find_robot_2(data)
    print(f"Robot at ({r},{c})")
    for ch in moves:
        r, c = move_2(data, r, c, move_dir.index(ch))
        # print_data(data)
    print_data(data)
    text_data(data)
    sum = gps_sum_2(data)
    print(f"{sum = }")


def main():
    # part_1()
    part_2()


if __name__ == "__main__":
    print(f"Day 11")
    print(f"Part 1 answer is 1360570")
    main()


def test_move_group_down__cant_move__returns_false():
    house = [
        '#######',
        '#......',
        '#...@..',
        '#..[]..',
        '#...[].',
        '#..[]..',
        '#######',
    ]
    data = convert_warehouse_2(house)
    r, c = find_robot_2(data)
    boxes = []
    can_move = can_move_down(data, r, c, boxes)
    assert not can_move


def test_move_group_down__move_down__moves_all_boxes():
    house = [
        '#######',
        '#......',
        '#...@..',
        '#..[]..',
        '#...[].',
        '#..[]..',
        '#......',
        '#......',
        '#######',
    ]
    data = convert_warehouse_2(house)
    r, c = find_robot_2(data)
    boxes = []
    can_move = can_move_down(data, r, c, boxes)
    assert can_move


def test_move_group_left__cant_move__returns_false():
    house = [
        '#######',
        '#......',
        '#[][]@.',
        '#......',
        '#######',
    ]
    data = convert_warehouse_2(house)
    r, c = find_robot_2(data)
    boxes = []
    can_move = can_move_left(data, r, c, boxes)
    assert len(boxes) == 2
    assert not can_move


def test_move_group_left__can_move__returns_true():
    house = [
        '########',
        '#.......',
        '#.[][]@.',
        '#.......',
        '########',
    ]
    data = convert_warehouse_2(house)
    r, c = find_robot_2(data)
    boxes = []
    can_move = can_move_left(data, r, c, boxes)
    assert len(boxes) == 2
    assert can_move


def test_move_group_left__moves_all_boxes():
    house = [
        '########',
        '#.......',
        '#.[][]@.',
        '#.......',
        '########',
    ]
    house_after = [
        '########',
        '#.......',
        '#[][]@..',
        '#.......',
        '########',
    ]
    data = convert_warehouse_2(house)
    r, c = find_robot_2(data)
    boxes = []
    can_move = can_move_left(data, r, c, boxes)
    assert len(boxes) == 2
    assert can_move
    move_left(data, r, c, boxes)
    data_expect = convert_warehouse_2(house_after)
    assert data == data_expect


def test_move_up_tree__cant_move__returns_false():
    house = [
        '######',
        '[][][]',
        '.[][].',
        '..[]..',
        '...@..',
        '......',
        '......',
        '######',
    ]
    data = convert_warehouse_2(house)
    r, c = find_robot_2(data)
    boxes = []
    can_move = can_move_up(data, r, c, boxes)
    assert not can_move


def test_move_up_tree__can_move__returns_true():
    house = [
        '######',
        '......',
        '[][][]',
        '.[][].',
        '..[]..',
        '...@..',
        '......',
        '######',
    ]
    data = convert_warehouse_2(house)
    r, c = find_robot_2(data)
    boxes = []
    can_move = can_move_up(data, r, c, boxes)
    assert len(boxes) == 6
    assert can_move


def test_tree_can_move_up__move_up__moves_all():
    house = [
        '######',
        '......',
        '[][][]',
        '.[][].',
        '..[]..',
        '...@..',
        '......',
        '######',
    ]
    house_after = [
        '######',
        '[][][]',
        '.[][].',
        '..[]..',
        '...@..',
        '......',
        '......',
        '######',
    ]
    data = convert_warehouse_2(house)
    r, c = find_robot_2(data)
    boxes = []
    can_move = can_move_up(data, r, c, boxes)
    assert len(boxes) == 6
    assert can_move
    move_up(data, r, c, boxes)
    data_expect = convert_warehouse_2(house_after)
    assert data == data_expect

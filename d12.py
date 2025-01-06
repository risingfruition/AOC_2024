import itertools
import re
from functools import cache, partial
from d12_region import (
    LEFT,
    RIGHT,
    UP,
    DOWN,
    NUM_DIRECTIONS,
    corners,
    directions,
    opposite_compass,
    all_neighbors,
    Region,
    Regions,
)


def read_input(file):
    with open(file,"r") as f:
        s = f.read().rstrip().rsplit()
    return s


def neighbor_to(d, r, c):
    dr, dc = directions[d]
    return r + dr, c + dc


regions = []
added = {}


def main():
    data = read_input("input12.txt")
    # data = read_input("input12_sample.txt")
    # data = read_input("input12_diagonal.txt")
    # data = read_input("input12_small.txt")
    for d in data:
        print(d)
    regs = Regions()
    for r, row in enumerate(data):
        for c, plant in enumerate(row):
              regs.add_plot(data, r, c)
    print(f"Part 1: Total fence cost = {regs.fence_cost()}")

    corner_count = 0
    price = 0
    for reg in regs.regs:
        sides = reg.sides()
        corner_count += sides
        area = reg.area()
        p = sides * area
        print(f"Region {reg.plant}  {sides=}  {area=}  {p=}")
        price += p
    print(f"Part 2: {corner_count = } {price = }")
    # Correct price is 851994


def is_land_locked(plots, r, c):
    for dr, dc in all_neighbors(r, c):
        if (r, c) not in plots:
            return False
    return True


def count_lines(plots, r, c):
    count = []
    for dr, dc in directions:
        if (r + dr, c + dc) in plots:
            count.append((dr, dc))
    return count


def is_up_left_corner(plots, r, c):
    return neighbor_to(LEFT, r, c) not in plots and neighbor_to(UP, r, c) not in plots


def find_up_left_corner(plots):
    for r, c in plots.keys():
        if is_up_left_corner(plots, r, c):
            return r, c


def inwise_turn(dir, outwise):
    return opposite_compass[outwise], dir


def outwise_turn(dir, outwise):
    return outwise, opposite_compass[dir]


def lines(plots, r, c, plant):
    # FIX
    # NEED TO SOMEHOW MARK plots as checked without
    # excluding them. Maybe store the directions that have
    # been used. Then, if an (r, c) has the same direction,
    # we are done with that loop, or something is wrong.

    # FIX
    # Also, for plot holes (a plot inside a plot), there
    # may be no up_left corner. Change so those get found.
    # Maybe go without marking or counting lines until you
    # turn a corner.

    # This calcs # perimeter lines for one region
    # All plot values == plant when this is called.
    # r, c is a top left corner, due to the direction data was scanned.
    r, c = find_up_left_corner(plots)
    line_count = 1
    dir = RIGHT
    outwise = UP
    start = (outwise, r, c)
    print(f"Start: {r},{c} {dir=} {outwise=} {plant=}")
    stop_after = 20
    while True:
        # stop_after -= 1
        # if stop_after <= 0:
        #     print(f"Stopping after too many.")
        #     break
        nr, nc = neighbor_to(dir, r, c)

        # in-wise turn
        if (nr, nc) not in plots:
            # r, c - no change
            dir, outwise = inwise_turn(dir, outwise)
            print(f"Inwise turn: {r},{c} {dir=} {outwise=}")
            if start == (outwise, r, c):
                break
            line_count += 1
            continue

        nr, nc = neighbor_to(outwise, nr, nc)
        # Go straight
        if (nr, nc) not in plots:
            r, c = neighbor_to(dir, r, c)
            print(f"Straight   : {r},{c} {dir=} {outwise=}")
            if start == (outwise, r, c):
                break
            continue

        # Outwise turn
        dir, outwise = outwise_turn(dir, outwise)
        r, c = nr, nc
        print(f"Outwise turn   : {r},{c} {dir=} {outwise=}")
        if start == (outwise, r, c):
            break
        line_count += 1
    return line_count


def corner_pairs(r, c):
    for (ar, ac), (br, bc) in itertools.pairwise(directions + [directions[0]]):
        yield (r + ar, c + ac), (r + br, c + bc)


if __name__ == "__main__":
    main()
    print(f"Day 12")
    print(f"Part 1: Sample fence cost is 1930.")
    print(f"Part 1: Answer: 1400386")


def test_corners__inside_and_outside_corners_counted():
    plots = {
        (0,0): True,
        (0,1): True,
        (1,1): True,
    }
    expect = 6
    result = corners(plots)
    assert expect == result


def test_corner_pairs__generates_4_sets():
    count = 0
    for a, b in corner_pairs(0, 0):
        count += 1
    assert count == 4


def test_region__connected_rc__is_touching_returns_true():
    data = read_input("input12_sample.txt")
    reg = Region(data, 1, 3)
    print(reg)
    r, c = 2, 3  # On next line below: touching.
    expected = True
    assert expected == reg.is_touching(r, c)

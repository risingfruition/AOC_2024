import itertools
import re
from functools import cache, partial


# with open(file,"r") as f:
#     s = f.read().strip()
#     s = map(str.rstrip, s)
#     # s = map(colon_blow, s)
#     # s = map(join_list, s)
#     # s = map(str.split, s)
#     # s = map(list_int, s)
#     s = list(s.strip())
# return s
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
    with open(file, "r") as f:
        s = f.read().rstrip().rsplit()
        s = map(partial(re.findall, r"-?\d+"), s)
        s = list(s)
    return s


class Robot:
    def __init__(self, p, v, x, y):
        self.px = p[0]
        self.py = p[1]
        self.vx = v[0]
        self.vy = v[1]
        self.size_x = x
        self.size_y = y

    def pos(self, steps):
        x = self.px + self.vx * steps
        x = x % self.size_x
        y = self.py + self.vy * steps
        y = y % self.size_y
        return (
            x,
            y
        )


def read_sample_input():
    data = read_input("input14_sample.txt")
    return data, 11, 7


def read_full_input():
    data = read_input("input14.txt")
    return data, 101, 103


def main():
    data, size_x, size_y = read_full_input()
    # data, size_x, size_y = read_sample_input()
    print(data)
    data = [[int(num) for num in d] for d in data]
    robots = []
    for i in range(len(data) // 2):
        robot = i * 2
        robots.append(Robot(tuple(data[robot]), tuple(data[robot+1]), size_x, size_y))
    print(robots)

    quad = [0, 0, 0, 0]
    positions = {}
    half_x = size_x // 2
    half_y = size_y // 2
    for r in robots:
        pos = r.pos(100)
        print(pos)
        if pos[0] == half_x or pos[1] == half_y:
            continue
        if pos[0] < half_x:
            if pos[1] < half_y:
                quad[0] += 1
            else:
                quad[1] += 1
        else:
            if pos[1] < half_y:
                quad[2] += 1
            else:
                quad[3] += 1

    print(quad)
    result = quad[0] * quad[1] * quad[2] * quad[3]
    print(f"Part 1: Result = {result}")

    i = 0
    while True:
        grid = [[0 for _ in range(size_x)] for _ in range(size_y)]
        for r in robots:
            pos = r.pos(i)
            grid[pos[1]][pos[0]] += 1
        tree_grid = []
        for g in grid:
            tree_line = ''.join(['.' if item == 0 else str(item) for item in g])
            tree_grid.append(tree_line)
        print(i)
        for line in range(25):
            print(tree_grid[line])
        # if (is_balanced(tree_grid[10]) and is_balanced(tree_grid[20]) and
        #         is_balanced(tree_grid[30]) and is_balanced(tree_grid[40])):
        #     for tree_line in tree_grid:
        #         print(tree_line)
        # else:
        #     i += 1
        #     continue
        print()
        print(i)
        command = input("Input: ")
        if command == "b":
            break
        if command == "p":
            i -= 2
        elif command == 'a':
            for line in tree_grid:
                print(line)
            print()
            print(i)
        elif command != '':
            i = int(command) - 1
        i += 1


def is_balanced(s):
    air = re.findall(r"^([\\.]*)", s)
    left = air[0]
    air = re.findall(r"([\\.]*)$", s)
    right = air[0]

    return left == right


if __name__ == "__main__":
    main()
    print(f"Day 14")
    print(f"Day 14 Part 1: Sample ???.")
    print(f"Day 14 Part 1: Answer: ???")


def test_is_balanced__returns_true__when_dots_are_balanced():
    s = "...44444..."
    result = is_balanced(s)
    assert result


def test_is_balanced__returns_false__when_dots_are_unbalanced():
    s = "........44444.."
    result = is_balanced(s)
    assert result == False

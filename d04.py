import re
from functools import partial


def look_there(framed, f, c, dx, dy):
    s = ''
    for i in range(4):
        s += framed[f+dx*i][c+dy*i]
    if s == 'XMAS':
        return 1
    return 0


def look(framed, f, c):
    sum = 0
    sum += look_there(framed, f, c, 1, 0)
    sum += look_there(framed, f, c, 1, 1)
    sum += look_there(framed, f, c, 0, 1)
    sum += look_there(framed, f, c, -1, 1)
    sum += look_there(framed, f, c, -1, 0)
    sum += look_there(framed, f, c, -1, -1)
    sum += look_there(framed, f, c, 0, -1)
    sum += look_there(framed, f, c, 1, -1)
    return sum


def is_x_mas(framed, f, c):
    one = framed[f-1][c-1] + framed[f+1][c+1]
    if one != 'MS' and one != 'SM':
        return 0
    two = framed[f-1][c+1] + framed[f+1][c-1]
    if two == 'MS' or two == 'SM':
        return 1
    return 0


def main():
    with open("input04.txt", mode="r") as f:
        s = f.readlines()

    s = list(map(str.rstrip, s))

    length = len(s[0])

    framed = []
    for i in range(3):
        framed.append(" " * (length + 6))
    for line in s:
        framed.append('   ' + line + '   ')
    for i in range(3):
        framed.append(" " * (length + 6))

    for f in framed:
        print(f)

    sum = 0
    for f, frame in enumerate(framed):
        for c, char in enumerate(frame):
            if char == 'X':
                sum += look(framed, f, c)

    print(f"Day 4 Part 1  XMAS appears {sum} times.")

    total = 0
    for f, frame in enumerate(framed):
        for c, char in enumerate(frame):
            if char == 'A':
                total += is_x_mas(framed, f, c)

    print(f"Day 4 Part 2  X-MAS appears {total} times.")


if __name__ == "__main__":
    main()


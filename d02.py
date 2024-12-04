import re
from functools import partial


def all_dec(line):
    prev = 0
    for i, v in enumerate(line):
        if i == 0:
            prev = v
            continue
        if prev <= v or abs(prev - v) > 3:
            return False
        prev = v
    return True


def all_inc(line):
    prev = 0
    for i, v in enumerate(line):
        if i == 0:
            prev = v
            continue
        if prev >= v or abs(prev - v) > 3:
            return False
        prev = v
    return True


def damp_all_dec(line):
    bad = 0
    prev_prev = None
    prev = None
    for i, v in enumerate(line):
        if i == 0:
            prev = v
            continue
        if prev <= v or abs(prev - v) > 3:
            if bad == 0:
                bad = 1
                if prev_prev is None:
                    prev = v
                else:
                    prev = prev_prev
                    prev_prev = None
                continue
            return False
        prev_prev = prev
        prev = v
    return True


def damp_all_inc_skip_left(line):
    bad = 0
    prev = None
    for i, v in enumerate(line):
        if i == 0:
            prev = v
            continue
        if prev >= v or abs(prev - v) > 3:
            if bad == 0:
                bad = 1
                # prev shouldn't change so we skip v
                continue
            return False
        prev = v
    return True


def damp_all_inc_skip_right(line):
    bad = 0
    prev = None
    for i, v in enumerate(line):
        if i == 0:
            prev = v
            continue
        if prev >= v or abs(prev - v) > 3:
            if bad == 0:
                bad = 1
                prev = v  # skip prev
                continue
            return False
        prev = v
    return True


def damp_all_dec_skip_left(line):
    bad = 0
    prev = None
    for i, v in enumerate(line):
        if i == 0:
            prev = v
            continue
        if prev <= v or abs(prev - v) > 3:
            if bad == 0:
                bad = 1
                # prev shouldn't change so we skip v
                continue
            return False
        prev = v
    return True


def damp_all_dec_skip_right(line):
    bad = 0
    prev = None
    for i, v in enumerate(line):
        if i == 0:
            prev = v
            continue
        if prev <= v or abs(prev - v) > 3:
            if bad == 0:
                bad = 1
                prev = v  # skip prev
                continue
            return False
        prev = v
    return True


def is_safe(line):
    return all_dec(line) or all_inc(line)


def is_damp_safe(line):
    for i in range(len(line)):
        damp = line[:i] + line[i + 1:]
        print(damp)
        if is_safe(damp):
            return True
    return False


def main():
    with open("input02.txt", mode="r") as f:
        s = f.readlines()

    s = map(str.rstrip, s)
    s = map(str.split, s)
    s = map(partial(map, int), s)
    s = map(tuple, s)

    s = list(s)

    total = 0
    for line in s:
        print(line)
        if all_dec(line):
            print('All decreasing')
            total += 1
            continue
        else:
            print('NOT DEC')

        if all_inc(line):
            print('All INCREASING')
            total += 1
            continue
        else:
            print('NOT INCR')

    total2 = 0
    for line in s:
        print(line)
        if is_damp_safe(line):
            total2 += 1

    print(f"day 2 part 1 {total}")

    print(f"day 2 part 2 {total2}")


if __name__ == "__main__":
    assert is_damp_safe((20, 25, 26, 27))
    assert is_damp_safe((20, 23, 25, 29))

    main()



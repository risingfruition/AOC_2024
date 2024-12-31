import functools
import itertools
import re
from functools import partial


def read_input(file):
    with open(file,"r") as f:
        s = f.readlines()

    s = map(str.rstrip, s)
    s = list(s)

    rules = []
    updates = []

    ups = False
    for line in s:
        if not line:
            ups = True
            continue
        if ups:
            updates.append(line)
        else:
            rules.append(line)
    return rules, updates


def read_data(file):
    rules, updates = read_input(file)
    split_rules = []
    for r in rules:
        l = r.split('|')
        m = tuple(map(int, l))
        split_rules.append(m)
    split_updates = []
    for u in updates:
        l = u.split(',')
        m = list(map(int, l))
        split_updates.append(m)
    return split_rules, split_updates


def make_db(rules, update):
    d = {}
    for a, b in itertools.combinations(update, 2):
        if (a, b) in rules:
            d[(a, b)] = True
        if (b, a) in rules:
            d[(b, a)] = True
    return d


def good_update(d, update):
    for a, b in itertools.pairwise(update):
        if (a, b) not in d:
            return False
    return True


def part1(split_rules, split_updates):
    total = 0
    num_bad_updates = 0
    num_good_updates = 0
    bad_updates = []
    for update in split_updates:
        little_d = make_db(split_rules, update)

        if good_update(little_d, update):
            total += update[len(update) // 2]
            num_good_updates += 1
        else:
            num_bad_updates += 1
            bad_updates.append(update)

    print(f"good updates: {num_good_updates}")
    print(f"bad updates:  {num_bad_updates}")
    # 4569 is right.
    print(f"Part 1 {total = }")
    return total, bad_updates


def part2(bad_updates, split_rules):
    rules = map(tuple, split_rules)
    rules = set(rules)

    @functools.cmp_to_key
    def better_order(a, b):
        return -1 if (a, b) in rules else +1

    count_fixed = 0
    total_fixed = 0
    for update in bad_updates:
        sorted_up = sorted(update, key=better_order)
        total_fixed += sorted_up[len(sorted_up) // 2]
        count_fixed += 1

    # 6316 is too low
    # 6456 is the right answer
    print(f"Part 2 {count_fixed = }  {total_fixed = }")
    return total_fixed


def main():
    split_rules, split_updates = read_data("input05.txt")
    total, bad_updates = part1(split_rules, split_updates)

    part2(bad_updates, split_rules)


if __name__ == "__main__":
    main()
    # My answer for part 1 is 4569, part 2 is 6456


def test_part1_total_is_4569():
    split_rules, split_updates = read_data("input05.txt")
    total, bad_updates = part1(split_rules, split_updates)
    assert total == 4569

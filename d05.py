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


def main():
    split_rules, split_updates = read_data("input05.txt")

    total, bad_updates = part1(split_rules, split_updates)

    part2(bad_updates, split_rules)

    bad_total = 0
    for up in bad_updates:
        bad_total += up[len(up) // 2]
    print(f"Bad total = {bad_total}")


def part1(split_rules, split_updates):
    total = 0
    num_bad_updates = 0
    num_good_updates = 0
    bad_updates = []
    for up in split_updates:
        little_d = make_db(split_rules, up)

        if good_update(little_d, up):
            # print(f"good update: {up}")
            total += up[len(up) // 2]
            num_good_updates += 1
        else:
            num_bad_updates += 1
            bad_updates.append(up)
    print(f"good updates: {num_good_updates}")
    print(f"bad updates:  {num_bad_updates}")
    # 4569 is right.
    print(f"total is {total}")
    return total, bad_updates


def part2(bad_updates, split_rules):
    print(split_rules)
    rules = map(tuple, split_rules)
    # assert False

    @functools.cmp_to_key
    def better_order(a, b):
        return -1 if (a, b) in rules else +1
        # if (a, b) in rules:
        #     return 1
        # else:
        #     return -1

    total = 0
    for bad in bad_updates:
        up = bad[:]
        sorted_up = sorted(up, key=better_order)
        # assert up != sorted_up
        total += sorted_up[len(sorted_up) // 2]
    # 6316 is too low
    print(f"Part 2 Total: {total}")
    return total


if __name__ == "__main__":
    main()


def test_this_needs_to_return_true_from_in_order():
    '''
    bad_before: [74, 64, 82, 87, 27]
    Star Up STILL BAD: (64, 82, 87, 74, 27)
    STILL BAD:  [64, 82, 87, 74, 27]
                {64: [74, 82], 82: [87], 87: [27]}
    '''
    rules = {64: [74, 82], 82: [87], 87: [27]}
    bad_updates = [ [74, 64, 82, 87, 27] ]
    query_good = [64, 74, 82, 87, 27]
    assert part2(bad_updates, rules) == 82


def test_part1_total_is_4569():
    split_rules, split_updates = read_data("input05.txt")
    total, bad_updates = part1(split_rules, split_updates)
    assert total == 4569


def test_sort_update__reversed_pages__returns_sorted_pages():
    rules = RulesDB()
    rules.add(1,3)
    rules.add(3,5)
    update = [5, 3, 1]

    sorted_update = sort_update(rules.db, update)
    assert good_update(rules.db, update)


def test_good_update__sorted_pages__return_true():
    rules = RulesDB()
    rules.add(1,3)
    rules.add(3,5)
    update = [1, 3, 5]

    assert good_update(rules.db, update)

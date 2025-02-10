# Code Chronicle

def read_input(file):
    with open(file,"r") as f:
        s = f.read().split("\n")
    count = 0
    index = 0
    locks_and_keys = []
    max_index = len(s) - 1
    while True:
        lock_or_key = []
        while count < 7:
            lock_or_key.append(s[index])
            count += 1
            index += 1
        locks_and_keys.append(lock_or_key)
        if index >= max_index:
            break
        index += 1  # Skip blank line
        count = 0
    return locks_and_keys


def main():
    locks_and_keys = read_input("input25.txt")
    print(locks_and_keys)
    locks = []
    keys = []
    for item in locks_and_keys:
        thing = [item[i+1] for i in range(5)]
        if item[0][0] == '#':
            locks.append(thing)
        else:
            keys.append(thing)
    print("------")
    print(f"{locks = }")
    print()
    print(f"{keys = }")

    lock_heights = [tally(item) for item in locks]
    print(f"{lock_heights = }")
    key_heights = [tally(item) for item in keys]
    print(f"{key_heights = }")
    print()
    count = 0
    for key in key_heights:
        for lock in lock_heights:
            if does_fit(lock, key):
                count += 1

    print(f"{count = }")
    # Answer for Part 1: 3269


def does_fit(lock, key):
    for i, l in enumerate(lock):
        if l + key[i] > 5:
            return False
    return True


def tally(item):
    counts = [0, 0, 0, 0, 0]
    for line in item:
        for i, c in enumerate(line):
            if c == '#':
                # print(f"{i = }")
                counts[i] += 1
    return counts


if __name__ == "__main__":
    print(f"Day 25")
    main()
    print(f"Day 25")


def test_false():
    assert False

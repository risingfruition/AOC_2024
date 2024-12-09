import itertools
import re
from functools import partial


def read_input(file):
    with open(file,"r") as f:
        s = f.read().strip()
    #     s = map(str.rstrip, s)
    #     # s = map(colon_blow, s)
    #     # s = map(join_list, s)
    #     # s = map(str.split, s)
    #     # s = map(list_int, s)
    #     s = list(s.strip())
    return s
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
    pass


def main():
    data = read_input("input09.txt")
    # data = read_input("input09_sample.txt")
    print(f"data: {data}")
    # file 0 blocks, free blocks, file 1 blocks, free blocks, ...
    arr, file_lens = get_arr(data)
    arr2 = arr[:]
    print(file_lens)
    part_1_defrag(arr, data)
    total = checksum(arr, data)
    # Answer is 6334655979668
    print(f"Part 1  Checksum = {total}")

    arr = arr2
    part_2_defrag(arr, data, file_lens)
    total = checksum2(arr, data)
    # Answer is
    print(f"Part 2  Checksum = {total}")
    print()


def checksum2(arr, data):
    left = int(data[0])
    total = 0
    # while arr[left] > 0:
    #     total += left * arr[left]
    #     left += 1
    for i, a in enumerate(arr):
        if a > 0:
            total += i * arr[i]
    return total


def part_2_defrag(arr, data, file_lens):
    len_arr = len(arr)
    right = -1
    file_id = 1
    start = int(data[0])
    while file_id > 0:
        while arr[right] == 0:
            right -= 1
            if right + len_arr <= 0:
                return
        file_id = arr[right]
        # print(f"file_id {file_id}")
        file_len = file_lens[file_id]
        left = get_first_gap_of(arr, start, file_len, right + len_arr)
        if left == -1:
            while arr[right] == file_id:
                right -= 1
            continue
        for i in range(file_len):
            arr[left] = arr[right]
            arr[right] = -22
            left += 1
            right -= 1


def get_first_gap_of(arr, start, file_len, max_index):
    index = start
    while True:
        while arr[index] > 0:
            index += 1
        if index > max_index:
            return -1
        count_gap = 0
        while arr[index] <= 0:
            count_gap += 1
            if index > max_index:
                return -1
            index += 1
        if count_gap >= file_len:
            return index - count_gap


def checksum(arr, data):
    left = int(data[0])
    total = 0
    while arr[left] > 0:
        total += left * arr[left]
        left += 1
    # for i, a in enumerate(arr):
    #     if a > 0:
    #         total += a * arr[i]
    return total


def part_1_defrag(arr, data):
    left = int(data[0])  # skip file ID 0 blocks
    right = -1
    while left < right + len(arr):
        arr[left] = arr[right]
        arr[right] = -11
        left += 1
        right -= 1
        while arr[left] != 0:
            left += 1
        while arr[right] == 0:
            right -= 1
        # print(arr)
    print('---------')
    print(arr)


def get_arr(data):
    file_index = 0
    arr = []
    file_lens = {}
    for i, ch in enumerate(data):
        if i % 2 == 0:
            file_len = int(ch)
            file_lens[file_index] = file_len
            for num in range(file_len):
                arr.append(file_index)
            file_index += 1
        else:
            for num in range(int(ch)):
                arr.append(0)
    return arr, file_lens


if __name__ == "__main__":
    main()
    print(f"Day 9")


def test_thing():
    assert False

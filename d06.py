import itertools
import re
from functools import partial


turn = {
    "N": "E",
    "E": "S",
    "S": "W",
    "W": "N"
}

stuff = {
    "N": [0, -1],
    "E": [1, 0],
    "S": [0, 1],
    "W": [-1, 0]
}


def get_stuff(direction):
    return stuff[direction]


def read_input(file):
    with open(file,"r") as f:
        s = f.readlines()
    return s


def find_start(data, char_to_find='^'):
    r = 0
    c = 0
    for row, line in enumerate(data):
        if char_to_find in line:
            r = row
            for col, char in enumerate(line):
                if char == char_to_find:
                    c = col
                    return r, c
    raise Exception


def next_position(r, c, direction: str):
    x, y = get_stuff(direction)
    r = r + y
    c = c + x
    return r, c


def is_barrier(data, r, c):
    if r < 0 or c < 0:
        raise IndexError
    return data[r][c] == '#'


def loop_detected(value):
    return value > 10


def unique_positions(data, r, c):
    direction = "N"
    visited = {}
    num_r = len(data)
    num_c = len(data[0])

    while True:
        if r < 0 or c < 0 or r >= num_r or c >= num_c:
            break
        key = f"r{r}c{c}"
        visited[key] = visited.get(key, 0) + 1
        if loop_detected(visited[key]):
            return visited
        try:
            rr, cc = next_position(r, c, direction)
            while is_barrier(data, rr, cc):
                direction = turn[direction]
                rr, cc = next_position(r, c, direction)
            r = rr
            c = cc
        except IndexError:
            break
    # 5024 is not the answer
    # 4883 is the answer
    return visited


def add_barrier(s, index):
    return s[:index] + '#' + s[index + 1:]


def causes_loop(data, r, c, ro, co):
    direction = "N"
    visited = {}

    num_r = len(data)
    num_c = len(data[0])
    temp = data[ro]
    data[ro] = add_barrier(data[ro], co)
    while True:
        if r < 0 or c < 0 or r >= num_r or c >= num_c:
            data[ro] = temp
            return None
        key = f"r{r}c{c}"
        visited[key] = visited.get(key, 0) + 1
        if loop_detected(visited[key]):
            # Rough hack loop detection: loop detected
            data[ro] = temp
            return visited
        try:
            rr, cc = next_position(r, c, direction)
            while is_barrier(data, rr, cc):
                direction = turn[direction]
                rr, cc = next_position(r, c, direction)
            r = rr
            c = cc
        except IndexError:
            data[ro] = temp
            return None


def main():
    use_file("input06.txt")


def use_file(file_name):
    return use_data(read_input(file_name))


def use_data(data):
    # find # of distinct positions the guard visits before leaving the map.
    r, c = find_start(data)
    v = unique_positions(data, r, c)
    unique = len(v.items())
    # The answer is 4883
    print(f"unique = {unique}")

    count_stuff_before = len(re.findall('#', "".join(data)))
    loops = 0
    visited = {}
    for k in v.keys():
        row_col = row_col_from(k)
        assert 2 == len(row_col)
        ro = int(row_col[0])
        co = int(row_col[1])
        if ro == r and co == c:
            continue  # skip where the guard starts
        visited = causes_loop(data[:], r,c,ro,co)
        if visited:
            loops += 1
    # print(visited)
    # 4585 is too high
    # 1658 is too high
    # 1657 is too high (ignored the guard starting position)
    # The answer is 1655
    print(f"loops {loops}")
    count_stuff_after = len(re.findall('#', "".join(data)))
    print(f"counts: before={count_stuff_before} after={count_stuff_after}")
    return unique, loops


def row_col_from(line):
    return re.findall(r'(\d{1,3})', line)


if __name__ == "__main__":
    main()


def test_negative_x_index_does_not_cause_loop():
    data = [
        '#.#....',
        '...#...',
        '.......',
        '..^...o',
        '..#....',
    ]
    r, c = find_start(data)
    ro, co = find_start(data, "o")
    assert ro == 3
    assert co == 6
    assert causes_loop(data, r, c, ro, co) is None


def test_two_turns__loop__detects_loop():
    d = [
        '..#....',
        '..|#...',
        '..|....',
        '-o^....',
        '..#....',
    ]
    # 'o' is where adding a barrier would create a loop.
    # '-' is where guard travels left/right on original path.
    # '|' is where guard travels up/down on original path.
    # '^' is where guard starts.
    unique, loops = use_data(d)
    assert 5 == unique
    assert 1 == loops


def test_two_turns__no_loop__exits_grid():
    d = [
        '..#....',
        '...#...',
        '.......',
        '..^....',
        '.......',
    ]
    unique, loops = use_data(d)
    assert 4 == unique
    assert 0 == loops


def test_sample_data():
    unique, loops = use_file("input06_sample.txt")
    assert unique == 41
    assert loops == 6


def test_add_barrier():
    s = '0123456789'
    index = 3
    barrier = add_barrier(s, index)
    expected = '012#456789'

    assert barrier == expected


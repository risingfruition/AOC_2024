import functools
import itertools
import operator


def list_int(lyst):
    return list(map(int, lyst))


def join_list(lyst):
    stuff = ""
    for i in lyst:
        stuff = stuff + i
    return stuff


def colon_blow(st):
    return str.split(st, ':')


def read_input(file):
    with open(file,"r") as f:
        s = f.readlines()
        s = map(str.rstrip, s)
        s = map(colon_blow, s)
        s = map(join_list, s)
        s = map(str.split, s)
        s = map(list_int, s)
        s = list(s)
    return s


def stuff(data):
    for d in data:
        pass


def calc(d, th):
    index = 2
    value = d[1]
    index_th = 0
    while index < len(d):
        if th[index_th] == '+':
            value = value + d[index]
        elif th[index_th] == '|':
            value = int(str(value) + str(d[index]))
        else:
            value = value * d[index]
        index += 1
        index_th += 1
    return value


def recur(d, value, goal):
    return value



class MathOp:
    def __init__(self, update=None):
        self.update = update
        self.op = '+'

    def tic(self):
        if self.op == '+':
            self.op = '*'
            return
        if self.op == '*':
            self.op = '+'
            if self.update:
                self.update.tic()

    def value(self):
        return self.op


class MathList:
    def __init__(self, num):
        self.math_ops = []
        prev = None
        for i in range(num):
            prev = MathOp(prev)
            self.math_ops.append(prev)
        self.last = self.math_ops[-1]

    def tic(self):
        self.last.tic()

    def value(self):
        return [i.value() for i in self.math_ops]


def main():
    data = read_input("input07.txt")
    print(data)
    ops = iter(operator.add, operator.mul)
    value = 5
    next = 3
    one = MathOp()
    two = MathOp(one)
    for i in range(20):
        print(f"{one.value()} {two.value()}")
        two.tic()

    math_list = MathList(5)
    for i in range(20):
        print(math_list.value())
        math_list.tic()

    thing = itertools.product('+*', repeat=7)

    for i in thing:
        print(i)

    total = 0
    for d in data:
        total += consistent_value(d)
    # The answer is 932137732557
    print(total)

    total = 0
    for d in data:
        total += consistent_value(d, '+*|')
    # The answer is 661823605105500
    print(total)


def consistent_value(d, ops='+*'):
    goal = d[0]
    thing = itertools.product(ops, repeat=len(d) - 2)
    for th in thing:
        value = calc(d, th)
        if value == goal:
            return value
    return 0


if __name__ == "__main__":
    main()


def test_consistent_value__uses_new_op():
    goal = (64*5*6)  # e.g. 2*3||4*5*6
    data = [goal, 2, 3, 4, 5, 6]

    value = consistent_value(data,'+*|')

    assert value == goal


def test_calc__needs_mmpmm__right_answer():
    goal = (((2*3)+4)*5*6)
    data = [goal, 2, 3, 4, 5, 6]

    value = consistent_value(data)

    assert value == goal

import re
from functools import partial


def muls(line):
    return re.findall(r'mul\(\d{1,3},\d{1,3}\)', line)


def sums(line):
    sum = 0
    print(f'line {line}')
    mul_list = muls(line)
    for mul in mul_list:
        print(f"mul {mul}")
        num_list = re.findall(r'\d+', mul)
        print(f'num_list {num_list}')
        nums = list(map(partial(int), num_list))
        prod = nums[0] * nums[1]
        sum += prod
    return sum


def main():
    with open("input03.txt", mode="r") as f:
        s = f.readlines()

    s = list(map(str.rstrip, s))

    sum = 0
    for line in s:
        sum += sums(line)

    print(f'Day 3 Part 1  Sum = {sum}')
    # Correct answer 183380722

    is_do = True
    total = 0
    for line in s:
        sum, is_do = do_dont(line, is_do)
        total += sum
    print(f"Day 3 Part 2  Sum = {total}")
    # 83546082 is too high


def do_dont(line, is_do):
    if is_do:
        line = 'do()' + line
    else:
        line = "don't()" + line
    do_lines = str.split(line, "do()")
    print(f"split on do(): {do_lines}")

    sum = 0
    for do_line in do_lines:
        print(f"do_line: {do_line}")
        dont_lines = str.split(do_line, "don't()")
        sum += sums(dont_lines[0])
        is_do = len(dont_lines) == 1

    return sum, is_do


if __name__ == "__main__":


    main()

    # line = "blahmul(2,300)gurfmul(25,3)&&mul(,0)ff"
    #
    # mul_list = re.findall(r'mul\(\d{1,3},\d{1,3}\)', line)
    # print(f'mul = {mul_list}')
    # print(sums(line))
    # print(do_dont('fake', True))
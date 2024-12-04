import re

with open("input.txt", mode="r") as f:
    input = f.readlines()

left = []
right = []
for i in input:
    numbers = re.findall(r'\d+\.?\d*', i)
    left.append(int(numbers[0]))
    right.append(int(numbers[1]))
    # print(f"stuff {left[-1]} {right[-1]}")

left.sort()
right.sort()

total = 0
for z in zip(left, right):
    total += abs(z[0] - z[1])

print(f"day 1 part 1 {total}")

print('part 2')

d = {}
for e in right:
    d[e] = d.get(e, 0) + 1

print()
print(d)

sim = 0

for l in left:
    if l in d:
        sim += l * d[l]


print()
print(f"similarity: {sim}")

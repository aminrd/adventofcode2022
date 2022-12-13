from functools import cmp_to_key
DEBUG = 0
PART_NUMBER = 1
input_file = "inputs/test.txt" if DEBUG else "inputs/day13.txt"
with open(input_file) as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]


def ordered(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        elif left == right:
            return 0
        else:
            return 1

    if isinstance(left, list) and isinstance(right, list):
        l1, l2 = len(left), len(right)
        if l1 == 0 and l2 == 0:
            return 0
        if l1 == 0:
            return -1
        if l2 == 0:
            return 1

        top = ordered(left[0], right[0])
        if top != 0:
            return top

        return ordered(left[1:], right[1:])

    if isinstance(left, int):
        return ordered([left], right)

    if isinstance(right, int):
        return ordered(left, [right])

index = 1
sum_of_index = 0
part_two = []
while len(lines) > 0:
    a, b, lines = lines[0], lines[1], lines[3:]
    ea, eb = eval(a), eval(b)
    part_two.append(ea)
    part_two.append(eb)

    if ordered(ea, eb) == -1:
        sum_of_index += index
    index += 1

print(sum_of_index)


# Part two:
divider = ([[2]], [[6]])
part_two.append(divider[0])
part_two.append(divider[1])

arr = sorted(part_two, key=cmp_to_key(ordered))


ans2 = 1
for i, obj in enumerate(arr):
    if obj == divider[0] or obj == divider[1]:
        ans2 *= (i+1)

print(ans2)
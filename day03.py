with open("inputs/day3.txt") as f:
    content = f.readlines()


def get_priority(char: str):
    if char.islower():
        return ord(char) - ord('a') + 1
    else:
        return ord(char) - ord('A') + 27


total_sum = 0
for line in content:
    n = len(line)
    a, b = line[:n // 2], line[n // 2:]

    s1, s2 = set(a), set(b)

    for char in s1.intersection(s2):
        total_sum += get_priority(char)

print(f"Solution for part one is :{total_sum}")

group_sum = 0
n_line = len(content)
for g in range(n_line // 3):
    glines = content[3 * g: 3 * g + 3]
    s1, s2, s3 = set(glines[0][:-1]), set(glines[1][:-1]), set(glines[2][:-1])

    common = s1.intersection(s2)
    common = list(common.intersection(s3))

    if len(common) > 0:
        group_sum += get_priority(common[0])

print(f"Solution for part two is :{group_sum}")

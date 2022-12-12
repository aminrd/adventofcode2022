with open("inputs/day2.txt") as f:
    plays = f.readlines()


def get_num(p, base):
    return ord(p) - ord(base)


def game_score(a, b):
    if a == b:
        return 3
    if a == 0:
        return 6 if b == 1 else 0
    if a == 1:
        return 6 if b == 2 else 0
    if a == 2:
        return 6 if b == 0 else 0


def get_shape_score(a, b):
    if b == 0:
        if a == 0:
            return 3
        elif a == 1:
            return 1
        else:
            return 2
    elif b == 1:
        return 1 + a
    else:
        if a == 0:
            return 2
        elif a == 1:
            return 3
        else:
            return 1


score_part1 = 0
for play in plays:
    a, b = play.split()

    a = get_num(a, 'A')
    b = get_num(b, 'X')

    score = 1 + b + game_score(a, b)
    score_part1 += score

print(f"Part one answer is: {score_part1}")

score_part2 = 0
for play in plays:
    a, b = play.split()

    a = get_num(a, 'A')
    b = get_num(b, 'X')

    score = b * 3 + get_shape_score(a, b)
    score_part2 += score

print(score_part2)

print(f"Part two answer is: {score_part1}")

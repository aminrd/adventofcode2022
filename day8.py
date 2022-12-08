with open("inputs/day8.txt") as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

m, n = len(lines), len(lines[0])
grid = [[0 for _ in range(n)] for _ in range(m)]

for i in range(m):
    for j in range(n):
        grid[i][j] = int(lines[i][j])


def process_line_l2r(l: list):
    n = len(l)
    result = [False] * n
    result[0] = True
    max_sofar = l[0]

    for i in range(1, n):
        if l[i] > max_sofar:
            result[i] = True
        max_sofar = max(max_sofar, l[i])

    return result


def process_line(l: list):
    res1 = process_line_l2r(l)
    res2 = process_line_l2r(l[::-1])[::-1]
    return [r1 or r2 for r1, r2 in zip(res1, res2)]


def transpose(matrix):
    return [*zip(*matrix)]


horizontal = [process_line(row) for row in grid]
vertical = [process_line(col) for col in transpose(grid)]
vertical = transpose(vertical)

count = 0
for i in range(m):
    for j in range(n):
        if horizontal[i][j] or vertical[i][j]:
            count += 1
print(count)

# Part two:
directions = ((1, 0), (-1, 0), (0, 1), (0, -1))


def calc_score(i, j):
    dir_score = [1, 1, 1, 1]
    for dindex, (di, dj) in enumerate(directions):
        cnt = 0
        ai, aj = i + di, j + dj
        while 0 <= ai < m and 0 <= aj < n:
            cnt += 1
            if grid[ai][aj] < grid[i][j]:
                ai, aj = ai + di, aj + dj
            else:
                break

        dir_score[dindex] = cnt

    mul = 1
    for i in range(4):
        mul *= dir_score[i]

    return mul


scores = [[calc_score(i, j) for j in range(n)] for i in range(m)]
ans2 = max(max(row) for row in scores)
print(ans2)

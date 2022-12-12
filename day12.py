DEBUG = 0
PART_NUMBER = 1
input_file = "inputs/test.txt" if DEBUG else "inputs/day12.txt"
with open(input_file) as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]


def get_height(character : str):
    if character == 'S':
        return 1
    if character == 'E':
        return 26
    return ord(character) - ord('a')


m, n = len(lines), len(lines[0])
grid = [[0] * n for _ in range(m)]

src, dst = None, None
all_as = []

for i, row in enumerate(lines):
    for j, char in enumerate(row):
        if char == 'S':
            src = (i, j)
        if char == 'E':
            dst = (i, j)
        grid[i][j] = get_height(char)
        if grid[i][j] == 0:
            all_as.append((i, j))

directions = ((0, 1), (0, -1), (1, 0), (-1, 0))


def bfs(start, target):
    queue = [(start, 0)]
    visited = {start}
    while len(queue) > 0:
        (i, j), d = queue.pop(0)

        for di, dj in directions:
            ai, aj = i + di, j + dj
            if 0 <= ai < m and 0 <= aj < n and grid[ai][aj] - grid[i][j] <= 1:
                if (ai, aj) == target:
                    return d + 1
                if (ai, aj) in visited:
                    continue

                queue.append(((ai, aj), d+1))
                visited.add((ai, aj))


ans1 = bfs(src, dst)
print(f"Part one = {ans1}")


# Part two
found = False
queue = [((i, j), 0) for i, j in all_as]
visited = set(all_as)

while len(queue) > 0 and not found:
    (i, j), d = queue.pop(0)

    for di, dj in directions:
        ai, aj = i + di, j + dj
        if 0 <= ai < m and 0 <= aj < n and grid[ai][aj] - grid[i][j] <= 1:
            if (ai, aj) == dst:
                print(f"Part two = {d+1}")
                found = True
                break
            if (ai, aj) in visited:
                continue

            queue.append(((ai, aj), d + 1))
            visited.add((ai, aj))

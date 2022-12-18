DEBUG = 0
PART_NUMBER = 1
input_file = "inputs/test.txt" if DEBUG else "inputs/day18.txt"
with open(input_file) as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]

cubes = set()
maxs = list(map(int, lines[0].split(',')))
for line in lines:
    x, y, z = map(int, line.split(','))
    cubes.add((x, y, z))

directions = [
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (0, 0, 1),
    (0, 0, -1)
]


def get_adj(x, y, z):
    return [(x+dx, y+dy, z+dz) for dx, dy, dz in directions]


sides = 0

for cube in cubes:
    for i in range(3):
        maxs[i] = max(maxs[i], cube[i])

    sides += sum(adj not in cubes for adj in get_adj(*cube))

ans1 = sides
print(f"Answer part one is {ans1}")

N = 25
grid = [[[0] * N for _ in range(N)] for _ in range(N)]

for x, y, z in cubes:
    grid[x][y][z] = 2

queue = [
    (0, 0, 0),
    (0, 0, N-1),
    (0, N-1, 0),
    (N-1, 0, 0),
    (N - 1, N-1, 0),
    (N - 1, 0, N - 1),
    (0, N - 1, N - 1),
    (N-1, N - 1, N - 1),
]

queue = [start for start in queue if start not in cubes]
for x, y, z in queue:
    grid[x][y][z] = 1

while len(queue) > 0:
    x, y, z = queue.pop(0)
    if grid[x][y][z] == 2:
        continue

    for dx, dy, dz in directions:
        ax, ay, az = x+dx, y+dy, z+dz
        adj = (ax, ay, az)
        if all(0 <= ai < N for ai in adj) and grid[ax][ay][az] == 0:
            queue.append(adj)
            grid[ax][ay][az] = 1


sides_two = 0
for cube in cubes:
    sides_two += sum(grid[ax][ay][az] == 1 for ax, ay, az in get_adj(*cube))

ans2 = sides_two
print(f"Answer part two is {ans2}")
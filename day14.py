DEBUG = 0
PART_NUMBER = 2
input_file = "inputs/test.txt" if DEBUG else "inputs/day14.txt"
with open(input_file) as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]


def get_points(line: str):
    line = line.strip().replace(" ", "")
    point_split = line.split('->')
    return [tuple(map(int, p.split(','))) for p in point_split]


rocks = [get_points(line) for line in lines]

blocked = set()
directions = ((0, 1), (-1, 1), (1, 1))
min_x, max_x = 500, 500
max_y = 0

for rock in rocks:
    for p1, p2 in zip(rock[0:-1], rock[1:]):
        x1, y1 = p1
        x2, y2 = p2

        min_x = min((min_x, x1, x2))
        max_x = max((max_x, x1, x2))
        max_y = max((max_y, y1, y2))

        if x1 == x2:
            for yhat in range(min(y1, y2), max(y1, y2) + 1):
                blocked.add((x1, yhat))
        else:
            for xhat in range(min(x1, x2), max(x1, x2) + 1):
                blocked.add((xhat, y1))


def move(x, y):
    for di, dj in directions:
        if (x + di, y + dj) not in blocked:
            return x + di, y + dj
    return x, y


def insert(pos):
    x, y = pos
    if all((x + di, y + dj) in blocked for di, dj in directions):
        return False

    while pos[1] < max_y + 1:
        new_pos = move(pos[0], pos[1])
        if new_pos == pos:
            blocked.add(pos)
            return True

        pos = new_pos

    blocked.add(pos)
    return False if PART_NUMBER == 1 else True


count = 0
source = (500, 0)
while insert(source):
    count += 1

print(count)

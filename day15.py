import collections

DEBUG = 0
PART_NUMBER = 1
input_file = "inputs/test.txt" if DEBUG else "inputs/day15.txt"
with open(input_file) as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]


def man_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def parse_xy(s):
    coords = s[s.find("at ") + 3:]
    xs, ys = coords.split(',')
    x = int(xs.strip()[2:])
    y = int(ys.strip()[2:])
    return x, y


pairs = []
for line in lines:
    p1, p2 = line.strip().split(":")
    s, b = parse_xy(p1), parse_xy(p2)
    pairs.append((s, b))

qy = 10 if DEBUG == 1 else 2000000
covered = collections.defaultdict(set)


def generate_points(d, at_y):
    points = set()
    dy = abs(at_y)
    if dy > d:
        return points

    for x in range(d - dy + 1):
        points.add((x, at_y))
        points.add((-x, at_y))

    return points


for S, B in pairs:
    d = man_dist(S, B)

    for dx, dy in generate_points(d, qy - S[1]):
        x = S[0] + dx
        y = S[1] + dy
        if (x, y) != B:
            covered[y].add((x, y))

print(f"Answer one is {len(covered[qy])}")

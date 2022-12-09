#with open("inputs/test.txt") as f:
with open("inputs/day9.txt") as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

directions = {
    "L": (0, -1),
    "R": (0, 1),
    "D": (1, 0),
    "U": (-1, 0)
}

def diag_dir(dst, pos):
    xt, yt = dst
    x0, y0 = pos

    if abs(xt - x0) == 1:
        return (1, 0) if xt > x0 else (-1, 0)
    return (0, 1) if yt > y0 else (0, -1)


def parse_line(line):
    d, count = line.split()
    return directions[d], int(count)


moves = [parse_line(line) for line in lines]


def dist(p1, p2):
    return sum(abs(x - y) for x, y in zip(p1, p2))


def adj(p1, p2):
    distance = dist(p1, p2)
    return distance <= 1 or (distance == 2 and p1[0] != p2[0] and p1[1] != p2[1])


def step(position, d):
    return [pos + di for pos, di in zip(position, d)]

head = [0, 0]
tail = [0, 0]
visited = {(0, 0)}

for d, count in moves:
    for _ in range(count):
        #print(f"Head : {head}, Tail : {tail}")
        head = step(head, d)
        if not adj(head, tail):
            if head[0] == tail[0]:
                tail[1] += d[1]
            elif head[1] == tail[1]:
                tail[0] += d[0]
            else:
                ddir = diag_dir(head, tail)
                final_dir = (d[0] + ddir[0], d[1]+ ddir[1])
                tail = step(tail, final_dir)

        visited.add(tuple(tail))

ans1 = len(visited)
print(ans1)



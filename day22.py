from bisect import bisect_left
from collections import defaultdict

DEBUG = 0
PART_NUMBER = 1
input_file = "inputs/test.txt" if DEBUG else "inputs/day22.txt"
with open(input_file) as f:
    lines = f.readlines()

instruction_line = lines[-1].strip() + "S"
lines = [line[:-1] for line in lines[:-2]]


class Node:
    def __init__(self, ii, jj, char):
        self.i = ii
        self.j = jj
        self.char = char

    def position(self):
        return self.i, self.j

    def blocked(self):
        return self.char == "#"

    def __str__(self):
        return f"( {self.i}, {self.j}, {self.char} )"

    def __repr__(self):
        return self.__str__()


def parse_instructions(s):
    l = []
    i = 0
    while i < len(s):
        j = i
        while s[j].isnumeric():
            j += 1
        l.append((s[j], int(s[i:j])))
        i = j + 1
    return l


instructions = parse_instructions(instruction_line)

rows = defaultdict(list)
cols = defaultdict(list)

N = 4 if DEBUG else 50
cube = [
    [[None] * N for _ in range(N)],
    [[None] * N for _ in range(N)],
    [[None] * N for _ in range(N)],
    [[None] * N for _ in range(N)],
    [[None] * N for _ in range(N)],
    [[None] * N for _ in range(N)]
]

debug_cube_indexer = [
    [None, None, 0, None],
    [1, 2, 3, None],
    [None, None, 4, 5],
]

real_cube_indexer = [
    [None, 0, 1],
    [None, 2, None],
    [3, 4, None],
    [5, None, None]
]


def get_cube_index(i, j):
    if DEBUG:
        ci = debug_cube_indexer[i // N][j // N]
        return ci, i % N, j % N
    else:
        ci = real_cube_indexer[i // N][j // N]
        return ci, i % N, j % N


for i, row in enumerate(lines):
    for j, c in enumerate(row):
        if c == " ":
            continue
        node = Node(i, j, c)
        rows[i].append(node)
        cols[j].append(node)

        cind, cy, cx = get_cube_index(i, j)
        cube[cind][cy][cx] = node


def find_index(array, i, j):
    index = bisect_left([node.position() for node in array], (i, j))
    return index


di = 0
clockwise_directions = "RDLU"
I, J = rows[0][0].position()

for rotate, move in instructions:
    d = clockwise_directions[di]
    array = rows[I] if d in "LR" else cols[J]
    ind = find_index(array, I, J)

    step = 1 if d in "RD" else -1
    for _ in range(move):
        ind = (ind + step) % len(array)
        if array[ind].blocked():
            break
        I, J = array[ind].position()

    if rotate == "R":
        di = (di + 1) % 4
    elif rotate == "L":
        di = (di - 1) % 4
    else:
        break

password = 1000 * (I + 1) + 4 * (J + 1) + di
print(f"Answer part one is {password}")

# Part two

debug_cube_horizontal = [
    [None, None, 0, None],
    [1, 2, 3, None],
    [None, None, 4, 5],
]

real_cube_indexer = [
    [None, 0, 1],
    [None, 2, None],
    [3, 4, None],
    [5, None, None]
]

ci, I, J = 0, 0, 0
dy, dx = 0, 1

for rotate, move in instructions:
    for _ in range(move):
        ai, aj = I+dy, J+dx
        if 0 <= ai < N and 0 <= aj < N:
            if cube[ci][ai][aj].blocked():
                break
            else:
                I, J = ai, aj
        else:
            pass
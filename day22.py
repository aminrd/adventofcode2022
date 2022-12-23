from bisect import bisect_left
from collections import defaultdict

DEBUG = 0
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

# (C_Dest, flip_indices?, Side_dst)
# Side_src = [RDLU]
debug_mapper = {
    0: [(5, True, 'R'), (3, False, 'U'), (2, False, 'U'), (1, True, 'U')],
    1: [(2, False, 'L'), (4, True, 'D'), (5, True, 'D'), (0, True, 'U')],
    2: [(3, False, 'L'), (4, True, 'L'), (1, False, 'R'), (0, False, 'L')],
    3: [(5, True, 'U'), (4, False, 'U'), (2, False, 'R'), (0, False, 'D')],
    4: [(5, False, 'L'), (1, True, 'D'), (2, True, 'D'), (3, False, 'D')],
    5: [(0, True, 'R'), (1, True, 'L'), (4, False, 'R'), (3, True, 'R')],
}
real_mapper = {
    0: [(1, False, 'L'), (2, False, 'U'), (3, True, 'L'), (5, False, 'L')],
    1: [(4, True, 'R'), (2, False, 'R'), (0, False, 'R'), (5, False, 'D')],
    2: [(1, False, 'D'), (4, False, 'U'), (3, False, 'U'), (0, False, 'D')],
    3: [(4, False, 'L'), (5, False, 'U'), (0, True, 'L'), (2, False, 'L')],
    4: [(1, True, 'R'), (5, False, 'R'), (3, False, 'R'), (2, False, 'D')],
    5: [(4, False, 'D'), (1, False, 'U'), (0, False, 'U'), (3, False, 'D')],
}


def get_node_index_and_direction(ind, flip, entrance):
    index = N - ind - 1 if flip else ind
    if entrance == 'R':
        return (index, N - 1), 'L'
    elif entrance == 'D':
        return (N - 1, index), 'U'
    elif entrance == 'L':
        return (index, 0), 'R'
    else:
        return (0, index), 'D'


def get_next_node(c_src, i, j):
    mapper = debug_mapper[c_src] if DEBUG else real_mapper[c_src]

    if j == N:  # Right exit
        c_next, flip, entrance = mapper[0]
        index, direction = get_node_index_and_direction(i, flip, entrance)
    elif i == N:  # Down exit
        c_next, flip, entrance = mapper[1]
        index, direction = get_node_index_and_direction(j, flip, entrance)
    elif j == -1:  # Left exit
        c_next, flip, entrance = mapper[2]
        index, direction = get_node_index_and_direction(i, flip, entrance)
    else:  # Top exit
        c_next, flip, entrance = mapper[3]
        index, direction = get_node_index_and_direction(j, flip, entrance)

    return c_next, index, direction


ci, I, J = 0, 0, 0
dy, dx = 0, 1
direction_mapper = {
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1),
    'U': (-1, 0)
}
direction_point = {
    (0, 1): 0,
    (1, 0): 1,
    (0, -1): 2,
    (-1, 0): 3
}
rotate_right = {
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1)
}
rotate_left = {
    (0, 1): (-1, 0),
    (1, 0): (0, 1),
    (0, -1): (1, 0),
    (-1, 0): (0, -1)
}

for rotate, move in instructions:
    for _ in range(move):
        ai, aj = I + dy, J + dx
        if 0 <= ai < N and 0 <= aj < N:
            if cube[ci][ai][aj].blocked():
                break
            else:
                I, J = ai, aj
        else:
            c_next, (ai, aj), direction = get_next_node(ci, ai, aj)
            if cube[c_next][ai][aj].blocked():
                break
            else:
                ci, I, J = c_next, ai, aj
                dy, dx = direction_mapper[direction]

    if rotate == "R":
        dy, dx = rotate_right[(dy, dx)]
    elif rotate == "L":
        dy, dx = rotate_left[(dy, dx)]
    else:
        break

node = cube[ci][I][J]
final_i, final_j = node.position()
password = 1000 * (final_i + 1) + 4 * (final_j + 1) + direction_point[(dy, dx)]
print(f"Answer part two is {password}")

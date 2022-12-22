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
for i, row in enumerate(lines):
    for j, c in enumerate(row):
        if c == " ":
            continue
        node = Node(i, j, c)
        rows[i].append(node)
        cols[j].append(node)


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

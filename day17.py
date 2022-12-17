from tqdm import tqdm
from collections import OrderedDict
DEBUG = 0
VERBOSE = 0
PART_NUMBER = 2
input_file = "inputs/test.txt" if DEBUG else "inputs/day17.txt"
with open(input_file) as f:
    commands = f.read().strip()


class Shape:
    def __init__(self, rows):
        self.rows = rows
        self.h = len(rows)
        self.w = len(rows[0])

        self.blocks = []
        for i, row in enumerate(rows[::-1]):
            for j, c in enumerate(row):
                if c == "#":
                    self.blocks.append((i, j))


shapes = [
    Shape(['####']),
    Shape([".#.", "###", ".#."]),
    Shape(['..#', "..#", "###"]),
    Shape(['#', "#", "#", '#']),
    Shape(['##', '##'])
]

W, H, ci = 7, 3, 0
grid = []
blocked = OrderedDict()
shape_number = 0


def can_move_down(shape, x, y):
    return y > 0 and all((y + i - 1, x + j) not in blocked for i, j in shape.blocks)


def can_move_left(shape, x, y):
    return x > 0 and all((y + i, x + j - 1) not in blocked for i, j in shape.blocks)


def can_move_right(shape, x, y):
    return (x+shape.w) < W and all((y + i, x + j + 1) not in blocked for i, j in shape.blocks)


def move_horizontal(shape, x, y, command):
    if command == "<":
        return -1 if can_move_left(shape, x, y) else 0
    else:
        return 1 if can_move_right(shape, x, y) else 0


def add_block(shape, x, y):
    for i, j in shape.blocks:
        blocked[(y+i, x+j)] = True


def print_grid(top):
    table = [['_'] * W for _ in range(top + 1)]
    for y, x in blocked:
        table[y][x] = "#"

    for row in table[::-1]:
        print("".join(row))
    print("\n\n")



empty_row = "." * W
shape_cnt = 0
n_max = 2022 if PART_NUMBER == 1 else 1000000000000
n_commands = len(commands)

tallest = 0
checkpoint = 0

# X, Y = Bottom-Left cornet of the shape
for shape_cnt in tqdm(range(n_max)):
    shape = shapes[shape_cnt % len(shapes)]
    shape_cnt += 1

    x = 2
    y = tallest + H

    stop = False
    while not stop:
        x += move_horizontal(shape, x, y, commands[ci % n_commands])
        ci += 1

        if can_move_down(shape, x, y):
            y -= 1
        else:
            stop = True

    add_block(shape, x, y)
    tallest = max(tallest, y + shape.h)

    # Avoid blocked set from growing
    if PART_NUMBER == 2 and tallest - checkpoint > 500:
        for key in list(blocked.keys())[:-200]:
            blocked.pop(key)
        checkpoint = tallest

    if VERBOSE:
        print_grid(tallest)
        x = 1


print(f"Tallest point is at {tallest}")


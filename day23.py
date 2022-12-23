from collections import defaultdict
DEBUG = 0
PART_NUMBER = 1
input_file = "inputs/test.txt" if DEBUG else "inputs/day23.txt"
with open(input_file) as f:
    lines = f.readlines()

lines = [line.strip() for line in lines]

elves = set()
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == "#":
            elves.add((i, j))

directions = [
    ((-1, -1), (-1, 0), (-1, 1)),
    ((1, -1), (1, 0), (1, 1)),
    ((1, -1), (0, -1), (-1, -1)),
    ((1, 1), (0, 1), (-1, 1))
]
all_dirs = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

for _ in range(10):
    propose = dict()
    propose_count = defaultdict(int)

    next_elves = set()
    for i, j in elves:

        if all((i+di, j+dj) not in elves for di, dj in all_dirs):
            next_elves.add((i, j))
            continue

        for dirs in directions:
            if all((i+di, j+dj) not in elves for di, dj in dirs):
                next_position = (i + dirs[1][0], j + dirs[1][1])
                propose[(i, j)] = next_position
                propose_count[next_position] += 1
                break

        if (i, j) not in propose:
            next_elves.add((i, j))

    for (i, j), (pi, pj) in propose.items():
        if propose_count[(pi, pj)] == 1:
            next_elves.add((pi, pj))
        else:
            next_elves.add((i, j))

    elves = next_elves
    first_dirs = directions.pop(0)
    directions.append(first_dirs)

locations = list(elves)
min_i, min_j = locations[0]
max_i, max_j = locations[0]

for i, j in locations:
    min_i = min(min_i, i)
    min_j = min(min_j, j)
    max_i = max(max_i, i)
    max_j = max(max_j, j)


empty_cells = (max_i - min_i + 1) * (max_j - min_j + 1) - len(elves)
print(f"Answer part one is {empty_cells}")
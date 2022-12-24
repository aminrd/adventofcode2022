import math
from tqdm import tqdm

DEBUG = 0
PART_NUMBER = 2
input_file = "inputs/test.txt" if DEBUG else "inputs/day24.txt"
with open(input_file) as f:
    lines = f.readlines()

lines = [line.strip() for line in lines]
directions = ((0, 1), (0, -1), (-1, 0), (1, 0), (0, 0))
M, N = len(lines), len(lines[0])

period = math.lcm(M-2, N-2)

class Snowflake:
    def __init__(self, i, j, direction):
        self.i = i
        self.j = j

        if direction == '>':
            self.direction = (0, 1)
        elif direction == '<':
            self.direction = (0, -1)
        elif direction == '^':
            self.direction = (-1, 0)
        else:
            self.direction = (1, 0)

    def loc(self):
        return self.i, self.j

    def move(self):
        self.i, self.j = self.i + self.direction[0], self.j + self.direction[1]

        if self.i == 0:
            self.i = M - 2
        elif self.i == M - 1:
            self.i = 1
        elif self.j == 0:
            self.j = N - 2
        elif self.j == N-1:
            self.j = 1

snowflakes = []
wall = set()
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == '#':
            wall.add((i, j))
        elif c != '.':
            flake = Snowflake(i, j, c)
            snowflakes.append(flake)

MAX_TURN = 10**6

if PART_NUMBER == 1:
    start = (0, 1)
    goal = (M-1, N-2)
    my_locs = [start]
    goal_found = False
    processed_states = {(*start, 0)}

    for t in tqdm(range(MAX_TURN)):
        blocked = set()
        for flake in snowflakes:
            flake.move()
            blocked.add(flake.loc())

        next_round_locs = []
        for i, j in my_locs:
            for di, dj in directions:
                ai, aj = i+di, j+dj
                state = (ai, aj, (t+1) % period)
                if 0 <= ai < M and 0 <= aj < N and (ai, aj) not in wall and (ai, aj) not in blocked and state not in processed_states:
                    processed_states.add(state)
                    if (ai, aj) == goal:
                        goal_found = True
                    next_round_locs.append((ai, aj))

        my_locs = next_round_locs
        if goal_found:
            break

    print(f"Answer part one is {t+1}")

else:
    # Loc = (i, j, goal_index)
    start = (0, 1, 0)
    goals = [(M-1, N-2), (0, 1), (M-1, N-2)]

    my_locs = [start]
    goal_found = False
    processed_states = {(*start, 0)}

    for t in tqdm(range(MAX_TURN)):
        blocked = set()
        for flake in snowflakes:
            flake.move()
            blocked.add(flake.loc())

        next_round_locs = []
        for i, j, goal_index in my_locs:
            for di, dj in directions:
                ai, aj = i+di, j+dj
                if 0 <= ai < M and 0 <= aj < N and (ai, aj) not in wall and (ai, aj) not in blocked:
                    if goal_index == 2 and (ai, aj) == goals[2]:
                        goal_found = True

                    if (ai, aj) == goals[goal_index]:
                        state = (ai, aj, goal_index + 1, (t + 1) % period)
                    else:
                        state = (ai, aj, goal_index, (t + 1) % period)

                    if state not in processed_states:
                        processed_states.add(state)
                        next_round_locs.append((ai, aj, state[2]))

        my_locs = next_round_locs
        if goal_found:
            break

    print(f"Answer part two is {t + 1}")

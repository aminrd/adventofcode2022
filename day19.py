from tqdm import tqdm

DEBUG = 0
PART_NUMBER = 1
input_file = "inputs/test.txt" if DEBUG else "inputs/day19.txt"
with open(input_file) as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]

index = {
    "ore": 0,
    "clay": 1,
    "obsidian": 2,
    "geode": 3
}


class Robot:
    def __init__(self, line):
        words = line.strip().split()
        self.type = index[words[1]]
        required = [0] * 4

        i = 3
        while i < len(words):
            type_index = index[words[i + 2]]
            required[type_index] = int(words[i + 1])
            i += 3

        self.required = tuple(required)

    def enough(self, resources: tuple) -> bool:
        return all(want <= has for want, has in zip(self.required, resources))

    def subtract(self, resources: tuple) -> tuple:
        return tuple(has - want for want, has in zip(self.required, resources))


class Blueprint:
    def __init__(self, line):
        self.robots = []
        _, robots_string = line.split(':')

        for robot_string in robots_string.strip().split('.'):
            if len(robot_string) < 1:
                continue
            self.robots.append(Robot(robot_string))


MAX_TIME = 24
blue_prints = [Blueprint(line) for line in lines]


# Generating one new ore robot each round, can generate parallel robots, remove ore dependency for last two robots
def upperbound(b: Blueprint, t: int, robots: tuple, resources: tuple):
    res = list(resources)
    r = list(robots)
    required = (0, b.robots[1].required[0], b.robots[2].required[1], b.robots[3].required[2])

    for _ in range(MAX_TIME - t):
        prev_r = tuple(r)

        r[0] += 1
        for i in range(1, 4):
            if required[i] <= res[i - 1]:
                res[i - 1] -= required[i]
                r[i] += 1

        for i in range(4):
            res[i] += prev_r[i]

    return res[-1]


def get_best(b: Blueprint, t: int, robots: tuple, resources: tuple, best: int, visited_states: set) -> int:
    if t >= MAX_TIME:
        return max(best, resources[-1])

    key = (*robots, *resources, t)
    if key in visited_states:
        return best

    if upperbound(b, t, robots, resources) <= best:
        visited_states.add(key)
        return best

    new_resources = tuple(resource + robot_cnt for resource, robot_cnt in zip(resources, robots))
    for ri in (3, 2, 1, 0):
        r = b.robots[ri]
        if r.enough(resources):
            new_robots = list(robots)
            new_robots[ri] += 1
            best = get_best(b, t + 1, tuple(new_robots), r.subtract(new_resources), best, visited_states)

    # Also do nothing:
    best = get_best(b, t + 1, robots, new_resources, best, visited_states)
    visited_states.add(key)

    return best


total_sum = 0
for bi, blue_print in tqdm(list(enumerate(blue_prints))):
    best = get_best(blue_print, 0, (1, 0, 0, 0), (0, 0, 0, 0), 0, set())
    total_sum += (bi + 1) * best

print(f"Answer part one is {total_sum}")

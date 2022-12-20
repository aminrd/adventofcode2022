from tqdm import tqdm
DEBUG = 1
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

def get_best(b: Blueprint, t: int, robots: tuple, resources: tuple, best: int) -> int:
    if t >= MAX_TIME:
        return max(best, resources[-1])

    if t > 10 and resources[-1] + (MAX_TIME - t) * (robots[-1]+1) < best:
        return best

    new_resources = tuple(resource + robot_cnt for resource, robot_cnt in zip(resources, robots))
    for ri in (3, 2, 1, 0):
        r = b.robots[ri]
        if r.enough(resources):
            new_robots = list(robots)
            new_robots[ri] += 1
            best = get_best(b, t + 1, tuple(new_robots), r.subtract(new_resources), best)

    # Also do nothing:
    best = get_best(b, t + 1, robots, new_resources, best)

    return best


total_sum = 0
for bi, blue_print in tqdm(list(enumerate(blue_prints))):
    best = get_best(blue_print, 0, (1, 0, 0, 0), (0, 0, 0, 0), 0)
    total_sum += (bi+1) * best

print(f"Answer part one is {total_sum}")

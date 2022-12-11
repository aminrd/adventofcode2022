from collections import defaultdict

with open("inputs/day11.txt") as f:
    lines = f.readlines()

lines = [line.strip() for line in lines]

'''
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3
'''
item_kw_length = len("Starting items: ")
operation_kw_length = len("Operation: new = old ")
test_kw_length = len("Test: divisible by ")
true_kw_length = len("If true: throw to monkey ")
false_kw_length = len("If false: throw to monkey ")


class Monkey:
    def __init__(self, lines: list):
        items = lines[0][item_kw_length:].replace(" ", "").split(',')
        self.items = list(map(int, items))

        op, value = lines[1][operation_kw_length:].split()
        if value == "old":
            self.op_value = None
            self.operation = "square" if op == "*" else "double"
        else:
            self.operation = op
            self.op_value = int(value)

        self.test_value = int(lines[2][test_kw_length:])

        self.true_target = int(lines[3][true_kw_length])
        self.false_target = int(lines[4][false_kw_length])
        self.cnt = 0

    def add_item(self, new_items: list):
        self.items += new_items

    def compute(self, value):
        if self.operation == "*":
            return value * self.op_value
        elif self.operation == "+":
            return value + self.op_value
        elif self.operation == "double":
            return value * 2
        elif self.operation == "square":
            return value ** 2

    def process(self):
        output = defaultdict(list)
        for item in self.items:
            self.cnt += 1
            new_val = self.compute(item)
            new_val = new_val // 3

            if new_val % self.test_value == 0:
                output[self.true_target].append(new_val)
            else:
                output[self.false_target].append(new_val)
        self.items = []
        return output


monkies = []
while len(lines) >= 6:
    inputs, lines = lines[:6], lines[6:]
    monkies.append(Monkey(inputs[1:]))

    if len(lines) > 0 and len(lines[0]) < 1:
        lines.pop(0)

finished = lambda: sum(len(monkey.items) for monkey in monkies) < 1


def print_monkies():
    for monkey in monkies:
        print(monkey.items)


for round in range(20):
    print(f"Running round {round + 1}")
    # print_monkies()

    for monkey in monkies:
        output = monkey.process()
        for k, v in output.items():
            monkies[k].add_item(v)

counts = sorted([monkey.cnt for monkey in monkies])
print(counts[-1] * counts[-2])

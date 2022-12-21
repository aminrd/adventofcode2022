DEBUG = 0
PART_NUMBER = 1
input_file = "inputs/test.txt" if DEBUG else "inputs/day21.txt"
with open(input_file) as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]

def get_op(s):
    for c in "+-/*":
        if c in s:
            return c
    return ""

class Node:
    def __init__(self, key, s):
        self.key = key
        self.result = None

        s = s.strip()
        op = get_op(s)
        if op == "":
            self.result = int(s)
        else:
            self.op = op
            k1, k2 = s.split(op)
            self.k1 = k1.strip()
            self.k2 = k2.strip()

nodes = dict()
for line in lines:
    key = line[:4]
    nodes[key] = Node(key, line[6:])

def compute(key):
    node = nodes[key]
    if node.result is not None:
        return node.result

    v1 = compute(node.k1)
    v2 = compute(node.k2)
    if node.op == "+":
        node.result = v1 + v2
    elif node.op == "-":
        node.result = v1 - v2
    elif node.op == "*":
        node.result = v1 * v2
    else:
        node.result = v1 // v2

    return node.result

ans1 = compute("root")
print(f"Answer for part one is {ans1}")

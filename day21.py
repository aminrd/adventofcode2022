DEBUG = 0
PART_NUMBER = 2
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
        self.parametric = False

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

def compute2(key):
    node = nodes[key]

    if node.result is not None:
        return node.result, node.parametric

    v1, p1 = compute2(node.k1)
    v2, p2 = compute2(node.k2)

    node.parametric = p1 or p2

    if p1:
        node.result = v1 + [("x", node.op, v2)]
    elif p2:
        node.result = v2 + [(v1, node.op, "x")]
    else:
        if node.op == "+":
            node.result = v1 + v2
        elif node.op == "-":
            node.result = v1 - v2
        elif node.op == "*":
            node.result = v1 * v2
        else:
            node.result = v1 // v2

    return node.result, node.parametric



if PART_NUMBER == 1:
    ans1 = compute("root")
    print(f"Answer for part one is {ans1}")
else:
    nodes["humn"].parametric = True
    nodes["humn"].result = []

    root = nodes["root"]
    v1, p1 = compute2(root.k1)
    v2, p2 = compute2(root.k2)

    if p2:
        v1, v2 = v2, v1

    result = v2
    for left, op, right in v1[::-1]:
        if left == 'x':
            if op == '+':   result -= right
            elif op == '-': result += right
            elif op == '*': result //= right
            else:           result *= right
        else:
            if op == '+':   result -= left
            elif op == '-': result = left - result
            elif op == '*': result //= left
            else:           result = left // result

    print(f"Answer for part two is {result}")
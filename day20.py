from tqdm import tqdm
DEBUG = 0
PART_NUMBER = 2
input_file = "inputs/test.txt" if DEBUG else "inputs/day20.txt"
with open(input_file) as f:
    content = f.read()
    nums = list(map(int, content.split()))

n = len(nums)


class Node:
    def __init__(self, val, ind, prev=None, next=None):
        self.val = val
        self.ind = ind
        self.prev = prev
        self.next = next

    def move_right(self):
        right = self.next
        self.prev.next = right
        right.next.prev = self
        self.next = right.next
        right.prev = self.prev
        right.next = self
        self.prev = right
        self.ind, right.ind = right.ind, self.ind

    def move_left(self):
        left = self.prev
        self.next.prev = left
        left.prev.next = self
        self.prev = left.prev
        left.next = self.next
        left.prev = self
        self.next = left
        self.ind, left.ind = left.ind, self.ind

    def __str__(self):
        return f"{self.prev.val}<-[{self.val}]->{self.next.val}"

def print_nodes(nodes : list[Node]):
    s = " , ".join(node.__str__() for node in sorted(nodes, key=lambda nd: nd.ind))
    print(s)


node_zero = None
initial_order = [Node(nums[0], 0)]
for i, num in enumerate(nums[1:]):
    prev = initial_order[-1]
    new_node = Node(num, i + 1, prev=prev)
    prev.next = new_node
    initial_order.append(new_node)

    if new_node.val == 0:
        node_zero = new_node

first, last = initial_order[0], initial_order[-1]
first.prev, last.next = last, first


def sum_indices(node_0, indices: list[int]):
    sume_values = 0
    node = node_0
    indice_set = set(ind % n for ind in indices)

    for i in range(n):
        if i in indice_set:
            sume_values += node.val
        node = node.next
    return sume_values

if PART_NUMBER == 1:
    for node in tqdm(initial_order):
        if node.val > 0:
            for _ in range(node.val % (n-1)):
                node.move_right()

        elif node.val < 0:
            for _ in range((-node.val) % (n-1)):
                node.move_left()

        if DEBUG:
            print_nodes(initial_order)
            x = 1
    ans1 = sum_indices(node_zero, [1000, 2000, 3000])
    print(f"Answer for part one is {ans1}")
else:
    mult = 811589153

    for iteration in range(10):
        print(f"Running iteration #{iteration}")

        for node in tqdm(initial_order):
            if node.val > 0:
                for _ in range((node.val * mult) % (n - 1)):
                    node.move_right()

            elif node.val < 0:
                for _ in range((-node.val * mult) % (n - 1)):
                    node.move_left()

            if DEBUG:
                print_nodes(initial_order)
                x = 1

    ans2 = sum_indices(node_zero, [1000, 2000, 3000])
    print(f"Answer for part two is {ans2 * mult}")

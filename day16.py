DEBUG = 0
PART_NUMBER = 1
input_file = "inputs/test.txt" if DEBUG else "inputs/day16.txt"
with open(input_file) as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]


def copy_matrix(matrix):
    return [[c for c in row] for row in matrix]


class Node:
    def __init__(self, key, cap):
        self.key = key
        self.cap = cap
        self.adj = []
        self.dist = dict()

    def parse_adj(self, s: str):
        s = s.strip()
        if "," in s:
            adj_list = s[23:].split(',')
        else:
            adj_list = [s[22:]]

        for adj in adj_list:
            self.adj.append(adj.strip())

    def weight(self):
        return len(self.adj)

    def __str__(self):
        return f"Node : {self.key} has cap {self.cap} ----> {self.adj}"


graph = dict()
for line in lines:
    node_part, adj_part = line.split(';')
    key = node_part[6:8]
    cap = int(node_part[23:])
    graph[key] = Node(key, cap)
    graph[key].parse_adj(adj_part)

n = len(graph.keys())
key2num = {key: i for i, key in enumerate(graph.keys())}
num2key = {num: key for key, num in key2num.items()}

# Building all shortest paths
INF = 10 ** 6
dist = [[INF] * n for _ in range(n)]

for key, node in graph.items():
    num = key2num[key]
    dist[num][num] = 0
    for adj in node.adj:
        adj_num = key2num[adj]
        dist[num][adj_num] = 1


for r in range(n):
    for p in range(n):
        for q in range(n):
            dist[p][q] = min(dist[p][q], dist[p][r] + dist[r][q])

for i, key in num2key.items():
    node = graph[key]
    for j, adj in num2key.items():
        node.dist[adj] = dist[i][j]

# Finding all non-zero capacities
non_zero_caps = [key for key, node in graph.items() if node.cap > 0]
non_zero_caps.sort(key=lambda x: graph[x].cap, reverse=True)


def upperbound(not_visited, limit):
    sorted_caps = sorted([graph[key].cap for key in not_visited], reverse=True)
    return sum((limit-i)*cap for i, cap in enumerate(sorted_caps))


# Best = [DD, BB, JJ, HH, EE, CC]
def traverse(node: Node, limit: int, open_sofar: int, not_visited: set, best: int):
    if node.cap > 0:
        open_sofar += limit * node.cap
    best = max(best, open_sofar)
    if len(not_visited) < 1:
        return best

    if upperbound(not_visited, limit-2) + open_sofar < best:
        return best

    for next_key in not_visited:
        d = node.dist[next_key]
        if d+1 >= limit:
            continue

        next_node = graph[next_key]
        result = traverse(next_node, limit-d-1, open_sofar, not_visited - {next_key}, best)
        best = max(best, result)

    return best

ans1 = traverse(graph["AA"], 30, 0, set(non_zero_caps), 0)
print(f"Answer one is {ans1}")

DEBUG = 0
PART_NUMBER = 1
input_file = "inputs/test.txt" if DEBUG else "inputs/day18.txt"
with open(input_file) as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]


cubes = set()
for line in lines:
    x, y, z = map(int, line.split(','))
    cubes.add((x, y, z))

def get_adj(x,y,z):
    adj = [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]
    return adj

sides = 0
for cube in cubes:
    sides += sum(adj not in cubes for adj in get_adj(*cube))

ans1 = sides
print(f"Answer part one is {ans1}")
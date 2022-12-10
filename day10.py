from bisect import bisect_left

#with open("inputs/test.txt") as f:
with open("inputs/day10.txt") as f:
    lines = f.readlines()

lines = [line.strip() for line in lines]

x = 1
t = 0

values = [(0, 1)]
eps = 0.00000001

for line in lines:
    if line.startswith("noop"):
        t += 1
    elif line.startswith("addx"):
        _, val = line.split()
        x += int(val)
        t += 2
    values.append((t + eps, x))


query = [20, 60, 100, 140, 180, 220]
times = [t for t, _ in values]

strength = 0
for qt in query:
    ind = bisect_left(times, qt)
    if times[ind] <= qt:
        strength += qt * values[ind][1]
    else:
        strength += qt * values[ind-1][1]

print(strength)
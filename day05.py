with open("inputs/day5.txt") as f:
    content = f.readlines()

lines = content

top = []
moves = []
N = 9

while len(lines) > 0 and len(lines[0]) == N * 4:
    top.append(lines.pop(0))

rest = [l.strip() for l in lines[1:]]

stacks = [[] for _ in range(N)]
top = top[:-1][::-1]

for t in top:
    for i in range(N):
        val = t[4 * i : 4 * i + 4]
        if val[1] != " ":
            stacks[i].append(val[1])

question_part_number = 1

for r in rest:
    params = r.split()

    cnt = int(params[1])
    src = int(params[3])
    dst = int(params[-1])

    if question_part_number == 1:
        for c in range(cnt):
            stacks[dst - 1].append(stacks[src - 1].pop(0))
    else:
        stacks[dst - 1] += stacks[src - 1][-cnt:]
        stacks[src - 1] = stacks[src - 1][:-cnt]

ans = "".join(s[-1] for s in stacks)
print(ans)

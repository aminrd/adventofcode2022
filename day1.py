with open("inputs/day1.txt") as f:
    content = f.read()

separated = content.split('\n\n')
elves = [[int(num) for num in s.split()] for s in separated]

ans1 = max(sum(e) for e in elves)
print(ans1)

sorted_list = list(sorted(sum(e) for e in elves))
ans2 = sorted_list[-3:]
print(sum(ans2))

print('Finish')
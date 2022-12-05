class Range:
    def __init__(self, pair):
        s, e = pair.split('-')
        self.start = int(s)
        self.end = int(e)

    def cover(self, other):
        return self.start <= other.start and self.end >= other.end

    def has_overlap(self, other):
        if self.end < other.start or other.end < self.start:
            return False
        return True


with open("inputs/day4.txt") as f:
    content = f.readlines()

cover_cnt = 0
has_overlap = 0
for line in content:
    if line.endswith('\n'):
        line = line[:-1]
    pairs = line.split(',')

    r0 = Range(pairs[0])
    r1 = Range(pairs[1])

    if r0.cover(r1) or r1.cover(r0):
        cover_cnt += 1

    if r0.has_overlap(r1):
        has_overlap += 1

print(cover_cnt)
print(has_overlap)

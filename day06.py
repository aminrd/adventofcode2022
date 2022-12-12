with open("inputs/day6.txt") as f:
    content = f.read().strip()


def find_start_index(index_size):
    last = list(content[:index_size])
    for i in range(index_size, len(content)):
        if len(set(last)) < index_size:
            last = last[1:] + [content[i]]
        else:
            return i


part_one = find_start_index(4)
part_two = find_start_index(14)

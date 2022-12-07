with open("inputs/day7.txt") as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class Directory:
    def __init__(self):
        self.files = dict()
        self.children = dict()

    def get_file_sum(self):
        if len(self.files.keys()) < 1:
            return 0
        return sum(f.size for f in self.files.values())

    def file_count(self):
        return len(self.files.keys())

    def dir_count(self):
        return len(self.children.keys())


root = Directory()
path = [root]


def parse_line(line: str):
    if line.startswith("dir"):
        _, name = line.split()
        return "Directory", name, 0
    else:
        size, name = line.split()
        return "File", name, int(size)


while len(lines) > 0:
    line = lines.pop(0)[2:]

    if line.startswith("cd"):
        rest = line[3:]
        if rest == "..":
            path.pop(-1)
        elif rest == "/":
            path = [root]
        else:
            current = path[-1]
            path.append(current.children[rest])
    elif line.startswith("ls"):
        # read more lines

        while len(lines) > 0 and not lines[0].startswith("$"):
            line = lines.pop(0)
            c_type, name, size = parse_line(line)

            if c_type == "File":
                if name not in path[-1].files.keys():
                    path[-1].files[name] = File(name, size)
            else:
                if name not in path[-1].children.keys():
                    path[-1].children[name] = Directory()


def traverse_tree(root: Directory, threshold=100000):
    # Return : (this_size, sum_of_all_below_threshold)
    total_sum = 0

    current_size = root.get_file_sum()
    if root.dir_count() < 1:
        if current_size <= threshold:
            return current_size, current_size
        else:
            return current_size, 0

    dir_sum = 0
    for child in root.children.values():
        dir_size, traverse_sum = traverse_tree(child, threshold)
        total_sum += traverse_sum
        dir_sum += dir_size

    total_current_size = dir_sum + current_size
    if total_current_size <= threshold:
        total_sum += total_current_size

    return total_current_size, total_sum


print(traverse_tree(root))

disk_size = 70000000
space_needed = 30000000

directory_sizes = dict()


def size_traverse(root: Directory, path):
    current = root.get_file_sum()
    if len(root.children) < 1:
        directory_sizes[path] = current
        return current

    dir_sum = sum(size_traverse(child, path + "/" + name) for name, child in root.children.items())
    current += dir_sum

    directory_sizes[path] = current
    return current


size_traverse(root, "/")

size_array = sorted([dsize for dsize in directory_sizes.values()])
used_space = sum(size_array)

for dsize in size_array:
    if (disk_size - size_array[-1] + dsize) >= space_needed:
        print(f"answer 2 = {dsize}")
        break

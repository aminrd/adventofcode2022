DEBUG = 0
PART_NUMBER = 1
input_file = "inputs/test.txt" if DEBUG else "inputs/day25.txt"
with open(input_file) as f:
    lines = f.readlines()
lines = [line.strip() for line in lines]


decimal_map = {
    '0': 0,
    '1': 1,
    '2': 2,
    '-': -1,
    '=': -2
}
sanfu_map = {
    0: '0',
    1: '1',
    2: '2',
    -1: '-',
    -2: '='
}

def to_decimal(s):
    num = 0
    for c in s:
        num = num * 5 + decimal_map[c]
    return num

def to_sanfu(num):
    i = 0
    arr = [0] * 200

    while num > 0 or arr[i] > 2:
        num, mod = divmod(num, 5)
        arr[i] += mod
        arr[i+1] += arr[i] // 5
        arr[i] = arr[i] % 5
        if arr[i] == 4:
            arr[i+1] += 1
            arr[i] = -1
        elif arr[i] == 3:
            arr[i+1] += 1
            arr[i] = -2

        i += 1

    while len(arr) > 0 and arr[-1] == 0:
        arr.pop(-1)

    if len(arr) < 1:
        return '0'

    return "".join(sanfu_map[c] for c in arr[::-1])

total = sum(to_decimal(line) for line in lines)
print(to_sanfu(total))
from collections import Counter
def process_input(inp):
    patterns = []
    pattern = []
    for l in inp.split("\n"):
        if l=='':
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(list(l))
    patterns.append(pattern)
    ph, pw = len(pattern), len(pattern[0])
    locks, keys = [], []
    for pattern in patterns:
        if pattern[0] == ["#"]*len(pattern[0]):
            # lock
            cols = []
            for c in range(pw):
                col_len = Counter([pattern[h][c] for h in range(ph)])["#"]-1
                cols.append(col_len)
            locks.append(cols)
        else:
            # key
            cols = []
            for c in range(pw):
                col_len = Counter([pattern[h][c] for h in range(ph)])["#"]-1
                cols.append(col_len)
            keys.append(cols)
    return locks, keys, ph, pw

def sol1_bruteforce(locks, keys, height, width):
    count = 0
    for l in locks:
        for k in keys:
            valid = True
            for i in range(len(l)):
                if l[i]+k[i]>height-2:
                    valid = False
                    break
            if valid:
                count += 1
    return count

test_input = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

test_locks, test_keys, height, width = process_input(test_input)
print(sol1_bruteforce(test_locks, test_keys, height, width))

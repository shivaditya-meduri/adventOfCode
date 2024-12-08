from collections import defaultdict
def process_input(inp):
    return [list(i) for i in inp.split("\n") if i!=""]


def cal_antinodes(an1, an2):
    antinode1_x, antinode1_y = an1[0]+(an1[0]-an2[0]), an1[1]+(an1[1]-an2[1])
    antinode2_x, antinode2_y = an2[0]+(an2[0]-an1[0]), an2[1]+(an2[1]-an1[1])
    return [[antinode1_x, antinode1_y], [antinode2_x, antinode2_y]]
def sol1_bruteforce(inp):
    antennas = defaultdict(list)
    height, width = len(inp), len(inp[0])
    for i in range(height):
        for j in range(width):
            if inp[i][j] != ".":
                antennas[inp[i][j]].append([i, j])
    antinodes = set()
    for ant, locations in antennas.items():
        num_antennas = len(locations)
        for i in range(num_antennas):
            for j in range(i+1, num_antennas):
                for antinode_x, antinode_y in cal_antinodes(locations[i], locations[j]):
                    if 0<=antinode_x<height and 0<=antinode_y<width:
                        antinodes.add((antinode_x, antinode_y))
    return len(antinodes)    

def is_whole_number(x):
    return abs(round(x) - x) < 1e-10
def get_line_points(h1, w1, h2, w2, height, width):
    points = set()
    if w2-w1 == 0: # vertical line
        for h in range(height):
            points.add((h, w1))
        return points
    if h2-h1 == 0: # horizontal line
        for w in range(width):
            points.add((h1, w))
        return points
    m = (h2-h1)/(w2-w1)
    c = h2-m*w2
    for w in range(width):
        h = m*w+c
        if is_whole_number(h):
            points.add((int(round(h)), w))
    for h in range(height):
        w = (h-c)/m
        if is_whole_number(w):
            points.add((h, int(round(w))))
    return points

def sol2_bruteforce(inp):
    antennas = defaultdict(list)
    height, width = len(inp), len(inp[0])
    for i in range(height):
        for j in range(width):
            if inp[i][j] != ".":
                antennas[inp[i][j]].append([i, j])
    antinodes = set()
    for ant, locations in antennas.items():
        num_antennas = len(locations)
        for i in range(num_antennas):
            for j in range(i+1, num_antennas):
                for antinode_x, antinode_y in get_line_points(locations[i][0], locations[i][1], locations[j][0], locations[j][1], height, width):
                    if 0<=antinode_x<height and 0<=antinode_y<width:
                        antinodes.add((antinode_x, antinode_y))
    return antinodes

test_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

test_input = process_input(test_input)
print(sol1_bruteforce(inp))
print(len(sol2_bruteforce(test_input)))

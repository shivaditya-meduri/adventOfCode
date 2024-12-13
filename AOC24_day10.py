def generate_topographical_map(inp):
    return [list(map(int, list(i))) for i in inp.split("\n") if i!=""]

def get_trail_score(h, w, topological_map, trail_ends = None):
    # Returns number of unique 9 positions that can be reached from the given trail head using flood fill algorithm
    height, width = len(topological_map), len(topological_map[0])
    if trail_ends is None:
        trail_ends = defaulr
    if topological_map[h][w] == 9:
        trail_ends.add((h, w))
        return trail_ends
    # extend in 4 directions
    for diff_h, diff_y in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
        h2, w2 = h+diff_h, w+diff_y
        if 0 <= h2 < height and 0 <= w2 < width:
            if topological_map[h2][w2] == topological_map[h][w]+1:
                trail_ends = get_trail_score(h2, w2, topological_map, trail_ends) #Up
    return trail_ends
    
def sol1_floodfill(topological_map):
    height, width = len(topological_map), len(topological_map[0])
    trail_head_scores = []
    for h in range(height):
        for w in range(width):
            if topological_map[h][w]==0:
                trail_ends = get_trail_score(h, w, topological_map)
                trail_head_scores.append(len(trail_ends))
    return sum(trail_head_scores)

from collections import defaultdict

def get_trailhead_rating(h, w, topological_map, trail_ends=None):
    height, width = len(topological_map), len(topological_map[0])
    if trail_ends is None:
        trail_ends = defaultdict(int)
    if topological_map[h][w]==9:
        trail_ends[(h, w)] += 1
        return trail_ends
    for diff_h, diff_w in [[-1, 0], [1, 0], [0, 1], [0, -1]]:
        h2, w2 = h+diff_h, w+diff_w
        if 0<=h2<height and 0<=w2<width:
            if topological_map[h2][w2] == 1+topological_map[h][w]:
                trail_ends = get_trailhead_rating(h2, w2, topological_map, trail_ends)
    return trail_ends

def sol2_floodfill(topological_map):
    height, width = len(topological_map), len(topological_map[0])
    trail_head_scores = []
    for h in range(height):
        for w in range(width):
            if topological_map[h][w]==0:
                trail_ends = get_trailhead_rating(h, w, topological_map)
                trail_head_scores.append(sum(list(dict(trail_ends).values())))
    return sum(trail_head_scores)

test_input = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
topological_map = generate_topographical_map(test_input)
print(sol1_floodfill(topological_map))
print(sol2_floodfill(topological_map))

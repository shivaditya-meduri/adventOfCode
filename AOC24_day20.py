from collections import defaultdict
import heapq
def process_input(inp):
    code_map = []
    for l in inp.split("\n"):
        if l!="":
            code_map.append(list(l))
    return code_map

def map2graph(code_map):
    code_graph = defaultdict(list)
    dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]] #Up, Down, Left, Right
    height, width = len(code_map), len(code_map[0])
    for hi in range(height):
        for wi in range(width):
            if code_map[hi][wi] == "S":
                start_h, start_w = hi, wi
            if code_map[hi][wi] == "E":
                end_h, end_w = hi, wi
            if code_map[hi][wi] != "#":
                for diff_h, diff_w in dirs:
                    h2, w2 = hi+diff_h, wi+diff_w
                    if 0<=h2<height and 0<=w2<width:
                        if code_map[h2][w2] != "#":
                            code_graph[(hi, wi)].append((h2, w2))
    return code_graph, start_h, start_w, end_h, end_w


def dijkstras(code_graph, start_h, start_w, end_h, end_w):
    distance_hashmap = {n:float('inf') for n in code_graph.keys()}
    distance_hashmap[(start_h, start_w)] = 0
    parent_hashmap = {n:None for n in code_graph.keys()}
    parent_hashmap[(start_h, start_w)] = (start_h, start_w)
    pq = [[0, start_h, start_w]]
    visited = set()
    while pq:
        cost, hi, wi = heapq.heappop(pq)
        if hi==end_h and wi==end_w:
            path = []
            current = (hi, wi)
            while current != (start_h, start_w):
                path.append(current)
                current = parent_hashmap[current]
            path.append((start_h, start_w))
            return cost, path[::-1]
        if (hi, wi) not in visited:
            visited.add((hi, wi))
            for nh, nw in code_graph[(hi, wi)]:
                if (nh, nw) not in visited:
                    new_distance = cost+1
                    if new_distance < distance_hashmap[(nh, nw)]:
                        distance_hashmap[(nh, nw)] = new_distance
                        parent_hashmap[(nh, nw)] = (hi, wi)
                        heapq.heappush(pq, (new_distance, nh, nw))
    return float('inf'), []

def sol(code_map, max_cheat, min_dist_saved):
    # No need for dijkstras
    # can simply determine the distance saved by substracting the manhattan distance between 2 points where phasing will be applied when compared to actual distance
    height, width = len(code_map), len(code_map[0])
    code_graph, start_h, start_w, end_h, end_w = map2graph(code_map)
    shortest_distance, shortest_distance_path = dijkstras(code_graph, start_h, start_w, end_h, end_w)
    dot_points = []
    for hi in range(height):
        for wi in range(width):
            if code_map[hi][wi] != "#":
                dot_points.append([hi, wi])
    dot_count = len(dot_points)
    valid_dot_combs = []
    for i in range(dot_count):
        for j in range(i+1, dot_count):
            h1, w1 = dot_points[i]
            h2, w2 = dot_points[j]
            if abs(h2-h1)+abs(w2-w1) <= max_cheat:
                valid_dot_combs.append([(h1, w1), (h2, w2)])
    distanceLeft = {}
    shortest_distance_copy = shortest_distance
    for (i,j) in shortest_distance_path:
        distanceLeft[(i, j)] = shortest_distance_copy
        shortest_distance_copy -= 1
    distanceSaved = {}
    for (h1, w1), (h2, w2) in valid_dot_combs:
        md = abs(h2-h1) + abs(w2-w1)
        ad = abs(distanceLeft[(h1, w1)]- distanceLeft[(h2, w2)])
        distanceSaved[(h1, w1, h2, w2)] = ad-md
    return len([[k, v] for k,v in distanceSaved.items() if v>=min_dist_saved])

test_input = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
test_code_map = process_input(test_input)
print(sol(code_map=test_code_map, max_cheat=2, min_dist_saved=100))
print(sol(code_map=test_code_map, max_cheat=20, min_dist_saved=100))

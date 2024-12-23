def process_input(inp, height, width, bits_fallen):
    memory_grid = [["."]*width for _ in range(height)]
    inp = [list(map(int, i.split(","))) for i in  inp.split("\n") if i!=""]
    for wi, hi in inp[:bits_fallen]:
        memory_grid[hi][wi] = "#"
    return memory_grid

from collections import defaultdict
import heapq
def memgrid2graph(mem_grid):
    # adjacency list representation
    g = defaultdict(list)
    dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]] #Up, Down, Left, Right
    height, width = len(mem_grid), len(mem_grid[0])
    for hi in range(height):
        for wi in range(width):
            for diff_h, diff_w in dirs:
                h2, w2 = hi+diff_h, wi+diff_w
                if 0<=h2<height and 0<=w2<width and mem_grid[h2][w2]!="#":
                    g[(hi, wi)].append([h2, w2])
    return g
def dijkstras(graph, start_h, start_w, end_h, end_w):
    pq = [(0, start_h, start_w)]
    distance_hashmap = {n:float('inf') for n in graph.keys()}
    distance_hashmap[(start_h, start_w)] = 0
    prev_hashmap = {n:None for n in graph.keys()}
    prev_hashmap[(start_h, start_w)] = (start_h, start_w)
    visited = set()
    while pq:
        current_dist, hi, wi = heapq.heappop(pq) 
        if (hi, wi) in visited:
            continue
        visited.add((hi, wi))
        if hi==end_h and wi==end_w:
            path = []
            current = (hi, wi)
            while current in prev_hashmap and current != prev_hashmap[current]:
                path.append(current)
                current = prev_hashmap[current]
            path.append((start_h, start_w))
            return current_dist, path[::-1]
        for n_h, n_w in graph[(hi, wi)]:
            if (n_h, n_w) not in visited:  # Added visited check here too
                new_distance = 1 + current_dist
                if new_distance < distance_hashmap[(n_h, n_w)]:
                    distance_hashmap[(n_h, n_w)] = new_distance
                    prev_hashmap[(n_h, n_w)] = (hi, wi)
                    heapq.heappush(pq, (new_distance, n_h, n_w))
    return float('inf'), []
def sol1_pathfinding(inp, height, width, bitstaken):
    memory_grid = process_input(inp, height, width, bitstaken)
    start_h, start_w, end_h, end_w = 0, 0, len(memory_grid)-1, len(memory_grid[0])-1
    g = memgrid2graph(memory_grid)
    return dijkstras(g, start_h, start_w, end_h, end_w)[0]
def sol2(inp, height, width):
    num_bytes = len([i for i in inp.split("\n") if i!=""])
    for i in range(num_bytes):
        if sol1_pathfinding(inp, height, width, i)==float('inf'):
            return [i for i in inp.split("\n") if i!=""][i-1]

test_width, test_height = 7, 7
test_input = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
print(sol1_pathfinding(test_input, test_height, test_width, 12))
print(sol2(test_input, test_height, test_width))

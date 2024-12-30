import heapq
from functools import lru_cache
from itertools import product, chain

numpad = {'7':(0, 0), '8':(0, 1), '9':(0, 2), '4':(1, 0), '5':(1, 1), '6':(1, 2), '1':(2, 0), '2':(2, 1), '3':(2, 2), '0':(3, 1), 'A':(3, 2)} 
dpad = {'^':(0,1), 'A':(0,2), '<':(1,0),'v':(1,1), '>':(1,2)}
dirs = [[-1, 0, '^'], [1, 0, 'v'], [0, 1, '>'], [0, -1, '<']] #Up, Down, Right, Left
a2k_dist = {">":0, "^":1, "v":2, "<":3}

def extract_path(parent_hashmap, curr_h, curr_w, tar_h, tar_w, path=None):
    if path is None:
        path = []
    if (curr_h,curr_w)==(tar_h, tar_w):
        return [path[::-1]]
    paths = []
    for ch, cw, dm in parent_hashmap[(curr_h, curr_w)]:
        path2 = path.copy()
        path2.append(dm)
        paths.extend(extract_path(parent_hashmap, ch, cw, tar_h, tar_w, path2))
    return paths

def dijkstras(start_code, code, pad_dict):
    distance_hashmap = {v : float('inf') for v in pad_dict.values()}
    distance_hashmap[pad_dict[start_code]] = 0
    parent_hashmap = {v : [] for v in pad_dict.values()}
    start_h, start_w = pad_dict[start_code]
    end_h, end_w = pad_dict[code]
    pq = [[0, start_h, start_w]]
    visited = set()
    while pq:
        cost, hi, wi = heapq.heappop(pq)
        if (hi, wi) in visited:
            continue
        visited.add((hi, wi))
        if hi==end_h and wi==end_w:
            return extract_path(parent_hashmap, end_h, end_w, start_h, start_w)
        else:
            for diff_h, diff_w, dmove in dirs:
                h2, w2 = hi+diff_h, wi+diff_w
                if (h2, w2) in distance_hashmap:
                    new_cost = 1+cost
                    if new_cost <= distance_hashmap[(h2, w2)]:
                        distance_hashmap[(h2, w2)] = new_cost
                        parent_hashmap[(h2, w2)].append((hi, wi, dmove))
                        heapq.heappush(pq, [new_cost, h2, w2])
    return [] # No paths found

def generate_ways(a, b , keypad):
    ways = dijkstras(a, b, keypad)
    for wi in range(len(ways)):
        ways[wi] += ["A"]
    return ways

from functools import lru_cache

@lru_cache(None)
def get_min_cost(A, B, depth):
    if depth == 1:
        return min([len(l) for l in generate_ways(A, B, dpad)])
    ways = generate_ways(A, B, dpad)
    min_cost = float('inf')
    for way in ways:
        start_code = "A"
        way_cost = 0
        for code in way:
            cost = get_min_cost(start_code, code, depth-1)
            way_cost += cost
            start_code = code
        min_cost = min(min_cost, way_cost)
    #print(A, B, depth, ways, min_cost)
    return min_cost

def sol(inp_codes, depth):
    # Using dynamic programming and state compression
    # Recursive way to calculate costs of one move in the numpad level to the historian level
    comp = 0
    for codes in inp_codes:
        codes = list(codes)
        num_part = int("".join([i for i in codes if i.isdigit()]))
        start_code = 'A'
        paths = []
        for code in codes:
            if code != start_code:
                ps = dijkstras(start_code, code, numpad)
                for pi in range(len(ps)):
                    ps[pi] += ["A"]
                paths.append(ps)
            else:
                paths.append([["A"]])
            start_code = code
        ways1 = [list(chain(*l)) for l in product(*paths)]
        min_cost = float('inf')
        for way in ways1:
            way_cost = 0
            start_code = "A"
            for code in way:
                cost = get_min_cost(start_code, code, depth)
                way_cost += cost
                start_code = code
            min_cost = min(way_cost, min_cost)
        comp += min_cost*num_part
    return comp

print(sol(["985A", "540A", "463A", "671A", "382A"], 2)) # Part 1
print(sol(["985A", "540A", "463A", "671A", "382A"], 25)) # Part 2

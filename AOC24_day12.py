from collections import defaultdict

def process_input(inp):
    return [list(i) for i in inp.split("\n") if i!=""]

def process_input(inp):
    return [list(i) for i in inp.split("\n") if i!=""]
def calc_perimeter(region, height, width):
    region_perimeter = 0
    for hi, wi in region:
        diffs = [[0, 1], [0, -1], [1, 0], [-1, 0]] # Right, Left, Down, Up
        for diff_h, diff_w in diffs:
            h2, w2 = hi+diff_h, wi+diff_w
            if (h2, w2) not in region:
                region_perimeter += 1
    return region_perimeter
    
def calc_fence_cost(regions, height, width):
    cost = 0
    for region in regions:
        area = len(region)
        perimeter = calc_perimeter(region, height, width)
        cost += area*perimeter
    return cost
def flood_fill(h, w, inpmap, region = None):
    if region is None:
        region = set()
    height, width = len(inpmap), len(inpmap[0])
    if (h, w) in region:
        return region
    region.add((h, w))
    diffs = [[0, 1], [0, -1], [1, 0], [-1, 0]] # Right, Left, Down, Up
    for diff_h, diff_w in diffs:
        h2, w2 = h+diff_h, w+diff_w
        if 0 <= h2 < height and 0 <= w2 < width and inpmap[h2][w2]==inpmap[h][w]:
            region.update(flood_fill(h2, w2, inpmap, region))
    return region 
def sol_floodfill(inp):
    height, width = len(inp), len(inp[0])
    regions = []
    for h in range(height):
        for w in range(width):
            already_seen = False
            for r in regions:
                if (h, w) in r:
                    already_seen = True
                    break
            if already_seen:
                continue
            regions.append(flood_fill(h, w, inp))
    return calc_fence_cost(regions, height, width)

test_input = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
test_input = process_input(test_input)
sol_floodfill(test_input)

### Part 2
def perimeter_ff(h, w, boundary, d, visited=None, side=None):
    if visited is None:
        visited = set()
    if side is None:
        side = set()
    if (h, w) in visited:
        return side
    visited.add((h, w))
    side.add((h, w))
    if d=='h':
        if (h, w-1) in boundary:
            side.update(perimeter_ff(h, w-1, boundary, d, visited, side))
        if (h, w+1) in boundary:
            side.update(perimeter_ff(h, w+1, boundary, d, visited, side))
    elif d=='v':
        if (h-1, w) in boundary:
            side.update(perimeter_ff(h-1, w, boundary, d, visited, side))
        if (h+1, w) in boundary:
            side.update(perimeter_ff(h+1, w, boundary, d, visited, side))
    return side
def calc_perimeter_2(region):
    region_perimeter = 0
    boundary = []
    for hi, wi in region:
        diffs = [["r", 0, 1], ["l", 0, -1], ["d", 1, 0], ["u", -1, 0]] # Right, Left, Down, Up
        for d, diff_h, diff_w in diffs:
            h2, w2 = hi+diff_h, wi+diff_w
            if (h2, w2) not in region:
                region_perimeter += 1
                boundary.append((d, h2, w2))
    number_sides = 0
    for d in ["r", "l", "d", "u"]: 
        vp = [(bi[1], bi[2]) for bi in boundary if bi[0]==d]
        vsides = []
        for x,y in vp:
            already_covered=False
            if len(vsides)!=0:
                for side in vsides:
                    if (x,y) in side:
                        already_covered=True
                        break
            if not already_covered:
                if d=="u" or d=="d":
                    vsides.append(perimeter_ff(x, y, vp, 'h'))
                elif d=="l" or d=="r":
                    vsides.append(perimeter_ff(x, y, vp, 'v'))
        number_sides += len(vsides)
    return number_sides
def calc_fence_cost_2(regions, height, width):
    cost = 0
    for region in regions:
        area = len(region)
        perimeter = calc_perimeter_2(region)
        cost += area*perimeter
    return cost
def sol_floodfill_2(inp):
    height, width = len(inp), len(inp[0])
    regions = []
    for h in range(height):
        for w in range(width):
            already_seen = False
            for r in regions:
                if (h, w) in r:
                    already_seen = True
                    break
            if already_seen:
                continue
            regions.append(flood_fill(h, w, inp))
    return calc_fence_cost_2(regions, height, width)

test_input = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
test_input = process_input(test_input)
sol_floodfill_2(test_input)


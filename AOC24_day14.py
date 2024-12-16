def process_input(inp):
    robots = []
    for line in inp.split("\n"):
        if line!="":
            pw, ph = map(int, line.split(" ")[0].replace("p=", "").split(","))
            vw, vh = map(int, line.split(" ")[1].replace("v=", "").split(","))
            robots.append([ph, pw, vh, vw])
    return robots

def sol1_bruteforce(inp, inpH, inpW, time=100):
    final_state = []
    for ph, pw, vh, vw in inp:
        for _ in range(time):
            ph += vh
            pw += vw
            ph = ph%inpH
            pw = pw%inpW
        final_state.append([ph, pw])
    inpMap = [[0 for _ in range(inpW)] for _ in range(inpH)]
    for ph, pw in final_state:
        inpMap[ph][pw] = inpMap[ph][pw] + 1
    tlq = [l[:(inpW//2)] for l in inpMap[:inpH//2]]
    trq = [l[(inpW//2)+1:] for l in inpMap[:inpH//2]]
    blq = [l[:(inpW//2)] for l in inpMap[(inpH//2)+1:]]
    brq = [l[(inpW//2)+1:] for l in inpMap[(inpH//2)+1:]]
    num_robots = lambda q: sum(sum(sublist) for sublist in q)
    safety_factor = num_robots(tlq)*num_robots(trq)*num_robots(blq)*num_robots(brq)
    return safety_factor

test_input = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
test_width, test_height = 11, 7
robots = process_input(test_input)
print(sol1_bruteforce(robots, test_height, test_width))


# Christmas tree is in one of the quadrants and in the time frame when this happens the safety factor will be minimum as robots will all be concentrated in that quadrant

# Find the time second where the safety factor is the minimum

# Maximum time is width * height because after that the patterns will start repeating again


def sol2_minimumsf(inp, inpH, inpW):
    best_iteration, min_sf = None, float('inf')
    for frame in range(inpH*inpW):
        final_state = []
        for ph, pw, vh, vw in inp:
            ph += vh
            pw += vw
            ph = ph%inpH
            pw = pw%inpW
            final_state.append([ph, pw, vh, vw])
        inpMap = [[0 for _ in range(inpW)] for _ in range(inpH)]
        for ph, pw, _, _ in final_state:
            inpMap[ph][pw] = inpMap[ph][pw] + 1
        tlq = [l[:(inpW//2)] for l in inpMap[:inpH//2]]
        trq = [l[(inpW//2)+1:] for l in inpMap[:inpH//2]]
        blq = [l[:(inpW//2)] for l in inpMap[(inpH//2)+1:]]
        brq = [l[(inpW//2)+1:] for l in inpMap[(inpH//2)+1:]]
        num_robots = lambda q: sum(sum(sublist) for sublist in q)
        safety_factor = num_robots(tlq)*num_robots(trq)*num_robots(blq)*num_robots(brq)
        if safety_factor < min_sf:
            min_sf = safety_factor
            best_iteration = frame
        inp = final_state
    return best_iteration+1

test_input = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
test_width, test_height = 11, 7
robots = process_input(test_input)
sol2_minimumsf(robots, test_height, test_width)

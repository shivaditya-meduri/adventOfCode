from collections import defaultdict

def process_input(inp):
    return [int(i) for i in inp.replace("\n", "").split(" ") if i!=""]

def evolve_stone(s, blinks, dpDict=None):
    if blinks==0:
        return 1
    if dpDict is None:
        dpDict = defaultdict(int)
    if (s, blinks) in dpDict:
        return dpDict[(s, blinks)]
    s_str = str(s)
    strlen = len(s_str)
    if s==0:
        p = evolve_stone(1, blinks-1, dpDict)
        dpDict[(s, blinks)] = p
        return p
    elif strlen%2==0:
        p1 = evolve_stone(int(s_str[:(strlen//2)]), blinks-1, dpDict)
        p2 = evolve_stone(int(s_str[(strlen//2):]), blinks-1, dpDict)
        dpDict[(s, blinks)] = p1+p2
        return p1+p2
    else:
        p = evolve_stone(s*2024, blinks-1, dpDict)
        dpDict[(s, blinks)] = p
        return p
    
def sol_dynamicProgramming(stone_state, blinks):
    dpDict = defaultdict(int)
    out = 0
    for s in stone_state:
        out += evolve_stone(s, blinks, dpDict)
    return out
inp = "0 4 4979 24 4356119 914 85734 698829"
inp = process_input(inp)
print(sol_dynamicProgramming(inp, 75))

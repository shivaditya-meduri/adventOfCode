import copy
def sol1_bruteforce(inp):
    inp_map = copy.deepcopy(inp)
    height, width = len(inp_map), len(inp_map[0])
    for i in range(height):
        for j in range(width):
            if inp_map[i][j] in ["^", "v", ">", "<"]:
                s_x, s_y = i, j
    dir_map = {"^":[-1, 0], "v":[1, 0], ">":[0, 1], "<":[0, -1]}
    turn90 = {"^":">",">":"v","v":"<","<":"^"}
    visited = set()
    visited.add((s_x, s_y))
    while True:
        diff_x, diff_y = dir_map[inp_map[s_x][s_y]]
        new_x, new_y = s_x+diff_x, s_y+diff_y
        if not 0<=new_x<height or not 0<=new_y<width: # Out of the grid
            break
        elif inp_map[new_x][new_y] == "#": # Obstacle
            inp_map[s_x][s_y] = turn90[inp_map[s_x][s_y]]
            continue
        else:
            inp_map[new_x][new_y] = inp_map[s_x][s_y]
            inp_map[s_x][s_y] = "."
            s_x, s_y = new_x, new_y
            visited.add((s_x, s_y))
    return visited
def process_input(inp):
    return [list(i) for i in inp.split("\n") if i!=""]
print(len(sol1_bruteforce(test_input)))
def loop_detected(inp):
    inp_map = copy.deepcopy(inp)
    height, width = len(inp_map), len(inp_map[0])
    for i in range(height):
        for j in range(width):
            if inp_map[i][j] in ["^", "v", ">", "<"]:
                s_x, s_y = i, j
    dir_map = {"^":[-1, 0], "v":[1, 0], ">":[0, 1], "<":[0, -1]}
    turn90 = {"^":">",">":"v","v":"<","<":"^"}
    visited = set()
    visited.add((s_x, s_y, inp_map[s_x][s_y]))
    while True:
        diff_x, diff_y = dir_map[inp_map[s_x][s_y]]
        new_x, new_y = s_x+diff_x, s_y+diff_y
        if not 0<=new_x<height or not 0<=new_y<width: # Out of the grid
            break
        elif inp_map[new_x][new_y] == "#": # Obstacle
            inp_map[s_x][s_y] = turn90[inp_map[s_x][s_y]]
            if (s_x, s_y, inp_map[s_x][s_y]) in visited:
                return True
            else:
                visited.add((s_x, s_y, inp_map[s_x][s_y]))
            continue
        else:
            inp_map[new_x][new_y] = inp_map[s_x][s_y]
            inp_map[s_x][s_y] = "."
            s_x, s_y = new_x, new_y
            if (s_x, s_y, inp_map[s_x][s_y]) in visited:
                return True
            else:
                visited.add((s_x, s_y, inp_map[s_x][s_y]))
    return False
    
def sol2_bruteforce(inp):
    guard_path = sol1_bruteforce(inp)
    height, width = len(inp), len(inp[0])
    for i in range(height):
        for j in range(width):
            if inp[i][j] in ["^", "v", ">", "<"]:
                s_x, s_y = i, j
    guard_path.remove((s_x, s_y))
    possible_obstacle_positions = []
    for x, y in guard_path:
        inp_map_with_obstacle = copy.deepcopy(inp)
        inp_map_with_obstacle[x][y] = "#"
        if loop_detected(inp_map_with_obstacle):
            possible_obstacle_positions.append([x, y])
    return possible_obstacle_positions

print(len(sol2_bruteforce(test_input)))

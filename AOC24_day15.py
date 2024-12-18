def process_input(inp):
    inpMap = []
    attempts = []
    for ln, i in enumerate(inp.split("\n")):
        if i!="":
            inpMap.append(list(i))
        else:
            emptyLine = ln
            break
    for i in inp.split("\n")[emptyLine+1:]:
        if i!="":
            attempts.extend(list(i))
    return inpMap, attempts

def evolve_map(mapi, robot_h, robot_w, attempt):
    dir_map = {'^':[-1, 0], 'v':[1, 0], '<':[0, -1], '>':[0, 1]}
    diff_h, diff_w = dir_map[attempt]
    if mapi[robot_h+diff_h][robot_w+diff_w] == ".":
        mapi[robot_h][robot_w] = "."
        mapi[robot_h+diff_h][robot_w+diff_w] = "@"
        return mapi, robot_h+diff_h, robot_w+diff_w
    elif mapi[robot_h+diff_h][robot_w+diff_w] == "#":
        return mapi, robot_h, robot_w
    else:
        map_ahead = []
        h_i, w_i = robot_h, robot_w
        while True:
            h_i, w_i = h_i+diff_h, w_i+diff_w
            if mapi[h_i][w_i]=="#":
                break
            elif mapi[h_i][w_i]==".":
                map_ahead.append(".")
                break
            else:
                map_ahead.append("O")
        if "." not in map_ahead:
            # No space to move
            return mapi, robot_h, robot_w
        else:
            mapi[robot_h][robot_w] = "."
            robot_h_new, robot_w_new = robot_h+diff_h, robot_w+diff_w
            mapi[robot_h_new][robot_w_new] = "@"
            th, tw = robot_h_new, robot_w_new
            for elem in map_ahead[:-1]:
                th, tw = th+diff_h, tw+diff_w
                mapi[th][tw] = elem
            return mapi, robot_h_new, robot_w_new
                
        
def sum_gps(mapi):
    height, width = len(mapi), len(mapi[0])
    sumGPS = 0
    for hi in range(height):
        for wi in range(width):
            if mapi[hi][wi] == "O":
                  sumGPS += (100*hi+wi)
    return sumGPS

def sol1_brute_force(inMap, inattems):
    mapi = inMap
    height, width = len(inMap), len(inMap[0])
    for hi in range(height):
        for wi in range(width):
            if mapi[hi][wi]=="@":
                robot_h, robot_w = hi, wi
                break
    for attempt in inattems:
        mapi, robot_h, robot_w = evolve_map(mapi, robot_h, robot_w, attempt)
    return sum_gps(mapi)

test_input = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""


inpMap, attempts =  process_input(test_input)
print(sol1_brute_force(inpMap, attempts))

##### Part 2
def printinpMap(inpMap):
    for l in inpMap:
        print("".join(l))
def process_input_2(inp):
    inpMap = []
    attempts = []
    convertDict = {"#":"##", ".":"..", "@":"@.", "O":"[]"}
    for ln, i in enumerate(inp.split("\n")):
        if i!="":
            for old, new in convertDict.items():
                i = i.replace(old, new)
            inpMap.append(list(i))
        else:
            emptyLine = ln
            break
    for i in inp.split("\n")[emptyLine+1:]:
        if i!="":
            attempts.extend(list(i))
    return inpMap, attempts

def is_box_movable(mapi, lh, lw, rh, rw, diff_h, diff_w):
    if diff_h == 0:
        # Horizontal movement : Left, Right
        if diff_w == -1:
            # left
            lh2, lw2, rh2, rw2 = lh+diff_h, lw+diff_w, rh+diff_h, rw+diff_w
            if mapi[lh2][lw2]==".":
                return True
            elif mapi[lh2][lw2]=="#":
                return False
            else:
                return is_box_movable(mapi, lh2, lw2-1, lh2, lw2, diff_h, diff_w)
        elif diff_w == 1:
            # right
            lh2, lw2, rh2, rw2 = lh+diff_h, lw+diff_w, rh+diff_h, rw+diff_w
            if mapi[rh2][rw2]==".":
                return True
            elif mapi[rh2][rw2]=="#":
                return False
            else:
                return is_box_movable(mapi, rh2, rw2, rh2, rw2+1, diff_h, diff_w)
    else:
        # Vertical movement : Up, Down
        lh2, lw2, rh2, rw2 = lh+diff_h, lw+diff_w, rh+diff_h, rw+diff_w
        if mapi[lh2][lw2]=="." and mapi[rh2][rw2]==".":
            return True
        elif mapi[lh2][lw2]=="#" or mapi[rh2][rw2]=="#":
            return False
        else:
            if mapi[lh2][lw2]=="[" and mapi[rh2][rw2]=="]":
                return is_box_movable(mapi, lh2, lw2, rh2, rw2, diff_h, diff_w)
            elif mapi[lh2][lw2]=="]" and mapi[rh2][rw2]==".":
                return is_box_movable(mapi, lh2, lw2-1, lh2, lw2, diff_h, diff_w)
            elif mapi[lh2][lw2]=="." and mapi[rh2][rw2]=="[":
                return is_box_movable(mapi, rh2, rw2, rh2, rw2+1, diff_h, diff_w)
            elif mapi[lh2][lw2]=="]" and mapi[rh2][rw2]=="[":
                return is_box_movable(mapi, lh2, lw2-1, lh2, lw2, diff_h, diff_w) and is_box_movable(mapi, rh2, rw2, rh2, rw2+1, diff_h, diff_w)
            
            
def move_box(mapi, lh, lw, rh, rw, diff_h, diff_w):
    if diff_h == 0:
        # Horizontal movement : Left, Right
        if diff_w == -1:
            # left
            lh2, lw2, rh2, rw2 = lh+diff_h, lw+diff_w, rh+diff_h, rw+diff_w
            if mapi[lh2][lw2]==".":
                mapi[lh2][lw2] = "["
                mapi[rh2][rw2] = "]"
                mapi[rh][rw] = "."
            else:
                move_box(mapi, lh2, lw2-1, lh2, lw2, diff_h, diff_w)
                mapi[lh2][lw2] = "["
                mapi[rh2][rw2] = "]"
                mapi[rh][rw] = "."
        elif diff_w == 1:
            # right
            lh2, lw2, rh2, rw2 = lh+diff_h, lw+diff_w, rh+diff_h, rw+diff_w
            if mapi[rh2][rw2]==".":
                mapi[lh2][lw2] = "["
                mapi[rh2][rw2] = "]"
                mapi[lh][lw] = "."
            else:
                move_box(mapi, rh2, rw2, rh2, rw2+1, diff_h, diff_w)
                mapi[lh2][lw2] = "["
                mapi[rh2][rw2] = "]"
                mapi[lh][lw] = "."
    else:
        # Vertical movement : Up, Down
        lh2, lw2, rh2, rw2 = lh+diff_h, lw+diff_w, rh+diff_h, rw+diff_w
        if mapi[lh2][lw2]=="." and mapi[rh2][rw2]==".":
            mapi[lh2][lw2] = "["
            mapi[rh2][rw2] = "]"
            mapi[lh][lw] = "."
            mapi[rh][rw] = "."
        else:
            if mapi[lh2][lw2]=="[" and mapi[rh2][rw2]=="]":
                move_box(mapi, lh2, lw2, rh2, rw2, diff_h, diff_w)
            elif mapi[lh2][lw2]=="]" and mapi[rh2][rw2]==".":
                move_box(mapi, lh2, lw2-1, lh2, lw2, diff_h, diff_w)
            elif mapi[lh2][lw2]=="." and mapi[rh2][rw2]=="[":
                move_box(mapi, rh2, rw2, rh2, rw2+1, diff_h, diff_w)
            elif mapi[lh2][lw2]=="]" and mapi[rh2][rw2]=="[":
                move_box(mapi, lh2, lw2-1, lh2, lw2, diff_h, diff_w)
                move_box(mapi, rh2, rw2, rh2, rw2+1, diff_h, diff_w)
            mapi[lh2][lw2] = "["
            mapi[rh2][rw2] = "]"
            mapi[lh][lw] = "."
            mapi[rh][rw] = "."

    
def evolve_map_2(mapi, robot_h, robot_w, attempt):
    dir_map = {'^':[-1, 0], 'v':[1, 0], '<':[0, -1], '>':[0, 1]}
    diff_h, diff_w = dir_map[attempt]
    if mapi[robot_h+diff_h][robot_w+diff_w] == ".":
        mapi[robot_h][robot_w] = "."
        mapi[robot_h+diff_h][robot_w+diff_w] = "@"
        return mapi, robot_h+diff_h, robot_w+diff_w
    elif mapi[robot_h+diff_h][robot_w+diff_w] == "#":
        return mapi, robot_h, robot_w
    else:
        h_i, w_i = robot_h, robot_w
        h2, w2 = h_i+diff_h, w_i+diff_w
        if mapi[h2][w2]=="[":
            if is_box_movable(mapi, h2, w2, h2, w2+1, diff_h, diff_w):
                move_box(mapi, h2, w2, h2, w2+1, diff_h, diff_w)
                mapi[robot_h][robot_w] = "."
                mapi[robot_h+diff_h][robot_w+diff_w] = "@"
                return mapi, robot_h+diff_h, robot_w+diff_w
            else:
                # Box ahead not movable
                return mapi, robot_h, robot_w
        elif mapi[h2][w2]=="]":
            if is_box_movable(mapi, h2, w2-1, h2, w2, diff_h, diff_w):
                move_box(mapi, h2, w2-1, h2, w2, diff_h, diff_w)
                mapi[robot_h][robot_w] = "."
                mapi[robot_h+diff_h][robot_w+diff_w] = "@"
                return mapi, robot_h+diff_h, robot_w+diff_w
            else:
                # Box ahead not movable
                return mapi, robot_h, robot_w
                
        
def sum_gps_2(mapi):
    height, width = len(mapi), len(mapi[0])
    sumGPS = 0
    for hi in range(height):
        for wi in range(width):
            if mapi[hi][wi] == "[":
                  sumGPS += (100*hi+wi)
    return sumGPS

def sol2_brute_force(inMap, inattems):
    mapi = inMap
    height, width = len(inMap), len(inMap[0])
    for hi in range(height):
        for wi in range(width):
            if mapi[hi][wi]=="@":
                robot_h, robot_w = hi, wi
                break
    for attempt in inattems:
        mapi, robot_h, robot_w = evolve_map_2(mapi, robot_h, robot_w, attempt)
    return sum_gps_2(mapi)

test_input = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""


inpMap, attempts =  process_input_2(test_input)
print(sol2_brute_force(inpMap, attempts))

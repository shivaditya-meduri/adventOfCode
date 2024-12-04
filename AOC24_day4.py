def find_xmas_1(input_string):
    ### find all occurrences of x
    height, width = len(input_string), len(input_string[0])
    # E, W, S, N, NE, NW, SE, SW
    diffs = [[[0, 1], [0, 2], [0, 3]], [[0, -1], [0, -2], [0, -3]],
             [[1, 0], [2, 0], [3, 0]], [[-1, 0], [-2, 0], [-3, 0]],
             [[1, 1], [2, 2], [3, 3]], [[-1, -1], [-2, -2], [-3, -3]],
             [[1, -1], [2, -2], [3, -3]], [[-1, 1], [-2, 2], [-3, 3]]]
    xmas_count = 0
    for i in range(height):
        for j in range(width):
            if input_string[i][j]=="X":
                for direc in diffs:
                    match = list("MAS")
                    for diff in direc:
                        i2, j2 = i+diff[0], j+diff[1]
                        if not (0 <= i2 < height and 0 <= j2 < width):
                            break
                        if input_string[i2][j2] == match.pop(0):
                            if not match:
                                xmas_count+=1
                            else:
                                continue
                        else:
                            break
    return xmas_count

def find_xmas_2(input_string):
    ### find all occurrences of A
    height, width = len(input_string), len(input_string[0])
    # diagnol, reverse diagnol
    diffs = [[[-1, 1], [1, -1]], [[-1, -1], [1, 1]]]
    x_mas_count = 0
    for i in range(height):
        for j in range(width):
            if input_string[i][j]=="A":
                c = 0
                for direc in diffs:
                    match = list("MS")
                    for diff in direc:
                        i2, j2 = i+diff[0], j+diff[1]
                        if not (0 <= i2 < height and 0 <= j2 < width):
                            break
                        if input_string[i2][j2] in match:
                            match.remove(input_string[i2][j2])
                            if not match:
                                c+=1
                            else:
                                continue
                        else:
                            break
                if c == 2:
                    x_mas_count += 1
    return x_mas_count

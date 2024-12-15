import numpy as np

# Solve the system of linear equations using the Matrix inversion method

def process_input(inp):
    claw_machines = []
    cmConfig = {}
    for line in inp.split("\n"):
        if line=="":
            claw_machines.append(cmConfig)
            cmConfig = {}
        elif line.startswith("Button A:"):
            cmConfig['ax'] = int(line.replace("Button A: ", "").split(", ")[0].split("+")[1])
            cmConfig['ay'] = int(line.replace("Button A: ", "").split(", ")[1].split("+")[1])
        elif line.startswith("Button B:"):
            cmConfig['bx'] = int(line.replace("Button B: ", "").split(", ")[0].split("+")[1])
            cmConfig['by'] = int(line.replace("Button B: ", "").split(", ")[1].split("+")[1])
        elif line.startswith("Prize:"):
            cmConfig['px'] = int(line.replace("Prize: ", "").split(", ")[0].split("=")[1])
            cmConfig['py'] = int(line.replace("Prize: ", "").split(", ")[1].split("=")[1])
    if cmConfig != {}:
        claw_machines.append(cmConfig)
    return claw_machines

def find_solution_with_min_cost(ax, bx, px):
    # na = (px-nb*bx)/ax
    nb = int(px/bx)
    while True:
        if (px-nb*bx)%ax == 0:
            na = (px-nb*bx)//ax
            return na, nb

def cmConfigAnalyzer_closedForm(cmConfig):
    ax, ay, bx, by, px, py = cmConfig['ax'], cmConfig['ay'], cmConfig['bx'], cmConfig['by'], cmConfig['px'], cmConfig['py']
    A = np.array([[ax, bx], [ay, by]])
    b = np.array([px, py])
    if np.linalg.det(A) != 0:
        x = np.linalg.inv(A) @ b
        na, nb = round(x[0]), round(x[1])
        if (na*ax + nb*bx == px) and (na*ay + nb*by == py):
            return 3*na + nb
        else:
            # Not valid integer solutions
            return None
    else:
        rank_A  = np.linalg.matrix_rank(A)
        rank_Ab = np.linalg.matrix_rank(np.column_stack((A, b)))
        if rank_A != rank_Ab:
            # No solutions
            return None
        # Infinite solutions
        if ax != 0 or bx != 0:
            na, nb = find_solution_with_min_cost(ax, bx, px)
            return 3*na+nb
        elif ay != 0 or by != 0:
            na, nb = find_solution_with_min_cost(ay, by, py)
            return 3*na+nb
def sol2_closedform(inp):
    cost = 0
    for cmConfig in inp:
        minCost = cmConfigAnalyzer_closedForm(cmConfig)
        if minCost is not None:
            cost += minCost
    return cost

test_input = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279"""
test_input = process_input(test_input)
print(sol2_closedform(test_input))

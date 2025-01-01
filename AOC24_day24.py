def process_input(inp):
    inp_dict = {}
    bool_eqs = []
    bool_vars = set()
    for l in inp.split("\n"):
        if l!="":
            if "->" not in l:
                i, v = l.split(": ")
                inp_dict[i] = bool(int(v))
            else:
                bool_eq_lhs, bool_eq_rhs = l.split(" -> ")
                ops = bool_eq_lhs.split(" ")
                bool_eqs.append([ops[0], ops[1], ops[2], bool_eq_rhs])
                bool_vars.update([ops[0], ops[2], bool_eq_rhs])
    return inp_dict, bool_eqs, bool_vars

def sol1_bruteforce(inp_dict, bool_eqs, bool_vars):
    bops_dict = {"AND":lambda x: x[0] & x[1] , "OR":lambda x: x[0] | x[1], "XOR":lambda x: x[0] ^ x[1]}
    while len(bool_vars-set(inp_dict.keys()))!=0:
        for inp1, boolop, inp2, out in bool_eqs:
            if inp1 in inp_dict and inp2 in inp_dict:
                if out not in inp_dict:
                    inp_dict[out] = bops_dict[boolop]((inp_dict[inp1],inp_dict[inp2])) 
    # isolating z values from the input dictionary
    z = sorted([[k, v] for k, v in inp_dict.items() if k.startswith("z")], key=lambda x : x[0])
    # convert z to decimal
    res = 0
    p = 0
    for i, [zk, zv] in enumerate(z):
        res += int(zv)*(2**p)
        p += 1
    return res

test_input = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

with open(r"inputDay24AOC24.txt") as f:
    inp = f.read()
inp_dict, bool_eqs, bool_vars = process_input(inp)
inp_dict_copy = copy.deepcopy(inp_dict)
print(sol1_bruteforce(inp_dict_copy, bool_eqs, bool_vars)) # part 1
# I solved part 2 by identifying the bits which are probleamatic and seeing the correspoding equations and if the patterns were matching with the other output bits and if not made the necessary swaps

import copy
def error_count(inp_dict, bool_eqs, bool_vars):
    bops_dict = {"AND":lambda x: x[0] & x[1] , "OR":lambda x: x[0] | x[1], "XOR":lambda x: x[0] ^ x[1]}
    while len(bool_vars-set(inp_dict.keys()))!=0:
        for inp1, boolop, inp2, out in bool_eqs:
            if inp1 in inp_dict and inp2 in inp_dict:
                if out not in inp_dict:
                    inp_dict[out] = bops_dict[boolop]((inp_dict[inp1],inp_dict[inp2]))
    # convvert x to decimal
    x = sorted([[k, v] for k, v in inp_dict.items() if k.startswith("x")], key=lambda x : x[0])
    xres = 0
    p = 0
    for i, [xk, xv] in enumerate(x):
        xres += int(xv)*(2**p)
        p += 1
    # convvert y to decimal
    y = sorted([[k, v] for k, v in inp_dict.items() if k.startswith("y")], key=lambda x : x[0])
    yres = 0
    p = 0
    for i, [yk, yv] in enumerate(y):
        yres += int(yv)*(2**p)
        p += 1
    # convert z to decimal
    z = sorted([[k, v] for k, v in inp_dict.items() if k.startswith("z")], key=lambda x : x[0])
    zres = 0
    p = 0
    for i, [zk, zv] in enumerate(z):
        zres += int(zv)*(2**p)
        p += 1
    zresActualBin, zresExpectedBin = bin(zres)[2:], bin(xres+yres)[2:]
    print(f"Expected z decimal : {xres+yres}, Actual z decimal {zres}")
    if len(zresActualBin) != len(zresExpectedBin):
        return None
    errors = 0
    for zind in range(len(zresActualBin)):
        if zresActualBin[zind]!=zresExpectedBin[zind]:
            errors += 1
    return errors

inp_keys = list(inp_dict.keys())
# Find which bits from 0-45 have mismatches which helps narrowing down the problem
for i in range(10):
    inp_dict = {k:False for k in inp_keys}
    inp_dict[f'x0{i}'], inp_dict[f'y0{i}'] = True, True
    ec = error_count(inp_dict, bool_eqs, bool_vars)
    print(f"For {i}, ec = {ec}")
for i in range(10, 45):
    inp_dict = {k:False for k in inp_keys}
    inp_dict[f'x{i}'], inp_dict[f'y{i}'] = True, True
    ec = error_count(inp_dict, bool_eqs, bool_vars)
    print(f"For {i}, ec = {ec}")
# For my input case, there was a problem with 9, 10, 17, 18, 24, 32
def generate_circuits(bout, bool_eqs):
    opMap = {"AND":"&", "OR":"|","XOR":"^"}
    for in1, op, in2, out in bool_eqs:
        if out==bout:
            if in1.startswith("x") or in1.startswith("y"):
                lhs = in1
            else:
                lhs = generate_circuits(in1, bool_eqs)
            if in2.startswith("x") or in2.startswith("y"):
                rhs = in2
            else:
                rhs = generate_circuits(in2, bool_eqs)
            lhs, rhs = sorted([lhs, rhs])
            return f"({lhs} {opMap[op]} {rhs})"
# Generate circuits to investigate the probleamatic bits
print("\n")
print("Circuits before correction!!!!")
print("\n")
for i in range(10):
    print(f"z0{i} = {generate_circuits(f'z0{i}', bool_eqs)}\n")
for i in range(10, 45):
    print(f"z{i} = {generate_circuits(f'z{i}', bool_eqs)}\n")

# After identifying the necessary swaps from manual intervention
import copy
bool_eqs_copy = copy.deepcopy(bool_eqs)
s1, s2 = 87, 37
bool_eqs_copy[s1][-1], bool_eqs_copy[s2][-1] = bool_eqs_copy[s2][-1], bool_eqs_copy[s1][-1]
s1, s2 = 49, 55
bool_eqs_copy[s1][-1], bool_eqs_copy[s2][-1] = bool_eqs_copy[s2][-1], bool_eqs_copy[s1][-1]
s1, s2 = 64, 208
bool_eqs_copy[s1][-1], bool_eqs_copy[s2][-1] = bool_eqs_copy[s2][-1], bool_eqs_copy[s1][-1]
s1, s2 = 180, 210
bool_eqs_copy[s1][-1], bool_eqs_copy[s2][-1] = bool_eqs_copy[s2][-1], bool_eqs_copy[s1][-1]
# printing corrrect circuits
print("\n")
print("Circuits after correction!!!!")
print("\n")
for i in range(10):
    print(f"z0{i} = {generate_circuits(f'z0{i}', bool_eqs_copy)}\n")
for i in range(10, 45):
    print(f"z{i} = {generate_circuits(f'z{i}', bool_eqs_copy)}\n")

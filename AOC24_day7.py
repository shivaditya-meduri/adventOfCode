def get_result_operands(inp):
    inp = [i for i in inp.split(" ")]
    return [int(inp[0].replace(":","")), list(map(int, inp[1:]))]
def process_input(inp):
    return [get_result_operands(i) for i in inp.split("\n") if i!=""]
  import math
def generate_combinations(vals, n, curr=None):
    if curr is None:
        curr = []
    if n == 0:
        yield curr
        return
    for val in vals:
        for v in generate_combinations(vals, n-1, curr+[val]):
            yield v
def evaluate_exp(op, oprns):
    operands, operations = op.copy(), oprns.copy()
    while len(operations)>0:
        op = operations.pop(0)
        op1, op2 = operands.pop(0), operands.pop(0)
        if op == "+":
            result = op1 + op2
        elif op == "*":
            result = op1 * op2
        elif op == "||":
            result = op1*(10**(1+math.floor(math.log(op2, 10))))+op2
        operands.insert(0, result)
    return operands[0]
        
def sol1_bruteforce(inp):
    out = 0
    for result, operands in inp:
        n = len(operands)
        for operation in generate_combinations(["+", "*"], n-1):
            if evaluate_exp(operands, operation) == result:
                out += result
                break
            else:
                continue
    return out

def sol2_bruteforce(inp):
    out = 0
    for result, operands in inp:
        n = len(operands)
        for operation in generate_combinations(["+", "*", "||"], n-1):
            if evaluate_exp(operands, operation) == result:
                out += result
                break
            else:
                continue
    return out

test_input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

test_input = process_input(test_input)

print(sol1_bruteforce(test_input))
print(sol2_bruteforce(test_input))

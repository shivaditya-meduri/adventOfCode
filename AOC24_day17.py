def compOp(op, a, b, c):
    if op<=3:
        return op
    elif op == 4:
        return a
    elif op == 5:
        return b
    elif op == 6:
        return c

def executor(a, b, c, opcode, operand, inp):
    jumped = False
    out = None
    if opcode == 0:
        # adv instruction = A/2^(comb(op)) -> A
        a = a//2**compOp(operand, a, b, c)
    elif opcode == 1:
        # bxl instruction b ^ operand -> b
        b = b ^ operand
    elif opcode == 2:
        # bst instruction comb(op)%8 -> b
        b = compOp(operand, a, b, c)%8
    elif opcode == 3:
        # jnz instruction if A !=0 
        if a!=0:
            inp = operand
            jumped = True
    elif opcode == 4:
        # bxc instruction
        b = b^c
    elif opcode == 5:
        # out
        out = compOp(operand, a, b, c)%8
    elif opcode == 6:
        # bdv
        b = a//2**compOp(operand, a, b, c)
    elif opcode == 7:
        # cdv
        c = a//2**compOp(operand, a, b, c)
    if not jumped:
        inp += 2
    return a, b, c, inp, out
def sol1_bruteforce(a, b, c, program):
    inp = 0
    outs = []
    while inp < len(program):
        a, b, c, inp, out = executor(a, b, c, program[inp], program[inp+1], inp)
        if out is not None:
            outs.append(str(out))
    return ",".join(outs)

inp_a, inp_b, inp_c = 28066687, 0, 0
inp_program = [2,4,1,1,7,5,4,6,0,3,1,4,5,5,3,0]

print(sol1_bruteforce(inp_a, inp_b, inp_c, inp_program))

# part 2
# if a register value is multiplied by 8, the output string shifts to the right with a number added on the left
# we can use the back tracking approach to find the a register value which returns the desired output

target_function = lambda a : sol1_bruteforce(a, 0, 0, inp_program).replace(",", "")
target_str = "2411754603145530"
def sol2_backtracking(target_function, target_str):
    def back_tracking(a, num_digits):
        if num_digits == len(target_str):
            return a
        i2 = a*8
        for j in range(8):
            if target_function(i2+j) == target_str[-(num_digits+1):]:
                solution = back_tracking(i2+j, num_digits+1)
                if solution is not None:
                    return solution
    
    
    num_digs = 0
    for i in range(8):
        if target_function(i) == target_str[-(num_digs+1):]:
            solution = back_tracking(i, 1)
            return solution

print(sol2_backtracking(target_function, target_str))

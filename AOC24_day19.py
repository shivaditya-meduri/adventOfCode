def process_input(inp):
    inp = inp.split("\n")
    available_patterns = inp[0].split(", ")
    designs = []
    for ln in range(2, len(inp)):
        if inp[ln]!="":
            designs.append(inp[ln])
    return available_patterns, designs

def numberOfPossibleSolutions(design, patterns):
    # problem can be broken into overlapping sub-problems
    # f(i) = sum( f(i + len(pattern)) for each pattern that matches at position i )
    len_des = len(design)
    dp = [0]*(len_des+1) # dp[i] signifies the number of solutions for the string design[i:]
    dp[len_des] = 1 # Empty string can be formed in only 1 way i.e. no patterns
    for i in range(len_des-1, -1, -1):
        # start from the right end to be able to use overlapping subproblems
        for pattern in patterns:
            if i+len(pattern)<=len_des:
                if design[i:i+len(pattern)] == pattern:
                    dp[i] += dp[i+len(pattern)]
    return dp[0] # Total number of ways to create the complete string from existing patterns
                
    
    
def sol1_dynamicprogramming(patterns, designs):
    num_valid_designs = 0
    for design in designs:
        numSolutions = numberOfPossibleSolutions(design, patterns)
        if numSolutions > 0:
            num_valid_designs += 1
    return num_valid_designs

def sol2_dynamicprogramming(patterns, designs):
    total_num_arrangements = 0
    for design in designs:
        numSolutions = numberOfPossibleSolutions(design, patterns)
        total_num_arrangements += numSolutions
    return total_num_arrangements

test_input = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
test_patterns, test_designs = process_input(test_input)
print(sol1_dynamicprogramming(test_patterns, test_designs))
print(sol2_dynamicprogramming(test_patterns, test_designs))

import re
def sol(input_str):
    pattern = "mul\((\d+),(\d+)\)"
    prod = 0
    for match in re.finditer(pattern, input_str):
        num1, num2 = int(match.group(1)), int(match.group(2))
        prod += num1*num2
    return prod

def sol_2(input_str):
    pattern1 = "mul\((\d+),(\d+)\)"
    pattern2 = "do\(\)"
    pattern3 = "don't\(\)"
    combined_pattern = f"{pattern1}|{pattern2}|{pattern3}"
    prod = 0
    do = True
    for match in re.finditer(combined_pattern, input_str):
        if match.group() == "do()":
            do = True
        elif match.group() == "don't()":
            do = False
        else:
            if do == True:
                num1, num2 = int(match.group(1)), int(match.group(2))
                prod += num1*num2
    return prod

def process_input(inp):
    rules, updates = [], []
    brk = False
    for i in inp.split("\n"):
        if not brk:
            if i!="":
                rules.append(list(map(int, i.split("|"))))
            else:
                brk = True
        else:
            if i!="":
                updates.append(list(map(int, i.split(","))))
    return rules, updates

def is_update_valid(update, rules):
    for rule in rules:
        p1, p2 = rule
        p1_exists, p2_exists = False, False
        for p in update:
            if p == p1:
                if p2_exists:
                    return False
                else:
                    p1_exists = True
            elif p == p2:
                p2_exists = True
                if p1_exists:
                    break
    return True

def sol_1(rules, updates):
    out = 0
    for update in updates:
        if is_update_valid(update, rules):
            out += update[len(update)//2]
    return out

from collections import defaultdict

def DFS(v, g, visited, path):
    visited.add(v)
    for c in g[v]:
        if c not in visited:
            DFS(c, g, visited, path)
    path.append(v)
    return path

def topo_sort(g):
    visited = set()
    path = []
    for node in list(g):
        if node not in visited:
            DFS(node, g, visited, path)
    return path[::-1] 

def fix_update(update, rules):
    update = set(update)
    applicable_rules = []
    graph = defaultdict(list)
    for rule in rules:
        if set(rule).issubset(update):
            graph[rule[0]].append(rule[1])
    fixed_update = topo_sort(graph)
    return fixed_update
        
def sol_2(rules, updates):
    out = 0
    for update in updates:
        if not is_update_valid(update, rules):
            fixed_update = fix_update(update, rules)
            out += fixed_update[len(fixed_update)//2]
    return out

test_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
rules, updates = process_input(test_input)
print(sol_1(rules, updates), sol_2(rules, updates))

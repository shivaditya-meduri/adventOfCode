from itertools import chain
from tqdm import tqdm

def process_input(inp):
    # We are using frozen sets as they are hashable and can be stored in a set for faster reads
    return [frozenset(i.split("-")) for i in inp.split("\n") if i!=""]


def sol1_bruteforce(inp):
    all_computers = list(set(list(chain(*inp))))
    num_comp = len(all_computers)
    all_3comp_comb = []
    for c1 in tqdm(range(num_comp)):
        for c2 in range(c1+1, num_comp):
            for c3 in range(c2+1, num_comp):
                if any([all_computers[c1].startswith("t"), all_computers[c2].startswith("t"), all_computers[c3].startswith("t")]):
                    all_3comp_comb.append([all_computers[c1], all_computers[c2], all_computers[c3]])
    valid_nets = []
    inp = set(inp)
    for c1, c2, c3 in tqdm(all_3comp_comb):
        if set([c1, c2]) in inp:
            if set([c2, c3]) in inp:
                if set([c1, c3]) in inp:
                    valid_nets.append([c1, c2, c3])
    return len(valid_nets)

test_input = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
test_input_processed = process_input(test_input)
print(sol1_bruteforce(test_input_processed))

from collections import defaultdict
from itertools import combinations
def find_cliques_from_subgraph(g, nodes):
    def is_clique(potential_nodes):
        return all(
            other in g[node] 
            for node in potential_nodes 
            for other in potential_nodes 
            if node != other
        )
    cliques = []
    n = len(nodes)
    for size in range(n, 2, -1):
        for combo in combinations(nodes, size):
            combo_set = set(combo)
            if is_clique(combo_set):
                if not any(combo_set.issubset(existing) for existing in cliques):
                    cliques.append(combo_set)
    return cliques
def sol2(inp):
    # create and adjacency list graph data structure from the undirected edges list
    g = defaultdict(set)
    for u, v in input_processed:
        g[u].add(v)
        g[v].add(u)
    # Sort nodes by degree
    nodes_by_degree = sorted(g.keys(), key=lambda x: len(g[x]), reverse=True)

    all_cliques = []
    processed = set()

    for start_node in nodes_by_degree:
        if start_node in processed:
            continue

        possible_nodes = {start_node} | g[start_node]
        # Find all cliques in this subgraph
        new_cliques = find_cliques_from_subgraph(g, possible_nodes)

        for clique in new_cliques:
            if not any(clique.issubset(existing) for existing in all_cliques):
                all_cliques.append(clique)
                processed.update(clique)
    return ",".join(sorted(list(sorted(all_cliques, key=len, reverse=True)[0])))

print(sol2(test_input_processed))

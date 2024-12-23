from util import tokenedlines, getlines
import networkx as nx

day = "23"
lines = getlines(day)

links = set([tuple(line.split("-")) for line in lines])
graph = nx.Graph(links)

links.update(((y, x) for x,y in list(links)))
ts = set(x[0] for x in links if x[0][0] == 't')
all_nodes = set(x[0] for x in links)

triplets = set([])

for x, y in links:
    for t in all_nodes:
        if (x, t) in links and (y, t) in links:
            triplets.add(frozenset([x, y, t]))

print(len(triplets))

def num_neighbors(node):
    ret = 0
    for n2 in all_nodes:
        if (node, n2) in links:
            ret += 1
    return ret
degrees = [(num_neighbors(node), node) for node in all_nodes]
print(sorted(degrees))

for triplet in triplets:
    s = set(triplet)
    for node in all_nodes:
        if all((node, t) in links for t in s):
            s.add(node)
print(len(all_nodes))
bylen = [(len(x), sorted(x)) for x in nx.find_cliques(graph)]
bylen.sort()
print(",".join(bylen[-1][1]))
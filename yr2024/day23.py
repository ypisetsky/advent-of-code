from util import tokenedlines, getlines
import networkx as nx

day = "23"
lines = getlines(day)

links = set([tuple(line.split("-")) for line in lines])


links.update(((y, x) for x,y in list(links)))
ts = set(x[0] for x in links if x[0][0] == 't')

triplets = set([])

for x, y in links:
    for t in ts:
        if (x, t) in links and (y, t) in links:
            triplets.add(frozenset([x, y, t]))

print(len(triplets))

graph = nx.Graph(links)
bylen = [(len(x), sorted(x)) for x in nx.find_cliques(graph)]
bylen.sort()
print(",".join(bylen[-1][1]))
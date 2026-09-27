"""networkx group_betweenness_centrality: results depend on node labels (3.7 regression).

Group betweenness counts, over pairs of non-group nodes, the fraction of shortest paths
that pass through the group. It depends on the graph only up to isomorphism. networkx
3.6.1 returns the values below; 3.7.0 does not. Reference: brute force over all shortest
paths.

Run: python networkx_group_betweenness_regression.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import networkx as nx


def reference(G, C):
    C, nodes, total = set(C), list(G), 0.0
    for i, s in enumerate(nodes):
        for t in nodes[i + 1:]:
            if s in C or t in C or not nx.has_path(G, s, t):
                continue
            paths = list(nx.all_shortest_paths(G, s, t))
            total += sum(any(u in C for u in p[1:-1]) for p in paths) / len(paths)
    return total


star = nx.Graph([(6, 11), (6, 2), (6, 3)])
path = nx.path_graph([4, 1, 0, 6, 3, 2, 8, 7]); path.add_node(5)
cases = [(star, [11, 3]), (path, [0, 4, 5, 7, 8])]
rows = [(nx.group_betweenness_centrality(G, C, normalized=False), reference(G, C)) for G, C in cases]
verdict(any(abs(g - w) > 1e-9 for g, w in rows), f"(got, expected) = {rows}")

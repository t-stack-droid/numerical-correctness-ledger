"""networkx group_betweenness_centrality: adding an isolated node to the group changes the result.

An isolated node lies on no shortest path, so adding it to the group cannot change the
unnormalized group betweenness. On the graph formed by the path 4-1-0-6-3-2-8-7 and the
isolated node 5, the group {0, 4, 7, 8} gives 3 and the brute-force value of both {0, 4,
7, 8} and {0, 4, 5, 7, 8} is 3, but the library returns 5 for {0, 4, 5, 7, 8}.
Relabelling the nodes in path order gives 3. The verdict requires the wrong value with
node 5 in the group and the correct value without it, on the same graph.

Run: python networkx_group_betweenness_isolate.py
Exit status: 1 = the discrepancy was detected in the installed version; 0 = not reproduced by
this comparison; 2 = the script could not run or a precondition failed.
"""
import os
import sys
import traceback


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)


def _could_not_run(exc_type, exc, tb):
    traceback.print_exception(exc_type, exc, tb)
    print(f"could not run: {exc_type.__name__}: {exc}")
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(2)


sys.excepthook = _could_not_run

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


G = nx.path_graph([4, 1, 0, 6, 3, 2, 8, 7]); G.add_node(5)
gbc = lambda C, H=G: nx.group_betweenness_centrality(H, C, normalized=False)
with5, without5 = gbc([0, 4, 5, 7, 8]), gbc([0, 4, 7, 8])
order = {v: i for i, v in enumerate([4, 1, 0, 6, 3, 2, 8, 7, 5])}
relabelled = gbc([order[c] for c in (0, 4, 5, 7, 8)], nx.relabel_nodes(G, order))
want = reference(G, [0, 4, 5, 7, 8])
verdict(not (abs(with5 - want) <= 1e-9) and abs(without5 - reference(G, [0, 4, 7, 8])) <= 1e-9,
        f"group with node 5: {with5}; without node 5: {without5}; relabelled, with node 5: {relabelled}; brute force {want}")

"""networkx group_betweenness_centrality: the result depends on node labels (regression in 3.7rc0).

Group betweenness counts, over pairs of non-group nodes, the fraction of shortest paths
that pass through the group, so it depends on the graph only up to isomorphism. For the
star with centre 6, leaves 11, 2 and 3, and the group {11, 3}, the only pair of non-
group nodes (6 and 2) is adjacent, so the value is 0. The library returns 0.5; the same
star relabelled 0 to 3 gives 0. The verdict requires both: a wrong value with the
original labels and the correct value after relabelling. Reference: brute force over all
shortest paths. Earlier releases do not reproduce it (see VERSIONS.md).

Run: python networkx_group_betweenness_regression.py
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


star = nx.Graph([(6, 11), (6, 2), (6, 3)])
got = nx.group_betweenness_centrality(star, [11, 3], normalized=False)
relabelled = nx.group_betweenness_centrality(nx.relabel_nodes(star, {6: 0, 11: 1, 2: 2, 3: 3}), [1, 3], normalized=False)
want = reference(star, [11, 3])
verdict(not (abs(got - want) <= 1e-9) and abs(relabelled - want) <= 1e-9,
        f"labels 6, 11, 2, 3: {got}; relabelled 0 to 3: {relabelled}; brute force {want}")

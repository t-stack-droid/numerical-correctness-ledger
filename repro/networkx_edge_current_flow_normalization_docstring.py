"""networkx edge_current_flow_betweenness_centrality: docstring and code normalise differently.

The docstring says normalised values are scaled by 2/[(n-1)(n-2)]. On a path of 4 nodes
(a tree, where current follows the unique path) the unnormalised values are 3, 4, 3, so
the documented values are 1.0, 1.333, 1.0. The code divides by (n-1)(n-2) and returns
0.5, 0.667, 0.5, which matches edge_betweenness_centrality. The documentation, not the
value, looks wrong.

Run: python networkx_edge_current_flow_normalization_docstring.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import networkx as nx

got = nx.edge_current_flow_betweenness_centrality(nx.path_graph(4), normalized=True)
verdict(abs(got[(0, 1)] - 1.0) > 1e-9, f"got {got}; documented normalisation gives 1.0, 1.333, 1.0")

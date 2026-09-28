"""networkx node_degree_xy(nodes=...): docstring and code select different edges.

The docstring says the generator yields a pair for each edge incident to a node in
`nodes`. The code yields only edges with both endpoints in `nodes`. For the path 1-2-3
and nodes=[2], the documented output has 4 pairs; the code yields none.

Run: python networkx_node_degree_xy_nodes_docstring.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import networkx as nx

got = list(nx.node_degree_xy(nx.Graph([(1, 2), (2, 3)]), nodes=[2]))
verdict(len(got) != 4, f"got {got}; the documented behaviour gives 4 pairs")

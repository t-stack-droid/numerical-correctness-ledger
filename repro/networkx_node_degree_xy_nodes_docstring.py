"""networkx node_degree_xy(nodes=...): docstring and code select different edges.

The docstring says the generator yields a (degree, degree) pair 'for each edge in G
incident to a node in nodes', and its Notes say that for undirected graphs each edge is
produced twice, once for each representation (u, v) and (v, u). For the path 1-2-3 and
nodes=[2], both edges are incident to 2, so the documented output is the four pairs (1,
2), (2, 1), (2, 1), (1, 2). The code keeps only edges with both endpoints in nodes and
yields none. The script reads the installed docstring.

Run: python networkx_node_degree_xy_nodes_docstring.py
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

import inspect
import networkx as nx

doc = " ".join(inspect.getdoc(nx.node_degree_xy).split())
documented = "incident to a node in `nodes`" in doc and "each edge is produced twice" in doc
got = sorted(nx.node_degree_xy(nx.Graph([(1, 2), (2, 3)]), nodes=[2]))
want = sorted([(1, 2), (2, 1), (2, 1), (1, 2)])
verdict(documented and got != want, f"got {got}; the documented behaviour gives {want}; docstring wording present: {documented}")

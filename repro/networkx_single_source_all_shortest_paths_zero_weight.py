"""networkx single_source_all_shortest_paths: the source's own path is listed twice when a zero-weight edge touches the source.

The function is documented to produce each shortest simple path once. In this undirected
example with edges 0-1 (weight 0) and 1-2 (weight 1), node 1 is a predecessor of the
source 0 at distance 0, and the path generator yields [0] once for reaching the source
and again after backtracking through 1. The expected output is {0: [[0]], 1: [[0, 1]],
2: [[0, 1, 2]]}; only the source's entry is duplicated here.

Run: python networkx_single_source_all_shortest_paths_zero_weight.py
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

G = nx.Graph()
G.add_weighted_edges_from([(0, 1, 0), (1, 2, 1)])
got = dict(nx.single_source_all_shortest_paths(G, 0, weight="weight"))
verdict(got.get(0) != [[0]], f"got {got}; expected {{0: [[0]], 1: [[0, 1]], 2: [[0, 1, 2]]}}")

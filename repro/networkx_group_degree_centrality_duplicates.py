"""networkx group_degree_centrality: S = [1, 1] and S = {1} give different results (question).

The docstring describes S as a list or set, 'a group of nodes which belong to G', and
does not say how repeated nodes are treated. On a path of 5 nodes, S = [1] and S = {1}
give 2 / 4 = 0.5 (2 neighbours outside the group, 4 nodes outside it), but S = [1, 1]
gives 2 / 3, because the duplicate is counted in the group size. The script reads the
installed docstring.

Run: python networkx_group_degree_centrality_duplicates.py
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

documented = "S : list or set" in inspect.getdoc(nx.group_degree_centrality)
G = nx.path_graph(5)
got = {str(S): nx.group_degree_centrality(G, S) for S in ([1], {1}, [1, 1])}
verdict(documented and not (abs(got["[1, 1]"] - got["{1}"]) <= 1e-12),
        f"{got}; docstring accepts a list or set: {documented}")

"""networkx find_induced_nodes returns an empty set for a star graph.

The star with centre 0 and leaves 1..4 is chordal and (1, 2) is not an edge, as the
function requires. The only induced path from 1 to 2 is 1-0-2, so the induced nodes are
{0, 1, 2}. The library returns an empty set.

Run: python networkx_find_induced_nodes_star.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import networkx as nx

got = nx.find_induced_nodes(nx.star_graph(4), 1, 2)
verdict(got != {0, 1, 2}, f"got {got!r}, expected {{0, 1, 2}}")

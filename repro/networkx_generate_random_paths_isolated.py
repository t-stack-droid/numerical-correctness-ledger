"""networkx generate_random_paths raises for a graph with an isolated node (crash).

The code comments that isolated nodes are handled, but a zero row sum produces NaN
transition probabilities and numpy raises.

Run: python networkx_generate_random_paths_isolated.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import networkx as nx
import numpy as np

G = nx.Graph(); G.add_node(0)
try:
    list(nx.generate_random_paths(G, sample_size=1, path_length=1, seed=np.random.RandomState(8)))
    verdict(False, "returned paths")
except Exception as e:
    verdict(True, f"raised {type(e).__name__}: {e}")

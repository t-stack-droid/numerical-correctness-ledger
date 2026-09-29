"""mne permutation_cluster_1samp_test: adjacency=False reports a one-location cluster with empty indices.

The docstring says: "If ``False``, assumes no adjacency (each location is treated as
independent and unconnected)." With data of shape (4, 1), the mean as statistic,
threshold 0.5 and tail = 1, the single location has statistic 1 and forms a cluster.
With adjacency=None the cluster's indices are (0,); with adjacency=False they are empty.

Run: python mne_permutation_cluster_1samp_adjacency_false.py
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

import numpy as np
from mne.stats import permutation_cluster_1samp_test

X = np.array([[4.0], [0.0], [0.0], [0.0]])
out = {}
for adj in (None, False):
    t, clusters, p, H0 = permutation_cluster_1samp_test(X, threshold=0.5, tail=1, adjacency=adj, out_type="indices",
                                                        n_permutations=16, stat_fun=lambda z: z.mean(axis=0),
                                                        seed=0, verbose=False)
    out[adj] = [tuple(np.atleast_1d(c[0]).tolist()) for c in clusters]
if out[None] != [(0,)]:
    raise RuntimeError(f"precondition: adjacency=None gives cluster (0,), got {out[None]}")
verdict(out[False] != [(0,)], f"clusters with adjacency=None: {out[None]}; with adjacency=False: {out[False]}")

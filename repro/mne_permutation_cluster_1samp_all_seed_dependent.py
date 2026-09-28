"""mne permutation_cluster_1samp_test(n_permutations='all'): p-values depend on the seed.

An exact test enumerates every sign class, so its p-values cannot depend on the random
seed. With n = 10 observations (RandomState(5) normals plus 0.3, 4 locations, threshold
1, tail=0) the data form two clusters, the same for every seed. The script matches
clusters by their location indices, prints each cluster's p-value for seeds 0 and 1, and
flags any difference. The reference enumerates the 512 sign classes independently (as in
mne_permutation_cluster_1samp_all_not_exact.py) and gives the exact value for each
cluster.

Run: python mne_permutation_cluster_1samp_all_seed_dependent.py
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

import itertools

import numpy as np
from mne.stats import permutation_cluster_1samp_test


def tvals(Z):
    return Z.mean(0) / (Z.std(0, ddof=1) / np.sqrt(len(Z)))


def max_cluster(t, thr):
    runs = []
    for sign in (1, -1):
        cur = 0.0
        for v in list(t) + [0.0]:
            if sign * v > thr:
                cur += v
            elif cur:
                runs.append(abs(cur))
                cur = 0.0
    return max(runs, default=0.0)


X = np.random.RandomState(5).standard_normal((10, 4)) + 0.3
t_ref = tvals(X)
null = [max_cluster(tvals(X * np.array((1,) + s)[:, None]), 1.0) for s in itertools.product((1, -1), repeat=9)]
res = {}
for seed in (0, 1):
    t, c, p, H0 = permutation_cluster_1samp_test(X, threshold=1.0, tail=0, n_permutations="all", seed=seed,
                                                out_type="indices", verbose=False)
    res[seed] = {tuple(np.atleast_1d(cl[0]).tolist()): float(pv) for cl, pv in zip(c, p)}
assert set(res[0]) == set(res[1]), f"precondition: same clusters for both seeds, got {sorted(res[0])} and {sorted(res[1])}"
rows, differ = [], False
for idx in sorted(res[0]):
    stat = abs(float(t_ref[list(idx)].sum()))
    exact = sum(v >= stat * (1 - 1e-12) for v in null) / 512
    differ = differ or not (abs(res[0][idx] - res[1][idx]) <= 1e-12)
    rows.append(f"cluster {idx}: seed 0 p = {res[0][idx]:.6f}, seed 1 p = {res[1][idx]:.6f}, exact {exact:.6f}")
verdict(differ, "; ".join(rows))

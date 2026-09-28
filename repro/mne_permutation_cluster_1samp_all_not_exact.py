"""mne permutation_cluster_1samp_test(n_permutations='all'): p = 1/511 where the exact test gives 1/512.

The docstring says n_permutations='all' performs an exact test. With n = 10 observations
and tail=0, sign flips form 2**10 / 2 = 512 classes (a pattern and its negation give the
same statistic). The reference enumerates the 512 classes independently: t statistic per
location, clusters of adjacent locations beyond the threshold, maximum absolute cluster
sum. Here the data form one cluster over all four locations, and only the observed
pattern reaches its statistic, so the exact p-value is 1/512. The library returns 1/511
for seeds 0 and 1; the verdict compares that p-value with the reference for the matched
cluster. Diagnostics (not part of the verdict): the library's null has 511 entries, a
one-entry deficit in the rounded absolute-statistic multiset, and the missing value
differs between the two seeds.

Run: python mne_permutation_cluster_1samp_all_not_exact.py
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
from collections import Counter

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


X = np.random.RandomState(0).standard_normal((10, 4)) + 1.0
t_ref = tvals(X)
obs = abs(t_ref.sum())  # the one cluster covers locations 0-3 (all t > 1)
assert all(t_ref > 1.0), "precondition: one cluster over all four locations"
null = [max_cluster(tvals(X * np.array((1,) + s)[:, None]), 1.0) for s in itertools.product((1, -1), repeat=9)]
p_exact = sum(v >= obs * (1 - 1e-12) for v in null) / 512
ce = Counter(np.round(null, 9))
bad, rows, deficits = False, [], []
for seed in (0, 1):
    t, c, p, H0 = permutation_cluster_1samp_test(X, threshold=1.0, tail=0, n_permutations="all", seed=seed,
                                                out_type="indices", verbose=False)
    idx = [tuple(np.atleast_1d(cl[0]).tolist()) for cl in c]
    assert idx == [(0, 1, 2, 3)], f"precondition: one cluster over locations 0-3, got {idx}"
    bad = bad or not (abs(float(p[0]) - p_exact) <= 1e-12)
    ch = Counter(np.round(np.abs(H0), 9))
    missing = {float(k): ce[k] - ch.get(k, 0) for k in ce if ce[k] > ch.get(k, 0)}
    extra = {float(k): ch[k] - ce.get(k, 0) for k in ch if ch[k] > ce.get(k, 0)}
    deficits.append((missing, extra))
    rows.append(f"seed {seed}: p = {float(p[0]):.6g}, len(H0) = {len(H0)}, missing {missing}, extra {extra}")
one_entry = all(sum(m.values()) == 1 and not e for m, e in deficits)
differs = one_entry and deficits[0][0] != deficits[1][0]
verdict(bad, f"cluster (0, 1, 2, 3): exact p from 512 classes = {p_exact:.6g}; " + "; ".join(rows)
        + f"; one-entry deficit for both seeds: {one_entry}, missing value differs between seeds: {differs}")

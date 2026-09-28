"""mne permutation_cluster_1samp_test: exact one-tailed null counts the observed statistic twice.

For tail=1 and n = 6 observations, n_permutations=64 enumerates all 2**6 sign patterns.
The reference computes the cluster statistic of each pattern independently (one
location, so the statistic is t when t > 0.5 and 0 otherwise): the observed t = 4.88
occurs once and 0 occurs 43 times, so the exact p-value is 1/64. The library's 64-entry
null distribution has the observed statistic twice and 0 only 42 times, and p = 2/64.

Run: python mne_permutation_cluster_1samp_exact_one_tailed.py
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

X = np.array([[0.5], [1.2], [0.8], [1.5], [0.3], [1.1]])
tstat = lambda z: z.mean() / (z.std(ddof=1) / np.sqrt(len(z)))
null = [(lambda v: v if v > 0.5 else 0.0)(tstat(X[:, 0] * np.array(s))) for s in itertools.product((1, -1), repeat=6)]
obs = tstat(X[:, 0])
p_exact = sum(v >= obs * (1 - 1e-12) for v in null) / 64
t_obs, clusters, pv, H0 = permutation_cluster_1samp_test(X, threshold=0.5, tail=1, n_permutations=64,
                                                         out_type="indices", verbose=False)
same = Counter(np.round(null, 9)) == Counter(np.round(np.asarray(H0, float), 9))
counts = lambda vals: (int(np.isclose(vals, obs).sum()), int((np.asarray(vals) == 0).sum()))
verdict(len(H0) != 64 or not (abs(float(pv[0]) - p_exact) <= 1e-12) or not same,
        f"p = {float(pv[0])!r} vs exact {p_exact!r}; (observed, zeros) in H0 {counts(H0)}, in the enumeration {counts(null)}")

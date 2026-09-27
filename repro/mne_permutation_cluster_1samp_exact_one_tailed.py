"""mne permutation_cluster_1samp_test, exact one-tailed test: identity counted twice.

With tail=1 and n_permutations >= 2**n the null should contain each of the 2**n sign
patterns once. The code drops the all-flip pattern instead of the identity and then adds
the observed statistic again, so it appears twice and the smallest attainable p-value
doubles.

Run: python mne_permutation_cluster_1samp_exact_one_tailed.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import numpy as np
from mne.stats import permutation_cluster_1samp_test

X = np.array([[0.5], [1.2], [0.8], [1.5], [0.3], [1.1]])
t_obs, clusters, pv, H0 = permutation_cluster_1samp_test(X, threshold=0.5, tail=1, n_permutations=64,
                                                         out_type="indices", verbose=False)
count = int(np.isclose(H0, t_obs[0]).sum())
verdict(count != 1, f"observed statistic appears {count} times in the 64-pattern null; expected 1")

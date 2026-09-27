"""mne permutation_cluster_1samp_test(n_permutations='all') is not exact.

'all' should enumerate every sign-flip class: 2**(n-1) for a two-sided test. The code
sets n_permutations = max_perms and then tests max_perms < n_permutations, which is
false, so it samples randomly: 511 of 512 classes for n = 10, and p-values that change
with the seed.

Run: python mne_permutation_cluster_1samp_all_not_exact.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import numpy as np
from mne.stats import permutation_cluster_1samp_test

X = np.random.RandomState(0).standard_normal((10, 4)) + 1.0
kw = dict(threshold=1.0, tail=0, out_type="indices", verbose=False)
t_all, c_all, p_all, H0_all = permutation_cluster_1samp_test(X, n_permutations="all", **kw)
t_ex, c_ex, p_ex, H0_ex = permutation_cluster_1samp_test(X, n_permutations=512, **kw)
assert len(c_all) > 0, "no cluster formed; the example needs at least one cluster"
verdict(len(H0_all) != 512 or not np.allclose(p_all, p_ex),
        f"'all': len(H0) = {len(H0_all)}, p = {p_all.tolist()}; exact (n_permutations=512): "
        f"len(H0) = {len(H0_ex)}, p = {p_ex.tolist()}")

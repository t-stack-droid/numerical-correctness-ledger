"""mne f_mway_rm(correction=True): Greenhouse-Geisser epsilon from uncentered cross-products.

The Greenhouse-Geisser epsilon is tr(S)**2 / ((k-1) tr(S @ S)) with S the sample
covariance of orthonormal contrasts. The code uses Y.T @ Y without removing the column
means, which differ from 0 whenever the conditions differ.

Run: python mne_f_mway_rm_greenhouse_geisser.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import numpy as np
from scipy import stats
from mne.stats import f_mway_rm

rs = np.random.RandomState(47)
n, k = 20, 4
x = rs.standard_normal((n, k)); x[:, 0] += 1.5
F, p = f_mway_rm(x, [k], correction=True)
C = np.linalg.qr(np.column_stack([np.ones(k), np.eye(k)[:, :k - 1]]))[0][:, 1:]
S = np.cov(x @ C, rowvar=False)
eps = np.trace(S) ** 2 / ((k - 1) * np.trace(S @ S))
want = stats.f.sf(float(np.atleast_1d(F)[0]), eps * (k - 1), eps * (k - 1) * (n - 1))
got = float(np.atleast_1d(p)[0])
verdict(abs(got - want) > 1e-9 * want, f"p = {got!r}, expected {float(want)!r} (epsilon {eps:.4f})")

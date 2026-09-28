"""mne f_mway_rm(correction=True): Greenhouse-Geisser epsilon from uncentered cross-products.

The Greenhouse-Geisser epsilon is tr(S)^2 / ((k - 1) tr(S^2)) with S the covariance
(centered) of orthonormal contrasts. The reference computes F independently (one-way
repeated-measures ANOVA sums of squares) and the corrected p-value from F with degrees
of freedom eps (k - 1) and eps (k - 1)(n - 1). F agrees with the library; the corrected
p-value does not, because the library forms the cross-products without centering.

Run: python mne_f_mway_rm_greenhouse_geisser.py
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
from scipy import stats
from mne.stats import f_mway_rm

rs = np.random.RandomState(47)
n, k = 20, 4
x = rs.standard_normal((n, k)); x[:, 0] += 1.5
F, p = f_mway_rm(x, [k], correction=True)
F, got = float(np.atleast_1d(F)[0]), float(np.atleast_1d(p)[0])
gm = x.mean()
ss_cond = n * ((x.mean(0) - gm) ** 2).sum()
ss_subj = k * ((x.mean(1) - gm) ** 2).sum()
ss_err = ((x - gm) ** 2).sum() - ss_cond - ss_subj
F_ref = (ss_cond / (k - 1)) / (ss_err / ((k - 1) * (n - 1)))
C = np.linalg.qr(np.column_stack([np.ones(k), np.eye(k)[:, :k - 1]]))[0][:, 1:]
S = np.cov(x @ C, rowvar=False)
eps = np.trace(S) ** 2 / ((k - 1) * np.trace(S @ S))
want = float(stats.f.sf(F_ref, eps * (k - 1), eps * (k - 1) * (n - 1)))
verdict(not (abs(got - want) <= 1e-9 * want),
        f"p = {got!r}, expected {want!r} (epsilon {eps:.4f}); F = {F:.6f}, independent F = {F_ref:.6f} "
        f"(agree: {abs(F - F_ref) <= 1e-9 * F_ref})")

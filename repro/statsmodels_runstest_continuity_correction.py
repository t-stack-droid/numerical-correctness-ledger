"""statsmodels runstest_1samp: continuity correction with the wrong sign for deviations between 0 and 0.5.

The docstring says the statistic is corrected by 0.5 'following the SAS manual'. SAS
Usage Note 33092 gives the rule: 'if N GE 50 then Z = (Runs - mu) / sigma; else if Runs-
mu LT 0 then Z = (Runs-mu+0.5)/sigma; else Z = (Runs-mu-0.5)/sigma'. statsmodels uses
`elif rdemean < 0.5: z = rdemean + 0.5`, so for 0 <= Runs - mu < 0.5 it adds 0.5 where
the SAS rule subtracts it. For ten values with one above the cutoff there are 3 runs
against an expectation of 14/5 (variance 4/25): the SAS rule gives z = -0.75, p =
0.4533; the library returns z = 1.75, p = 0.0801. When Runs equals mu only the sign of z
differs, so the two-sided p-value is unchanged.

Run: python statsmodels_runstest_continuity_correction.py
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

import math
from fractions import Fraction as F
import numpy as np
from statsmodels.stats.api import runstest_1samp

x = np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0.0])
ind = (x >= 0.5).astype(int)
runs = 1 + int(np.sum(ind[1:] != ind[:-1]))
n1, n0 = int(ind.sum()), int(len(ind) - ind.sum())
n = n0 + n1
mu = F(2 * n0 * n1, n) + 1
var = F(2 * n0 * n1 * (2 * n0 * n1 - n), n * n * (n - 1))
d = runs - mu
num = d + F(1, 2) if d < 0 else d - F(1, 2)
z_sas = float(num) / math.sqrt(float(var))
p_sas = math.erfc(abs(z_sas) / math.sqrt(2))
z, p = (float(v) for v in runstest_1samp(x, cutoff=0.5, correction=True))
verdict(not (abs(z - z_sas) <= 1e-12 and abs(p - p_sas) <= 1e-12),
        f"runs {runs}, expectation {mu}; library z = {z:.4f}, p = {p:.4f}; SAS rule z = {z_sas:.4f}, p = {p_sas:.4f}")

"""statsmodels runstest_2samp: the same continuity-correction sign error.

runstest_2samp returns `Runs(xindicator).runs_test(correction=correction)`, the same
method and `elif rdemean < 0.5` branch as runstest_1samp (see that script for the SAS
rule the docstring cites). For x = [3, 7] and y = [1, 2, 4, 5, 6] the pooled order is y
y x y y y x, 4 runs against an expectation of 27/7 (variance 130/147): the SAS rule
gives z = -0.3798, p = 0.7041; the library returns z = 0.6836, p = 0.4942.

Run: python statsmodels_runstest_2samp_continuity_correction.py
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
from statsmodels.stats.api import runstest_2samp

x, y = [3.0, 7.0], [1.0, 2.0, 4.0, 5.0, 6.0]
lab = [g for _, g in sorted([(v, 0) for v in x] + [(v, 1) for v in y])]
runs = 1 + sum(a != b for a, b in zip(lab, lab[1:]))
n0, n1 = len(x), len(y)
n = n0 + n1
mu = F(2 * n0 * n1, n) + 1
var = F(2 * n0 * n1 * (2 * n0 * n1 - n), n * n * (n - 1))
d = runs - mu
num = d + F(1, 2) if d < 0 else d - F(1, 2)
z_sas = float(num) / math.sqrt(float(var))
p_sas = math.erfc(abs(z_sas) / math.sqrt(2))
z, p = (float(v) for v in runstest_2samp(np.array(x), np.array(y), correction=True))
verdict(not (abs(z - z_sas) <= 1e-12 and abs(p - p_sas) <= 1e-12),
        f"runs {runs}, expectation {mu}; library z = {z:.4f}, p = {p:.4f}; SAS rule z = {z_sas:.4f}, p = {p_sas:.4f}")

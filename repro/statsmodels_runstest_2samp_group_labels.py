"""statsmodels runstest_2samp: group labels other than 0 and 1 give -inf or NaN.

The docstring says: "If group labels are not [0,1], then the unique values found in
groups are used as the two group labels." The code passes the raw labels to Runs, which
counts ones and zeros. For x = 0..7 with groups 0, 0, 1, 1, 1, 1, 0, 0 the statistic is
z = -1.146; relabelling the groups 1 and 2 gives z = -inf and p = 0, and 5 and 7 give
NaN, although the runs statistic does not depend on the labels.

Run: python statsmodels_runstest_2samp_group_labels.py
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
import numpy as np
from statsmodels.stats.api import runstest_2samp

x = np.arange(8.0)
ref = runstest_2samp(x, groups=np.array([0, 0, 1, 1, 1, 1, 0, 0]))
rel = runstest_2samp(x, groups=np.array([1, 1, 2, 2, 2, 2, 1, 1]))
z0, z1 = float(ref[0]), float(rel[0])
rel2 = runstest_2samp(x, groups=np.array([5, 5, 7, 7, 7, 7, 5, 5]))
if not math.isfinite(z0):
    raise RuntimeError("precondition: labels 0/1 give a finite statistic")
same = lambda a: all(math.isfinite(float(u)) and abs(float(u) - float(v)) <= 1e-12 for u, v in zip(a, ref))
verdict(not (same(rel) and same(rel2)),
        f"groups 0/1: {tuple(float(v) for v in ref)}; groups 1/2: {tuple(float(v) for v in rel)}; "
        f"groups 5/7: {tuple(float(v) for v in rel2)}")

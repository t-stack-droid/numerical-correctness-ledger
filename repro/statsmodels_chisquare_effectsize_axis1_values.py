"""statsmodels chisquare_effectsize(axis=1): wrong per-row effect sizes.

The docstring says: "Both probs0 and probs1 are normalized to add to one (in the
``axis`` dimension)." With cohen=False the effect size is sum((p1 - p0)^2 / p0) along
that axis. For probs0 = [[1, 3], [2, 6]] and probs1 = [[2, 2], [6, 2]] the rows
normalise to p0 = (1/4, 3/4), (1/4, 3/4) and p1 = (1/2, 1/2), (3/4, 1/4), so the exact
values are 1/3 and 4/3. The library returns 0.292 and 2.333 with axis=1; the transposed
input with axis=0 gives 1/3 and 4/3.

Run: python statsmodels_chisquare_effectsize_axis1_values.py
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

from fractions import Fraction as F
import numpy as np
from statsmodels.stats.api import chisquare_effectsize

p0 = [[1, 3], [2, 6]]
p1 = [[2, 2], [6, 2]]
want = []
for ra, rb in zip(p0, p1):
    sa, sb = sum(ra), sum(rb)
    want.append(float(sum((F(y, sb) - F(v, sa)) ** 2 / F(v, sa) for v, y in zip(ra, rb))))
got = np.asarray(chisquare_effectsize(p0, p1, cohen=False, axis=1), dtype=float).ravel().tolist()
tr = np.asarray(chisquare_effectsize(np.array(p0).T, np.array(p1).T, cohen=False, axis=0), dtype=float).ravel().tolist()
ok = len(got) == len(want) and all(abs(g - w) <= 1e-12 for g, w in zip(got, want))
verdict(not ok, f"axis=1: {got}; exact per-row effect sizes {want}; axis=0 on the transposed input: {tr}")

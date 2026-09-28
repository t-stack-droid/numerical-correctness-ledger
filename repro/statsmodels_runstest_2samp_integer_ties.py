"""statsmodels runstest_2samp raises for integer arrays with ties (crash, not a wrong value).

Tie handling adds a float offset to an integer array in place, which numpy refuses. The
same values given as floats return z = 0, p = 1.

Run: python statsmodels_runstest_2samp_integer_ties.py
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
from statsmodels.stats.api import runstest_2samp

xi, yi = np.array([1, 2, 2]), np.array([2, 3, 3])
ref = tuple(float(v) for v in runstest_2samp(xi.astype(float), yi.astype(float), correction=False))
try:
    got = tuple(float(v) for v in runstest_2samp(xi, yi, correction=False))
    verdict(not np.allclose(got, ref), f"integer input returned {got}; float input {ref}")
except TypeError as e:
    verdict(True, f"integer input raised {type(e).__name__}: {e}; the same values as floats give {ref}")

"""statsmodels runstest_2samp: wrong continuity correction.

runstest_2samp computes the same runs statistic on the combined ordering and has the
same `elif rdemean < 0.5` branch as runstest_1samp. For the combined order x x x y y x y
y x y there are 6 runs, the expected number is 2*5*5/10 + 1 = 6, so the statistic must
be 0 and the p-value 1.

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

import numpy as np
from statsmodels.stats.api import runstest_2samp

z, p = runstest_2samp(np.array([1, 2, 3, 6, 9.0]), np.array([4, 5, 7, 8, 10.0]), correction=True)
verdict(not (abs(float(z)) <= 1e-12 and abs(float(p) - 1) <= 1e-12), f"z={float(z):.4f} p={float(p):.4f}; expected z=0, p=1")

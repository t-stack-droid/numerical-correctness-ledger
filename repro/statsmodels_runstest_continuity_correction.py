"""statsmodels runstest_1samp: wrong continuity correction.

With correction=True (the default) and fewer than 50 observations, the code uses `elif
rdemean < 0.5: z = rdemean + 0.5`, where rdemean is the number of runs minus its
expectation. The continuity correction moves the deviation towards 0 by 0.5 and should
give 0 when the deviation is between -0.5 and 0.5; for deviations strictly between -0.5
and 0.5 the code returns the deviation plus 0.5 instead (at -0.5 the result, 0, is
right). When the number of runs equals its expectation the statistic must be 0 and the
p-value 1.

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

import numpy as np
from statsmodels.stats.api import runstest_1samp

# [1,1,0,1,0,0]: 3 ones, 3 zeros, 4 runs; expected runs 2*3*3/6 + 1 = 4
z, p = runstest_1samp(np.array([1, 1, 0, 1, 0, 0.0]), cutoff=0.5, correction=True)
verdict(not (abs(float(z)) <= 1e-12 and abs(float(p) - 1) <= 1e-12), f"z={float(z):.4f} p={float(p):.4f}; expected z=0, p=1")

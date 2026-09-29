"""scipy.stats.skewtest: a perfectly symmetric sample gets Z = 1.01, p = 0.31.

For x = 1..8 the sample skewness is exactly 0. The source replaces y = 0 by 1 (`y =
xp.where(y == 0, 1., y)`) before the transformation Z = delta * log(y / alpha + sqrt((y
/ alpha)**2 + 1)), which is finite at y = 0 and equals 0 there, so exact zero skewness
gives Z = 1.0108 and p = 0.3121 instead of 0 and 1. The docstring example for this
sample prints the same output, so it records the substitution rather than a separate
rule.

Run: python scipy_skewtest_symmetric_sample.py
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
import scipy.stats as st

r = st.skewtest(np.arange(1.0, 9.0))
verdict(not (abs(float(r.statistic)) <= 1e-9 and abs(float(r.pvalue) - 1) <= 1e-9),
        f"statistic={float(r.statistic)!r} pvalue={float(r.pvalue)!r}; expected 0 and 1")

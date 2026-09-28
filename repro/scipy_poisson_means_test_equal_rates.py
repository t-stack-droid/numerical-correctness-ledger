"""scipy.stats.poisson_means_test: p-value below 1 when the two observed rates are equal.

When the observed statistic is 0, every outcome is at least as extreme, so the p-value
is 1. The outcome (0, 0) has variance 0, the statistic becomes 0/0 = NaN, the comparison
with NaN is false, and that outcome's probability is dropped (here exp(-2) = 0.1353).

Run: python scipy_poisson_means_test_equal_rates.py
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

import scipy.stats as st

got = float(st.poisson_means_test(1, 1.0, 1, 1.0).pvalue)
verdict(not (abs(got - 1.0) <= 1e-12), f"pvalue = {got!r}, expected 1.0")

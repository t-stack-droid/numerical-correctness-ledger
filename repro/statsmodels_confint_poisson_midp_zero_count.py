"""statsmodels confint_poisson(0, 1, method='midp-c'): a nearly collapsed, slightly reversed interval instead of (0, log 20).

For an observed count of 0 and Poisson mean mu, the lower mid-p tail is exp(-mu) / 2 and
the upper is 1 - exp(-mu) / 2, so the central two-sided mid-p value is exp(-mu). The
interval {mu: exp(-mu) >= 0.05} is [0, log(20)] = [0, 2.9957] for exposure 1. The
library minimizes the squared distance between the p-value and alpha from both ends;
both searches converge to the upper root, giving (2.99573228, 2.99573227), lower above
upper.

Run: python statsmodels_confint_poisson_midp_zero_count.py
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
from statsmodels.stats.rates import confint_poisson

lo, hi = (float(v) for v in confint_poisson(0, 1, method="midp-c"))
verdict(not (abs(lo) <= 1e-9) or not (abs(hi - math.log(20)) <= 1e-6),
        f"got ({lo!r}, {hi!r}), expected (0, {math.log(20)!r})")

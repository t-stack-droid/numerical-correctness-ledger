"""statsmodels score_test_proportions_2indep(compare='diff', value != 0): wrong constrained estimate, which shifts the Miettinen-Nurminen score interval.

The score test uses the maximum likelihood estimate of the two proportions under the
null p1 - p2 = value. The log-likelihood is concave in p2 on the feasible interval, so
the estimate is the unique root of its derivative, found here by bisection in mpmath.
The library solves a cubic whose linear coefficient uses count2 where nobs2 belongs
(value**2 * count2 instead of value**2 * nobs2); the error vanishes at value = 0, so the
default test is unaffected, but confint_proportions_2indep(method='score',
compare='diff'), which inverts the test over nonzero values, is. For 12/35 vs 18/42 the
library's interval is (-0.2871, 0.1335); inverting the score test with the exact
estimate gives (-0.2944, 0.1341). For 5/20 vs 15/25 the library raises ValueError (NaN
inside the root finder).

Run: python statsmodels_score_test_proportions_2indep_constrained_mle.py
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

import mpmath as mp
from statsmodels.stats.proportion import score_test_proportions_2indep

mp.mp.dps = 40


def null_estimate(c1, n1, c2, n2, d):
    c1, n1, c2, n2, d = map(mp.mpf, (c1, n1, c2, n2, d))
    g = lambda p: c1 / (p + d) - (n1 - c1) / (1 - p - d) + c2 / p - (n2 - c2) / (1 - p)
    lo, hi = max(mp.mpf(0), -d) + mp.mpf(10) ** -30, min(mp.mpf(1), 1 - d) - mp.mpf(10) ** -30
    for _ in range(150):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if g(mid) > 0 else (lo, mid)
    return float((lo + hi) / 2)


r = score_test_proportions_2indep(12, 35, 18, 42, value=0.1, compare="diff")
want = null_estimate(12, 35, 18, 42, 0.1)
verdict(not (abs(float(r.prop2_null) - want) <= 1e-9),
        f"constrained estimate of p2 under p1 - p2 = 0.1: got {float(r.prop2_null):.6f}, expected {want:.6f}")

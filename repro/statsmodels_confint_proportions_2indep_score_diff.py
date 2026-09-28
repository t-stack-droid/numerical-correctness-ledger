"""statsmodels confint_proportions_2indep(method='score', compare='diff'): shifted interval.

The score (Miettinen-Nurminen) interval for p1 - p2 inverts the score test over the null
difference d, using the maximum likelihood estimate of the proportions under p1 - p2 = d
and the variance factor n / (n - 1) (the default correction=True). The reference finds
that estimate by bisection on the derivative of the concave log-likelihood and inverts
the test by bisection, in mpmath. For 12/35 vs 18/42 it gives (-0.29444, 0.13412); the
library returns (-0.28706, 0.13349). The cause is the constrained estimate
(statsmodels_score_test_proportions_2indep_constrained_mle.py).

Run: python statsmodels_confint_proportions_2indep_score_diff.py
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
from statsmodels.stats.proportion import confint_proportions_2indep

mp.mp.dps = 30


def bisect(f, lo, hi, it):
    flo = f(lo) > 0
    for _ in range(it):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == flo:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def score(c1, n1, c2, n2, d):
    g = lambda p: c1 / (p + d) - (n1 - c1) / (1 - p - d) + c2 / p - (n2 - c2) / (1 - p)
    eps = mp.mpf(10) ** -25
    p2 = bisect(g, max(mp.mpf(0), -d) + eps, min(mp.mpf(1), 1 - d) - eps, 120)
    p1 = p2 + d
    var = (p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2) * mp.mpf(n1 + n2) / (n1 + n2 - 1)
    return (mp.mpf(c1) / n1 - mp.mpf(c2) / n2 - d) / mp.sqrt(var)


c1, n1, c2, n2 = 12, 35, 18, 42
z = mp.sqrt(2) * mp.erfinv(mp.mpf("0.95"))
est = mp.mpf(c1) / n1 - mp.mpf(c2) / n2
lo = float(bisect(lambda d: score(c1, n1, c2, n2, d) - z, -1 + mp.mpf(10) ** -9, est, 60))
hi = float(bisect(lambda d: score(c1, n1, c2, n2, d) + z, est, 1 - mp.mpf(10) ** -9, 60))
got = tuple(float(v) for v in confint_proportions_2indep(c1, n1, c2, n2, method="score", compare="diff"))
verdict(not (abs(got[0] - lo) <= 1e-6 and abs(got[1] - hi) <= 1e-6),
        f"12/35 vs 18/42: got ({got[0]:.6f}, {got[1]:.6f}), expected ({lo:.6f}, {hi:.6f})")

"""statsmodels nonequivalence_poisson_2indep: p-value above 1.

For counts 30 and 20 with exposures 10 and 12, method='score', compare='ratio' and the
bounds 0.5 and 2, the returned p-value is 1.285 = 1 + erf(1/sqrt(15)). The docstring
defines the p-value as `2 * min(pvalue_low, pvalue_upp)`, and the code computes exactly
that; both one-sided p-values exceed 1/2 here, so the documented formula exceeds 1.
Doubled one-sided p-values are usually capped at 1; the returned number is not a
probability. This is a documentation and convention question: the code follows its
documentation.

Run: python statsmodels_nonequivalence_poisson_2indep.py
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
import statsmodels.stats.rates as r

res = r.nonequivalence_poisson_2indep(30, 10.0, 20, 12.0, 0.5, 2.0, method="score", compare="ratio")
p = float(res.pvalue)
verdict(not (math.isfinite(p) and 0 <= p <= 1), f"pvalue={p!r}")

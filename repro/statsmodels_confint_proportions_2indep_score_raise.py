"""statsmodels confint_proportions_2indep(method='score', compare='diff') raises for 5/20 vs 15/25.

The score interval exists for these counts (inverting the score test with the exact
constrained estimate gives about (-0.5853, -0.0556)). The library's root finder meets a
NaN from the constrained-estimate formula and raises ValueError. Unexpected exception,
not a wrong value.

Run: python statsmodels_confint_proportions_2indep_score_raise.py
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

from statsmodels.stats.proportion import confint_proportions_2indep

try:
    ci = confint_proportions_2indep(5, 20, 15, 25, method="score", compare="diff")
    verdict(False, f"returned {tuple(float(v) for v in ci)}")
except ValueError as e:
    verdict(True, f"raised ValueError: {e}")

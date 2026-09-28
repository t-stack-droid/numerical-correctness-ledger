"""statsmodels jonckheere_terpstra: completely tied samples raise or not depending on group sizes (minor).

When every observation is equal, the tie-corrected null variance is exactly 0, and the
code is written to raise ValueError ('the asymptotic variance is zero; the test is
undefined for completely tied samples'). The guard tests var <= 0 on a floating-point
sum of terms that cancel. For group sizes (4, 4, 4) the sum is 0 and the error is
raised; for (5, 4, 6) it is a small positive number and the function returns z = 0, p =
0.5.

Run: python statsmodels_jonckheere_terpstra_fully_tied.py
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

import statsmodels.stats.api as sms


def run(sizes):
    try:
        r = sms.jonckheere_terpstra([[1.0] * k for k in sizes])
        return f"returned p = {float(r.pvalue)!r} (var_null {float(r.var_null)!r})"
    except ValueError:
        return "raised ValueError"


a, b = run((4, 4, 4)), run((5, 4, 6))
verdict(not (a == b == "raised ValueError"), f"sizes (4, 4, 4): {a}; sizes (5, 4, 6): {b}")

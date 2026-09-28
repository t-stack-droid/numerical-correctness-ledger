"""scipy.stats.spearmanr with nan_policy='omit': p-value 1.0 for perfectly monotone data.

After the pair containing NaN is removed, x = y = [1, 2, 3, 4], so rho = 1 exactly, and
the statistic t = rho * sqrt((n - 2) / (1 - rho**2)) that scipy uses is infinite, giving
the asymptotic two-sided p-value 0. The library computes rho slightly above 1, the
variance ratio becomes negative and is clipped to 0, so t = 0 and p = 1. The script
requires rho within 1e-12 of 1 and a p-value in [0, 1e-12].

Run: python scipy_spearmanr_omit_pvalue.py
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
import numpy as np
import scipy.stats as st

r = st.spearmanr([1.0, 2, 3, 4, 5], [1.0, 2, 3, 4, np.nan], nan_policy="omit")
rho, p = float(r.statistic), float(r.pvalue)
verdict(not (abs(rho - 1) <= 1e-12 and math.isfinite(p) and 0 <= p <= 1e-12),
        f"statistic={rho!r} pvalue={p!r}; expected statistic 1 and pvalue 0")

"""statsmodels transform_corr_normal(method='spearman', return_var=True) raises for correlations of mixed sign.

Without return_var the transformed correlations are returned (-0.5176 and 0.5176 for
-0.5 and 0.5). With return_var=True the variance computation builds an integration grid
from the sorted correlations with 0 prepended, which is not monotone when negative
values are present, and scipy raises. Crash, not a wrong value.

Run: python statsmodels_transform_corr_normal_spearman.py
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
from statsmodels.stats.api import transform_corr_normal

r = np.array([-0.5, 0.5])
plain = np.asarray(transform_corr_normal(r, method="spearman")).tolist()
try:
    res = transform_corr_normal(r, method="spearman", return_var=True)
    ok = bool(np.all(np.isfinite(res.var))) and np.allclose(res.corr, plain)
    verdict(not ok, f"returned corr {np.asarray(res.corr).tolist()}, var {np.asarray(res.var).tolist()}")
except ValueError as e:
    verdict(True, f"return_var=True raised ValueError: {e}; without return_var the result is {plain}")

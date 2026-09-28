"""statsmodels fdrcorrection_twostage(maxiter=True) runs two stages instead of full iteration.

The docstring says: maxiter=True is full iteration (maxiter=-1 or maxiter=len(pvals)).
The code calls range(maxiter), and range(True) has one element, so maxiter=True runs the
two-stage procedure, the same as maxiter=1. For the p-values below (alpha 0.2, method
'bky') full iteration gives different corrected p-values.

Run: python statsmodels_fdrcorrection_twostage_maxiter_true.py
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
from statsmodels.stats.multitest import fdrcorrection_twostage

p = np.array([0.01, 0.02, 0.03, 0.3, 0.9])
run = lambda m: np.asarray(fdrcorrection_twostage(p, alpha=0.2, method="bky", maxiter=m)[1])
verdict(not np.allclose(run(True), run(-1)),
        f"corrected p with maxiter=True {np.round(run(True), 4).tolist()}, maxiter=-1 {np.round(run(-1), 4).tolist()}, "
        f"maxiter=1 {np.round(run(1), 4).tolist()}")

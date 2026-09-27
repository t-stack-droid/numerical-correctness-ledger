"""statsmodels fdrcorrection_twostage: boolean maxiter runs the wrong number of stages.

The docstring states that maxiter=False is the two-stage procedure (maxiter=1). The code
calls range(maxiter), and range(False) is empty, so maxiter=False runs a single stage.

Run: python statsmodels_fdrcorrection_twostage_bool_maxiter.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import numpy as np
from statsmodels.stats.multitest import fdrcorrection_twostage

p = np.array([0.01, 0.02, 0.03, 0.3, 0.9])
a = fdrcorrection_twostage(p, alpha=0.2, method="bky", maxiter=False)
b = fdrcorrection_twostage(p, alpha=0.2, method="bky", maxiter=1)
same = np.array_equal(a[0], b[0]) and np.allclose(a[1], b[1])
verdict(not same, f"maxiter=False corrected p {np.round(a[1], 4).tolist()}, "
                  f"maxiter=1 {np.round(b[1], 4).tolist()}")

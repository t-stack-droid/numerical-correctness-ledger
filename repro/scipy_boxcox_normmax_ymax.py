"""scipy.stats.boxcox_normmax(method='mle', ymax=...) can return a lambda that violates the ymax bound.

ymax is documented to constrain the optimization so that the magnitude of the
transformed data does not exceed ymax. For data above 1 and ymax below log(max(x)), the
helper that finds the boundary lambda takes the k=-1 branch of the Lambert W function,
which returns the spurious root lambda = 0; lambda = 0 is the log transform, whose
maximum is log(max(x)) > ymax. A feasible lambda exists: the transform of max(x)
increases with lambda from 0 (lambda to -inf) to log(max(x)) (lambda = 0), so the
boundary is the negative root, found here by bisection. For the sample below the
returned transform exceeds ymax by 35%.

Run: python scipy_boxcox_normmax_ymax.py
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
import warnings

import mpmath as mp
import numpy as np
import scipy.stats as st

warnings.simplefilter("ignore")
mp.mp.dps = 30
rs = np.random.RandomState(7)
x = rs.uniform(1.1, 5.0, rs.randint(10, 40))
ymax = 1.1816411742258899  # half the unconstrained maximum; log(max(x)) = 1.5923
lam = float(st.boxcox_normmax(x, method="mle", ymax=ymax))
top = max(abs(math.log(v)) if lam == 0 else abs(math.expm1(lam * math.log(v)) / lam) for v in x)
B = lambda L: mp.expm1(L * mp.log(max(x))) / L - ymax
lo, hi = mp.mpf(-50), mp.mpf(-1e-12)
for _ in range(120):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if B(mid) < 0 else (lo, mid)
verdict(not (top <= ymax * (1 + 1e-9)), f"returned lambda {lam:.3e}: max |transform| {top:.4f} > ymax {ymax:.4f}; "
                                  f"boundary lambda {float(lo):.4f} meets the bound")

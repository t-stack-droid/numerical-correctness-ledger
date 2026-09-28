"""scipy.special.y1p_zeros: real zeros 4 to 6 of Y1' have relative errors of 1e-9 to 1e-10.

Reference zeros from mpmath root finding on Y1'(x) = Y0(x) - Y1(x) / x at 40 digits,
started from the library's values. Relative errors of the first six real zeros: about 0,
5.6e-15, 7.4e-14, 1.4e-9, 2.7e-10 and 6.8e-11. Higher zeros were not measured.

Run: python scipy_y1p_zeros_real_accuracy.py
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
import scipy.special as sc

mp.mp.dps = 40
z, _ = sc.y1p_zeros(6)
errs = []
for zk in z:
    x0 = float(zk.real)
    root = mp.findroot(lambda x: mp.bessely(0, x) - mp.bessely(1, x) / x, x0)
    errs.append(abs(x0 - float(root)) / float(root))
verdict(any(not e <= 1e-12 for e in errs),
        "relative errors of the first six real zeros: " + ", ".join(f"{e:.1e}" for e in errs))

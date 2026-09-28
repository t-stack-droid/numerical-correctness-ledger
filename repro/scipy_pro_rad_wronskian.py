"""scipy.special.pro_rad1 / pro_rad2 fail their Wronskian identity at x = 1.1, 1.2 and 1.5 (m = n = 1, c = 1).

The prolate radial functions of the first and second kind satisfy R1 R2' - R1' R2 = 1 /
(c (x^2 - 1)). For m = n = 1 and c = 1 the scaled Wronskian (x^2 - 1)(R1 R2' - R1' R2)
is 0.9961, 0.9830 and 0.8704 at x = 1.1, 1.2 and 1.5 (relative errors 0.4%, 1.7% and
13.0%), against 1; it is 1 to six digits at x = 2 and 4. The identity tests the pair and
does not say which function is inaccurate.

Run: python scipy_pro_rad_wronskian.py
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

import scipy.special as sc

rows, bad = [], False
for x in (1.1, 1.2, 1.5, 2.0, 4.0):
    r1, r1p = sc.pro_rad1(1, 1, 1.0, x)
    r2, r2p = sc.pro_rad2(1, 1, 1.0, x)
    w = float((r1 * r2p - r1p * r2) * (x * x - 1))
    bad = bad or not abs(w - 1) <= 1e-3
    rows.append(f"x={x}: {w:.6f}")
verdict(bad, "scaled Wronskian (expected 1): " + "; ".join(rows))

"""scipy.special.pro_rad1 / pro_rad2 fail their Wronskian identity at x = 1.1, 1.2 and 1.5 (m = n = 1, c = 1).

The prolate radial functions solve the prolate radial equation (DLMF 30.2.1), which is
in Sturm-Liouville form with leading coefficient x^2 - 1, so by Abel's identity the
scaled Wronskian (x^2 - 1)(R1 R2' - R1' R2) is the same at every x > 1 for any
normalisation (1/c with the usual one). For m = n = 1 and c = 1 it is 1.0000 at x = 2
and 4 but 0.9961, 0.9830 and 0.8704 at x = 1.1, 1.2 and 1.5: the values are inconsistent
across these points. The identity does not say which function or which point is wrong.

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

import math
import scipy.special as sc

vals, rows = [], []
for x in (1.1, 1.2, 1.5, 2.0, 4.0):
    r1, r1p = sc.pro_rad1(1, 1, 1.0, x)
    r2, r2p = sc.pro_rad2(1, 1, 1.0, x)
    w0 = float(r1 * r2p - r1p * r2)
    scale = max(abs(float(r1 * r2p)), abs(float(r1p * r2)))
    if scale > 0 and not (abs(w0) / scale >= 1e-10):
        raise RuntimeError(f"precondition: the Wronskian at x={x} cancels to below 1e-10 of its terms")
    w = w0 * (x * x - 1)
    vals.append(w)
    rows.append(f"x={x}: {w:.6f}")
top = max(abs(v) for v in vals)
consistent = all(math.isfinite(v) for v in vals) and top > 0 and all(abs(v - vals[-1]) <= 1e-3 * top for v in vals)
verdict(not consistent, "scaled Wronskian, which must be the same at every x: " + "; ".join(rows))

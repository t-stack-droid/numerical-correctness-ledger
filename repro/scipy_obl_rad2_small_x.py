"""scipy.special.obl_rad1 / obl_rad2 fail their Wronskian identity at x = 0.2, 0.5 and 1 (m = n = 0, c = 1).

The oblate radial functions solve a second-order equation in Sturm-Liouville form with
leading coefficient x^2 + 1 (DLMF 30.2.1 with the oblate substitution), so by Abel's
identity (x^2 + 1)(R1 R2' - R1' R2) is the same at every x for any normalisation; with
the usual normalisation it is 1/c. For m = n = 0 and c = 1 it is 1.0 at x = 2 but about
1e-320 at x = 0.2, 0.5 and 1, where obl_rad2 returns values of order 1e-320. The
identity tests the pair; the tiny obl_rad2 values point to it.

Run: python scipy_obl_rad2_small_x.py
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
for x in (0.2, 0.5, 1.0, 2.0, 4.0):
    r1, r1p = sc.obl_rad1(0, 0, 1.0, x)
    r2, r2p = sc.obl_rad2(0, 0, 1.0, x)
    w = float(r1 * r2p - r1p * r2)
    scale = max(abs(float(r1 * r2p)), abs(float(r1p * r2)))
    if scale > 0 and not (abs(w) / scale >= 1e-10):
        raise RuntimeError(f"precondition: the Wronskian at x={x} cancels to below 1e-10 of its terms")
    s = w * (x * x + 1)
    vals.append(s)
    rows.append(f"x={x}: obl_rad2={float(r2):.4g}, (x^2+1) W={s:.6g}")
top = max(abs(v) for v in vals)
consistent = all(math.isfinite(v) for v in vals) and top > 0 and all(abs(v - vals[-1]) <= 1e-3 * top for v in vals)
verdict(not consistent, "scaled Wronskian, which must be the same at every x: " + "; ".join(rows))

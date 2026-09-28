"""scipy.special.obl_rad1 / obl_rad2 fail their Wronskian identity at x = 0.2, 0.5 and 1 (m = n = 0, c = 1).

The oblate radial functions of the first and second kind satisfy R1 R2' - R1' R2 = 1 /
(c (x^2 + 1)). For m = n = 0 and c = 1 the pair gives about 0 instead of 0.96, 0.8 and
0.5 at x = 0.2, 0.5 and 1, where obl_rad2 returns values of order 1e-320; at x = 2 the
identity holds. The identity tests the pair; the tiny obl_rad2 values point to it.

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

import scipy.special as sc

rows, bad = [], False
for x in (0.2, 0.5, 1.0, 2.0):
    r1, r1p = sc.obl_rad1(0, 0, 1.0, x)
    r2, r2p = sc.obl_rad2(0, 0, 1.0, x)
    w, want = float(r1 * r2p - r1p * r2), 1 / (x * x + 1)
    err = abs(w - want) / want
    bad = bad or not err <= 1e-3
    rows.append(f"x={x}: obl_rad2={float(r2):.4g}, Wronskian={w:.6g}, expected {want:.6g}, rel. error {err:.1e}")
verdict(bad, "; ".join(rows))
